from pathlib import Path
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from PIL import Image


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_faltung_als_fensterkopien"
    / "04B_faltung_als_ueberlappung"
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

RESULT_BLACK = "0.15"
RECTANGLE_BLUE = "#2b7bbb"
SAWTOOTH_GREEN = "#66b77a"
OVERLAP_RED = "#d7263d"
FUTURE_GREY = "0.80"
RESULT_YMAX = 0.56
HELPER_LINE_ALPHA = 0.45
STATIC_H_FILL_ALPHA = 0.16
GIF_H_FILL_ALPHA = 0.24

TAU_START = -2.0
TAU_END = 3.0
SHIFT_START = TAU_START
SHIFT_END = TAU_END
TAU_VALUES = np.linspace(TAU_START, TAU_END, 3000)
SHIFT_VALUES = np.linspace(SHIFT_START, SHIFT_END, 3000)
COMMON_XTICKS = np.arange(TAU_START, TAU_END + 1e-9, 1.0)

RECT_LEFT = 0.0
RECT_RIGHT = 1.0

STATIC_SHIFT_STEP = 0.125
GIF_SHIFT_STEP = STATIC_SHIFT_STEP / 4.0
STATIC_PRE_GIF_SHIFTS = [0.0, -0.5, -0.375, -0.25]
GIF_SPLIT_VALUE = 1.0
GIF_MIN_SHIFT = -0.25
GIF_MAX_SHIFT = 2.25
GIF_SEQUENCE_MIN_TO_ONE = np.round(np.arange(GIF_MIN_SHIFT, GIF_SPLIT_VALUE + 1e-9, GIF_SHIFT_STEP), 5).tolist()
GIF_SEQUENCE_ONE_TO_MAX = np.round(np.arange(GIF_SPLIT_VALUE, GIF_MAX_SHIFT + 1e-9, GIF_SHIFT_STEP), 5).tolist()
GIF_NAME_MIN_TO_ONE = "08_shift_animation_t_min_bis_1.gif"
GIF_NAME_ONE_TO_MAX = "09_shift_animation_t_1_bis_max.gif"
STATIC_AT_ONE_FILENAME = "10_shift_t_plus1.png"
STATIC_AT_MAX_FILENAME = "11_shift_t_max.png"
GIF_FRAME_DURATION_MS = 220
GIF_HOLD_FIRST_MS = 900
GIF_HOLD_LAST_MS = 1200


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*"):
        if image_file.suffix.lower() in {".png", ".gif"}:
            image_file.unlink()


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


def gif_compatible_frame(image):
    canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
    canvas.alpha_composite(image)
    return canvas.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE)


