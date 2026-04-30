from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "05_herleitung_und_dualitaet"
    / "05A_zeitbereichsanalyse"
)

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (11.0, 4.8)
PHASOR_FIGSIZE = (6.8, 6.8)
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEGEND_SIZE = 13

SIGNAL_BLACK = "0.10"
FUTURE_GREY = "0.72"
SPECTRUM_BLUE = "tab:blue"
IMAG_ORANGE = "tab:orange"
WINDOW_GREEN = "#66b77a"
ACTIVE_RED = "crimson"
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
PHASOR_GRID_ALPHA = 0.22

TIME_VALUES = np.linspace(-1.5, 1.5, 6250)
FREQ_STEP = 0.005
FREQ_VALUES_EXT = np.arange(-12.0, 12.0 + 0.5 * FREQ_STEP, FREQ_STEP)
DISPLAY_MASK = np.abs(FREQ_VALUES_EXT) <= 6.0
FREQ_VALUES = FREQ_VALUES_EXT[DISPLAY_MASK]
COMMON_TIME_XTICKS = np.arange(-1.0, 1.01, 0.5)
COMMON_FREQ_XTICKS = np.arange(-6.0, 6.01, 2.0)
TIME_AMPLITUDE_LIMIT = 2.0
TIME_VIEW_LIMIT = 1.5

PROBE_F = 2.0
KERNEL_BASE_F = 0.0
FINAL_PROBE_F_VALUES = [0.0, 2.0, 4.0]
SIGNAL_COMPONENTS = [
    ("cos", 1.00, 2.0, np.pi / 4.0),
    ("cos", 0.85, 5.0, -np.pi / 2.0),
]
WINDOW_HALF_WIDTH = 1.0
WINDOW_DURATION = 2.0 * WINDOW_HALF_WIDTH


def clear_owned_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_DIR.glob("*"):
        if path.is_file() and path.suffix.lower() in {".png", ".gif"}:
            path.unlink()


def create_figure(figsize):
    return plt.subplots(figsize=figsize)


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def add_inset_legend(ax, handles, loc="upper right"):
    ax.legend(
        handles=handles,
        loc=loc,
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )


def raw_signal_x_t(values):
    signal = np.zeros_like(values)
    for kind, amplitude, frequency_hz, phase_rad in SIGNAL_COMPONENTS:
        angle = 2.0 * np.pi * frequency_hz * values + phase_rad
        if kind == "cos":
            signal += amplitude * np.cos(angle)
        elif kind == "sin":
            signal += amplitude * np.sin(angle)
        else:
            raise ValueError(f"Unknown signal type: {kind}")
    return signal


def signal_x_t(values):
    return raw_signal_x_t(values)


def window_w_t(values):
    return (np.abs(values) <= WINDOW_HALF_WIDTH).astype(float)


def line_spectrum_from_components(components):
    line_map = {}
    for kind, amplitude, frequency_hz, phase_rad in components:
        if kind == "cos":
            positive = 0.5 * amplitude * np.exp(1j * phase_rad)
            negative = 0.5 * amplitude * np.exp(-1j * phase_rad)
        elif kind == "sin":
            positive = -0.5j * amplitude * np.exp(1j * phase_rad)
            negative = 0.5j * amplitude * np.exp(-1j * phase_rad)
        else:
            raise ValueError(f"Unknown signal type: {kind}")
        line_map[frequency_hz] = line_map.get(frequency_hz, 0.0 + 0.0j) + positive
        line_map[-frequency_hz] = line_map.get(-frequency_hz, 0.0 + 0.0j) + negative
    line_freqs = np.array(sorted(line_map.keys()), dtype=float)
    line_coeffs = np.array([line_map[freq] for freq in line_freqs], dtype=np.complex128)
    return line_freqs, line_coeffs


def continuous_ft(time_values, signal_values, freq_values, chunk_size=120):
    result = np.zeros_like(freq_values, dtype=np.complex128)
    for start in range(0, len(freq_values), chunk_size):
        stop = min(start + chunk_size, len(freq_values))
        freq_chunk = freq_values[start:stop]
        phase_matrix = np.exp(-1j * 2.0 * np.pi * freq_chunk[:, None] * time_values[None, :])
        integrand = phase_matrix * signal_values[None, :]
        result[start:stop] = np.trapezoid(integrand, time_values, axis=1)
    return result


def interp_complex(x_values, complex_values, x_target):
    real_part = np.interp(x_target, x_values, complex_values.real)
    imag_part = np.interp(x_target, x_values, complex_values.imag)
    return real_part + 1j * imag_part


