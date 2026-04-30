from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "01_leakage_und_fenstervergleich"
    / "01D_fenstervergleich"
)

DPI = 200
SINGLE_FIGSIZE = (11.0, 4.8)
COMPARE_FIGSIZE = (11.4, 12.8)

TITLE_SIZE = 24
PANEL_TITLE_SIZE = 18
LABEL_SIZE = 19
TICK_SIZE = 16

WINDOW_GREEN = "#66b77a"
SPECTRUM_BLUE = "#2b7bbb"
COMPARE_ORANGE = "#d98c2f"
BLACKMAN_RED = "#c45b4d"
ACTIVE_RED = "#d7263d"
GRID_GREY = "0.78"

FS_HZ = 16.0
N = 16
SIGNAL_FREQUENCY_HZ = 2.5
AMPLITUDE = 1.0
PHASE_RAD = np.pi / 4.0

DISPLAY_FREQ_MIN_HZ = -17.0
DISPLAY_FREQ_MAX_HZ = 17.0
DISPLAY_FREQS_HZ = np.linspace(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ, 6000)
DISPLAY_BINS_HZ = np.arange(int(DISPLAY_FREQ_MIN_HZ), int(DISPLAY_FREQ_MAX_HZ) + 1, 1)
SPECTRUM_TICKS_HZ = (-16.0, -12.0, -8.0, -4.0, 0.0, 4.0, 8.0, 12.0, 16.0)
LOG_FLOOR_DB = -60.0

SAMPLE_INDICES = np.arange(N, dtype=float)

WINDOW_SPECS = [
    ("rectangular", "Rectangular", WINDOW_GREEN, np.ones(N)),
    ("hann", "Hann", SPECTRUM_BLUE, np.hanning(N)),
    ("hamming", "Hamming", COMPARE_ORANGE, np.hamming(N)),
    ("blackman", "Blackman", BLACKMAN_RED, np.blackman(N)),
]


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def create_single_figure():
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.20, top=0.86)
    return fig, ax


def create_compare_figure():
    fig, axes = plt.subplots(len(WINDOW_SPECS), 1, figsize=COMPARE_FIGSIZE, sharex=True, sharey=True)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.06, top=0.89, hspace=0.42)
    return fig, axes


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def build_windowed_signal(window_values: np.ndarray) -> np.ndarray:
    return window_values * AMPLITUDE * np.cos(
        2.0 * np.pi * SIGNAL_FREQUENCY_HZ * SAMPLE_INDICES / FS_HZ + PHASE_RAD
    )


def coherent_gain_normalized_spectrum(window_values: np.ndarray, frequency_values_hz: np.ndarray) -> np.ndarray:
    signal_values = build_windowed_signal(window_values)
    coherent_gain = np.mean(window_values)
    phase_matrix = np.exp(-1j * 2.0 * np.pi * frequency_values_hz[:, None] * SAMPLE_INDICES[None, :] / FS_HZ)
    return np.sum(signal_values[None, :] * phase_matrix, axis=1) / coherent_gain


def coherent_gain_normalized_dft(window_values: np.ndarray):
    signal_values = build_windowed_signal(window_values)
    coherent_gain = np.mean(window_values)
    coefficients = np.fft.fftshift(np.fft.fft(signal_values) / coherent_gain)
    frequencies_hz = np.fft.fftshift(np.fft.fftfreq(N, d=1.0 / FS_HZ))
    visible_mask = (frequencies_hz >= DISPLAY_FREQ_MIN_HZ) & (frequencies_hz <= DISPLAY_FREQ_MAX_HZ)
    return frequencies_hz[visible_mask], coefficients[visible_mask]


WINDOW_DATA = {}
for key, label, color, window_values in WINDOW_SPECS:
    spectrum = coherent_gain_normalized_spectrum(window_values, DISPLAY_FREQS_HZ)
    dft_frequencies_hz, dft_coefficients = coherent_gain_normalized_dft(window_values)
    magnitude = np.abs(spectrum)
    dft_magnitude = np.abs(dft_coefficients)
    reference_magnitude = np.max(magnitude)
    WINDOW_DATA[key] = {
        "label": label,
        "color": color,
        "window_values": window_values,
        "spectrum": spectrum,
        "magnitude": magnitude,
        "magnitude_db": 20.0 * np.log10(np.maximum(magnitude / reference_magnitude, 10.0 ** (LOG_FLOOR_DB / 20.0))),
        "dft_frequencies_hz": dft_frequencies_hz,
        "dft_magnitude": dft_magnitude,
        "dft_magnitude_db": 20.0
        * np.log10(np.maximum(dft_magnitude / reference_magnitude, 10.0 ** (LOG_FLOOR_DB / 20.0))),
    }

