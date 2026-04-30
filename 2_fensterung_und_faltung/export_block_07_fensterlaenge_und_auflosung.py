from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "07_fensterlaenge_und_auflosung"
)

DPI = 200
FIGSIZE = (12.0, 4.4)
SINGLE_WINDOW_FIGSIZE = (12.0, 11.2)
REFERENCE_PAIR_FIGSIZE = (12.0, 6.6)
REFERENCE_TRIPLET_FIGSIZE = (12.0, 11.2)
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEGEND_SIZE = 14
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86
REFERENCE_TITLE_SIZE = 22
REFERENCE_LABEL_SIZE = 18
REFERENCE_TICK_SIZE = 15
REFERENCE_LEGEND_SIZE = 13
REFERENCE_BOTTOM_MARGIN = 0.10
REFERENCE_TOP_MARGIN = 0.92
REFERENCE_HSPACE = 0.42

SIGNAL_BLACK = "0.10"
WINDOW_GREEN = "#66b77a"
SPECTRUM_BLUE = "#2b7bbb"
COMPARE_ORANGE = "#d98c2f"
BLACKMAN_RED = "#c45b4d"
GREY_MEDIUM = "0.55"
BOUNDARY_GREY = "0.72"
SMALL_WINDOW_GREY = "0.90"

TIME_HALF_WIDTH = 2.0
SMALL_TIME_HALF_WIDTH = 1.0
TIME_START = -2.2
TIME_END = 2.2
FREQ_START = -6.0
FREQ_END = 6.0
EXT_FREQ_START = -12.0
EXT_FREQ_END = 12.0
LOG_FLOOR_DB = -80.0
FREQ_CHUNK_SIZE = 180

TIME_VALUES = np.linspace(TIME_START, TIME_END, 8801)
FREQUENCY_VALUES = np.linspace(FREQ_START, FREQ_END, 5001)
FREQUENCY_VALUES_EXT = np.linspace(EXT_FREQ_START, EXT_FREQ_END, 9001)
COMMON_TIME_XTICKS = np.arange(-2.0, 2.01, 1.0)
COMMON_FREQ_XTICKS = np.arange(FREQ_START, FREQ_END + 1e-9, 2.0)
COSINE_LINE_FREQUENCIES = (-2.0, 2.0)
COSINE_LINE_AMPLITUDES = (0.5, 0.5)
TIME_COSINE_FREQUENCY = 2.0


def inside_support(time_values):
    return np.abs(time_values) <= TIME_HALF_WIDTH


def inside_support_with_half_width(time_values, half_width):
    return np.abs(time_values) <= half_width


def rect_window(time_values):
    values = np.zeros_like(time_values)
    mask = inside_support(time_values)
    values[mask] = 1.0
    return values


def hann_window(time_values):
    values = np.zeros_like(time_values)
    mask = inside_support(time_values)
    values[mask] = 0.5 * (1.0 + np.cos(np.pi * time_values[mask] / TIME_HALF_WIDTH))
    return values


def hamming_window(time_values):
    values = np.zeros_like(time_values)
    mask = inside_support(time_values)
    values[mask] = 0.54 + 0.46 * np.cos(np.pi * time_values[mask] / TIME_HALF_WIDTH)
    return values


def blackman_window(time_values):
    values = np.zeros_like(time_values)
    mask = inside_support(time_values)
    phase = np.pi * time_values[mask] / TIME_HALF_WIDTH
    values[mask] = 0.42 + 0.50 * np.cos(phase) + 0.08 * np.cos(2.0 * phase)
    return values


def rect_window_with_half_width(time_values, half_width):
    values = np.zeros_like(time_values)
    mask = inside_support_with_half_width(time_values, half_width)
    values[mask] = 1.0
    return values


def hann_window_with_half_width(time_values, half_width):
    values = np.zeros_like(time_values)
    mask = inside_support_with_half_width(time_values, half_width)
    values[mask] = 0.5 * (1.0 + np.cos(np.pi * time_values[mask] / half_width))
    return values


