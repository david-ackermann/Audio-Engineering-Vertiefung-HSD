from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import storyboard_paths as paths


OUTPUT_DIR = paths.TWO_SIDED_COSINE_DIR
DPI = 220
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
TIME_FIGSIZE = (12.0, 4.8)
SPECTRUM_FIGSIZE = (11.0, 4.8)
OVERVIEW_FIGSIZE = (12.4, 12.8)
TIME_END = 2.0
SAMPLE_COUNT = 2000
AMPLITUDE = 1.0
FREQUENCY_HZ = 2.0
PHASE_RAD = 0.0
TIME_COLOR = "tab:blue"
NEG_COLOR = "#26a043"
POS_COLOR = "tab:purple"
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
FREQ_AXIS_LIMIT = 5.0
MAG_LINEWIDTH = 3.2
POINT_SIZE = 10


TIME_VALUES = np.linspace(0.0, TIME_END, SAMPLE_COUNT)
SIGNAL_VALUES = AMPLITUDE * np.cos(2.0 * np.pi * FREQUENCY_HZ * TIME_VALUES + PHASE_RAD)
SPECTRUM_FREQS = np.array([-FREQUENCY_HZ, FREQUENCY_HZ])
SPECTRUM_MAGS = np.array([AMPLITUDE / 2.0, AMPLITUDE / 2.0])
PHASE_DEG = np.degrees(PHASE_RAD)
SPECTRUM_PHASES = np.array([-PHASE_DEG, PHASE_DEG])
SPECTRUM_COLORS = [NEG_COLOR, POS_COLOR]


def save_figure(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def style_time_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(0.0, TIME_END)
    ax.set_ylim(-1.15, 1.15)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_frequency_axis(ax, title, y_limits, y_label):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-FREQ_AXIS_LIMIT, FREQ_AXIS_LIMIT)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def plot_line_spectrum(ax, values, y_limits, y_label, title):
    for frequency_hz, value, color in zip(SPECTRUM_FREQS, values, SPECTRUM_COLORS):
        ax.vlines(frequency_hz, 0.0, value, color=color, lw=MAG_LINEWIDTH)
        ax.plot([frequency_hz], [value], "o", color=color, ms=POINT_SIZE)
    style_frequency_axis(ax, title, y_limits, y_label)


def export_time_signal():
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=TIME_COLOR, lw=2.8)
    style_time_axis(ax, r"Time signal $x(t)=\cos(2\pi f_0 t)$")
    save_figure(fig, "01_time_signal.png")


def export_magnitude_spectrum():
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    plot_line_spectrum(ax, SPECTRUM_MAGS, (0.0, 0.62), r"$|X(f)|$", "Two-sided magnitude spectrum")
    save_figure(fig, "02_magnitude_spectrum.png")


def export_phase_spectrum():
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    plot_line_spectrum(ax, SPECTRUM_PHASES, (-180.0, 180.0), r"$\angle X(f)$ [deg]", "Two-sided phase spectrum")
    save_figure(fig, "03_phase_spectrum.png")


def export_overview():
    fig, axes = plt.subplots(3, 1, figsize=OVERVIEW_FIGSIZE)

    axes[0].plot(TIME_VALUES, SIGNAL_VALUES, color=TIME_COLOR, lw=2.8)
    style_time_axis(axes[0], r"Time signal $x(t)=\cos(2\pi f_0 t)$")

    plot_line_spectrum(axes[1], SPECTRUM_MAGS, (0.0, 0.62), r"$|X(f)|$", "Two-sided magnitude spectrum")
    plot_line_spectrum(axes[2], SPECTRUM_PHASES, (-180.0, 180.0), r"$\angle X(f)$ [deg]", "Two-sided phase spectrum")

    fig.subplots_adjust(left=0.12, right=0.96, top=0.96, bottom=0.07, hspace=0.45)
    save_figure(fig, "00_overview.png")


def main():
    export_time_signal()
    export_magnitude_spectrum()
    export_phase_spectrum()
    export_overview()
    print(f"Saved outputs to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
