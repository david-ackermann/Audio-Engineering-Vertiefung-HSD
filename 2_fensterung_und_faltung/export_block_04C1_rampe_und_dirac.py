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
    / "04C1_rampe_und_dirac"
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

IMPULSE_BLUE = "#2b7bbb"
RAMP_GREEN = "#66b77a"
RESULT_BLACK = "0.15"
ACTIVE_RED = "#d7263d"
FUTURE_GREY = "0.80"
HELPER_LINE_ALPHA = 0.45
STATIC_RAMP_FILL_ALPHA = 0.14
GIF_RAMP_FILL_ALPHA = 0.24

AXIS_START = -2.0
AXIS_END = 3.0
AUX_VALUES = np.linspace(AXIS_START, AXIS_END, 3000)
OUTPUT_VALUES = np.linspace(AXIS_START, AXIS_END, 3000)
COMMON_XTICKS = np.arange(AXIS_START, AXIS_END + 1e-9, 1.0)

RAMP_LEFT = 0.0
RAMP_RIGHT = 1.0

STATIC_FRAMES = [-0.25, 0.60]
GIF_VALUES = np.round(np.arange(-0.25, 1.25 + 1e-9, 0.025), 3).tolist()
GIF_NAME = "06_dirac_ramp_animation.gif"


def clear_owned_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_DIR.iterdir():
        if path.suffix.lower() in {".png", ".gif"}:
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


def gif_compatible_frame(image):
    canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
    canvas.alpha_composite(image)
    return canvas.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE)


def style_aux_axis(ax, title, current_t=None, show_current_line=True):
    ax.axhline(0.0, color="0.75", lw=0.9)
    if current_t is not None and show_current_line:
        ax.axvline(current_t, color=ACTIVE_RED, alpha=HELPER_LINE_ALPHA, lw=2.0, ls="--", zorder=6)
    ax.set_xlim(AXIS_START, AXIS_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=TITLE_SIZE)
    ax.set_xlabel(r"Auxiliary variable $\tau$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_output_axis(ax, title, current_t=None, show_current_line=True):
    ax.axhline(0.0, color="0.75", lw=0.9)
    if current_t is not None and show_current_line:
        ax.axvline(current_t, color=ACTIVE_RED, alpha=HELPER_LINE_ALPHA, lw=2.0, ls="--", zorder=4)
    ax.set_xlim(AXIS_START, AXIS_END)
    ax.set_ylim(-0.08, 1.18)
    ax.set_xticks(COMMON_XTICKS)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=8, fontsize=TITLE_SIZE)
    ax.set_xlabel("Variable t", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


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


def value_slug(value):
    sign = "plus" if value >= 0.0 else "minus"
    magnitude = f"{abs(value):.3f}".rstrip("0").rstrip(".").replace(".", "p")
    return f"{sign}{magnitude}"


def ramp(values):
    return np.where((values >= RAMP_LEFT) & (values <= RAMP_RIGHT), values, 0.0)


def h_t_minus_tau(values, current_t):
    return ramp(current_t - values)


def plot_function(ax, values, function_values, color, alpha_fill=STATIC_RAMP_FILL_ALPHA, lw=2.5, zorder=2):
    ax.fill_between(values, 0.0, function_values, color=color, alpha=alpha_fill, zorder=zorder - 1)
    ax.plot(values, function_values, color=color, lw=lw, zorder=zorder)


def draw_vertical_line(ax, position, height, color, lw=2.2, zorder=4):
    if height <= 0.0:
        return
    ax.vlines(position, 0.0, height, color=color, lw=lw, zorder=zorder)


def plot_result_panel(ax, current_t=None, show_full=False):
    full_result = ramp(OUTPUT_VALUES)
    ax.plot(OUTPUT_VALUES, full_result, color=FUTURE_GREY, lw=2.0, zorder=1)

    if show_full:
        ax.plot(OUTPUT_VALUES, full_result, color=RESULT_BLACK, lw=2.6, zorder=3)
        style_output_axis(ax, r"Convolution result $y(t)=h(t)$")
        return

    if current_t is not None:
        built_values = np.where(OUTPUT_VALUES <= current_t, full_result, np.nan)
        ax.plot(OUTPUT_VALUES, built_values, color=RESULT_BLACK, lw=2.6, zorder=3)
        current_value = float(ramp(np.array([current_t]))[0])
        ax.plot(current_t, current_value, marker="o", ms=7, color=ACTIVE_RED, zorder=5)
        style_output_axis(
            ax,
            rf"Convolution result $y({format_value(current_t)})=h({format_value(current_t)})$",
            current_t=current_t,
        )
        return

    style_output_axis(ax, r"Convolution result $y(t)=h(t)$")


def build_shift_figure(current_t, ramp_fill_alpha=STATIC_RAMP_FILL_ALPHA):
    fig, (ax_top, ax_bottom) = create_figure()

    ramp_values = ramp(AUX_VALUES)
    plot_function(ax_top, AUX_VALUES, h_t_minus_tau(AUX_VALUES, current_t), RAMP_GREEN, alpha_fill=ramp_fill_alpha, zorder=2)
    draw_vertical_line(ax_top, 0.0, 1.0, IMPULSE_BLUE, zorder=4)

    weighted_value = float(ramp(np.array([current_t]))[0])
    draw_vertical_line(ax_top, 0.0, weighted_value, ACTIVE_RED, zorder=5)

    style_aux_axis(
        ax_top,
        rf"Pointwise product of $\delta(\tau)$ and $h({format_value(current_t)}-\tau)$",
        current_t=current_t,
    )
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=IMPULSE_BLUE, lw=2.2, label=r"$x(\tau)=\delta(\tau)$"),
            Line2D([0], [0], color=RAMP_GREEN, lw=2.5, label=rf"$h({format_value(current_t)}-\tau)$"),
            Line2D([0], [0], color=ACTIVE_RED, lw=2.2, label=rf"$h({format_value(current_t)})\delta(\tau)$"),
        ],
    )

    plot_result_panel(ax_bottom, current_t=current_t)
    return fig


