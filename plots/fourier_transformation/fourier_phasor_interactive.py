import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider


# -------------------------
# Parameters
# -------------------------
T_MAX = 7.0
FS = 180
NORMALIZE_BY_WINDOW = False  # True => window average, False => classical FT on [-T_obs/2, T_obs/2]
WINDOW_COLOR = "#9bd3a8"

# Fixed mixed signal for the default case
SIGNAL_COMPONENTS = [
    ("cos", 1.00, 2.0, np.pi / 4.0),
    ("cos", 0.85, 5.0, -np.pi / 2.0),
]

SIGNAL_MODES = ("Mixed signal", "Cosine", "Sine", "Constant")
WINDOW_MODES = ("Rectangular", "Hann", "Hamming")

FREQ_MIN = 0.0
FREQ_MAX = 7.0
ANALYSIS_FREQ_MIN = 0.0
ANALYSIS_FREQ_MAX = 7.0
DISPLAY_FINE_FREQS = np.linspace(ANALYSIS_FREQ_MIN, ANALYSIS_FREQ_MAX, 1601)
DISPLAY_LIMIT_FREQS = np.linspace(ANALYSIS_FREQ_MIN, ANALYSIS_FREQ_MAX, 241)

DEFAULT_ANALYSIS_FREQ = 0.0
DEFAULT_SIGNAL_MODE = "Mixed signal"
DEFAULT_WINDOW_MODE = "Rectangular"
DEFAULT_SIGNAL_FREQ = 2.0
DEFAULT_OBS_DURATION = 2.0
OBS_DURATION_MIN = 0.5
SLIDER_STEP = 0.05
PHASE_VIS_REL_THRESHOLD = 0.15


def build_signal(time_values, components):
    signal = np.zeros_like(time_values)
    for kind, amplitude, frequency_hz, phase_rad in components:
        angle = 2.0 * np.pi * frequency_hz * time_values + phase_rad
        if kind == "cos":
            signal += amplitude * np.cos(angle)
        elif kind == "sin":
            signal += amplitude * np.sin(angle)
        else:
            raise ValueError(f"Unknown signal type: {kind}")
    return signal


def build_signal_label(components):
    parts = []
    for kind, amplitude, frequency_hz, phase_rad in components:
        if kind == "cos":
            text = f"{amplitude:.2f} cos(2pi*{frequency_hz:.1f}*t"
        else:
            text = f"{amplitude:.2f} sin(2pi*{frequency_hz:.1f}*t"

        if abs(phase_rad) > 1e-12:
            phase_sign = "+" if phase_rad >= 0 else "-"
            text += f" {phase_sign} {abs(phase_rad):.2f}"

        parts.append(text + ")")
    return "x(t) = " + " + ".join(parts)


def build_selectable_signal(time_values, signal_mode, signal_frequency):
    if signal_mode == "Mixed signal":
        return build_signal(time_values, SIGNAL_COMPONENTS), build_signal_label(SIGNAL_COMPONENTS)
    if signal_mode == "Cosine":
        return np.cos(2.0 * np.pi * signal_frequency * time_values), f"x(t) = cos(2pi*{signal_frequency:.2f}*t)"
    if signal_mode == "Sine":
        return np.sin(2.0 * np.pi * signal_frequency * time_values), f"x(t) = sin(2pi*{signal_frequency:.2f}*t)"
    if signal_mode == "Constant":
        return np.ones_like(time_values), "x(t) = 1"
    raise ValueError(f"Unknown signal mode: {signal_mode}")


def fmt_complex(value):
    sign = "+" if value.imag >= 0 else "-"
    return f"{value.real:+.3f} {sign} j{abs(value.imag):.3f}"


def observed_limits(obs_duration):
    half_duration = 0.5 * obs_duration
    return -half_duration, half_duration


def observed_mask(time_values, obs_duration):
    window_start, window_end = observed_limits(obs_duration)
    return (time_values >= (window_start - 1e-12)) & (time_values <= (window_end + 1e-12))


def full_time_limits():
    return observed_limits(T_MAX)


