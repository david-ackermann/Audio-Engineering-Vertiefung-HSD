from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator

import storyboard_paths as paths


OUTPUT_DIR = paths.HOMEWORK_MATCH_TIME_TO_SPECTRUM_DIR

DPI = 220
FIGSIZE = (13.0, 13.8)
TITLE_SIZE = 24
SUBTITLE_SIZE = 19
LABEL_SIZE = 18
TICK_SIZE = 15
LINEWIDTH = 3.0
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
NEG_COLOR = "#26a043"
POS_COLOR = "tab:purple"
TIME_COLOR = "#2b7bbb"
TIME_END = 1.0
SAMPLE_COUNT = 2400
TIME_VALUES = np.linspace(0.0, TIME_END, SAMPLE_COUNT)
COMMON_FREQ_LIMIT = 6.5
COMMON_MAG_LIMIT = 0.75
COMMON_TIME_LIMIT = 1.55


TASKS = [
    {
        "slug": "negativer_sinus_1hz",
        "components": [(1.0, 1.0, 90.0)],
        "candidates": [
            ("A", [(1.0, 1.0, -90.0)]),
            ("B", [(1.0, 1.0, 90.0)]),
            ("C", [(1.0, 1.0, 180.0)]),
            ("D", [(1.0, 1.0, 0.0)]),
        ],
    },
    {
        "slug": "negativer_cosinus_4hz",
        "components": [(1.0, 4.0, 180.0)],
        "candidates": [
            ("A", [(1.0, 2.0, 180.0)]),
            ("B", [(1.0, 4.0, 0.0)]),
            ("C", [(1.0, 4.0, 180.0)]),
            ("D", [(1.0, 4.0, 180.0), (0.35, 2.0, -90.0)]),
        ],
    },
]


def normalize_phase_deg(values):
    return ((np.asarray(values) + 180.0) % 360.0) - 180.0


def build_time_signal(components):
    signal = np.zeros_like(TIME_VALUES)
    for amplitude, frequency_hz, phase_deg in components:
        signal += amplitude * np.cos(2.0 * np.pi * frequency_hz * TIME_VALUES + np.deg2rad(phase_deg))
    return signal


def build_two_sided_spectrum(components):
    freqs = []
    mags = []
    phases = []
    for amplitude, frequency_hz, phase_deg in components:
        line_mag = 0.5 * abs(amplitude)
        positive_phase = normalize_phase_deg([phase_deg])[0]
        negative_phase = normalize_phase_deg([-phase_deg])[0]
        freqs.extend([-frequency_hz, frequency_hz])
        mags.extend([line_mag, line_mag])
        phases.extend([negative_phase, positive_phase])

    order = np.argsort(freqs)
    return np.asarray(freqs)[order], np.asarray(mags)[order], np.asarray(phases)[order]


def style_frequency_axis(ax, title, y_limits, y_label, y_step):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-COMMON_FREQ_LIMIT, COMMON_FREQ_LIMIT)
    ax.set_ylim(*y_limits)
    ax.grid(which="major", alpha=GRID_ALPHA)
    ax.set_title(title, pad=8, fontsize=SUBTITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.yaxis.set_major_locator(MultipleLocator(y_step))


def style_time_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(0.0, TIME_END)
    ax.set_ylim(-COMMON_TIME_LIMIT, COMMON_TIME_LIMIT)
    ax.grid(which="major", alpha=GRID_ALPHA)
    ax.set_title(title, pad=8, fontsize=SUBTITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.grid(which="minor", alpha=0.14)


def plot_line_spectrum(ax, freqs, values, title, y_limits, y_label, y_step):
    for frequency_hz, value in zip(freqs, values):
        color = NEG_COLOR if frequency_hz < 0.0 else POS_COLOR
        ax.vlines(frequency_hz, 0.0, value, color=color, lw=LINEWIDTH)
        ax.plot([frequency_hz], [value], "o", color=color, ms=8.5)
    style_frequency_axis(ax, title, y_limits, y_label, y_step)


def save_figure(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def export_task(index, task):
    freqs, mags, phases = build_two_sided_spectrum(task["components"])

    fig = plt.figure(figsize=FIGSIZE)
    grid = GridSpec(
        4,
        2,
        figure=fig,
        left=0.08,
        right=0.97,
        bottom=0.06,
        top=0.95,
        hspace=0.58,
        wspace=0.26,
        height_ratios=[1.0, 1.0, 1.0, 1.0],
    )

    ax_mag = fig.add_subplot(grid[0, :])
    ax_phase = fig.add_subplot(grid[1, :])
    candidate_axes = [
        fig.add_subplot(grid[2, 0]),
        fig.add_subplot(grid[2, 1]),
        fig.add_subplot(grid[3, 0]),
        fig.add_subplot(grid[3, 1]),
    ]

    plot_line_spectrum(ax_mag, freqs, mags, "Magnitude spectrum", (0.0, COMMON_MAG_LIMIT), r"$|X(f)|$", 0.25)
    plot_line_spectrum(ax_phase, freqs, phases, "Phase spectrum", (-180.0, 180.0), r"$\angle X(f)$ [deg]", 45.0)

    for ax, (label, components) in zip(candidate_axes, task["candidates"]):
        signal = build_time_signal(components)
        ax.plot(TIME_VALUES, signal, color=TIME_COLOR, lw=2.7)
        style_time_axis(ax, label)

    save_figure(fig, f"{index:02d}_{task['slug']}.png")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in OUTPUT_DIR.glob("*.png"):
        old_png.unlink()

    for index, task in enumerate(TASKS, start=1):
        export_task(index, task)

    print(f"Saved outputs to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