LINEAR_Y_LIMIT = 1.15 * max(
    0.55,
    max(np.max(window_data["magnitude"]) for window_data in WINDOW_DATA.values()),
    max(np.max(window_data["dft_magnitude"]) for window_data in WINDOW_DATA.values()),
)


def add_bin_guides(ax):
    for frequency_hz in DISPLAY_BINS_HZ:
        ax.axvline(frequency_hz, color="0.92", lw=0.8, zorder=0)


def style_linear_axis(ax, title: str, show_xlabel: bool):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ)
    ax.set_ylim(0.0, LINEAR_Y_LIMIT)
    ax.set_xticks(SPECTRUM_TICKS_HZ)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=PANEL_TITLE_SIZE, pad=8)
    ax.set_ylabel(r"$|X(f)|$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    if show_xlabel:
        ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    draw_fs_markers(ax, LINEAR_Y_LIMIT)


def style_db_axis(ax, title: str, show_xlabel: bool):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ)
    ax.set_ylim(LOG_FLOOR_DB, 5.0)
    ax.set_xticks(SPECTRUM_TICKS_HZ)
    ax.set_yticks(np.arange(LOG_FLOOR_DB, 1.0, 20.0))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=PANEL_TITLE_SIZE, pad=8)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    if show_xlabel:
        ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    draw_fs_markers(ax, 5.0)


def draw_fs_markers(ax, y_top: float) -> None:
    for fs_marker_hz, label in ((-FS_HZ, r"$-f_s$"), (FS_HZ, r"$f_s$")):
        if not (DISPLAY_FREQ_MIN_HZ <= fs_marker_hz <= DISPLAY_FREQ_MAX_HZ):
            continue
        ax.axvline(fs_marker_hz, color="0.45", lw=1.4, ls="--", zorder=0)
        ax.text(
            fs_marker_hz,
            y_top - 0.03 * (y_top - LOG_FLOOR_DB) if y_top == 5.0 else y_top * 0.96,
            label,
            ha="center",
            va="top",
            fontsize=LABEL_SIZE,
            color="0.35",
        )


def draw_linear_case(ax, window_data):
    add_bin_guides(ax)
    ax.plot(DISPLAY_FREQS_HZ, window_data["magnitude"], color=window_data["color"], lw=2.4, ls="--", zorder=2)
    ax.vlines(
        window_data["dft_frequencies_hz"],
        0.0,
        window_data["dft_magnitude"],
        color=ACTIVE_RED,
        lw=2.6,
        zorder=5,
    )
    ax.plot(
        window_data["dft_frequencies_hz"],
        window_data["dft_magnitude"],
        "o",
        color=ACTIVE_RED,
        ms=7.5,
        zorder=6,
    )


def draw_db_case(ax, window_data):
    add_bin_guides(ax)
    ax.plot(DISPLAY_FREQS_HZ, window_data["magnitude_db"], color=window_data["color"], lw=2.4, ls="--", zorder=2)
    ax.vlines(
        window_data["dft_frequencies_hz"],
        LOG_FLOOR_DB,
        window_data["dft_magnitude_db"],
        color=ACTIVE_RED,
        lw=2.0,
        zorder=5,
    )
    ax.plot(
        window_data["dft_frequencies_hz"],
        window_data["dft_magnitude_db"],
        "o",
        color=ACTIVE_RED,
        ms=6.5,
        zorder=6,
    )


def export_single_window_case(index: int, key: str):
    window_data = WINDOW_DATA[key]
    fig, ax = create_single_figure()
    draw_linear_case(ax, window_data)
    style_linear_axis(ax, window_data["label"], show_xlabel=True)
    save_figure(fig, f"{index:02d}_{key}_offbin_spectrum.png")


def export_linear_comparison():
    fig, axes = create_compare_figure()
    for axis, (key, _, _, _) in zip(axes, WINDOW_SPECS):
        window_data = WINDOW_DATA[key]
        draw_linear_case(axis, window_data)
        style_linear_axis(axis, window_data["label"], show_xlabel=axis is axes[-1])
    fig.suptitle("2.5 Hz off-bin tone", fontsize=TITLE_SIZE, y=0.97)
    save_figure(fig, "04_window_comparison_linear.png")


def export_db_comparison():
    fig, axes = create_compare_figure()
    for axis, (key, _, _, _) in zip(axes, WINDOW_SPECS):
        window_data = WINDOW_DATA[key]
        draw_db_case(axis, window_data)
        style_db_axis(axis, window_data["label"], show_xlabel=axis is axes[-1])
    fig.suptitle("2.5 Hz off-bin tone, normalized", fontsize=TITLE_SIZE, y=0.97)
    save_figure(fig, "05_window_comparison_db.png")


def main():
    clear_output_dir()
    export_single_window_case(1, "rectangular")
    export_single_window_case(2, "hann")
    export_single_window_case(3, "hamming")
    export_single_window_case(4, "blackman")
    export_linear_comparison()
    export_db_comparison()
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