def style_tau_axis(ax, title, current_shift=None):
    ax.axhline(0.0, color="0.75", lw=0.9)
    if current_shift is not None:
        ax.axvline(current_shift, color=OVERLAP_RED, alpha=HELPER_LINE_ALPHA, lw=2.0, ls="--", zorder=5)
    ax.set_xlim(TAU_START, TAU_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=TITLE_SIZE)
    ax.set_xlabel(r"Auxiliary variable $\tau$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_shift_axis(ax, title, ymax=RESULT_YMAX):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(SHIFT_START, SHIFT_END)
    ax.set_ylim(-0.02, ymax)
    ax.set_xticks(COMMON_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=TITLE_SIZE)
    ax.set_xlabel("Variable t", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


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


def x_tau(tau_values):
    return np.where((tau_values >= RECT_LEFT) & (tau_values <= RECT_RIGHT), 1.0, 0.0)


def h_tau(tau_values):
    return np.where((tau_values >= RECT_LEFT) & (tau_values <= RECT_RIGHT), tau_values, 0.0)


def h_neg_tau(tau_values):
    return h_tau(-tau_values)


def h_t_minus_tau(tau_values, shift_value):
    return h_tau(shift_value - tau_values)


TAU_STEP = TAU_VALUES[1] - TAU_VALUES[0]
X_SAMPLES = x_tau(TAU_VALUES)
H_SAMPLES = h_tau(TAU_VALUES)
CONVOLUTION_AXIS = np.linspace(
    TAU_START + TAU_START,
    TAU_END + TAU_END,
    X_SAMPLES.size + H_SAMPLES.size - 1,
)
CONVOLUTION_SAMPLES = np.convolve(X_SAMPLES, H_SAMPLES, mode="full") * TAU_STEP


def product_values(shift_value):
    return x_tau(TAU_VALUES) * h_t_minus_tau(TAU_VALUES, shift_value)


def convolution_result(shift_value):
    return float(np.interp(shift_value, CONVOLUTION_AXIS, CONVOLUTION_SAMPLES, left=0.0, right=0.0))


def convolution_result_curve(shift_values):
    shift_values = np.asarray(shift_values, dtype=float)
    return np.interp(shift_values, CONVOLUTION_AXIS, CONVOLUTION_SAMPLES, left=0.0, right=0.0)


def shift_slug(shift_value):
    sign = "plus" if shift_value >= 0.0 else "minus"
    magnitude = f"{abs(shift_value):.3f}".rstrip("0").rstrip(".").replace(".", "p")
    return f"{sign}{magnitude}"


def format_shift_value(shift_value):
    return f"{shift_value:.3f}"


def shifted_kernel_formula(shift_value):
    return rf"h({format_shift_value(shift_value)}-\tau)"


def plot_rectangle(ax, values, color, alpha_fill, lw=2.4, zorder=2):
    ax.fill_between(TAU_VALUES, 0.0, values, color=color, alpha=alpha_fill, zorder=zorder - 1)
    ax.plot(TAU_VALUES, values, color=color, lw=lw, zorder=zorder)


def plot_result_panel(ax, current_shift=None, display_shift_label=None):
    full_result = convolution_result_curve(SHIFT_VALUES)
    ax.plot(SHIFT_VALUES, full_result, color=FUTURE_GREY, lw=2.0, zorder=1)

    if current_shift is not None:
        built_mask = SHIFT_VALUES <= current_shift
        built_values = np.where(built_mask, full_result, np.nan)
        ax.plot(SHIFT_VALUES, built_values, color=RESULT_BLACK, lw=2.6, zorder=3)
        current_value = convolution_result(current_shift)
        ax.axvline(current_shift, color=OVERLAP_RED, alpha=HELPER_LINE_ALPHA, lw=2.0, ls="--", zorder=4)
        ax.plot(current_shift, current_value, marker="o", ms=7, color=OVERLAP_RED, zorder=5)

    title = r"Convolution result $y(t)=(x*h)(t)$"
    if current_shift is not None:
        current_t = display_shift_label if display_shift_label is not None else format_shift_value(current_shift)
        title = rf"Convolution result $y({current_t})=(x*h)({current_t})$"
    style_shift_axis(ax, title)


def build_shift_figure(shift_value, display_shift_label=None, shifted_fill_alpha=STATIC_H_FILL_ALPHA):
    fig, (ax_top, ax_bottom) = create_figure()

    fixed_values = x_tau(TAU_VALUES)
    shifted_values = h_t_minus_tau(TAU_VALUES, shift_value)
    product = product_values(shift_value)

    plot_rectangle(ax_top, fixed_values, RECTANGLE_BLUE, alpha_fill=0.14, zorder=2)
    plot_rectangle(ax_top, shifted_values, SAWTOOTH_GREEN, alpha_fill=shifted_fill_alpha, zorder=3)
    if np.max(product) > 0.0:
        ax_top.fill_between(
            TAU_VALUES,
            0.0,
            product,
            color=OVERLAP_RED,
            alpha=0.28,
            zorder=4,
            edgecolor="none",
            linewidth=0.0,
        )

    kernel_label = shifted_kernel_formula(shift_value)
    if display_shift_label is not None:
        kernel_label = rf"h({display_shift_label}-\tau)"

    title = rf"Pointwise product of $x(\tau)$ and ${kernel_label}$"
    legend_handles = [
        Line2D([0], [0], color=RECTANGLE_BLUE, lw=2.4, label=r"$x(\tau)$"),
        Line2D([0], [0], color=SAWTOOTH_GREEN, lw=2.4, label=rf"${kernel_label}$"),
        Patch(facecolor=OVERLAP_RED, edgecolor=OVERLAP_RED, alpha=0.28, label=rf"$x(\tau)\,{kernel_label}$"),
    ]

    style_tau_axis(ax_top, title, current_shift=shift_value)
    add_inset_legend(ax_top, legend_handles, "upper left")

    plot_result_panel(ax_bottom, current_shift=shift_value, display_shift_label=display_shift_label)
    return fig


def export_fixed_rectangle():
    fig, (ax_top, ax_bottom) = create_figure()
    plot_rectangle(ax_top, x_tau(TAU_VALUES), RECTANGLE_BLUE, alpha_fill=0.18, zorder=2)
    style_tau_axis(ax_top, r"Fixed rectangle $x(\tau)$")
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=RECTANGLE_BLUE, lw=2.4, label=r"$x(\tau)$"),
        ],
        "upper left",
    )
    style_shift_axis(ax_bottom, r"Convolution result $y(t)=(x*h)(t)$")
    save_figure(fig, "01_festes_rechteck_x_tau.png")