def build_window(time_values, obs_duration, window_mode):
    window_values = np.zeros_like(time_values)
    mask = observed_mask(time_values, obs_duration)
    time_obs = time_values[mask]

    if window_mode == "Rectangular":
        window_values[mask] = 1.0
    elif window_mode == "Hann":
        window_values[mask] = 0.5 * (1.0 + np.cos(2.0 * np.pi * time_obs / obs_duration))
    elif window_mode == "Hamming":
        window_values[mask] = 0.54 + 0.46 * np.cos(2.0 * np.pi * time_obs / obs_duration)
    else:
        raise ValueError(f"Unknown window mode: {window_mode}")

    return window_values


def add_centered_formula_segments(fig, y, segments, fontsize=12):
    texts = [
        fig.text(0.0, y, text, ha="left", va="center", fontsize=fontsize, color=color)
        for text, color in segments
    ]
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig_width_px = fig.get_size_inches()[0] * fig.dpi
    widths = [text.get_window_extent(renderer=renderer).width for text in texts]
    total_width_frac = sum(widths) / fig_width_px
    x = 0.50 - total_width_frac / 2.0
    for text, width_px in zip(texts, widths):
        text.set_position((x, y))
        x += width_px / fig_width_px
    return texts


def evaluate_frequency(probe_freq, time_values, signal_values, window_values, obs_duration, normalize_by_window):
    mask = observed_mask(time_values, obs_duration)
    time_obs = time_values[mask]
    signal_obs = signal_values[mask]
    window_obs = window_values[mask]
    weighted_signal_obs = signal_obs * window_obs
    basis_obs = np.exp(-1j * 2.0 * np.pi * probe_freq * time_obs)

    real_product_obs = weighted_signal_obs * basis_obs.real
    imag_product_obs = weighted_signal_obs * basis_obs.imag

    scale = (1.0 / obs_duration) if normalize_by_window else 1.0
    real_integral = np.trapezoid(real_product_obs, x=time_obs) * scale
    imag_integral = np.trapezoid(imag_product_obs, x=time_obs) * scale
    coefficient = real_integral + 1j * imag_integral

    signal_plot = np.where(mask, signal_values, np.nan)
    window_plot = np.where(mask, window_values, np.nan)
    basis_real_plot = np.full_like(time_values, np.nan, dtype=float)
    basis_imag_plot = np.full_like(time_values, np.nan, dtype=float)
    real_product_plot = np.full_like(time_values, np.nan, dtype=float)
    imag_product_plot = np.full_like(time_values, np.nan, dtype=float)
    basis_real_plot[mask] = basis_obs.real
    basis_imag_plot[mask] = basis_obs.imag
    real_product_plot[mask] = real_product_obs
    imag_product_plot[mask] = imag_product_obs

    return (
        signal_plot,
        window_plot,
        basis_real_plot,
        basis_imag_plot,
        real_product_plot,
        imag_product_plot,
        real_integral,
        imag_integral,
        coefficient,
    )


def compute_signal_cache(
    signal_values,
    window_values,
    time_values,
    obs_duration,
    normalize_by_window,
    basis_limit,
    basis_fine,
):
    mask = observed_mask(time_values, obs_duration)
    time_obs = time_values[mask]
    signal_obs = signal_values[mask]
    window_obs = window_values[mask]
    weighted_signal_obs = signal_obs * window_obs

    scale = (1.0 / obs_duration) if normalize_by_window else 1.0

    real_products_limit = weighted_signal_obs[None, :] * basis_limit[:, mask].real
    imag_products_limit = weighted_signal_obs[None, :] * basis_limit[:, mask].imag

    real_integrals_limit = np.trapezoid(real_products_limit, x=time_obs, axis=1) * scale
    imag_integrals_limit = np.trapezoid(imag_products_limit, x=time_obs, axis=1) * scale

    real_integrals_fine = np.trapezoid(
        weighted_signal_obs[None, :] * basis_fine[:, mask].real, x=time_obs, axis=1
    ) * scale
    imag_integrals_fine = np.trapezoid(
        weighted_signal_obs[None, :] * basis_fine[:, mask].imag, x=time_obs, axis=1
    ) * scale
    coefficients_fine = real_integrals_fine + 1j * imag_integrals_fine
    spectrum_fine = np.abs(coefficients_fine)
    phase_fine_full = np.degrees(np.angle(coefficients_fine))
    phase_threshold = 0.0
    phase_fine = phase_fine_full

    return {
        "signal_values": signal_values,
        "signal_limit": 1.15 * max(1.0, np.max(np.abs(signal_values))),
        "product_limit": 1.15 * max(
            1.0,
            np.max(np.abs(real_products_limit)),
            np.max(np.abs(imag_products_limit)),
        ),
        "real_integral_limit": 1.15 * max(1.0, np.max(np.abs(real_integrals_limit))),
        "imag_integral_limit": 1.15 * max(1.0, np.max(np.abs(imag_integrals_limit))),
        "complex_limit": 1.15 * max(
            1.0,
            np.max(np.abs(real_integrals_limit)),
            np.max(np.abs(imag_integrals_limit)),
        ),
        "spectrum_limit": 1.15 * max(1.0, np.max(spectrum_fine)),
        "spectrum_fine": spectrum_fine,
        "phase_fine_full": phase_fine_full,
        "phase_fine": phase_fine,
        "phase_threshold": phase_threshold,
    }


