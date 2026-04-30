from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "01_uebergang_ft_zu_fensterung"

# Match the single-figure export look from 1_fourier_transformation
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
WINDOW_GREEN = "#66b77a"
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
OBSERVED_SIGNAL = np.where(OBS_MASK, SIGNAL_VALUES, np.nan)
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


def style_time_axis(ax, title, x_limits):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_window_axis(ax, title):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(FULL_START, FULL_END)
    ax.set_ylim(-0.10, 1.15)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def export_long_signal():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLUE, lw=2.2)
    style_time_axis(ax, "Time signal x(t)", (FULL_START, FULL_END))
    save_figure(fig, "01_zeitverlauf_x_t.png")


def export_signal_with_observation_window():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=SIGNAL_BLUE, lw=2.2)
    ax.axvspan(OBS_START, OBS_END, color=WINDOW_GREEN, alpha=0.18, zorder=0)
    ax.axvline(OBS_START, color=WINDOW_GREEN, lw=2.0, ls="--")
    ax.axvline(OBS_END, color=WINDOW_GREEN, lw=2.0, ls="--")
    style_time_axis(ax, "Time signal with observation interval", (FULL_START, FULL_END))
    save_figure(fig, "02_zeitverlauf_mit_beobachtungszeitraum.png")


def export_signal_with_dimmed_outside():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES, SIGNAL_VALUES, color=INACTIVE_GREY, lw=2.0)
    ax.plot(TIME_VALUES[OBS_MASK], SIGNAL_VALUES[OBS_MASK], color=SIGNAL_BLUE, lw=2.4)
    ax.axvspan(OBS_START, OBS_END, color=WINDOW_GREEN, alpha=0.14, zorder=0)
    ax.axvline(OBS_START, color=WINDOW_GREEN, lw=2.0, ls="--")
    ax.axvline(OBS_END, color=WINDOW_GREEN, lw=2.0, ls="--")
    style_time_axis(ax, "Observed segment in x(t)", (FULL_START, FULL_END))
    save_figure(fig, "03_beobachteter_ausschnitt_im_zeitverlauf.png")


def export_observed_signal():
    fig, ax = create_figure()
    ax.plot(TIME_VALUES[OBS_MASK], SIGNAL_VALUES[OBS_MASK], color=SIGNAL_BLACK, lw=2.4)
    style_time_axis(ax, r"Observed time signal $x_{\mathrm{obs}}(t)$", (OBS_START, OBS_END))
    save_figure(fig, "04_beobachteter_zeitverlauf_x_obs_t.png")


def export_rectangular_window():
    fig, ax = create_figure()
    ax.fill_between(TIME_VALUES, 0.0, WINDOW_VALUES, color=WINDOW_GREEN, alpha=0.22)
    ax.plot(TIME_VALUES, WINDOW_VALUES, color=WINDOW_GREEN, lw=2.4)
    ax.axvline(OBS_START, color=WINDOW_GREEN, lw=2.0, ls="--")
    ax.axvline(OBS_END, color=WINDOW_GREEN, lw=2.0, ls="--")
    style_window_axis(ax, r"Rectangular window $w_{\mathrm{rect}}(t)$")
    save_figure(fig, "05_rechteckfenster_w_rect_t.png")


def main():
    clear_output_dir()
    export_long_signal()
    export_signal_with_observation_window()
    export_signal_with_dimmed_outside()
    export_observed_signal()
    export_rectangular_window()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