def hamming_window_with_half_width(time_values, half_width):
    values = np.zeros_like(time_values)
    mask = inside_support_with_half_width(time_values, half_width)
    values[mask] = 0.54 + 0.46 * np.cos(np.pi * time_values[mask] / half_width)
    return values


def blackman_window_with_half_width(time_values, half_width):
    values = np.zeros_like(time_values)
    mask = inside_support_with_half_width(time_values, half_width)
    phase = np.pi * time_values[mask] / half_width
    values[mask] = 0.42 + 0.50 * np.cos(phase) + 0.08 * np.cos(2.0 * phase)
    return values


WINDOW_SPECS = [
    ("rectangular", "Rectangular", WINDOW_GREEN, rect_window),
    ("hann", "Hann", SPECTRUM_BLUE, hann_window),
    ("hamming", "Hamming", COMPARE_ORANGE, hamming_window),
    ("blackman", "Blackman", BLACKMAN_RED, blackman_window),
]

SMALL_WINDOW_SPECS = {
    "rectangular": rect_window_with_half_width,
    "hann": hann_window_with_half_width,
    "hamming": hamming_window_with_half_width,
    "blackman": blackman_window_with_half_width,
}


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def create_figure():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=BOTTOM_MARGIN,
        top=TOP_MARGIN,
    )
    return fig, ax


def create_single_window_figure():
    fig, axes = plt.subplots(3, 1, figsize=SINGLE_WINDOW_FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=0.07,
        top=0.95,
        hspace=0.55,
    )
    return fig, axes


def create_reference_pair_figure():
    fig, axes = plt.subplots(2, 1, figsize=REFERENCE_PAIR_FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=REFERENCE_BOTTOM_MARGIN,
        top=REFERENCE_TOP_MARGIN,
        hspace=REFERENCE_HSPACE,
    )
    return fig, axes


def create_reference_triplet_figure():
    fig, axes = plt.subplots(3, 1, figsize=REFERENCE_TRIPLET_FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=0.07,
        top=0.95,
        hspace=0.55,
    )
    return fig, axes


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
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


def style_time_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(TIME_START, TIME_END)
    ax.set_xticks(COMMON_TIME_XTICKS)
    ax.set_ylim(-0.06, 1.12)
    ax.set_yticks(np.arange(0.0, 1.01, 0.2))
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_linear_frequency_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(FREQ_START, FREQ_END)
    ax.set_xticks(COMMON_FREQ_XTICKS)
    ax.set_ylim(-0.02, 1.05)
    ax.set_yticks(np.arange(0.0, 1.01, 0.2))
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Normalized magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_log_frequency_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(FREQ_START, FREQ_END)
    ax.set_xticks(COMMON_FREQ_XTICKS)
    ax.set_ylim(LOG_FLOOR_DB, 5.0)
    ax.set_yticks(np.arange(LOG_FLOOR_DB, 1.0, 20.0))
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_reference_aux_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(FREQ_START, FREQ_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_FREQ_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=REFERENCE_TITLE_SIZE)
    ax.set_xlabel(r"Auxiliary frequency $\nu$ [Hz]", fontsize=REFERENCE_LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=REFERENCE_LABEL_SIZE)
    ax.tick_params(labelsize=REFERENCE_TICK_SIZE)


def style_reference_output_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(FREQ_START, FREQ_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_FREQ_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=REFERENCE_TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=REFERENCE_LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=REFERENCE_LABEL_SIZE)
    ax.tick_params(labelsize=REFERENCE_TICK_SIZE)


def style_reference_log_output_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(FREQ_START, FREQ_END)
    ax.set_ylim(LOG_FLOOR_DB, 5.0)
    ax.set_xticks(COMMON_FREQ_XTICKS)
    ax.set_yticks(np.arange(LOG_FLOOR_DB, 1.0, 20.0))
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=REFERENCE_TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=REFERENCE_LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=REFERENCE_LABEL_SIZE)
    ax.tick_params(labelsize=REFERENCE_TICK_SIZE)


