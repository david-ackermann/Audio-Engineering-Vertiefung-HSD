from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "01_leakage_und_fenstervergleich"
    / "01C_spektrale_erklaerung"
)

DPI = 200
SPECTRUM_FIGSIZE = (11.0, 4.8)
COMPARE_FIGSIZE = (12.0, 5.6)

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17

WINDOW_GREEN = "#66b77a"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_ORANGE = "#d97a27"
ACTIVE_RED = "#d7263d"
ACTIVE_LIGHT_RED = "#ef8895"
INACTIVE_GREY = "0.72"
GRID_GREY = "0.78"

FS_HZ = 16.0
N = 16
AMPLITUDE = 1.0
PHASE_RAD = np.pi / 4.0

FREQ_ON_BIN_HZ = 2.0
FREQ_OFF_BIN_HZ = 2.5

DISPLAY_FREQ_MIN_HZ = -17.0
DISPLAY_FREQ_MAX_HZ = 17.0
DISPLAY_FREQS_HZ = np.linspace(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ, 6000)
DISPLAY_BINS_HZ = np.arange(int(DISPLAY_FREQ_MIN_HZ), int(DISPLAY_FREQ_MAX_HZ) + 1, 1)
SPECTRUM_TICKS_HZ = (-16.0, -12.0, -8.0, -4.0, 0.0, 4.0, 8.0, 12.0, 16.0)

SAMPLE_INDICES = np.arange(N, dtype=float)


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def create_spectrum_figure():
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.20, top=0.86)
    return fig, ax


def create_compare_figure():
    fig, axes = plt.subplots(1, 2, figsize=COMPARE_FIGSIZE, sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.20, top=0.86, wspace=0.16)
    return fig, axes


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def complex_component_spectrum(frequencies_hz: np.ndarray, component_frequency_hz: float, phase_rad: float) -> np.ndarray:
    offset_hz = frequencies_hz[:, None] - component_frequency_hz
    phase_matrix = np.exp(-1j * 2.0 * np.pi * offset_hz * SAMPLE_INDICES[None, :] / FS_HZ)
    return 0.5 * AMPLITUDE * np.exp(1j * phase_rad) * np.sum(phase_matrix, axis=1)


def total_spectrum(frequencies_hz: np.ndarray, signal_frequency_hz: float):
    positive = complex_component_spectrum(frequencies_hz, signal_frequency_hz, PHASE_RAD)
    negative = complex_component_spectrum(frequencies_hz, -signal_frequency_hz, -PHASE_RAD)
    total = positive + negative
    return positive, negative, total


def dft_samples(signal_frequency_hz: float):
    time_signal = AMPLITUDE * np.cos(2.0 * np.pi * signal_frequency_hz * SAMPLE_INDICES / FS_HZ + PHASE_RAD)
    coefficients = np.fft.fftshift(np.fft.fft(time_signal))
    frequencies_hz = np.fft.fftshift(np.fft.fftfreq(N, d=1.0 / FS_HZ))
    visible_mask = (frequencies_hz >= DISPLAY_FREQ_MIN_HZ) & (frequencies_hz <= DISPLAY_FREQ_MAX_HZ)
    return frequencies_hz[visible_mask], coefficients[visible_mask]


def build_context(signal_frequency_hz: float):
    positive, negative, total = total_spectrum(DISPLAY_FREQS_HZ, signal_frequency_hz)
    sample_frequencies_hz, sample_coefficients = dft_samples(signal_frequency_hz)
    return {
        "signal_frequency_hz": signal_frequency_hz,
        "positive": positive,
        "negative": negative,
        "total": total,
        "sample_frequencies_hz": sample_frequencies_hz,
        "sample_coefficients": sample_coefficients,
    }


CONTEXT_ON = build_context(FREQ_ON_BIN_HZ)
CONTEXT_OFF = build_context(FREQ_OFF_BIN_HZ)
Y_LIMIT = 1.15 * max(
    0.5,
    np.max(np.abs(CONTEXT_ON["total"])),
    np.max(np.abs(CONTEXT_OFF["total"])),
    np.max(np.abs(CONTEXT_OFF["positive"])),
    np.max(np.abs(CONTEXT_OFF["negative"])),
)


def style_frequency_axis(ax, title: str, ylabel: str = r"$|X(f)|$"):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ)
    ax.set_ylim(0.0, Y_LIMIT)
    ax.set_xticks(SPECTRUM_TICKS_HZ)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    draw_fs_markers(ax)


def draw_fs_markers(ax) -> None:
    for fs_marker_hz, label in ((-FS_HZ, r"$-f_s$"), (FS_HZ, r"$f_s$")):
        if not (DISPLAY_FREQ_MIN_HZ <= fs_marker_hz <= DISPLAY_FREQ_MAX_HZ):
            continue
        ax.axvline(fs_marker_hz, color="0.45", lw=1.4, ls="--", zorder=0)
        ax.text(
            fs_marker_hz,
            Y_LIMIT * 0.96,
            label,
            ha="center",
            va="top",
            fontsize=LABEL_SIZE + 1,
            color="0.35",
        )


def add_bin_guides(ax):
    for frequency_hz in DISPLAY_BINS_HZ:
        ax.axvline(frequency_hz, color="0.92", lw=0.8, zorder=0)


def draw_ideal_lines(ax, line_frequency_hz: float):
    line_height = 0.5 * AMPLITUDE * N
    ax.vlines([-line_frequency_hz, line_frequency_hz], 0.0, line_height, color=ACTIVE_RED, lw=3.0, zorder=3)
    ax.plot([-line_frequency_hz], [line_height], "o", color=ACTIVE_LIGHT_RED, ms=8, zorder=4)
    ax.plot([line_frequency_hz], [line_height], "o", color=ACTIVE_RED, ms=8, zorder=4)


