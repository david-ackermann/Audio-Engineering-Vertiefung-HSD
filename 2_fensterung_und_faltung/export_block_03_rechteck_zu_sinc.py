from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "03_rechteck_zu_sinc"

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

WINDOW_GREEN = "#66b77a"
ACTIVE_RED = "#d7263d"
SIDE_LOBE_APRICOT = "#efc18a"
GREY_LIGHT = "0.82"
GREY_MEDIUM = "0.66"
GREY_DARK = "0.50"

TIME_START = -2.0
TIME_END = 2.0
FREQ_START = -4.5
FREQ_END = 4.5

BASE_DURATION = 1.0
LONG_DURATION = 1.6
LONGER_DURATION = 2.4
UNNORMALIZED_COMPARISON_Y_MAX = LONG_DURATION * 1.08

TIME_VALUES = np.linspace(TIME_START, TIME_END, 2400)
FREQUENCY_VALUES = np.linspace(FREQ_START, FREQ_END, 4000)


def rect_window(time_values, duration):
    return np.where(np.abs(time_values) <= duration / 2.0, 1.0, 0.0)


def rect_spectrum_magnitude(frequency_values, duration):
    return np.abs(duration * np.sinc(frequency_values * duration))


def rect_spectrum_magnitude_normalized(frequency_values, duration):
    magnitude = rect_spectrum_magnitude(frequency_values, duration)
    return magnitude / np.max(magnitude)


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


def style_window_axis(ax, title, x_limits=(TIME_START, TIME_END), y_max=1.18):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(-0.08, y_max)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_frequency_axis(ax, title, y_max=1.12, x_limits=(FREQ_START, FREQ_END)):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(-0.02 * y_max, y_max)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
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


def duration_label(duration):
    return f"T = {duration:.1f} s"


def plot_window(ax, duration, color, alpha, lw=2.4, zorder=2):
    window_values = rect_window(TIME_VALUES, duration)
    ax.fill_between(TIME_VALUES, 0.0, window_values, color=color, alpha=alpha, zorder=zorder - 1)
    ax.plot(TIME_VALUES, window_values, color=color, lw=lw, zorder=zorder)


def plot_normalized_spectrum(ax, duration, color, lw=2.4, alpha=1.0, zorder=2):
    ax.plot(
        FREQUENCY_VALUES,
        rect_spectrum_magnitude_normalized(FREQUENCY_VALUES, duration),
        color=color,
        lw=lw,
        alpha=alpha,
        zorder=zorder,
    )


def plot_unnormalized_spectrum(ax, duration, color, lw=2.4, alpha=1.0, zorder=2):
    ax.plot(
        FREQUENCY_VALUES,
        rect_spectrum_magnitude(FREQUENCY_VALUES, duration),
        color=color,
        lw=lw,
        alpha=alpha,
        zorder=zorder,
    )


def export_rect_window_time_domain():
    fig, ax = create_figure()
    plot_window(ax, BASE_DURATION, WINDOW_GREEN, alpha=0.22)
    ax.axvline(-BASE_DURATION / 2.0, color=WINDOW_GREEN, lw=2.0, ls="--")
    ax.axvline(BASE_DURATION / 2.0, color=WINDOW_GREEN, lw=2.0, ls="--")
    style_window_axis(ax, r"Rectangular window $w_{\mathrm{rect}}(t)$")
    save_figure(fig, "01_rechteckfenster_im_zeitbereich.png")


def export_rect_window_spectrum():
    fig, ax = create_figure()
    ax.plot(FREQUENCY_VALUES, rect_spectrum_magnitude(FREQUENCY_VALUES, BASE_DURATION), color=WINDOW_GREEN, lw=2.4)
    style_frequency_axis(ax, r"Magnitude spectrum $|W_{\mathrm{rect}}(f)|$", y_max=UNNORMALIZED_COMPARISON_Y_MAX)
    save_figure(fig, "02_betragsspektrum_w_rect_f.png")


