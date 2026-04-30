from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "02_zeitbereich_und_frequenzraster"
    / "02a_signal_zu_x_n"
)

DPI = 200
FIGSIZE = (12.0, 4.4)
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
ACTIVE_RED = "#d7263d"
INACTIVE_GREY = "0.82"

TIME_START = 0.0
TIME_END = 1.0
SIGNAL_FREQ_HZ = 1.65
SIGNAL_PHASE_RAD = 0.18 * np.pi
SIGNAL_AMPLITUDE = 0.88
SAMPLE_PERIOD = 0.08
SAMPLE_INDICES = np.arange(13)
SAMPLE_TIMES = SAMPLE_INDICES * SAMPLE_PERIOD

TIME_VALUES = np.linspace(TIME_START, TIME_END, 2400)
SIGNAL_VALUES = SIGNAL_AMPLITUDE * np.cos(2.0 * np.pi * SIGNAL_FREQ_HZ * TIME_VALUES + SIGNAL_PHASE_RAD)
SAMPLE_VALUES = SIGNAL_AMPLITUDE * np.cos(2.0 * np.pi * SIGNAL_FREQ_HZ * SAMPLE_TIMES + SIGNAL_PHASE_RAD)
SIGNAL_LIMIT = 1.15 * max(1.0, np.max(np.abs(SIGNAL_VALUES)))


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


def style_time_axis(ax, title, show_xlabel=True):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(TIME_START, TIME_END)
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(np.arange(0.0, 1.01, 0.2))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]" if show_xlabel else "", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_discrete_axis(ax, title, show_xlabel=True):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(TIME_START, TIME_END)
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(SAMPLE_TIMES)
    ax.set_xticklabels([str(sample_index) for sample_index in SAMPLE_INDICES])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Sample index n" if show_xlabel else "", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def draw_sampling_guides(ax, alpha=1.0):
    ax.vlines(
        SAMPLE_TIMES,
        ymin=-SIGNAL_LIMIT,
        ymax=SIGNAL_LIMIT,
        color=INACTIVE_GREY,
        lw=1.2,
        alpha=alpha,
        zorder=0,
    )


def draw_time_samples(ax, with_labels=False):
    ax.scatter(
        SAMPLE_TIMES,
        SAMPLE_VALUES,
        s=75,
        color=ACTIVE_RED,
        edgecolor="white",
        linewidth=1.0,
        zorder=4,
    )
    if not with_labels:
        return

    for sample_index in range(1, 5):
        value = SAMPLE_VALUES[sample_index]
        if value >= 0.0:
            offset = (0, -18)
            vertical_alignment = "top"
        else:
            offset = (0, 12)
            vertical_alignment = "bottom"
        ax.annotate(
            fr"$n={sample_index}$",
            (SAMPLE_TIMES[sample_index], value),
            textcoords="offset points",
            xytext=offset,
            ha="center",
            va=vertical_alignment,
            fontsize=14,
            color=SIGNAL_BLACK,
            zorder=5,
        )

    ax.text(
        SAMPLE_TIMES[5],
        -0.88 * SIGNAL_LIMIT,
        r"$\dots$",
        fontsize=18,
        color=SIGNAL_BLACK,
        ha="center",
        va="center",
    )


def draw_discrete_sequence(ax):
    ax.vlines(
        SAMPLE_TIMES,
        ymin=0.0,
        ymax=SAMPLE_VALUES,
        color=SIGNAL_BLUE,
        lw=2.4,
        zorder=2,
    )
    ax.scatter(
        SAMPLE_TIMES,
        SAMPLE_VALUES,
        s=85,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )


def add_sampling_period_annotation(ax):
    x_left = SAMPLE_TIMES[2]
    x_right = SAMPLE_TIMES[3]
    y_level = -0.90 * SIGNAL_LIMIT
    ax.annotate(
        "",
        xy=(x_left, y_level),
        xytext=(x_right, y_level),
        arrowprops=dict(arrowstyle="<->", color=SIGNAL_BLACK, lw=1.4),
    )
    ax.text(
        0.5 * (x_left + x_right),
        y_level + 0.08,
        r"$T_s$",
        ha="center",
        va="bottom",
        fontsize=18,
        color=SIGNAL_BLACK,
    )


def add_formula_box(ax):
    ax.text(
        0.04,
        0.92,
        r"$x[n] = x_c(nT_s)$" + "\n" + r"$n = 0,1,2,\dots$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=20,
        color=SIGNAL_BLACK,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.75", alpha=0.96),
    )


def export_continuous_signal():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.4)
    style_time_axis(ax, r"Continuous-time signal $x_c(t)$")
    save_figure(fig, "01_kontinuierliches_signal_x_t.png")


def export_sampling_instants():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.2, zorder=2)
    draw_sampling_guides(ax)
    add_sampling_period_annotation(ax)
    style_time_axis(ax, r"Sampling instants with period $T_s$")
    save_figure(fig, "02_abtastzeitpunkte_eingefuehrt.png")


def export_marked_samples():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.2, zorder=2)
    draw_sampling_guides(ax)
    draw_time_samples(ax)
    style_time_axis(ax, r"Sample values taken from $x_c(t)$")
    save_figure(fig, "03_samples_auf_kurve_markiert.png")


def export_formula_view():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_LIGHT_BLUE, lw=2.0, zorder=1)
    draw_sampling_guides(ax, alpha=0.9)
    draw_time_samples(ax, with_labels=True)
    add_formula_box(ax)
    style_time_axis(ax, r"Discrete description via $x[n] = x_c(nT_s)$")
    save_figure(fig, "04_xn_formel_eingefuehrt.png")


def export_discrete_sequence():
    fig, ax = create_figure()
    draw_discrete_sequence(ax)
    style_discrete_axis(ax, r"Discrete sequence $x[n]$")
    ax.text(
        0.04,
        0.92,
        r"$x[n] = x_c(nT_s)$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=18,
        color=SIGNAL_BLACK,
        bbox=dict(boxstyle="round,pad=0.30", facecolor="white", edgecolor="0.75", alpha=0.96),
    )
    save_figure(fig, "05_diskrete_folge_x_n.png")


def main():
    clear_output_dir()
    export_continuous_signal()
    export_sampling_instants()
    export_marked_samples()
    export_formula_view()
    export_discrete_sequence()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