def draw_windowed_spectrum(ax, context, color=WINDOW_GREEN):
    ax.plot(DISPLAY_FREQS_HZ, np.abs(context["total"]), color=color, lw=2.4, ls="--", zorder=2)


def draw_dft_samples(ax, context):
    sample_frequencies_hz = context["sample_frequencies_hz"]
    sample_magnitudes = np.abs(context["sample_coefficients"])

    ax.vlines(sample_frequencies_hz, 0.0, sample_magnitudes, color=ACTIVE_RED, lw=2.8, zorder=5)
    ax.plot(sample_frequencies_hz, sample_magnitudes, "o", color=ACTIVE_RED, ms=8, zorder=6)


def annotate_component_center(ax, frequency_hz: float, label: str, color: str):
    ax.text(
        frequency_hz,
        0.93 * Y_LIMIT,
        label,
        color=color,
        fontsize=15,
        ha="center",
        va="bottom",
    )


def export_ideal_lines(signal_frequency_hz: float, filename: str):
    fig, ax = create_spectrum_figure()
    add_bin_guides(ax)
    draw_ideal_lines(ax, signal_frequency_hz)
    style_frequency_axis(ax, f"Ideal lines, {signal_frequency_hz:g} Hz")
    save_figure(fig, filename)


def export_windowed_spectrum(context, filename: str):
    fig, ax = create_spectrum_figure()
    add_bin_guides(ax)
    draw_windowed_spectrum(ax, context)
    style_frequency_axis(ax, f"Observed spectrum, {context['signal_frequency_hz']:g} Hz")
    save_figure(fig, filename)


def export_dft_sampling(context, filename: str):
    fig, ax = create_spectrum_figure()
    draw_windowed_spectrum(ax, context)
    draw_dft_samples(ax, context)
    style_frequency_axis(ax, f"DFT sampling, {context['signal_frequency_hz']:g} Hz", ylabel=r"$|X[k]|$")
    save_figure(fig, filename)


def export_compare_on_vs_off():
    fig, axes = create_compare_figure()

    for ax, context, title in (
        (axes[0], CONTEXT_ON, "2 Hz on-bin"),
        (axes[1], CONTEXT_OFF, "2.5 Hz off-bin"),
    ):
        draw_windowed_spectrum(ax, context)
        draw_dft_samples(ax, context)
        style_frequency_axis(ax, title, ylabel=r"$|X(f)|$")

    fig.suptitle("On-bin vs off-bin", fontsize=TITLE_SIZE, y=0.96)
    save_figure(fig, "07_vergleich_2_hz_und_2p5_hz.png")


def export_positive_component():
    fig, ax = create_spectrum_figure()
    add_bin_guides(ax)
    ax.plot(DISPLAY_FREQS_HZ, np.abs(CONTEXT_OFF["positive"]), color=SIGNAL_BLUE, lw=2.4)
    annotate_component_center(ax, FREQ_OFF_BIN_HZ, "+2.5 Hz", SIGNAL_BLUE)
    style_frequency_axis(ax, "+2.5 Hz contribution")
    save_figure(fig, "08_positiver_beitrag_2p5_hz.png")


def export_negative_component():
    fig, ax = create_spectrum_figure()
    add_bin_guides(ax)
    ax.plot(DISPLAY_FREQS_HZ, np.abs(CONTEXT_OFF["negative"]), color=SIGNAL_ORANGE, lw=2.4)
    annotate_component_center(ax, -FREQ_OFF_BIN_HZ, "-2.5 Hz", SIGNAL_ORANGE)
    style_frequency_axis(ax, "-2.5 Hz contribution")
    save_figure(fig, "09_negativer_beitrag_2p5_hz.png")


def export_combined_spectrum():
    fig, ax = create_spectrum_figure()
    ax.plot(DISPLAY_FREQS_HZ, np.abs(CONTEXT_OFF["positive"]), color=SIGNAL_BLUE, lw=1.7, ls="--", alpha=0.85)
    ax.plot(DISPLAY_FREQS_HZ, np.abs(CONTEXT_OFF["negative"]), color=SIGNAL_ORANGE, lw=1.7, ls="--", alpha=0.85)
    ax.plot(DISPLAY_FREQS_HZ, np.abs(CONTEXT_OFF["total"]), color=WINDOW_GREEN, lw=2.6, ls="--")
    draw_dft_samples(ax, CONTEXT_OFF)
    annotate_component_center(ax, FREQ_OFF_BIN_HZ, "+2.5 Hz", SIGNAL_BLUE)
    annotate_component_center(ax, -FREQ_OFF_BIN_HZ, "-2.5 Hz", SIGNAL_ORANGE)
    style_frequency_axis(ax, "Combined spectrum, 2.5 Hz")
    save_figure(fig, "10_summe_beider_beitraege_2p5_hz.png")


def main():
    clear_output_dir()
    export_ideal_lines(FREQ_ON_BIN_HZ, "01_ideales_linienspektrum_2_hz.png")
    export_windowed_spectrum(CONTEXT_ON, "02_beobachtetes_spektrum_2_hz.png")
    export_dft_sampling(CONTEXT_ON, "03_dft_abtastung_2_hz.png")
    export_ideal_lines(FREQ_OFF_BIN_HZ, "04_ideales_linienspektrum_2p5_hz.png")
    export_windowed_spectrum(CONTEXT_OFF, "05_beobachtetes_spektrum_2p5_hz.png")
    export_dft_sampling(CONTEXT_OFF, "06_dft_abtastung_2p5_hz.png")
    export_compare_on_vs_off()
    export_positive_component()
    export_negative_component()
    export_combined_spectrum()
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