def compute_normalized_spectrum(window_values, frequency_values):
    spectrum = np.zeros_like(frequency_values, dtype=np.complex128)
    for start in range(0, len(frequency_values), FREQ_CHUNK_SIZE):
        stop = min(start + FREQ_CHUNK_SIZE, len(frequency_values))
        freq_chunk = frequency_values[start:stop]
        phase_matrix = np.exp(-1j * 2.0 * np.pi * freq_chunk[:, None] * TIME_VALUES[None, :])
        integrand = phase_matrix * window_values[None, :]
        spectrum[start:stop] = np.trapezoid(integrand, TIME_VALUES, axis=1)
    magnitude = np.abs(spectrum)
    return magnitude / np.max(magnitude)


WINDOW_DATA = {}
for key, label, color, window_fn in WINDOW_SPECS:
    time_values = window_fn(TIME_VALUES)
    magnitude_linear = compute_normalized_spectrum(time_values, FREQUENCY_VALUES)
    magnitude_linear_ext = compute_normalized_spectrum(time_values, FREQUENCY_VALUES_EXT)
    magnitude_db = 20.0 * np.log10(np.maximum(magnitude_linear, 10.0 ** (LOG_FLOOR_DB / 20.0)))
    WINDOW_DATA[key] = {
        "label": label,
        "color": color,
        "time_values": time_values,
        "magnitude_linear": magnitude_linear,
        "magnitude_linear_ext": magnitude_linear_ext,
        "magnitude_db": magnitude_db,
    }


SMALL_WINDOW_DATA = {}
for key, window_fn in SMALL_WINDOW_SPECS.items():
    time_values = window_fn(TIME_VALUES, SMALL_TIME_HALF_WIDTH)
    SMALL_WINDOW_DATA[key] = {
        "time_values": time_values,
        "magnitude_linear": compute_normalized_spectrum(time_values, FREQUENCY_VALUES),
        "magnitude_linear_ext": compute_normalized_spectrum(time_values, FREQUENCY_VALUES_EXT),
    }


def plot_window(ax, values, color, alpha=0.18):
    ax.fill_between(TIME_VALUES, 0.0, values, color=color, alpha=alpha, zorder=2)
    ax.plot(TIME_VALUES, values, color=color, lw=2.4, zorder=3)
    ax.axvline(-TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.3, ls="--", zorder=1)
    ax.axvline(TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.3, ls="--", zorder=1)


def shifted_window_copy(window_key):
    window = WINDOW_DATA[window_key]
    shifted_sum = np.zeros_like(FREQUENCY_VALUES, dtype=float)
    for line_frequency, line_amplitude in zip(COSINE_LINE_FREQUENCIES, COSINE_LINE_AMPLITUDES):
        shifted_sum += np.interp(
            FREQUENCY_VALUES - line_frequency,
            FREQUENCY_VALUES_EXT,
            window["magnitude_linear_ext"],
            left=0.0,
            right=0.0,
        ) * line_amplitude
    return shifted_sum


def shifted_small_window_copy(window_key):
    window = SMALL_WINDOW_DATA[window_key]
    shifted_sum = np.zeros_like(FREQUENCY_VALUES, dtype=float)
    for line_frequency, line_amplitude in zip(COSINE_LINE_FREQUENCIES, COSINE_LINE_AMPLITUDES):
        shifted_sum += np.interp(
            FREQUENCY_VALUES - line_frequency,
            FREQUENCY_VALUES_EXT,
            window["magnitude_linear_ext"],
            left=0.0,
            right=0.0,
        ) * line_amplitude
    return shifted_sum


def draw_reference_lines(ax):
    ax.vlines(COSINE_LINE_FREQUENCIES, 0.0, COSINE_LINE_AMPLITUDES, color=SPECTRUM_BLUE, lw=3.2, zorder=4)