def export_fixed_ramp():
    fig, (ax_top, ax_bottom) = create_figure()
    draw_vertical_line(ax_top, 0.0, 1.0, IMPULSE_BLUE, zorder=4)
    style_aux_axis(ax_top, r"Fixed impulse $x(\tau)=\delta(\tau)$", current_t=0.0, show_current_line=False)
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=IMPULSE_BLUE, lw=2.2, label=r"$x(\tau)=\delta(\tau)$"),
        ],
    )
    style_output_axis(ax_bottom, r"Convolution result $y(t)=h(t)$")
    save_figure(fig, "01_fixed_dirac_x_tau.png")


def export_mirrored_impulse():
    fig, (ax_top, ax_bottom) = create_figure()
    draw_vertical_line(ax_top, 0.0, 1.0, IMPULSE_BLUE, zorder=4)
    plot_function(ax_top, AUX_VALUES, ramp(-AUX_VALUES), RAMP_GREEN, alpha_fill=0.14, zorder=2)
    style_aux_axis(ax_top, r"Impulse $x(\tau)$ and mirrored ramp $h(-\tau)$", current_t=0.0, show_current_line=False)
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=IMPULSE_BLUE, lw=2.2, label=r"$x(\tau)=\delta(\tau)$"),
            Line2D([0], [0], color=RAMP_GREEN, lw=2.5, label=r"$h(-\tau)$"),
        ],
    )
    style_output_axis(ax_bottom, r"Convolution result $y(t)=h(t)$")
    save_figure(fig, "03_mirrored_ramp_h_minus_tau.png")


def export_unshifted_ramp():
    fig, (ax_top, ax_bottom) = create_figure()
    draw_vertical_line(ax_top, 0.0, 1.0, IMPULSE_BLUE, zorder=4)
    plot_function(ax_top, AUX_VALUES, ramp(AUX_VALUES), RAMP_GREEN, alpha_fill=0.14, zorder=2)
    style_aux_axis(ax_top, r"Impulse $x(\tau)$ and ramp $h(\tau)$", current_t=0.0, show_current_line=False)
    add_inset_legend(
        ax_top,
        [
            Line2D([0], [0], color=IMPULSE_BLUE, lw=2.2, label=r"$x(\tau)=\delta(\tau)$"),
            Line2D([0], [0], color=RAMP_GREEN, lw=2.5, label=r"$h(\tau)$"),
        ],
    )
    style_output_axis(ax_bottom, r"Convolution result $y(t)=h(t)$")
    save_figure(fig, "02_unshifted_ramp_h_tau.png")


def export_shift_frame(index, current_t):
    fig = build_shift_figure(current_t)
    save_figure(fig, f"{index:02d}_shift_t_{value_slug(current_t)}.png")


def export_gif():
    frames = []
    durations = []
    for current_t in GIF_VALUES:
        fig = build_shift_figure(current_t, ramp_fill_alpha=GIF_RAMP_FILL_ALPHA)
        frames.append(gif_compatible_frame(render_figure(fig)))
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
    fig = build_shift_figure(GIF_VALUES[-1])
    save_figure(fig, "07_ramp_result_at_t_max.png")


def main():
    clear_owned_outputs()
    export_fixed_ramp()
    export_unshifted_ramp()
    export_mirrored_impulse()
    for index, current_f in enumerate(STATIC_FRAMES, start=4):
        export_shift_frame(index, current_f)
    export_gif()
    export_last_frame()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