def compute_display_limits(signal_values, time_values, normalize_by_window, basis_limit, basis_fine):
    limit_keys = (
        "signal_limit",
        "product_limit",
        "real_integral_limit",
        "imag_integral_limit",
        "complex_limit",
        "spectrum_limit",
    )
    display_limits = {key: 0.0 for key in limit_keys}

    for window_mode in WINDOW_MODES:
        window_values = build_window(time_values, T_MAX, window_mode)
        cache = compute_signal_cache(
            signal_values,
            window_values,
            time_values,
            T_MAX,
            normalize_by_window,
            basis_limit,
            basis_fine,
        )
        for key in limit_keys:
            display_limits[key] = max(display_limits[key], cache[key])

    return display_limits


def main():
    plt.close("all")
    full_window_start, full_window_end = full_time_limits()
    time_values = np.linspace(full_window_start, full_window_end, int(T_MAX * FS), endpoint=False)

    basis_limit = np.exp(-1j * 2.0 * np.pi * DISPLAY_LIMIT_FREQS[:, None] * time_values[None, :])
    basis_fine = np.exp(-1j * 2.0 * np.pi * DISPLAY_FINE_FREQS[:, None] * time_values[None, :])

    initial_signal, initial_label = build_selectable_signal(
        time_values, DEFAULT_SIGNAL_MODE, DEFAULT_SIGNAL_FREQ
    )
    initial_window = build_window(time_values, DEFAULT_OBS_DURATION, DEFAULT_WINDOW_MODE)
    state = {
        "signal_mode": DEFAULT_SIGNAL_MODE,
        "window_mode": DEFAULT_WINDOW_MODE,
        "signal_freq": DEFAULT_SIGNAL_FREQ,
        "obs_duration": DEFAULT_OBS_DURATION,
        "signal_label": initial_label,
        "signal_values": initial_signal,
        "window_values": initial_window,
        "cache": compute_signal_cache(
            initial_signal,
            initial_window,
            time_values,
            DEFAULT_OBS_DURATION,
            NORMALIZE_BY_WINDOW,
            basis_limit,
            basis_fine,
        ),
        "display_cache": compute_display_limits(
            initial_signal,
            time_values,
            NORMALIZE_BY_WINDOW,
            basis_limit,
            basis_fine,
        ),
    }

    if NORMALIZE_BY_WINDOW:
        formula_line_1 = r"$X_{T_{\mathrm{obs}},w}(f)=\frac{1}{T_{\mathrm{obs}}}\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)e^{-j 2 \pi f t}\,\mathrm{d}t$"
    else:
        formula_line_1 = r"$X_{T_{\mathrm{obs}},w}(f)=\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)e^{-j 2 \pi f t}\,\mathrm{d}t$"

    fig = plt.figure(figsize=(18.6, 10.6))
    grid = fig.add_gridspec(
        2,
        4,
        width_ratios=[1.0, 1.0, 1.05, 0.95],
        height_ratios=[0.88, 1.12],
    )

    ax_real_time = fig.add_subplot(grid[0, 0])
    ax_imag_time = fig.add_subplot(grid[0, 1], sharex=ax_real_time, sharey=ax_real_time)
    ax_real_prod = fig.add_subplot(grid[1, 0], sharex=ax_real_time)
    ax_imag_prod = fig.add_subplot(grid[1, 1], sharex=ax_real_time, sharey=ax_real_prod)
    ax_complex = fig.add_subplot(grid[:, 2])
    spectrum_grid = grid[:, 3].subgridspec(2, 1, hspace=0.34)
    ax_magnitude = fig.add_subplot(spectrum_grid[0, 0])
    ax_phase = fig.add_subplot(spectrum_grid[1, 0], sharex=ax_magnitude)

    fig.subplots_adjust(left=0.05, right=0.985, top=0.89, bottom=0.29, wspace=0.42, hspace=0.34)
    fig.suptitle("Fourier Analysis as a Split into Cosine and Sine Components", fontsize=15)

    signal_limit = max(state["cache"]["signal_limit"], 1.15)

    # -------------------------
    # 1a) x(t), window, and cos(2 pi f t)
    # -------------------------
    signal_real_line, = ax_real_time.plot(time_values, state["signal_values"], color="0.10", lw=2.1)
    window_real_line, = ax_real_time.plot(time_values, state["window_values"], color=WINDOW_COLOR, lw=1.8)
    basis_real_line, = ax_real_time.plot([], [], color="tab:blue", lw=1.8, ls="--")
    ax_real_time.axhline(0.0, color="0.75", lw=0.9)
    ax_real_time.set_xlim(*observed_limits(DEFAULT_OBS_DURATION))
    ax_real_time.set_ylim(-signal_limit, signal_limit)
    ax_real_time.grid(alpha=0.25)
    ax_real_time.set_title("Time domain: x(t), w(t), and cos(2pi f t)", pad=10)
    ax_real_time.set_ylabel("Amplitude")
    ax_real_time.tick_params(axis="x", labelbottom=False)
    default_window_start, default_window_end = observed_limits(DEFAULT_OBS_DURATION)
    obs_line_real_time_left = ax_real_time.axvline(default_window_start, color="0.55", lw=1.1, ls=":")
    obs_line_real_time_right = ax_real_time.axvline(default_window_end, color="0.55", lw=1.1, ls=":")

    # -------------------------
    # 1b) Windowed product with cos and integral value
    # -------------------------
    real_product_line, = ax_real_prod.plot([], [], color="tab:blue", lw=2.0)
    real_integral_ax = ax_real_prod.twinx()
    real_integral_line, = real_integral_ax.plot([], [], color="tab:blue", lw=2.0, ls="--")

    ax_real_prod.axhline(0.0, color="0.75", lw=0.9)
    ax_real_prod.set_xlim(*observed_limits(DEFAULT_OBS_DURATION))
    ax_real_prod.set_ylim(-state["cache"]["product_limit"], state["cache"]["product_limit"])
    real_integral_ax.set_ylim(-state["cache"]["real_integral_limit"], state["cache"]["real_integral_limit"])
    ax_real_prod.grid(alpha=0.25)
    ax_real_prod.set_title("Windowed product and integral value", pad=10)
    ax_real_prod.set_xlabel("Time t [s]")
    ax_real_prod.set_ylabel(r"$x(t)w(t)\cos(2\pi f t)$", color="tab:blue")
    real_integral_ax.set_ylabel("Real-part integral value", color="tab:blue")
    ax_real_prod.tick_params(axis="y", colors="tab:blue")
    real_integral_ax.tick_params(axis="y", colors="tab:blue")
    real_integral_ax.patch.set_alpha(0.0)
    obs_line_real_prod_left = ax_real_prod.axvline(default_window_start, color="0.55", lw=1.1, ls=":")
    obs_line_real_prod_right = ax_real_prod.axvline(default_window_end, color="0.55", lw=1.1, ls=":")

    # -------------------------
    # 2a) x(t), window, and -sin(2 pi f t)
    # -------------------------
    signal_imag_line, = ax_imag_time.plot(time_values, state["signal_values"], color="0.10", lw=2.1)
    window_imag_line, = ax_imag_time.plot(time_values, state["window_values"], color=WINDOW_COLOR, lw=1.8)
    basis_imag_line, = ax_imag_time.plot([], [], color="tab:orange", lw=1.8, ls="--")
    ax_imag_time.axhline(0.0, color="0.75", lw=0.9)
    ax_imag_time.set_xlim(*observed_limits(DEFAULT_OBS_DURATION))
    ax_imag_time.set_ylim(-signal_limit, signal_limit)
    ax_imag_time.grid(alpha=0.25)
    ax_imag_time.set_title("Time domain: x(t), w(t), and -sin(2pi f t)", pad=10)
    ax_imag_time.tick_params(axis="x", labelbottom=False)
    obs_line_imag_time_left = ax_imag_time.axvline(default_window_start, color="0.55", lw=1.1, ls=":")
    obs_line_imag_time_right = ax_imag_time.axvline(default_window_end, color="0.55", lw=1.1, ls=":")

    # -------------------------
    # 2b) Windowed product with -sin and integral value
    # -------------------------
    imag_product_line, = ax_imag_prod.plot([], [], color="tab:orange", lw=2.0)
    imag_integral_ax = ax_imag_prod.twinx()
    imag_integral_line, = imag_integral_ax.plot([], [], color="tab:orange", lw=2.0, ls="--")

    ax_imag_prod.axhline(0.0, color="0.75", lw=0.9)
    ax_imag_prod.set_xlim(*observed_limits(DEFAULT_OBS_DURATION))
    ax_imag_prod.set_ylim(-state["cache"]["product_limit"], state["cache"]["product_limit"])
    imag_integral_ax.set_ylim(-state["cache"]["imag_integral_limit"], state["cache"]["imag_integral_limit"])
    ax_imag_prod.grid(alpha=0.25)
    ax_imag_prod.set_title("Windowed product and integral value", pad=10)
    ax_imag_prod.set_xlabel("Time t [s]")
    ax_imag_prod.set_ylabel(r"$x(t)w(t)(-\sin(2\pi f t))$", color="tab:orange")
    imag_integral_ax.set_ylabel("Imaginary-part integral value", color="tab:orange")
    ax_imag_prod.tick_params(axis="y", colors="tab:orange")
    imag_integral_ax.tick_params(axis="y", colors="tab:orange")
    imag_integral_ax.patch.set_alpha(0.0)
    obs_line_imag_prod_left = ax_imag_prod.axvline(default_window_start, color="0.55", lw=1.1, ls=":")
    obs_line_imag_prod_right = ax_imag_prod.axvline(default_window_end, color="0.55", lw=1.1, ls=":")

    # -------------------------
    # 3) Composition in the complex plane
    # -------------------------
    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)
    coefficient_vector, = ax_complex.plot([], [], color="crimson", lw=3.0)
    coefficient_tip, = ax_complex.plot([], [], "o", color="crimson", ms=7)
    real_projection, = ax_complex.plot([], [], color="tab:blue", lw=1.4, alpha=0.85)
    imag_projection, = ax_complex.plot([], [], color="tab:orange", lw=1.4, alpha=0.85)

    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.set_xlim(-state["display_cache"]["complex_limit"], state["display_cache"]["complex_limit"])
    ax_complex.set_ylim(-state["display_cache"]["complex_limit"], state["display_cache"]["complex_limit"])
    ax_complex.grid(alpha=0.22)
    ax_complex.set_xlabel(r"Re$\{X_T(f)\}$")
    ax_complex.set_ylabel(r"Im$\{X_T(f)\}$")
    ax_complex.set_title("Complex coefficient from both integral values", pad=10)

    complex_pos = ax_complex.get_position()

    # -------------------------
    # 4a) Magnitude spectrum
    # -------------------------
    magnitude_line, = ax_magnitude.plot(DISPLAY_FINE_FREQS, state["cache"]["spectrum_fine"], color="0.25", lw=2.0)
    magnitude_freq_line = ax_magnitude.axvline(DEFAULT_ANALYSIS_FREQ, color="tab:blue", lw=1.5, alpha=0.85)
    magnitude_marker, = ax_magnitude.plot([], [], "o", color="crimson", ms=8)

    ax_magnitude.axhline(0.0, color="0.75", lw=0.9)
    ax_magnitude.set_xlim(ANALYSIS_FREQ_MIN, ANALYSIS_FREQ_MAX)
    ax_magnitude.set_ylim(0.0, state["display_cache"]["spectrum_limit"])
    ax_magnitude.grid(alpha=0.25)
    ax_magnitude.set_ylabel(r"$|X_T(f)|$")
    ax_magnitude.set_title("Magnitude spectrum", pad=10)
    ax_magnitude.tick_params(axis="x", labelbottom=False)

    # -------------------------
    # 4b) Phase spectrum
    # -------------------------
    phase_line, = ax_phase.plot(DISPLAY_FINE_FREQS, state["cache"]["phase_fine"], color="0.45", lw=1.9)
    phase_freq_line = ax_phase.axvline(DEFAULT_ANALYSIS_FREQ, color="tab:blue", lw=1.5, alpha=0.85)
    phase_marker, = ax_phase.plot([], [], "o", color="crimson", ms=8)

    ax_phase.axhline(0.0, color="0.75", lw=0.9)
    ax_phase.set_xlim(ANALYSIS_FREQ_MIN, ANALYSIS_FREQ_MAX)
    ax_phase.set_ylim(-190.0, 190.0)
    ax_phase.set_yticks([-180, -90, 0, 90, 180])
    ax_phase.grid(alpha=0.25)
    ax_phase.set_xlabel("Frequency f [Hz]")
    ax_phase.set_ylabel("Phase [deg]")
    ax_phase.set_title("Phase spectrum", pad=10)

    result_box = fig.text(
        complex_pos.x0,
        complex_pos.y0 - 0.060,
        "",
        ha="left",
        va="top",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.92, edgecolor="0.85"),
    )

    fig.text(0.50, 0.205, formula_line_1, ha="center", fontsize=13)
    if NORMALIZE_BY_WINDOW:
        formula_segments = [
            (r"$=\frac{1}{T_{\mathrm{obs}}}\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)\,$", "black"),
            (r"$\cos(2\pi f t)$", "tab:blue"),
            (r"$\,\mathrm{d}t + j\,\frac{1}{T_{\mathrm{obs}}}\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)(-\,$", "black"),
            (r"$\sin(2\pi f t)$", "tab:orange"),
            (r"$)\,\mathrm{d}t$", "black"),
        ]
    else:
        formula_segments = [
            (r"$=\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)\,$", "black"),
            (r"$\cos(2\pi f t)$", "tab:blue"),
            (r"$\,\mathrm{d}t + j\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)(-\,$", "black"),
            (r"$\sin(2\pi f t)$", "tab:orange"),
            (r"$)\,\mathrm{d}t$", "black"),
        ]
    add_centered_formula_segments(fig, 0.177, formula_segments, fontsize=12)

    mode_ax = fig.add_axes([0.04, 0.025, 0.10, 0.12])
    mode_ax.set_title("", fontsize=10, pad=0)
    signal_mode_selector = RadioButtons(mode_ax, SIGNAL_MODES, active=SIGNAL_MODES.index(DEFAULT_SIGNAL_MODE))
    for label in signal_mode_selector.labels:
        label.set_fontsize(9)

    window_ax = fig.add_axes([0.16, 0.025, 0.12, 0.12])
    window_ax.set_title("", fontsize=10, pad=0)
    window_mode_selector = RadioButtons(window_ax, WINDOW_MODES, active=WINDOW_MODES.index(DEFAULT_WINDOW_MODE))
    for label in window_mode_selector.labels:
        label.set_fontsize(9)

    signal_label_text = fig.text(
        0.04,
        0.162,
        state["signal_label"],
        ha="left",
        va="bottom",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.90, edgecolor="0.82"),
    )

    duration_slider_ax = fig.add_axes([0.31, 0.040, 0.55, 0.030])
    obs_duration_slider = Slider(
        ax=duration_slider_ax,
        label="",
        valmin=OBS_DURATION_MIN,
        valmax=T_MAX,
        valinit=DEFAULT_OBS_DURATION,
        valstep=SLIDER_STEP,
        color="tab:blue",
    )
    fig.text(0.900, 0.056, "Observation duration T_obs [s]", ha="left", va="center", fontsize=10)

    signal_slider_ax = fig.add_axes([0.31, 0.080, 0.55, 0.030])
    signal_freq_slider = Slider(
        ax=signal_slider_ax,
        label="",
        valmin=FREQ_MIN,
        valmax=FREQ_MAX,
        valinit=DEFAULT_SIGNAL_FREQ,
        valstep=SLIDER_STEP,
        color="tab:blue",
    )
    fig.text(0.900, 0.096, "Signal frequency f_x [Hz]", ha="left", va="center", fontsize=10)

    analysis_slider_ax = fig.add_axes([0.31, 0.120, 0.55, 0.030])
    analysis_freq_slider = Slider(
        ax=analysis_slider_ax,
        label="",
        valmin=ANALYSIS_FREQ_MIN,
        valmax=ANALYSIS_FREQ_MAX,
        valinit=DEFAULT_ANALYSIS_FREQ,
        valstep=SLIDER_STEP,
        color="tab:blue",
    )
    fig.text(0.900, 0.136, "Probe frequency f [Hz]", ha="left", va="center", fontsize=10)

    real_positive_fill = None
    real_negative_fill = None
    imag_positive_fill = None
    imag_negative_fill = None

    def update_signal_control_style():
        active = signal_mode_selector.value_selected in ("Cosine", "Sine")
        alpha = 1.0 if active else 0.45
        signal_freq_slider.poly.set_alpha(alpha)
        signal_freq_slider.valtext.set_alpha(alpha)
        signal_slider_ax.patch.set_alpha(0.35 if active else 0.15)

    def apply_signal_cache():
        cache = state["cache"]
        display_cache = state["display_cache"]
        current_signal_limit = max(display_cache["signal_limit"], 1.15)
        window_start, window_end = observed_limits(state["obs_duration"])

        signal_real_line.set_data(time_values, state["signal_values"])
        signal_imag_line.set_data(time_values, state["signal_values"])
        window_real_line.set_data(time_values, state["window_values"])
        window_imag_line.set_data(time_values, state["window_values"])
        signal_label_text.set_text(state["signal_label"])

        ax_real_time.set_xlim(window_start, window_end)
        ax_imag_time.set_xlim(window_start, window_end)
        ax_real_prod.set_xlim(window_start, window_end)
        ax_imag_prod.set_xlim(window_start, window_end)

        ax_real_time.set_ylim(-current_signal_limit, current_signal_limit)
        ax_imag_time.set_ylim(-current_signal_limit, current_signal_limit)
        ax_real_prod.set_ylim(-display_cache["product_limit"], display_cache["product_limit"])
        ax_imag_prod.set_ylim(-display_cache["product_limit"], display_cache["product_limit"])
        real_integral_ax.set_ylim(-display_cache["real_integral_limit"], display_cache["real_integral_limit"])
        imag_integral_ax.set_ylim(-display_cache["imag_integral_limit"], display_cache["imag_integral_limit"])
        ax_complex.set_xlim(-display_cache["complex_limit"], display_cache["complex_limit"])
        ax_complex.set_ylim(-display_cache["complex_limit"], display_cache["complex_limit"])
        ax_magnitude.set_ylim(0.0, display_cache["spectrum_limit"])

        magnitude_line.set_data(DISPLAY_FINE_FREQS, cache["spectrum_fine"])
        phase_line.set_data(DISPLAY_FINE_FREQS, cache["phase_fine"])

        obs_line_real_time_left.set_xdata([window_start, window_start])
        obs_line_real_time_right.set_xdata([window_end, window_end])
        obs_line_real_prod_left.set_xdata([window_start, window_start])
        obs_line_real_prod_right.set_xdata([window_end, window_end])
        obs_line_imag_time_left.set_xdata([window_start, window_start])
        obs_line_imag_time_right.set_xdata([window_end, window_end])
        obs_line_imag_prod_left.set_xdata([window_start, window_start])
        obs_line_imag_prod_right.set_xdata([window_end, window_end])

    def redraw(probe_freq):
        nonlocal real_positive_fill, real_negative_fill, imag_positive_fill, imag_negative_fill

        (
            signal_plot,
            window_plot,
            basis_real_plot,
            basis_imag_plot,
            real_product,
            imag_product,
            real_integral,
            imag_integral,
            coefficient,
        ) = evaluate_frequency(
            probe_freq,
            time_values,
            state["signal_values"],
            state["window_values"],
            state["obs_duration"],
            NORMALIZE_BY_WINDOW,
        )
        window_start, window_end = observed_limits(state["obs_duration"])

        signal_real_line.set_data(time_values, signal_plot)
        signal_imag_line.set_data(time_values, signal_plot)
        window_real_line.set_data(time_values, window_plot)
        window_imag_line.set_data(time_values, window_plot)
        basis_real_line.set_data(time_values, basis_real_plot)
        basis_imag_line.set_data(time_values, basis_imag_plot)

        real_product_line.set_data(time_values, real_product)
        real_integral_line.set_data([window_start, window_end], [real_integral, real_integral])

        imag_product_line.set_data(time_values, imag_product)
        imag_integral_line.set_data([window_start, window_end], [imag_integral, imag_integral])

        obs_line_real_time_left.set_xdata([window_start, window_start])
        obs_line_real_time_right.set_xdata([window_end, window_end])
        obs_line_real_prod_left.set_xdata([window_start, window_start])
        obs_line_real_prod_right.set_xdata([window_end, window_end])
        obs_line_imag_time_left.set_xdata([window_start, window_start])
        obs_line_imag_time_right.set_xdata([window_end, window_end])
        obs_line_imag_prod_left.set_xdata([window_start, window_start])
        obs_line_imag_prod_right.set_xdata([window_end, window_end])

        if real_positive_fill is not None:
            real_positive_fill.remove()
        if real_negative_fill is not None:
            real_negative_fill.remove()
        if imag_positive_fill is not None:
            imag_positive_fill.remove()
        if imag_negative_fill is not None:
            imag_negative_fill.remove()

        real_positive_fill = ax_real_prod.fill_between(
            time_values,
            0.0,
            real_product,
            where=real_product >= 0.0,
            color="tab:blue",
            alpha=0.22,
            interpolate=True,
        )
        real_negative_fill = ax_real_prod.fill_between(
            time_values,
            0.0,
            real_product,
            where=real_product < 0.0,
            color="tab:red",
            alpha=0.18,
            interpolate=True,
        )
        imag_positive_fill = ax_imag_prod.fill_between(
            time_values,
            0.0,
            imag_product,
            where=imag_product >= 0.0,
            color="tab:orange",
            alpha=0.24,
            interpolate=True,
        )
        imag_negative_fill = ax_imag_prod.fill_between(
            time_values,
            0.0,
            imag_product,
            where=imag_product < 0.0,
            color="tab:red",
            alpha=0.18,
            interpolate=True,
        )

        coefficient_vector.set_data([0.0, coefficient.real], [0.0, coefficient.imag])
        coefficient_tip.set_data([coefficient.real], [coefficient.imag])
        real_projection.set_data([0.0, coefficient.real], [0.0, 0.0])
        imag_projection.set_data([coefficient.real, coefficient.real], [0.0, coefficient.imag])

        magnitude_freq_line.set_xdata([probe_freq, probe_freq])
        magnitude_marker.set_data([probe_freq], [abs(coefficient)])
        phase_freq_line.set_xdata([probe_freq, probe_freq])
        phase_marker.set_data([probe_freq], [np.degrees(np.angle(coefficient))])

        result_box.set_text(
            "\n".join([
                "Result",
                f"X_T(f) = {fmt_complex(coefficient)}",
                f"|X_T(f)| = {abs(coefficient):.3f}",
                "For real x(t): X_T(-f) = X_T^*(f)",
            ])
        )

        fig.canvas.draw_idle()

    def rebuild_signal(_=None):
        signal_mode = signal_mode_selector.value_selected
        window_mode = window_mode_selector.value_selected
        signal_freq = signal_freq_slider.val
        obs_duration = obs_duration_slider.val
        signal_values, signal_label = build_selectable_signal(time_values, signal_mode, signal_freq)
        window_values = build_window(time_values, obs_duration, window_mode)

        state["signal_mode"] = signal_mode
        state["window_mode"] = window_mode
        state["signal_freq"] = signal_freq
        state["obs_duration"] = obs_duration
        state["signal_values"] = signal_values
        state["window_values"] = window_values
        state["signal_label"] = signal_label
        state["cache"] = compute_signal_cache(
            signal_values,
            window_values,
            time_values,
            obs_duration,
            NORMALIZE_BY_WINDOW,
            basis_limit,
            basis_fine,
        )
        state["display_cache"] = compute_display_limits(
            signal_values,
            time_values,
            NORMALIZE_BY_WINDOW,
            basis_limit,
            basis_fine,
        )

        update_signal_control_style()
        apply_signal_cache()
        redraw(analysis_freq_slider.val)

    update_signal_control_style()
    apply_signal_cache()
    redraw(DEFAULT_ANALYSIS_FREQ)

    analysis_freq_slider.on_changed(redraw)
    obs_duration_slider.on_changed(rebuild_signal)
    signal_freq_slider.on_changed(rebuild_signal)
    signal_mode_selector.on_clicked(rebuild_signal)
    window_mode_selector.on_clicked(rebuild_signal)

    plt.show()


if __name__ == "__main__":
    main()

