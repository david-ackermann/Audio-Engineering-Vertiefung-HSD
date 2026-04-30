from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "06_fenstervergleich"
    / "06B_tradeoff_hauptkeule_und_nebenkeulen"
)

DPI = 200
FIGSIZE = (12.0, 4.4)
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEGEND_SIZE = 14
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

WINDOW_GREEN = "#66b77a"
SPECTRUM_BLUE = "#2b7bbb"
COMPARE_ORANGE = "#d98c2f"
BLACKMAN_RED = "#c45b4d"
BOUNDARY_GREY = "0.72"
SIGNAL_BLACK = "0.10"
GREY_MEDIUM = "0.55"

TIME_HALF_WIDTH = 1.0
TIME_START = -2.2
TIME_END = 2.2
FREQ_START = -6.0
FREQ_END = 6.0
LOG_FLOOR_DB = -80.0
FREQ_CHUNK_SIZE = 220
MIN_SIDELOBE_MAGNITUDE = 1.0e-3

TIME_VALUES = np.linspace(TIME_START, TIME_END, 8801)
FREQUENCY_VALUES = np.linspace(FREQ_START, FREQ_END, 5001)
POSITIVE_FREQUENCIES = np.linspace(0.0, 8.0, 40001)
COMMON_TIME_XTICKS = np.arange(-2.0, 2.01, 1.0)
COMMON_FREQ_XTICKS = np.arange(FREQ_START, FREQ_END + 1e-9, 2.0)


def inside_support(time_values):
    return np.abs(time_values) <= TIME_HALF_WIDTH


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


WINDOW_SPECS = [
    ("rectangular", "Rectangular", WINDOW_GREEN, rect_window),
    ("hann", "Hann", SPECTRUM_BLUE, hann_window),
    ("hamming", "Hamming", COMPARE_ORANGE, hamming_window),
    ("blackman", "Blackman", BLACKMAN_RED, blackman_window),
]


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


def create_pair_figure():
    fig, axes = plt.subplots(2, 1, figsize=(12.0, 7.3))
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=0.10,
        top=0.93,
        hspace=0.42,
    )
    return fig, axes


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


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


def first_local_minimum_index(values):
    slope = np.diff(values)
    for idx in range(1, len(slope)):
        if slope[idx - 1] < 0.0 and slope[idx] >= 0.0:
            return idx
    return int(np.argmin(values[1:])) + 1


def first_local_maximum_after(values, start_index):
    slope = np.diff(values)
    for idx in range(max(start_index + 1, 1), len(slope)):
        if slope[idx - 1] > 0.0 and slope[idx] <= 0.0:
            return idx
    return start_index + int(np.argmax(values[start_index:]))


def next_local_minimum_index(values, start_index):
    slope = np.diff(values)
    for idx in range(max(start_index + 1, 1), len(slope)):
        if slope[idx - 1] < 0.0 and slope[idx] >= 0.0:
            return idx
    return len(values) - 1


def first_relevant_local_maximum_after(values, start_index, min_height):
    slope = np.diff(values)
    for idx in range(max(start_index + 1, 1), len(slope)):
        if slope[idx - 1] > 0.0 and slope[idx] <= 0.0 and values[idx] >= min_height:
            return idx
    return first_local_maximum_after(values, start_index)


WINDOW_DATA = {}
for key, label, color, window_fn in WINDOW_SPECS:
    time_values = window_fn(TIME_VALUES)
    magnitude_display = compute_normalized_spectrum(time_values, FREQUENCY_VALUES)
    magnitude_positive = compute_normalized_spectrum(time_values, POSITIVE_FREQUENCIES)
    first_min_idx = first_local_minimum_index(magnitude_positive)
    first_max_idx = first_relevant_local_maximum_after(
        magnitude_positive,
        first_min_idx,
        MIN_SIDELOBE_MAGNITUDE,
    )
    WINDOW_DATA[key] = {
        "label": label,
        "color": color,
        "time_values": time_values,
        "magnitude_display": magnitude_display,
        "magnitude_positive": magnitude_positive,
        "main_lobe_half_width": POSITIVE_FREQUENCIES[first_min_idx],
        "main_lobe_full_width": 2.0 * POSITIVE_FREQUENCIES[first_min_idx],
        "first_sidelobe_frequency": POSITIVE_FREQUENCIES[first_max_idx],
        "first_sidelobe_level_db": 20.0 * np.log10(
            np.maximum(magnitude_positive[first_max_idx], 10.0 ** (LOG_FLOOR_DB / 20.0))
        ),
    }


