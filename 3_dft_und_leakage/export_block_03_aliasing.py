from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "03_aliasing" / "03A_aliasing"

DPI = 240
SMALL_ROW_FIGSIZE = (8.0, 3.0)
OVERLAY_FIGSIZE = (6.0, 3.0)
SUPTITLE_SIZE = 14
LABEL_SIZE = 10
TICK_SIZE = 9
LEGEND_SIZE = 9
LEFT_MARGIN = 0.08
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.83

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
REFERENCE_GREEN = "#66b77a"
ALIAS_RED = "#d7263d"
ALIAS_ORANGE = "#ff8c2a"
ALIAS_GREY_DARK = "#8f8f8f"
ALIAS_GREY_LIGHT = "#b7b7b7"

FS_KHZ = 6.0
TIME_START_MS = 0.0
TIME_END_MS = 1.0
TIME_VALUES_MS = np.linspace(TIME_START_MS, TIME_END_MS, 2400)
TIME_VALUES_S = TIME_VALUES_MS * 1e-3
SAMPLE_TIMES_S = np.arange(0.0, TIME_END_MS * 1e-3 + 0.5 / (FS_KHZ * 1e3), 1.0 / (FS_KHZ * 1e3))
SAMPLE_TIMES_MS = SAMPLE_TIMES_S * 1e3
AMPLITUDE_LIMIT = 1.12


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def cosine_values(frequency_khz, times_s):
    return np.cos(2.0 * np.pi * frequency_khz * 1e3 * times_s)


def create_small_row_figure():
    fig, axes = plt.subplots(1, 3, figsize=SMALL_ROW_FIGSIZE, sharex=True, sharey=True)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=BOTTOM_MARGIN,
        top=TOP_MARGIN,
        wspace=0.18,
    )
    return fig, axes


def create_overlay_figure():
    fig, ax = plt.subplots(figsize=OVERLAY_FIGSIZE)
    fig.subplots_adjust(
        left=0.12,
        right=0.98,
        bottom=0.18,
        top=0.88,
    )
    return fig, ax


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def style_time_axis(ax, show_ylabel=True):
    ax.axhline(0.0, color="0.75", lw=0.8)
    ax.set_xlim(TIME_START_MS, TIME_END_MS)
    ax.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_xlabel("Zeit [ms]", fontsize=LABEL_SIZE)
    if show_ylabel:
        ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    else:
        ax.set_ylabel("")
        ax.tick_params(labelleft=False)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_signal_with_samples(
    ax,
    frequency_khz,
    curve_color,
    label,
    curve_lw=1.6,
    curve_alpha=1.0,
    draw_samples=True,
):
    dense_values = cosine_values(frequency_khz, TIME_VALUES_S)
    sample_values = cosine_values(frequency_khz, SAMPLE_TIMES_S)
    ax.plot(
        TIME_VALUES_MS,
        dense_values,
        color=curve_color,
        lw=curve_lw,
        alpha=curve_alpha,
        label=label,
        zorder=2,
    )
    if not draw_samples:
        return sample_values

    ax.vlines(
        SAMPLE_TIMES_MS,
        ymin=0.0,
        ymax=sample_values,
        color=SIGNAL_BLUE,
        lw=1.8,
        zorder=3,
    )
    ax.scatter(
        SAMPLE_TIMES_MS,
        sample_values,
        s=20,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=0.6,
        zorder=4,
    )
    return sample_values


def add_small_legend(ax):
    ax.legend(loc="upper right", frameon=False, fontsize=LEGEND_SIZE, handlelength=1.8)


def export_family_row(filename, title, family):
    fig, axes = create_small_row_figure()
    for index, (ax, entry) in enumerate(zip(axes, family)):
        draw_signal_with_samples(
            ax,
            frequency_khz=entry["frequency_khz"],
            curve_color=entry["color"],
            label=entry["label"],
        )
        style_time_axis(ax, show_ylabel=index == 0)
        add_small_legend(ax)
    fig.suptitle(title, fontsize=SUPTITLE_SIZE, y=0.97)
    save_figure(fig, filename)


def export_family_overlay(filename, title, family):
    fig, ax = create_overlay_figure()
    for entry in family:
        draw_signal_with_samples(
            ax,
            frequency_khz=entry["frequency_khz"],
            curve_color=entry["color"],
            label=entry["label"],
            curve_lw=1.4,
            curve_alpha=0.92,
            draw_samples=False,
        )

    reference_values = cosine_values(family[0]["frequency_khz"], SAMPLE_TIMES_S)
    ax.vlines(
        SAMPLE_TIMES_MS,
        ymin=0.0,
        ymax=reference_values,
        color=SIGNAL_BLUE,
        lw=1.8,
        zorder=3,
    )
    ax.scatter(
        SAMPLE_TIMES_MS,
        reference_values,
        s=24,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=0.6,
        zorder=4,
    )
    style_time_axis(ax, show_ylabel=True)
    ax.set_title(title, fontsize=SUPTITLE_SIZE, pad=8)
    ax.legend(loc="upper right", frameon=False, fontsize=LEGEND_SIZE, handlelength=2.0)
    save_figure(fig, filename)


def main():
    clear_output_dir()

    family_1_5_7 = [
        {"frequency_khz": 1.0, "color": REFERENCE_GREEN, "label": "1 kHz"},
        {"frequency_khz": 5.0, "color": ALIAS_RED, "label": "5 kHz"},
        {"frequency_khz": 7.0, "color": ALIAS_ORANGE, "label": "7 kHz"},
    ]
    family_1_11_13 = [
        {"frequency_khz": 1.0, "color": REFERENCE_GREEN, "label": "1 kHz"},
        {"frequency_khz": 11.0, "color": ALIAS_GREY_DARK, "label": "11 kHz"},
        {"frequency_khz": 13.0, "color": ALIAS_GREY_LIGHT, "label": "13 kHz"},
    ]
    family_2_4_8 = [
        {"frequency_khz": 2.0, "color": REFERENCE_GREEN, "label": "2 kHz"},
        {"frequency_khz": 4.0, "color": ALIAS_RED, "label": "4 kHz"},
        {"frequency_khz": 8.0, "color": ALIAS_ORANGE, "label": "8 kHz"},
    ]

    export_family_row("01_aliasfamilie_1_5_7_einzelplots.png", "Alias-Familie 1 / 5 / 7 kHz", family_1_5_7)
    export_family_overlay("02_aliasfamilie_1_5_7_ueberlagerung.png", "Überlagerung 1 / 5 / 7 kHz", family_1_5_7)

    export_family_row("03_aliasfamilie_1_11_13_einzelplots.png", "Alias-Familie 1 / 11 / 13 kHz", family_1_11_13)
    export_family_overlay("04_aliasfamilie_1_11_13_ueberlagerung.png", "Überlagerung 1 / 11 / 13 kHz", family_1_11_13)

    export_family_row("05_aliasfamilie_2_4_8_einzelplots.png", "Alias-Familie 2 / 4 / 8 kHz", family_2_4_8)
    export_family_overlay("06_aliasfamilie_2_4_8_ueberlagerung.png", "Überlagerung 2 / 4 / 8 kHz", family_2_4_8)

    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