SIGNAL_VALUES = signal_x_t(TIME_VALUES)
WINDOW_VALUES = window_w_t(TIME_VALUES)
OBSERVED_VALUES = SIGNAL_VALUES * WINDOW_VALUES
COS_BASIS = np.cos(2.0 * np.pi * PROBE_F * TIME_VALUES)
MINUS_SIN_BASIS = -np.sin(2.0 * np.pi * PROBE_F * TIME_VALUES)
COS_BASIS_ZERO = np.cos(2.0 * np.pi * KERNEL_BASE_F * TIME_VALUES)
MINUS_SIN_BASIS_ZERO = -np.sin(2.0 * np.pi * KERNEL_BASE_F * TIME_VALUES)
REAL_PRODUCT = OBSERVED_VALUES * COS_BASIS
IMAG_PRODUCT = OBSERVED_VALUES * MINUS_SIN_BASIS
REAL_INTEGRAL = float(np.trapezoid(REAL_PRODUCT, TIME_VALUES))
IMAG_INTEGRAL = float(np.trapezoid(IMAG_PRODUCT, TIME_VALUES))
Y_FIXED_TIME = REAL_INTEGRAL + 1j * IMAG_INTEGRAL

KERNEL_REAL_VALUES = WINDOW_VALUES * COS_BASIS
KERNEL_IMAG_VALUES = WINDOW_VALUES * MINUS_SIN_BASIS
KERNEL_ZERO_REAL_VALUES = WINDOW_VALUES * COS_BASIS_ZERO
KERNEL_ZERO_IMAG_VALUES = WINDOW_VALUES * MINUS_SIN_BASIS_ZERO

X_LINE_FREQS, X_LINE_COEFFS = line_spectrum_from_components(SIGNAL_COMPONENTS)
W_VALUES_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * FREQ_VALUES_EXT)
G_VALUES_EXT = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (PROBE_F - FREQ_VALUES_EXT))
Y_VALUES_EXT = np.zeros_like(FREQ_VALUES_EXT, dtype=np.complex128)
for line_freq, line_coeff in zip(X_LINE_FREQS, X_LINE_COEFFS):
    Y_VALUES_EXT += line_coeff * WINDOW_DURATION * np.sinc(WINDOW_DURATION * (FREQ_VALUES_EXT - line_freq))

G_AT_LINE_FREQS = WINDOW_DURATION * np.sinc(WINDOW_DURATION * (PROBE_F - X_LINE_FREQS))
WEIGHTED_LINE_COEFFS = X_LINE_COEFFS * G_AT_LINE_FREQS
Y_FIXED_FREQ = np.sum(WEIGHTED_LINE_COEFFS)

Y_VALUES = Y_VALUES_EXT[DISPLAY_MASK]
W_VALUES = W_VALUES_EXT[DISPLAY_MASK]
G_VALUES = G_VALUES_EXT[DISPLAY_MASK]

SIGNAL_LIMIT = TIME_AMPLITUDE_LIMIT
WINDOW_LIMIT = TIME_AMPLITUDE_LIMIT
PRODUCT_LIMIT = TIME_AMPLITUDE_LIMIT
KERNEL_TIME_LIMIT = TIME_AMPLITUDE_LIMIT
COMMON_SPECTRUM_LIMIT = 0.5 * np.ceil(
    2.0
    * 1.15
    * max(
        np.max(np.abs(np.real(X_LINE_COEFFS))),
        np.max(np.abs(np.imag(X_LINE_COEFFS))),
        np.max(np.abs(np.real(WEIGHTED_LINE_COEFFS))),
        np.max(np.abs(np.imag(WEIGHTED_LINE_COEFFS))),
        np.max(np.abs(W_VALUES)),
        np.max(np.abs(G_VALUES)),
        np.max(np.abs(Y_VALUES)),
        1e-6,
    )
)
REAL_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
IMAG_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
KERNEL_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
MAGNITUDE_SPECTRUM_LIMIT = COMMON_SPECTRUM_LIMIT
SIGNED_SPECTRUM_YTICKS = np.arange(-COMMON_SPECTRUM_LIMIT, COMMON_SPECTRUM_LIMIT + 0.001, 0.5)
MAGNITUDE_SPECTRUM_YTICKS = np.arange(0.0, COMMON_SPECTRUM_LIMIT + 0.001, 0.5)
COMPLEX_LIMIT = 1.15 * max(
    np.abs(Y_FIXED_TIME.real),
    np.abs(Y_FIXED_TIME.imag),
    np.abs(Y_FIXED_FREQ.real),
    np.abs(Y_FIXED_FREQ.imag),
    1e-6,
)