def export_window_cosine_result(index, key):
    window = WINDOW_DATA[key]
    small_window = SMALL_WINDOW_DATA[key]
    fig, (ax_top, ax_mid, ax_bottom) = create_reference_triplet_figure()

    ax_top.fill_between(FREQUENCY_VALUES, 0.0, window["magnitude_linear"], color=window["color"], alpha=0.16, zorder=1)
    ax_top.plot(
        FREQUENCY_VALUES,
        small_window["magnitude_linear"],
        color=SMALL_WINDOW_GREY,
        lw=2.2,
        zorder=2,
    )
    ax_top.plot(FREQUENCY_VALUES, window["magnitude_linear"], color=window["color"], lw=2.5, zorder=2)
    draw_reference_lines(ax_top)
    style_reference_aux_axis(ax_top, f'{window["label"]} and mirrored spectral lines')
    ax_top.legend(
        [
            Line2D([0], [0], color=window["color"], lw=2.5),
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=3.2),
        ],
        [r"$W(\nu)$", r"$X(f)$ at $\pm 2$ Hz"],
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=REFERENCE_LEGEND_SIZE,
        borderaxespad=0.6,
    )

    observed_linear = shifted_window_copy(key)
    observed_linear_small = shifted_small_window_copy(key)
    observed_db = 20.0 * np.log10(
        np.maximum(observed_linear / np.max(observed_linear), 10.0 ** (LOG_FLOOR_DB / 20.0))
    )
    observed_db_small = 20.0 * np.log10(
        np.maximum(observed_linear_small / np.max(observed_linear_small), 10.0 ** (LOG_FLOOR_DB / 20.0))
    )

    ax_mid.plot(FREQUENCY_VALUES, observed_linear_small, color=SMALL_WINDOW_GREY, lw=2.2, zorder=2)
    ax_mid.plot(FREQUENCY_VALUES, observed_linear, color=SIGNAL_BLACK, lw=2.6, zorder=3)
    style_reference_output_axis(ax_mid, r"Observed Spectrum $Y(f)$")

    ax_bottom.plot(FREQUENCY_VALUES, observed_db_small, color=SMALL_WINDOW_GREY, lw=2.2, zorder=2)
    ax_bottom.plot(FREQUENCY_VALUES, observed_db, color=SIGNAL_BLACK, lw=2.6, zorder=3)
    style_reference_log_output_axis(ax_bottom, r"Observed Spectrum $Y(f)$ in dB")

    save_figure(fig, f"{index:02d}_{key}_observed_spectrum_full.png")


