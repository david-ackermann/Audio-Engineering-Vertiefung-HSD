from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from PIL import Image


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_faltung_als_fensterkopien"
    / "04C_eine_spektrallinie_eine_kopie"
    / "04C2_spektrum_und_spektrallinie"
)

DPI = 200
FIGSIZE = (12.0, 6.6)
TITLE_SIZE = 22
LABEL_SIZE = 18
TICK_SIZE = 15
LEGEND_SIZE = 13
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.10
TOP_MARGIN = 0.92
HSPACE = 0.42

SIGNAL_BLACK = "0.15"
SPECTRAL_LINE_BLUE = "#2b7bbb"
WINDOW_GREEN = "#66b77a"
ACTIVE_RED = "#d7263d"
FUTURE_GREY = "0.80"
HELPER_LINE_ALPHA = 0.45
SPECTRAL_LINE_WIDTH = 3.2
PRODUCT_LINE_WIDTH = 1.8

AXIS_START = -6.0
AXIS_END = 6.0
AUX_VALUES = np.linspace(AXIS_START, AXIS_END, 4000)
OUTPUT_VALUES = np.linspace(AXIS_START, AXIS_END, 4000)
COMMON_XTICKS = np.arange(AXIS_START, AXIS_END + 1e-9, 2.0)

F0 = 2.0
WINDOW_DURATION = 3.5

STATIC_FRAMES = [0.00]
GIF_VALUES = np.round(np.arange(0.00, 4.00 + 1e-9, 0.025), 3).tolist()
GIF_NAME = "05_shifted_window_animation.gif"


def clear_owned_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_DIR.glob("*"):
        if path.is_file() and path.suffix.lower() in {".png", ".gif"}:
            path.unlink()


def create_figure():
    fig, axes = plt.subplots(2, 1, figsize=FIGSIZE)
    fig.subplots_adjust(
        left=LEFT_MARGIN,
        right=RIGHT_MARGIN,
        bottom=BOTTOM_MARGIN,
        top=TOP_MARGIN,
        hspace=HSPACE,
    )
    return fig, axes


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def render_figure(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=DPI, facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    with Image.open(buffer) as image:
        return image.convert("RGBA").copy()


def style_aux_axis(ax, title, current_f=None, show_current_line=True):
    ax.axhline(0.0, color="0.75", lw=0.9)
    if current_f is not None and show_current_line:
        ax.axvline(current_f, color=ACTIVE_RED, alpha=HELPER_LINE_ALPHA, lw=2.0, ls="--", zorder=6)
    ax.set_xlim(AXIS_START, AXIS_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=TITLE_SIZE)
    ax.set_xlabel(r"Auxiliary frequency $\nu$ [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_output_axis(ax, title, current_f=None, show_current_line=True):
    ax.axhline(0.0, color="0.75", lw=0.9)
    if current_f is not None and show_current_line:
        ax.axvline(current_f, color=ACTIVE_RED, alpha=HELPER_LINE_ALPHA, lw=2.0, ls="--", zorder=4)
    ax.set_xlim(AXIS_START, AXIS_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_empty_output_axis(ax):
    style_output_axis(ax, r"Observed Spectrum $Y(f)$", show_current_line=False)


def add_inset_legend(ax, handles, loc="upper left"):
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


def format_value(value):
    return f"{value:.3f}"


def format_frequency(value):
    return str(int(round(value))) if float(value).is_integer() else f"{value:g}"


def value_slug(value):
    sign = "plus" if value >= 0.0 else "minus"
    magnitude = f"{abs(value):.3f}".rstrip("0").rstrip(".").replace(".", "p")
    return f"{sign}{magnitude}"


def window_spectrum(values):
    return np.abs(np.sinc(WINDOW_DURATION * values))


def shifted_window_for_integral(aux_values, current_f):
    return window_spectrum(current_f - aux_values)


def shifted_window_copy(output_values):
    return window_spectrum(output_values - F0)


def plot_function(ax, values, function_values, color, alpha_fill=0.16, lw=2.5, zorder=2):
    ax.fill_between(values, 0.0, function_values, color=color, alpha=alpha_fill, zorder=zorder - 1)
    ax.plot(values, function_values, color=color, lw=lw, zorder=zorder)


def draw_vertical_line(ax, position, height, color, lw=2.2, zorder=4):
    if height <= 0.0:
        return
    ax.vlines(position, 0.0, height, color=color, lw=lw, zorder=zorder)


def plot_result_panel(ax, current_f=None, show_full=False):
    full_result = shifted_window_copy(OUTPUT_VALUES)

    if show_full:
        ax.plot(OUTPUT_VALUES, full_result, color=SIGNAL_BLACK, lw=2.6, zorder=3)
        style_output_axis(ax, r"Observed Spectrum $Y(f)$", show_current_line=False)
        return

    ax.plot(OUTPUT_VALUES, full_result, color=FUTURE_GREY, lw=2.0, zorder=1)

    if current_f is not None:
        built_values = np.where(OUTPUT_VALUES <= current_f, full_result, np.nan)
        ax.plot(OUTPUT_VALUES, built_values, color=SIGNAL_BLACK, lw=2.6, zorder=3)
        style_output_axis(ax, r"Observed Spectrum $Y(f)$", current_f=current_f)
        return

    style_output_axis(ax, r"Observed Spectrum $Y(f)$", show_current_line=False)


def build_shift_figure(current_f):
    fig, (ax_top, ax_bottom) = create_figure()

    shifted_window_values = shifted_window_for_integral(AUX_VALUES, current_f)
    plot_function(ax_top, AUX_VALUES, shifted_window_values, WINDOW_GREEN, alpha_fill=0.16, zorder=2)
    draw_vertical_line(ax_top, F0, 1.0, SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, zorder=4)

    weighted_value = float(shifted_window_copy(np.array([current_f]))[0])
    draw_vertical_line(ax_top, F0, weighted_value, ACTIVE_RED, lw=PRODUCT_LINE_WIDTH, zorder=5)

    style_aux_axis(
        ax_top,
        rf"Pointwise product of $X(f)$ and $W({format_value(current_f)}-\nu)$",
        current_f=current_f,
    )
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.5, label=r"$W(f-\nu)$"),
            Line2D([0], [0], color=SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, label=rf"$X(f)$ at {format_frequency(F0)} Hz"),
            Line2D([0], [0], color=ACTIVE_RED, lw=PRODUCT_LINE_WIDTH, label=r"$X(f)W(f-\nu)$"),
        ],
    )

    plot_result_panel(ax_bottom, current_f=current_f)
    return fig