def export_rect_window_spectrum_with_lobes():
    fig, ax = create_figure()
    spectrum_values = rect_spectrum_magnitude(FREQUENCY_VALUES, BASE_DURATION)
    zero_spacing = 1.0 / BASE_DURATION
    main_lobe_mask = np.abs(FREQUENCY_VALUES) <= zero_spacing
    visible_zero_indices = np.arange(1, int(np.floor(FREQ_END / zero_spacing)) + 1)

    ax.plot(FREQUENCY_VALUES, spectrum_values, color=WINDOW_GREEN, lw=2.4)
    ax.fill_between(
        FREQUENCY_VALUES[main_lobe_mask],
        0.0,
        spectrum_values[main_lobe_mask],
        color=ACTIVE_RED,
        alpha=0.18,
    )
    for lobe_index in visible_zero_indices:
        left_zero = lobe_index * zero_spacing
        right_zero = (lobe_index + 1) * zero_spacing
        side_lobe_mask_right = (FREQUENCY_VALUES >= left_zero) & (FREQUENCY_VALUES <= right_zero)
        side_lobe_mask_left = (FREQUENCY_VALUES <= -left_zero) & (FREQUENCY_VALUES >= -right_zero)

        if np.any(side_lobe_mask_right):
            ax.fill_between(
                FREQUENCY_VALUES[side_lobe_mask_right],
                0.0,
                spectrum_values[side_lobe_mask_right],
                color=SIDE_LOBE_APRICOT,
                alpha=0.28,
            )
        if np.any(side_lobe_mask_left):
            ax.fill_between(
                FREQUENCY_VALUES[side_lobe_mask_left],
                0.0,
                spectrum_values[side_lobe_mask_left],
                color=SIDE_LOBE_APRICOT,
                alpha=0.28,
            )

    ax.axvline(-zero_spacing, color=ACTIVE_RED, lw=2.0, ls="--")
    ax.axvline(zero_spacing, color=ACTIVE_RED, lw=2.0, ls="--")
    style_frequency_axis(
        ax,
        r"Main lobe and side lobes of $|W_{\mathrm{rect}}(f)|$",
        y_max=UNNORMALIZED_COMPARISON_Y_MAX,
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.4, label="spectrum"),
            Patch(facecolor=ACTIVE_RED, edgecolor=ACTIVE_RED, alpha=0.18, label="main lobe"),
            Patch(facecolor=SIDE_LOBE_APRICOT, edgecolor=SIDE_LOBE_APRICOT, alpha=0.28, label="side lobes"),
            Line2D([0], [0], color=ACTIVE_RED, lw=2.0, ls="--", label="first zeros"),
        ],
        "upper right",
    )
    save_figure(fig, "03_hauptkeule_und_nebenkeulen_markiert.png")


def export_two_window_time_comparison():
    fig, ax = create_figure()
    plot_window(ax, BASE_DURATION, GREY_MEDIUM, alpha=0.18, zorder=2)
    plot_window(ax, LONG_DURATION, WINDOW_GREEN, alpha=0.22, zorder=3)
    style_window_axis(ax, "Rectangular windows", x_limits=(-1.55, 1.55), y_max=1.18)
    add_inset_legend(
        ax,
        [
            Patch(facecolor=GREY_MEDIUM, edgecolor=GREY_MEDIUM, alpha=0.18, label=duration_label(BASE_DURATION)),
            Patch(facecolor=WINDOW_GREEN, edgecolor=WINDOW_GREEN, alpha=0.22, label=duration_label(LONG_DURATION)),
        ],
        "upper left",
    )
    save_figure(fig, "04_vergleich_kurzes_und_langes_fenster.png")


def export_two_window_spectrum_comparison():
    fig, ax = create_figure()
    plot_normalized_spectrum(ax, BASE_DURATION, GREY_MEDIUM, zorder=2)
    plot_normalized_spectrum(ax, LONG_DURATION, WINDOW_GREEN, zorder=3)
    style_frequency_axis(ax, "Normalized spectra")
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=GREY_MEDIUM, lw=2.4, label=duration_label(BASE_DURATION)),
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.4, label=duration_label(LONG_DURATION)),
        ],
        "upper right",
    )
    save_figure(fig, "06_vergleich_normierter_sinc_spektren.png")


def export_two_window_spectrum_comparison_unnormalized():
    fig, ax = create_figure()
    plot_unnormalized_spectrum(ax, BASE_DURATION, GREY_MEDIUM, zorder=2)
    plot_unnormalized_spectrum(ax, LONG_DURATION, WINDOW_GREEN, zorder=3)
    style_frequency_axis(
        ax,
        "Spectra without normalization",
        y_max=UNNORMALIZED_COMPARISON_Y_MAX,
    )
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=GREY_MEDIUM, lw=2.4, label=duration_label(BASE_DURATION)),
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.4, label=duration_label(LONG_DURATION)),
        ],
        "upper right",
    )
    save_figure(fig, "05_vergleich_sinc_spektren_ohne_normierung.png")


def export_three_window_time_comparison():
    fig, ax = create_figure()
    plot_window(ax, BASE_DURATION, GREY_LIGHT, alpha=0.16, zorder=2)
    plot_window(ax, LONG_DURATION, GREY_MEDIUM, alpha=0.18, zorder=3)
    plot_window(ax, LONGER_DURATION, WINDOW_GREEN, alpha=0.22, zorder=4)
    style_window_axis(ax, "Rectangular windows", x_limits=(-1.55, 1.55), y_max=1.18)
    add_inset_legend(
        ax,
        [
            Patch(facecolor=GREY_LIGHT, edgecolor=GREY_LIGHT, alpha=0.16, label=duration_label(BASE_DURATION)),
            Patch(facecolor=GREY_MEDIUM, edgecolor=GREY_MEDIUM, alpha=0.18, label=duration_label(LONG_DURATION)),
            Patch(facecolor=WINDOW_GREEN, edgecolor=WINDOW_GREEN, alpha=0.22, label=duration_label(LONGER_DURATION)),
        ],
        "upper left",
    )
    save_figure(fig, "07_vergleich_noch_groesseres_fenster.png")