def style_time_axis(ax, title, y_limit, y_label="Amplitude"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-TIME_VIEW_LIMIT, TIME_VIEW_LIMIT)
    ax.set_ylim(-y_limit, y_limit)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_window_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-TIME_VIEW_LIMIT, TIME_VIEW_LIMIT)
    ax.set_ylim(-WINDOW_LIMIT, WINDOW_LIMIT)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_signed_frequency_axis(ax, title, y_limit, y_label, x_label=r"Auxiliary frequency $\nu$ [Hz]"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(FREQ_VALUES[0], FREQ_VALUES[-1])
    ax.set_ylim(-y_limit, y_limit)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel(x_label, fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_magnitude_frequency_axis(ax, title, y_limit, y_label="Magnitude", x_label="Frequency f [Hz]"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(FREQ_VALUES[0], FREQ_VALUES[-1])
    ax.set_ylim(0.0, y_limit)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel(x_label, fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_complex_plane_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-COMPLEX_LIMIT, COMPLEX_LIMIT)
    ax.set_ylim(-COMPLEX_LIMIT, COMPLEX_LIMIT)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=PHASOR_GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE + 2)
    ax.set_xlabel(r"Re$\{Y(f)\}$", fontsize=LABEL_SIZE + 2, color=SPECTRUM_BLUE)
    ax.set_ylabel(r"Im$\{Y(f)\}$", fontsize=LABEL_SIZE + 2, color=IMAG_ORANGE)
    ax.tick_params(axis="x", colors=SPECTRUM_BLUE, labelsize=TICK_SIZE + 2)
    ax.tick_params(axis="y", colors=IMAG_ORANGE, labelsize=TICK_SIZE + 2)


def draw_spectral_lines(ax, frequencies, values, color, lw=3.0, alpha=1.0):
    ax.vlines(frequencies, 0.0, values, color=color, lw=lw, alpha=alpha)


def export_signal_x_t():
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.2)
    style_time_axis(ax, r"Signal $x(t)$", SIGNAL_LIMIT)
    save_figure(fig, "01_signal_x_t.png")


def export_window_w_t():
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=2.6)
    style_window_axis(ax, r"Window $w(t)$")
    save_figure(fig, "02_window_w_t.png")


def export_observed_signal_x_obs_t():
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=FUTURE_GREY, lw=1.8)
    ax.plot(TIME_VALUES, OBSERVED_VALUES, color=SIGNAL_BLACK, lw=2.2)
    style_time_axis(ax, r"Observed signal $x_{obs}(t)=x(t)w(t)$", SIGNAL_LIMIT)
    save_figure(fig, "03_observed_signal_x_obs_t.png")


def export_observed_with_basis(filename, basis_values, color, title, basis_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=1.8, alpha=0.8)
    ax.plot(TIME_VALUES, OBSERVED_VALUES, color=SIGNAL_BLACK, lw=2.2)
    ax.plot(TIME_VALUES, basis_values, color=color, lw=1.9, ls="--")
    style_time_axis(ax, title, SIGNAL_LIMIT)
    save_figure(fig, filename)


def export_product_plot(filename, values, color, title, y_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, values, color=color, lw=2.2)
    style_time_axis(ax, title, PRODUCT_LIMIT, y_label)
    save_figure(fig, filename)


def export_integral_plot(filename, values, integral_value, color, title, y_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.plot(TIME_VALUES, values, color=color, lw=2.1)
    ax.fill_between(
        TIME_VALUES,
        0.0,
        values,
        where=values >= 0.0,
        color=color,
        alpha=0.22,
        interpolate=True,
    )
    ax.fill_between(
        TIME_VALUES,
        0.0,
        values,
        where=values < 0.0,
        color="tab:red",
        alpha=0.16,
        interpolate=True,
    )
    ax.plot([TIME_VALUES[0], TIME_VALUES[-1]], [integral_value, integral_value], color=color, lw=2.0, ls="--")
    style_time_axis(ax, title, PRODUCT_LIMIT, y_label)
    save_figure(fig, filename)


def export_complex_value(filename, value, title):
    fig, ax = create_figure(PHASOR_FIGSIZE)
    ax.plot([0.0, value.real], [0.0, value.imag], color=ACTIVE_RED, lw=3.0)
    ax.plot([value.real], [value.imag], "o", color=ACTIVE_RED, ms=8)
    ax.plot([0.0, value.real], [0.0, 0.0], color=SPECTRUM_BLUE, lw=1.5, alpha=0.85)
    ax.plot([value.real, value.real], [0.0, value.imag], color=IMAG_ORANGE, lw=1.5, alpha=0.85)
    style_complex_plane_axis(ax, title)
    save_figure(fig, filename)


def export_kernel_time_plot(filename, values, color, title, kernel_label):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=1.8, alpha=0.8)
    ax.plot(TIME_VALUES, values, color=color, lw=2.2)
    style_time_axis(ax, title, KERNEL_TIME_LIMIT)
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$w(t)$"),
            Line2D([0], [0], color=color, lw=2.2, label=kernel_label),
        ],
        loc="upper right",
    )
    save_figure(fig, filename)


