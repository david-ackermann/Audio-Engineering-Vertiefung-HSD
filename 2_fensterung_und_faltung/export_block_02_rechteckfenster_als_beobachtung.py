from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "02_rechteckfenster_als_beobachtung"

# Match the single-figure export look from 1_fourier_transformation
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

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
WINDOW_GREEN = "#66b77a"
ACTIVE_RED = "#d7263d"
INACTIVE_GREY = "0.82"

FULL_START = -2.0
FULL_END = 2.0
OBS_START = -0.5
OBS_END = 0.5
SIGNAL_FREQ_HZ = 2.0
SIGNAL_PHASE_RAD = 0.35 * np.pi

TIME_VALUES = np.linspace(FULL_START, FULL_END, 2400)
SIGNAL_VALUES = 0.92 * np.cos(2.0 * np.pi * SIGNAL_FREQ_HZ * TIME_VALUES + SIGNAL_PHASE_RAD)
OBS_MASK = (TIME_VALUES >= OBS_START) & (TIME_VALUES <= OBS_END)
WINDOW_VALUES = np.where(OBS_MASK, 1.0, 0.0)
OBSERVED_SIGNAL = SIGNAL_VALUES * WINDOW_VALUES
SIGNAL_LIMIT = 1.15 * max(1.0, np.max(np.abs(SIGNAL_VALUES)))

ZOOM_START = -0.78
ZOOM_END = -0.22


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


def style_time_axis(ax, title, x_limits):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_window_axis(ax, title, x_limits):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(-0.10, 1.15)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def add_inset_legend(ax, handles, loc):
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


def draw_window_guides(ax, alpha=1.0):
    ax.axvline(OBS_START, color=WINDOW_GREEN, lw=2.0, ls="--", alpha=alpha)
    ax.axvline(OBS_END, color=WINDOW_GREEN, lw=2.0, ls="--", alpha=alpha)


def export_signal_only():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLUE, lw=2.2)
    style_time_axis(ax, r"Input signal $x(t)$", (FULL_START, FULL_END))
    save_figure(fig, "01_ausgangssignal_x_t.png")


def export_window_only():
    fig, ax = create_figure()
    ax.fill_between(TIME_VALUES, 0.0, WINDOW_VALUES, color=WINDOW_GREEN, alpha=0.22)
    ax.plot(TIME_VALUES, WINDOW_VALUES, color=WINDOW_GREEN, lw=2.4)
    draw_window_guides(ax)
    style_window_axis(ax, r"Rectangular window $w_{\mathrm{rect}}(t)$", (FULL_START, FULL_END))
    save_figure(fig, "02_rechteckfenster_w_rect_t.png")


def export_overlay():
    fig, ax = create_figure()
    ax.fill_between(TIME_VALUES, 0.0, WINDOW_VALUES, color=WINDOW_GREEN, alpha=0.18, zorder=0)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLUE, lw=2.0, zorder=2)
    ax.plot(TIME_VALUES[OBS_MASK], SIGNAL_VALUES[OBS_MASK], color=SIGNAL_BLUE, lw=2.6, zorder=3)
    draw_window_guides(ax)
    style_time_axis(ax, r"Overlay of $x(t)$ and $w_{\mathrm{rect}}(t)$", (FULL_START, FULL_END))
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=SIGNAL_BLUE, lw=2.0, label="signal"),
            Line2D([0], [0], color=SIGNAL_BLUE, lw=2.6, label="signal in interval"),
            Patch(facecolor=WINDOW_GREEN, edgecolor=WINDOW_GREEN, alpha=0.18, label="window"),
        ],
        "upper right",
    )
    save_figure(fig, "03_ueberlagerung_x_t_und_w_rect_t.png")


def export_result():
    fig, ax = create_figure()
    ax.fill_between(TIME_VALUES, 0.0, WINDOW_VALUES, color=WINDOW_GREEN, alpha=0.10, zorder=0)
    ax.plot(TIME_VALUES, OBSERVED_SIGNAL, color=SIGNAL_BLACK, lw=2.6, zorder=3)
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_LIGHT_BLUE, lw=1.8, zorder=1)
    draw_window_guides(ax, alpha=0.8)
    style_time_axis(ax, r"Observed signal $x_{\mathrm{obs}}(t)=x(t)\,w_{\mathrm{rect}}(t)$", (FULL_START, FULL_END))
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=SIGNAL_BLACK, lw=2.6, label="observed signal"),
            Line2D([0], [0], color=SIGNAL_LIGHT_BLUE, lw=1.8, label="original signal"),
            Patch(facecolor=WINDOW_GREEN, edgecolor=WINDOW_GREEN, alpha=0.10, label="window"),
        ],
        "upper right",
    )
    save_figure(fig, "04_resultat_x_obs_t_nach_multiplikation.png")


def export_edge_zoom():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLUE, lw=1.8, zorder=1)
    ax.plot(TIME_VALUES, OBSERVED_SIGNAL, color=SIGNAL_BLACK, lw=2.6, zorder=3)
    ax.plot(TIME_VALUES, WINDOW_VALUES, color=WINDOW_GREEN, lw=2.2, zorder=2)
    ax.fill_between(TIME_VALUES, 0.0, WINDOW_VALUES, color=WINDOW_GREEN, alpha=0.10, zorder=0)
    ax.axvline(OBS_START, color=ACTIVE_RED, lw=2.2, ls="--", zorder=4)
    style_time_axis(ax, r"Window edge zoom", (ZOOM_START, ZOOM_END))
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=SIGNAL_BLACK, lw=2.6, label="observed signal"),
            Line2D([0], [0], color=SIGNAL_BLUE, lw=1.8, label="original signal"),
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.2, label="window"),
        ],
        "upper left",
    )
    save_figure(fig, "05_detailzoom_fensterrand_ausserhalb_null.png")


def main():
    clear_output_dir()
    export_signal_only()
    export_window_only()
    export_overlay()
    export_result()
    export_edge_zoom()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