def build_combined_reference_figure():
    fig, (ax_top, ax_bottom) = create_figure()
    plot_function(ax_top, AUX_VALUES, window_spectrum(AUX_VALUES), WINDOW_GREEN, alpha_fill=0.16, zorder=2)
    draw_vertical_line(ax_top, F0, 1.0, SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, zorder=4)
    style_aux_axis(ax_top, r"Window spectrum and spectral line")
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.5, label=r"$W(\nu)$"),
            Line2D([0], [0], color=SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, label=rf"$X(f)$ at {format_frequency(F0)} Hz"),
        ],
    )
    style_empty_output_axis(ax_bottom)
    return fig


def build_final_overview_figure():
    fig, (ax_top, ax_bottom) = create_figure()
    plot_function(ax_top, AUX_VALUES, window_spectrum(AUX_VALUES), WINDOW_GREEN, alpha_fill=0.16, zorder=2)
    draw_vertical_line(ax_top, F0, 1.0, SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, zorder=4)
    style_aux_axis(ax_top, r"Window spectrum and spectral line", show_current_line=False)
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=WINDOW_GREEN, lw=2.5, label=r"$W(\nu)$"),
            Line2D([0], [0], color=SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, label=rf"$X(f)$ at {format_frequency(F0)} Hz"),
        ],
    )
    plot_result_panel(ax_bottom, show_full=True)
    return fig


def export_window_spectrum():
    fig, (ax_top, ax_bottom) = create_figure()
    plot_function(ax_top, AUX_VALUES, window_spectrum(AUX_VALUES), WINDOW_GREEN, alpha_fill=0.18, zorder=2)
    style_aux_axis(ax_top, r"Window spectrum $W(\nu)$ of a longer window")
    add_inset_legend(ax_top, [Line2D([0], [0], color=WINDOW_GREEN, lw=2.5, label=r"$W(\nu)$")])
    style_empty_output_axis(ax_bottom)
    save_figure(fig, "01_window_spectrum_W_nu.png")


def export_spectral_line():
    fig, (ax_top, ax_bottom) = create_figure()
    draw_vertical_line(ax_top, F0, 1.0, SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, zorder=4)
    style_aux_axis(ax_top, rf"Single spectral line in $X(f)$ at {format_frequency(F0)} Hz")
    add_inset_legend(ax_top, [Line2D([0], [0], color=SPECTRAL_LINE_BLUE, lw=SPECTRAL_LINE_WIDTH, label=rf"$X(f)$ at {format_frequency(F0)} Hz")])
    style_empty_output_axis(ax_bottom)
    save_figure(fig, "02_single_spectral_line_X_f.png")


def export_combined_reference():
    fig = build_combined_reference_figure()
    save_figure(fig, "03_window_and_spectral_line.png")


def export_shift_frame(index, current_f):
    fig = build_shift_figure(current_f)
    save_figure(fig, f"{index:02d}_shifted_window_sampling_f_{value_slug(current_f)}.png")


def export_gif():
    frames = []
    durations = []
    for current_f in GIF_VALUES:
        fig = build_shift_figure(current_f)
        frames.append(render_figure(fig))
        durations.append(100)

    durations[0] = 800
    durations[-1] = 1000
    frames[0].save(
        OUTPUT_DIR / GIF_NAME,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def export_last_frame():
    fig = build_final_overview_figure()
    save_figure(fig, "06_observed_spectrum_full.png")


def main():
    clear_owned_outputs()
    export_window_spectrum()
    export_spectral_line()
    export_combined_reference()
    for index, current_f in enumerate(STATIC_FRAMES, start=4):
        export_shift_frame(index, current_f)
    export_gif()
    export_last_frame()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