def export_three_window_spectrum_comparison():
    fig, ax = create_figure()
    plot_normalized_spectrum(ax, BASE_DURATION, GREY_LIGHT, zorder=2)
    plot_normalized_spectrum(ax, LONG_DURATION, GREY_MEDIUM, zorder=3)
    plot_normalized_spectrum(ax, LONGER_DURATION, WINDOW_GREEN, zorder=4)
    style_frequency_axis(ax, "Normalized spectra")
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=GREY_LIGHT, lw=2.4, label=duration_label(BASE_DURATION)),
            Line2D([0], [0], color=GREY_MEDIUM, lw=2.4, label=duration_label(LONG_DURATION)),
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.4, label=duration_label(LONGER_DURATION)),
        ],
        "upper right",
    )
    save_figure(fig, "08_vergleich_noch_groesseres_spektrum.png")


def export_infinite_window_time_limit():
    fig, ax = create_figure()
    plot_window(ax, BASE_DURATION, GREY_LIGHT, alpha=0.14, zorder=2)
    plot_window(ax, LONG_DURATION, GREY_MEDIUM, alpha=0.16, zorder=3)
    plot_window(ax, LONGER_DURATION, GREY_DARK, alpha=0.18, zorder=4)
    ideal_window = np.ones_like(TIME_VALUES)
    ax.fill_between(TIME_VALUES, 0.0, ideal_window, color=WINDOW_GREEN, alpha=0.18, zorder=4.5)
    ax.plot(TIME_VALUES, ideal_window, color=WINDOW_GREEN, lw=2.4, zorder=5)
    style_window_axis(ax, "Rectangular windows", x_limits=(-1.55, 1.55), y_max=1.18)
    add_inset_legend(
        ax,
        [
            Patch(facecolor=GREY_LIGHT, edgecolor=GREY_LIGHT, alpha=0.14, label=duration_label(BASE_DURATION)),
            Patch(facecolor=GREY_MEDIUM, edgecolor=GREY_MEDIUM, alpha=0.16, label=duration_label(LONG_DURATION)),
            Patch(facecolor=GREY_DARK, edgecolor=GREY_DARK, alpha=0.18, label=duration_label(LONGER_DURATION)),
            Patch(facecolor=WINDOW_GREEN, edgecolor=WINDOW_GREEN, alpha=0.18, label=r"$T \to \infty$"),
        ],
        "upper left",
    )
    save_figure(fig, "09_theoretisch_unendliches_fenster.png")


def export_finite_spectrum_limit_only():
    fig, ax = create_figure()
    plot_normalized_spectrum(ax, BASE_DURATION, GREY_LIGHT, zorder=2)
    plot_normalized_spectrum(ax, LONG_DURATION, GREY_MEDIUM, zorder=3)
    plot_normalized_spectrum(ax, LONGER_DURATION, GREY_DARK, zorder=4)
    style_frequency_axis(ax, "Normalized spectra")
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=GREY_LIGHT, lw=2.4, label=duration_label(BASE_DURATION)),
            Line2D([0], [0], color=GREY_MEDIUM, lw=2.4, label=duration_label(LONG_DURATION)),
            Line2D([0], [0], color=GREY_DARK, lw=2.4, label=duration_label(LONGER_DURATION)),
        ],
        "upper right",
    )
    save_figure(fig, "10_endliche_spektren_ohne_dirac.png")


def export_infinite_window_spectrum_limit():
    fig, ax = create_figure()
    plot_normalized_spectrum(ax, BASE_DURATION, GREY_LIGHT, zorder=2)
    plot_normalized_spectrum(ax, LONG_DURATION, GREY_MEDIUM, zorder=3)
    plot_normalized_spectrum(ax, LONGER_DURATION, GREY_DARK, zorder=4)
    ax.vlines(0.0, 0.0, 1.02, color=ACTIVE_RED, lw=3.2, zorder=5)
    style_frequency_axis(ax, "Normalized spectra")
    add_inset_legend(
        ax,
        [
            Line2D([0], [0], color=GREY_LIGHT, lw=2.4, label=duration_label(BASE_DURATION)),
            Line2D([0], [0], color=GREY_MEDIUM, lw=2.4, label=duration_label(LONG_DURATION)),
            Line2D([0], [0], color=GREY_DARK, lw=2.4, label=duration_label(LONGER_DURATION)),
            Line2D([0], [0], color=ACTIVE_RED, lw=3.2, label=r"$\delta(f)$, $T \to \infty$"),
        ],
        "upper right",
    )
    save_figure(fig, "11_dirac_und_endliche_spektren.png")


def main():
    clear_output_dir()
    export_rect_window_time_domain()
    export_rect_window_spectrum()
    export_rect_window_spectrum_with_lobes()
    export_two_window_time_comparison()
    export_two_window_spectrum_comparison_unnormalized()
    export_two_window_spectrum_comparison()
    export_three_window_time_comparison()
    export_three_window_spectrum_comparison()
    export_infinite_window_time_limit()
    export_finite_spectrum_limit_only()
    export_infinite_window_spectrum_limit()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