def export_unflipped_kernel_overlay():
    fig, (ax_top, ax_bottom) = create_figure()
    plot_rectangle(ax_top, x_tau(TAU_VALUES), RECTANGLE_BLUE, alpha_fill=0.14, zorder=2)
    plot_rectangle(ax_top, h_tau(TAU_VALUES), SAWTOOTH_GREEN, alpha_fill=0.18, zorder=3)
    style_tau_axis(
        ax_top,
        r"Fixed rectangle $x(\tau)$ and sawtooth $h(\tau)$",
    )
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=RECTANGLE_BLUE, lw=2.4, label=r"$x(\tau)$"),
            Line2D([0], [0], color=SAWTOOTH_GREEN, lw=2.4, label=r"$h(\tau)$"),
        ],
        "upper left",
    )
    style_shift_axis(ax_bottom, r"Convolution result $y(t)=(x*h)(t)$")
    save_figure(fig, "02_rechteck_x_tau_und_saegezahn_h_tau.png")


def export_mirrored_rectangle():
    fig, (ax_top, ax_bottom) = create_figure()
    plot_rectangle(ax_top, x_tau(TAU_VALUES), RECTANGLE_BLUE, alpha_fill=0.14, zorder=2)
    plot_rectangle(ax_top, h_neg_tau(TAU_VALUES), SAWTOOTH_GREEN, alpha_fill=0.18, zorder=2)
    style_tau_axis(
        ax_top,
        r"Fixed rectangle $x(\tau)$ and mirrored sawtooth $h(-\tau)$",
    )
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=RECTANGLE_BLUE, lw=2.4, label=r"$x(\tau)$"),
            Line2D([0], [0], color=SAWTOOTH_GREEN, lw=2.4, label=r"$h(-\tau)$"),
        ],
        "upper left",
    )
    style_shift_axis(ax_bottom, r"Convolution result $y(t)=(x*h)(t)$")
    save_figure(fig, "03_gespiegelter_saegezahn_h_minus_tau.png")


def export_shift_frame(index, shift_value, display_shift_label=None):
    fig = build_shift_figure(shift_value, display_shift_label=display_shift_label)
    save_figure(fig, f"{index:02d}_shift_t_{shift_slug(shift_value)}.png")


def export_shift_gif(filename, shift_sequence):
    frames = []
    durations = []
    for shift_value in shift_sequence:
        fig = build_shift_figure(shift_value, shifted_fill_alpha=GIF_H_FILL_ALPHA)
        frames.append(gif_compatible_frame(render_figure(fig)))
        durations.append(GIF_FRAME_DURATION_MS)

    if not frames:
        return

    durations[0] = GIF_HOLD_FIRST_MS
    durations[-1] = GIF_HOLD_LAST_MS
    frames[0].save(
        OUTPUT_DIR / filename,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def main():
    clear_output_dir()
    export_fixed_rectangle()
    export_unflipped_kernel_overlay()
    export_mirrored_rectangle()
    for offset, shift_value in enumerate(STATIC_PRE_GIF_SHIFTS, start=4):
        if offset == 4 and shift_value == 0.0:
            export_shift_frame(offset, shift_value, display_shift_label="0")
        else:
            export_shift_frame(offset, shift_value)
    export_shift_gif(GIF_NAME_MIN_TO_ONE, GIF_SEQUENCE_MIN_TO_ONE)
    export_shift_gif(GIF_NAME_ONE_TO_MAX, GIF_SEQUENCE_ONE_TO_MAX)
    fig = build_shift_figure(GIF_SPLIT_VALUE)
    save_figure(fig, STATIC_AT_ONE_FILENAME)
    fig = build_shift_figure(GIF_MAX_SHIFT)
    save_figure(fig, STATIC_AT_MAX_FILENAME)
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