def export_windowed_cosine_time_plot(index, key):
    window = WINDOW_DATA[key]
    small_window = SMALL_WINDOW_DATA[key]
    cosine_values = np.cos(2.0 * np.pi * TIME_COSINE_FREQUENCY * TIME_VALUES)
    observed_time = window["time_values"] * cosine_values
    observed_time_small = small_window["time_values"] * cosine_values
    fig, ax = create_figure()

    ax.plot(TIME_VALUES, cosine_values, color=SPECTRUM_BLUE, lw=2.2, ls="--", zorder=1)
    ax.plot(TIME_VALUES, window["time_values"], color=window["color"], lw=2.2, zorder=2)
    ax.plot(TIME_VALUES, observed_time_small, color=SMALL_WINDOW_GREY, lw=2.2, zorder=2.5)
    ax.plot(TIME_VALUES, observed_time, color=SIGNAL_BLACK, lw=2.6, zorder=3)
    ax.axvline(-TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.2, ls="--", zorder=0)
    ax.axvline(TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.2, ls="--", zorder=0)
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(TIME_START, TIME_END)
    ax.set_xticks(COMMON_TIME_XTICKS)
    ax.set_ylim(-1.15, 1.15)
    ax.set_yticks(np.arange(-1.0, 1.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_title(f'{window["label"]} in time domain', pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.legend(
        [
            Line2D([0], [0], color=SPECTRUM_BLUE, lw=2.2, ls="--"),
            Line2D([0], [0], color=window["color"], lw=2.2),
            Line2D([0], [0], color=SIGNAL_BLACK, lw=2.6),
        ],
        [r"$\cos(2\pi \cdot 2\, t)$", r"$w(t)$", r"$x(t)w(t)$"],
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )

    save_figure(fig, f"{index:02d}_{key}_windowed_time_domain.png")


def export_single_window_overview(index, key):
    window = WINDOW_DATA[key]
    small_window = SMALL_WINDOW_DATA[key]
    fig, axes = create_single_window_figure()
    ax_time, ax_linear, ax_log = axes

    plot_window(ax_time, small_window["time_values"], SMALL_WINDOW_GREY, alpha=0.12)
    plot_window(ax_time, window["time_values"], window["color"], alpha=0.20)
    style_time_axis(ax_time, f'{window["label"]} window')
    add_inset_legend(
        ax_time,
        [
            Line2D([0], [0], color=SMALL_WINDOW_GREY, lw=2.4, label=r"reference support $\pm 1$ s"),
            Patch(facecolor=window["color"], edgecolor=window["color"], alpha=0.20, label=window["label"]),
            Line2D([0], [0], color=BOUNDARY_GREY, lw=1.3, ls="--", label=r"support $\pm T/2$"),
        ],
        loc="center left",
    )

    ax_linear.plot(FREQUENCY_VALUES, small_window["magnitude_linear"], color=SMALL_WINDOW_GREY, lw=2.2)
    ax_linear.plot(FREQUENCY_VALUES, window["magnitude_linear"], color=window["color"], lw=2.4)
    style_linear_frequency_axis(ax_linear, f'{window["label"]} spectrum (linear)')

    small_window_magnitude_db = 20.0 * np.log10(
        np.maximum(small_window["magnitude_linear"], 10.0 ** (LOG_FLOOR_DB / 20.0))
    )
    ax_log.plot(FREQUENCY_VALUES, small_window_magnitude_db, color=SMALL_WINDOW_GREY, lw=2.2)
    ax_log.plot(FREQUENCY_VALUES, window["magnitude_db"], color=window["color"], lw=2.4)
    style_log_frequency_axis(ax_log, f'{window["label"]} spectrum (logarithmic)')

    save_figure(fig, f"{index:02d}_{key}_window_and_spectra.png")


def export_combined_comparison():
    fig, axes = create_single_window_figure()
    ax_time, ax_linear, ax_log = axes

    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        ax_time.plot(TIME_VALUES, window["time_values"], color=window["color"], lw=2.4)
    ax_time.axvline(-TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.3, ls="--")
    ax_time.axvline(TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.3, ls="--")
    style_time_axis(ax_time, "Window functions")
    add_inset_legend(
        ax_time,
        [Line2D([0], [0], color=WINDOW_DATA[key]["color"], lw=2.4, label=WINDOW_DATA[key]["label"]) for key, _, _, _ in WINDOW_SPECS],
        loc="center left",
    )

    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        ax_linear.plot(FREQUENCY_VALUES, window["magnitude_linear"], color=window["color"], lw=2.4)
    style_linear_frequency_axis(ax_linear, "Window spectra (linear)")

    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        ax_log.plot(FREQUENCY_VALUES, window["magnitude_db"], color=window["color"], lw=2.4)
    style_log_frequency_axis(ax_log, "Window spectra (logarithmic)")

    save_figure(fig, "05_window_comparison_and_spectra.png")


def main():
    clear_output_dir()
    export_single_window_overview(1, "rectangular")
    export_single_window_overview(2, "hann")
    export_single_window_overview(3, "hamming")
    export_single_window_overview(4, "blackman")
    export_combined_comparison()
    export_window_cosine_result(6, "rectangular")
    export_window_cosine_result(7, "hann")
    export_window_cosine_result(8, "hamming")
    export_window_cosine_result(9, "blackman")
    export_windowed_cosine_time_plot(10, "rectangular")
    export_windowed_cosine_time_plot(11, "hann")
    export_windowed_cosine_time_plot(12, "hamming")
    export_windowed_cosine_time_plot(13, "blackman")
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