def export_kernel_basis_and_product_plot(
    filename, basis_values, product_values, color, title, basis_label, product_label
):
    fig, ax = create_figure(TIME_FIGSIZE)
    ax.step(TIME_VALUES, WINDOW_VALUES, where="mid", color=WINDOW_GREEN, lw=1.8, alpha=0.8)
    ax.plot(TIME_VALUES, basis_values, color=color, lw=1.9, ls="--")
    ax.plot(TIME_VALUES, product_values, color=color, lw=2.2)
    style_time_axis(ax, title, KERNEL_TIME_LIMIT)
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$w(t)$"),
            Line2D([0], [0], color=color, lw=1.9, ls="--", label=basis_label),
            Line2D([0], [0], color=color, lw=2.2, label=product_label),
        ],
        loc="upper right",
    )
    save_figure(fig, filename)


def export_real_spectrum_x_nu():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(X_LINE_COEFFS), SPECTRUM_BLUE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Real part of the ideal spectrum $X(\nu)$",
        REAL_SPECTRUM_LIMIT,
        r"Re$\{X(\nu)\}$",
    )
    save_figure(fig, "15_real_spectrum_X_nu.png")


def export_imag_spectrum_x_nu():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(X_LINE_COEFFS), IMAG_ORANGE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Imaginary part of the ideal spectrum $X(\nu)$",
        IMAG_SPECTRUM_LIMIT,
        r"Im$\{X(\nu)\}$",
    )
    save_figure(fig, "16_imaginary_spectrum_X_nu.png")


def export_kernel_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    ax.plot(FREQ_VALUES, W_VALUES, color=FUTURE_GREY, lw=1.9)
    ax.plot(FREQ_VALUES, G_VALUES, color=WINDOW_GREEN, lw=2.4)
    style_signed_frequency_axis(
        ax,
        rf"Spectrum of the analysis kernel $G_f(\nu)=W({int(PROBE_F)}-\nu)$",
        KERNEL_SPECTRUM_LIMIT,
        r"$G_f(\nu)$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.9, label=r"$W(\nu)$"),
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.4, label=r"$G_f(\nu)=W(f-\nu)$"),
        ],
        loc="upper right",
    )
    save_figure(fig, "17_analysis_kernel_spectrum_G_f_nu.png")


def export_weighted_real_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(X_LINE_COEFFS), FUTURE_GREY, lw=2.2)
    ax.plot(FREQ_VALUES, G_VALUES, color=WINDOW_GREEN, lw=1.8)
    draw_spectral_lines(ax, X_LINE_FREQS, np.real(WEIGHTED_LINE_COEFFS), SPECTRUM_BLUE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Real part of $X(\nu)\,G_f(\nu)$",
        REAL_SPECTRUM_LIMIT,
        r"Re$\{X(\nu)G_f(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"Re$\{X(\nu)\}$"),
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$G_f(\nu)$"),
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.2, label=r"Re$\{X(\nu)G_f(\nu)\}$"),
        ],
        loc="upper right",
    )
    save_figure(fig, "18_real_weighted_spectrum_XG.png")