def export_same_support_plot():
    fig, ax = create_figure()
    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        ax.plot(TIME_VALUES, window["time_values"], color=window["color"], lw=2.6)
    ax.axvline(-TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.3, ls="--")
    ax.axvline(TIME_HALF_WIDTH, color=BOUNDARY_GREY, lw=1.3, ls="--")
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(TIME_START, TIME_END)
    ax.set_xticks(COMMON_TIME_XTICKS)
    ax.set_ylim(-0.06, 1.12)
    ax.set_yticks(np.arange(0.0, 1.01, 0.2))
    ax.grid(alpha=0.25)
    ax.set_title("Same support, different window shape", pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.legend(
        [Line2D([0], [0], color=WINDOW_DATA[key]["color"], lw=2.6) for key, _, _, _ in WINDOW_SPECS],
        [WINDOW_DATA[key]["label"] for key, _, _, _ in WINDOW_SPECS],
        loc="center left",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )
    save_figure(fig, "01_same_support_window_shapes.png")


def export_main_lobe_plot():
    fig, ax = create_figure()
    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        ax.plot(FREQUENCY_VALUES, window["magnitude_display"], color=window["color"], lw=2.6)
        half_width = window["main_lobe_half_width"]
        ax.axvline(half_width, color=window["color"], lw=1.2, ls="--", alpha=0.55)
        ax.axvline(-half_width, color=window["color"], lw=1.2, ls="--", alpha=0.55)
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(-3.0, 3.0)
    ax.set_xticks(np.arange(-3.0, 3.01, 1.0))
    ax.set_ylim(-0.02, 1.05)
    ax.set_yticks(np.arange(0.0, 1.01, 0.2))
    ax.grid(alpha=0.25)
    ax.set_title("Main lobe width (linear)", pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Normalized magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    width_text = "\n".join(
        f'{WINDOW_DATA[key]["label"]}: {WINDOW_DATA[key]["main_lobe_full_width"]:.2f} Hz'
        for key, _, _, _ in WINDOW_SPECS
    )
    ax.text(
        0.98,
        0.96,
        width_text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=13,
        bbox={"facecolor": "white", "edgecolor": "0.75", "alpha": 0.95, "boxstyle": "round,pad=0.35"},
    )
    ax.legend(
        [Line2D([0], [0], color=WINDOW_DATA[key]["color"], lw=2.6) for key, _, _, _ in WINDOW_SPECS],
        [WINDOW_DATA[key]["label"] for key, _, _, _ in WINDOW_SPECS],
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )
    save_figure(fig, "02_main_lobe_width_linear.png")


def export_sidelobe_plot():
    fig, ax = create_figure()
    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        magnitude_db = 20.0 * np.log10(
            np.maximum(window["magnitude_positive"], 10.0 ** (LOG_FLOOR_DB / 20.0))
        )
        ax.plot(POSITIVE_FREQUENCIES, magnitude_db, color=window["color"], lw=2.6)
        ax.axhline(
            window["first_sidelobe_level_db"],
            color=window["color"],
            lw=1.1,
            ls="--",
            alpha=0.50,
            zorder=1,
        )
        ax.plot(
            window["first_sidelobe_frequency"],
            window["first_sidelobe_level_db"],
            marker="o",
            ms=6.5,
            color=window["color"],
            zorder=4,
        )
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(0.0, 6.0)
    ax.set_xticks(np.arange(0.0, 6.01, 1.0))
    ax.set_ylim(LOG_FLOOR_DB, 5.0)
    ax.set_yticks(np.arange(LOG_FLOOR_DB, 1.0, 20.0))
    ax.grid(alpha=0.25)
    ax.set_title("First sidelobes (logarithmic)", pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Positive frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    level_text = "\n".join(
        f'{WINDOW_DATA[key]["label"]}: {WINDOW_DATA[key]["first_sidelobe_level_db"]:.1f} dB'
        for key, _, _, _ in WINDOW_SPECS
    )
    ax.text(
        0.98,
        0.10,
        level_text,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=13,
        bbox={"facecolor": "white", "edgecolor": "0.75", "alpha": 0.95, "boxstyle": "round,pad=0.35"},
    )
    ax.legend(
        [Line2D([0], [0], color=WINDOW_DATA[key]["color"], lw=2.6) for key, _, _, _ in WINDOW_SPECS],
        [WINDOW_DATA[key]["label"] for key, _, _, _ in WINDOW_SPECS],
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )
    save_figure(fig, "03_first_sidelobes_logarithmic.png")


def export_bidirectional_linear_log_plot():
    fig, ax = create_figure()

    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        magnitude_db = 20.0 * np.log10(
            np.maximum(window["magnitude_display"], 10.0 ** (LOG_FLOOR_DB / 20.0))
        )
        ax.plot(FREQUENCY_VALUES, magnitude_db, color=window["color"], lw=2.6)
        ax.axhline(
            window["first_sidelobe_level_db"],
            color=window["color"],
            lw=1.1,
            ls="--",
            alpha=0.55,
            zorder=1,
        )

    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(-3.0, 3.0)
    ax.set_xticks(np.arange(-3.0, 3.01, 1.0))
    ax.set_ylim(LOG_FLOOR_DB, 5.0)
    ax.set_yticks(np.arange(LOG_FLOOR_DB, 1.0, 20.0))
    ax.grid(alpha=0.25)
    ax.set_title("Window spectra (logarithmic)", pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.legend(
        [Line2D([0], [0], color=WINDOW_DATA[key]["color"], lw=2.6) for key, _, _, _ in WINDOW_SPECS],
        [WINDOW_DATA[key]["label"] for key, _, _, _ in WINDOW_SPECS],
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
        borderaxespad=0.6,
    )
    bottom_text = "\n".join(
        f'{WINDOW_DATA[key]["label"]}: {WINDOW_DATA[key]["first_sidelobe_level_db"]:.1f} dB'
        for key, _, _, _ in WINDOW_SPECS
    )
    ax.text(
        0.98,
        0.10,
        bottom_text,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=13,
        bbox={"facecolor": "white", "edgecolor": "0.75", "alpha": 0.95, "boxstyle": "round,pad=0.35"},
    )

    save_figure(fig, "04_window_spectra_linear_and_log_bidirectional.png")


def export_tradeoff_plot():
    fig, ax = create_figure()
    for key, _, _, _ in WINDOW_SPECS:
        window = WINDOW_DATA[key]
        ax.scatter(
            window["main_lobe_full_width"],
            window["first_sidelobe_level_db"],
            s=150,
            color=window["color"],
            edgecolors="white",
            linewidths=1.1,
            zorder=3,
        )
        ax.text(
            window["main_lobe_full_width"] + 0.04,
            window["first_sidelobe_level_db"] + 1.0,
            window["label"],
            fontsize=13,
            color=SIGNAL_BLACK,
        )
    ax.grid(alpha=0.25)
    ax.set_xlim(0.9, 3.4)
    ax.set_xticks(np.arange(1.0, 3.41, 0.5))
    ax.set_ylim(LOG_FLOOR_DB, -5.0)
    ax.set_yticks(np.arange(LOG_FLOOR_DB, -4.9, 15.0))
    ax.set_title("Trade-off between main lobe and sidelobes", pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Main lobe width [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("First sidelobe level [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.annotate(
        "narrower main lobe",
        xy=(1.0, -77.0),
        xytext=(1.8, -77.0),
        arrowprops={"arrowstyle": "->", "color": GREY_MEDIUM, "lw": 1.2},
        fontsize=13,
        color=GREY_MEDIUM,
        ha="center",
    )
    ax.annotate(
        "lower sidelobes",
        xy=(3.28, -72.0),
        xytext=(3.28, -20.0),
        arrowprops={"arrowstyle": "->", "color": GREY_MEDIUM, "lw": 1.2},
        fontsize=13,
        color=GREY_MEDIUM,
        rotation=90,
        va="center",
    )
    save_figure(fig, "04_tradeoff_map.png")


def main():
    clear_output_dir()
    export_same_support_plot()
    export_main_lobe_plot()
    export_sidelobe_plot()
    export_bidirectional_linear_log_plot()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
