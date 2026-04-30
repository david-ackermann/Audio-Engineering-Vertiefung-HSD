from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_faltung_als_fensterkopien"
    / "04A_formelkarte_und_zutaten"
)

DPI = 200
FIGSIZE = (12.0, 3.3)
TITLE_SIZE = 22
LABEL_SIZE = 18
TICK_SIZE = 15
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.16
TOP_MARGIN = 0.84

SIGNAL_BLACK = "0.15"
SPECTRAL_LINE_BLUE = "#2b7bbb"
WINDOW_GREEN = "#66b77a"
PLACEHOLDER_GREY = "0.75"

FREQ_START = -6.0
FREQ_END = 6.0
FREQUENCY_VALUES = np.linspace(FREQ_START, FREQ_END, 4000)
COMMON_XTICKS = np.arange(FREQ_START, FREQ_END + 1e-9, 2.0)
F0 = 2.0
LINE_HEIGHT = 0.5
WINDOW_DURATION = 3.5


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


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def style_frequency_axis(ax, title, y_max=1.12, x_limits=(FREQ_START, FREQ_END)):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_xticks(COMMON_XTICKS)
    ax.set_ylim(-0.02 * y_max, y_max)
    ax.set_yticks(np.arange(0.0, y_max + 1e-9, 0.5))
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def normalized_window_spectrum():
    return np.abs(np.sinc(FREQUENCY_VALUES * WINDOW_DURATION))


def export_ideal_line_spectrum():
    fig, ax = create_figure()
    ax.vlines([-F0, F0], 0.0, [LINE_HEIGHT, LINE_HEIGHT], color=SPECTRAL_LINE_BLUE, lw=2.8)
    style_frequency_axis(ax, r"Ideal line spectrum $X(f)$", y_max=1.12)
    save_figure(fig, "01_ideales_linienspektrum_cosinus.png")


def export_window_spectrum():
    fig, ax = create_figure()
    ax.plot(FREQUENCY_VALUES, normalized_window_spectrum(), color=WINDOW_GREEN, lw=2.6)
    style_frequency_axis(ax, r"Window spectrum $|W(f)|$")
    save_figure(fig, "02_fensterspektrum_w_f.png")


def export_empty_target_spectrum():
    fig, ax = create_figure()
    style_frequency_axis(ax, r"Observed spectrum $X_{\mathrm{obs}}(f)$")
    ax.plot(FREQUENCY_VALUES, np.zeros_like(FREQUENCY_VALUES), color=PLACEHOLDER_GREY, lw=1.6, ls="--")
    save_figure(fig, "03_beobachtetes_spektrum_leer.png")


def export_ingredients_overview():
    fig, ax = create_figure()
    ax.vlines([-F0, F0], 0.0, [LINE_HEIGHT, LINE_HEIGHT], color=SPECTRAL_LINE_BLUE, lw=2.4, alpha=0.95)
    ax.plot(FREQUENCY_VALUES, normalized_window_spectrum(), color=WINDOW_GREEN, lw=2.4, alpha=0.95)
    style_frequency_axis(ax, "Ingredients for convolution", y_max=1.12)
    save_figure(fig, "04_zutaten_ueberblick.png")


def main():
    clear_output_dir()
    export_ideal_line_spectrum()
    export_window_spectrum()
    export_empty_target_spectrum()
    export_ingredients_overview()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