def export_weighted_imag_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(X_LINE_COEFFS), FUTURE_GREY, lw=2.2)
    ax.plot(FREQ_VALUES, G_VALUES, color=WINDOW_GREEN, lw=1.8)
    draw_spectral_lines(ax, X_LINE_FREQS, np.imag(WEIGHTED_LINE_COEFFS), IMAG_ORANGE, lw=3.2)
    style_signed_frequency_axis(
        ax,
        r"Imaginary part of $X(\nu)\,G_f(\nu)$",
        IMAG_SPECTRUM_LIMIT,
        r"Im$\{X(\nu)G_f(\nu)\}$",
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=FUTURE_GREY, lw=1.8, label=r"Im$\{X(\nu)\}$"),
            Line2D([0], [0], color=WINDOW_GREEN, lw=1.8, label=r"$G_f(\nu)$"),
            Line2D([0], [0], color=IMAG_ORANGE, lw=2.2, label=r"Im$\{X(\nu)G_f(\nu)\}$"),
        ],
        loc="upper right",
    )
    save_figure(fig, "19_imaginary_weighted_spectrum_XG.png")


def export_observed_magnitude_spectrum():
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    ax.plot(FREQ_VALUES, np.abs(Y_VALUES), color=SIGNAL_BLACK, lw=2.4, ls="--")
    style_magnitude_frequency_axis(ax, r"Observed magnitude spectrum $|Y(f)|$", MAGNITUDE_SPECTRUM_LIMIT)
    save_figure(fig, "21_observed_magnitude_spectrum_Y_f.png")


def output_magnitude_at(current_f):
    return float(np.interp(current_f, FREQ_VALUES, np.abs(Y_VALUES)))


def export_observed_magnitude_probe(index, current_f):
    fig, ax = create_figure(SPECTRUM_FIGSIZE)
    magnitude_values = np.abs(Y_VALUES)
    probe_value = output_magnitude_at(current_f)
    ax.plot(FREQ_VALUES, magnitude_values, color=SIGNAL_BLACK, lw=2.4, ls="--")
    ax.vlines(current_f, 0.0, probe_value, color=ACTIVE_RED, lw=2.5)
    style_magnitude_frequency_axis(
        ax,
        rf"Observed magnitude spectrum $|Y(f)|$ at $f = {int(current_f)}$ Hz",
        MAGNITUDE_SPECTRUM_LIMIT,
    )
    save_figure(fig, f"{index:02d}_observed_magnitude_probe_f_{int(current_f)}.png")


def main():
    clear_owned_outputs()
    export_signal_x_t()
    export_window_w_t()
    export_observed_with_basis(
        "03_observed_signal_with_cos.png",
        COS_BASIS,
        SPECTRUM_BLUE,
        rf"Observed signal, window, and $\cos(2\pi f t)$ for fixed $f = {int(PROBE_F)}$ Hz",
        r"$\cos(2\pi f t)$",
    )
    export_observed_with_basis(
        "04_observed_signal_with_minus_sin.png",
        MINUS_SIN_BASIS,
        IMAG_ORANGE,
        rf"Observed signal, window, and $-\sin(2\pi f t)$ for fixed $f = {int(PROBE_F)}$ Hz",
        r"$-\sin(2\pi f t)$",
    )
    export_product_plot(
        "05_product_x_obs_cos.png",
        REAL_PRODUCT,
        SPECTRUM_BLUE,
        rf"Product $x_{{obs}}(t)\cos(2\pi f t)$ for fixed $f = {int(PROBE_F)}$ Hz",
        r"$x_{obs}(t)\cos(2\pi f t)$",
    )
    export_product_plot(
        "06_product_x_obs_minus_sin.png",
        IMAG_PRODUCT,
        IMAG_ORANGE,
        rf"Product $x_{{obs}}(t)(-\sin(2\pi f t))$ for fixed $f = {int(PROBE_F)}$ Hz",
        r"$x_{obs}(t)(-\sin(2\pi f t))$",
    )
    export_integral_plot(
        "07_integral_cos.png",
        REAL_PRODUCT,
        REAL_INTEGRAL,
        SPECTRUM_BLUE,
        rf"Integral of $x_{{obs}}(t)\cos(2\pi f t)$ for fixed $f = {int(PROBE_F)}$ Hz",
        r"$x_{obs}(t)\cos(2\pi f t)$",
    )
    export_integral_plot(
        "08_integral_minus_sin.png",
        IMAG_PRODUCT,
        IMAG_INTEGRAL,
        IMAG_ORANGE,
        rf"Integral of $x_{{obs}}(t)(-\sin(2\pi f t))$ for fixed $f = {int(PROBE_F)}$ Hz",
        r"$x_{obs}(t)(-\sin(2\pi f t))$",
    )
    export_complex_value(
        "09_complex_value_Y_f_from_time.png",
        Y_FIXED_TIME,
        rf"Complex analysis value $Y(f)$ for fixed $f = {int(PROBE_F)}$ Hz",
    )
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
