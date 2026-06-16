from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from export_block_00_systembegriff import LOWPASS_IR_DISPLAY_GAIN, lowpass_impulse_response


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "02_diskrete_faltung"
OUTPUT_DIR_A = OUTPUT_ROOT / "2A"
OUTPUT_DIR_B = OUTPUT_ROOT / "2B"
OUTPUT_DIR_C = OUTPUT_ROOT / "2C"
OUTPUT_DIR_D = OUTPUT_ROOT / "2D"
OUTPUT_DIR_D_M_SERIES = OUTPUT_DIR_D / "m_0_bis_8"
CURRENT_OUTPUT_DIR = OUTPUT_DIR_A

DPI = 200
FIGSIZE = (12.0, 6.6)
TITLE_SIZE = 22
LABEL_SIZE = 18
TICK_SIZE = 15
LEGEND_SIZE = 13

SIGNAL_BLACK = "0.10"
SYSTEM_BLUE = "#2b7bbb"
SYSTEM_GREEN = "#66b77a"
ACTIVE_RED = "crimson"
COPY_LIGHT_BLUE = "#8ecae6"
FUTURE_GREY = "0.78"

M_MIN = -8
M_MAX = 17
N_MIN = 0
N_MAX = 17
M_GRID = np.arange(M_MIN, M_MAX + 1)
N_GRID = np.arange(N_MIN, N_MAX + 1)

M_MIN_C = M_MIN
M_MAX_C = M_MAX
N_MIN_C = N_MIN
N_MAX_C = N_MAX
M_GRID_C = M_GRID
N_GRID_C = N_GRID

STATIC_SHIFT_POSITIONS = list(range(-1, 4))
GIF_SHIFT_POSITIONS = list(range(1, M_MAX + 1))
GIF_NAME = "09_discrete_convolution_m_1_to_m_max.gif"

STATIC_SHIFT_POSITIONS_C = list(range(-1, 4))
GIF_SHIFT_POSITIONS_C = list(range(1, N_MAX_C + 1))
SPLIT_FRAME_C = 8
GIF_NAME_C_FIRST = "10_discrete_convolution_n_1_to_n_8.gif"
GIF_NAME_C_SECOND = "11_discrete_convolution_n_8_to_n_max.gif"
GIF_NAME_D = "08_shifted_scaled_impulse_responses.gif"
M_SERIES_2D = list(range(0, 9))

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def set_output_dir(output_dir: Path) -> None:
    global CURRENT_OUTPUT_DIR
    CURRENT_OUTPUT_DIR = output_dir


def clear_output_dirs() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_ROOT.glob("*"):
        if image_file.is_file() and image_file.suffix.lower() in {".png", ".gif"}:
            image_file.unlink()

    for output_dir in (OUTPUT_DIR_A, OUTPUT_DIR_B, OUTPUT_DIR_C, OUTPUT_DIR_D, OUTPUT_DIR_D_M_SERIES):
        output_dir.mkdir(parents=True, exist_ok=True)
        for image_file in output_dir.glob("*"):
            if image_file.suffix.lower() in {".png", ".gif"}:
                image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(CURRENT_OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def render_figure(fig) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=DPI, facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    with Image.open(buffer) as image:
        return image.convert("RGBA").copy()


def gif_compatible_frame(image: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
    canvas.alpha_composite(image)
    return canvas.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE)


def example_input() -> dict[int, float]:
    return {
        1: 0.80,
        3: -0.50,
        5: 0.62,
        7: -0.35,
    }


def lowpass_samples() -> dict[int, float]:
    n, h_lp = lowpass_impulse_response()
    return {int(index): float(value) for index, value in zip(n, h_lp) if abs(value) > 1e-12}


def display_scaled_samples(samples: dict[int, float]) -> dict[int, float]:
    return {index: LOWPASS_IR_DISPLAY_GAIN * value for index, value in samples.items()}


def first_input_index(x_samples: dict[int, float]) -> int:
    return min(x_samples)


def active_input_items(x_samples: dict[int, float]) -> list[tuple[int, float]]:
    return [(index, value) for index, value in sorted(x_samples.items()) if value != 0.0]


def shifted_h_formula(index: int) -> str:
    if index == 0:
        return "h[n]"
    sign = "-" if index > 0 else "+"
    return rf"h[n{sign}{abs(index)}]"


def copy_formula(index: int) -> str:
    return rf"x[{index}]{shifted_h_formula(index)}"


def copy_index_label(items: list[tuple[int, float]]) -> str:
    indices = [index for index, _ in items]
    if len(indices) == 1:
        return f"Copy m={indices[0]}"
    m_values = ",".join(str(index) for index in indices)
    return f"Copies m={m_values}"


def shift_position_to_output_index_for_2a(shift_position: int, x_samples: dict[int, float]) -> int:
    return shift_position


def shift_position_slug(shift_position: int) -> str:
    return f"minus_{abs(shift_position)}" if shift_position < 0 else str(shift_position)


def x_value(index: int, x_samples: dict[int, float]) -> float:
    return x_samples.get(index, 0.0)


def h_value(index: int) -> float:
    return 1.0 if index == 0 else 0.0


def h_lowpass_value(index: int, h_samples: dict[int, float]) -> float:
    return h_samples.get(index, 0.0)


def sequence_values(indices: np.ndarray, values_by_index: dict[int, float]) -> np.ndarray:
    return np.array([values_by_index.get(int(index), 0.0) for index in indices], dtype=float)


def fixed_dirac_values(indices: np.ndarray) -> np.ndarray:
    return np.array([h_value(int(index)) for index in indices], dtype=float)


def shifted_flipped_x_values(m_values: np.ndarray, n_shift: int, x_samples: dict[int, float]) -> np.ndarray:
    return np.array([x_value(n_shift - int(m), x_samples) for m in m_values], dtype=float)


def shifted_flipped_h_values(m_values: np.ndarray, n_shift: int) -> np.ndarray:
    return np.array([h_value(n_shift - int(m)) for m in m_values], dtype=float)


def lowpass_output_values(x_samples: dict[int, float], h_samples: dict[int, float]) -> np.ndarray:
    return np.array(
        [
            sum(h_lowpass_value(int(m), h_samples) * x_value(int(n) - int(m), x_samples) for m in M_GRID_C)
            for n in N_GRID_C
        ],
        dtype=float,
    )


def shifted_scaled_h_values(input_index: int, input_value: float, h_samples: dict[int, float]) -> np.ndarray:
    return np.array(
        [input_value * h_lowpass_value(int(n) - input_index, h_samples) for n in N_GRID_C],
        dtype=float,
    )


def shifted_h_values(input_index: int, h_samples: dict[int, float]) -> np.ndarray:
    return np.array([h_lowpass_value(int(n) - input_index, h_samples) for n in N_GRID_C], dtype=float)


def summed_shifted_scaled_h_values(
    selected_inputs: list[tuple[int, float]],
    h_samples: dict[int, float],
) -> np.ndarray:
    if not selected_inputs:
        return np.zeros_like(N_GRID_C, dtype=float)
    return np.sum(
        [shifted_scaled_h_values(input_index, input_value, h_samples) for input_index, input_value in selected_inputs],
        axis=0,
    )


def lowpass_partial_output_values(
    x_samples: dict[int, float],
    h_samples: dict[int, float],
    current_n: int,
) -> np.ndarray:
    values = lowpass_output_values(x_samples, h_samples)
    return np.where(N_GRID_C <= current_n, values, np.nan)


def output_values(x_samples: dict[int, float]) -> np.ndarray:
    return np.array([x_value(int(n), x_samples) for n in N_GRID], dtype=float)


def partial_output_values(x_samples: dict[int, float], current_n: int) -> np.ndarray:
    values = output_values(x_samples)
    return np.where(N_GRID <= current_n, values, np.nan)


def stem_sequence(
    ax,
    indices: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    alpha: float = 1.0,
    marker_size: float = 7.5,
    line_width: float = 2.5,
    zorder: int = 3,
) -> None:
    markerline, stemlines, baseline = ax.stem(indices, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.8)
    markerline.set_markersize(marker_size)
    markerline.set_alpha(alpha)
    markerline.set_zorder(zorder + 1)
    stemlines.set_color(color)
    stemlines.set_linewidth(line_width)
    stemlines.set_alpha(alpha)
    stemlines.set_zorder(zorder)
    baseline.set_color(SIGNAL_BLACK)
    baseline.set_linewidth(1.2)
    baseline.set_alpha(0.9)


def style_aux_axis(ax, title: str, current_n: int | None = None) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlim(M_MIN - 0.5, M_MAX + 0.5)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(M_MIN, M_MAX + 1, 2))
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel(r"Auxiliary index $m$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.axvline(0.0, color="0.65", lw=1.0, ls="--")
    if current_n is not None:
        ax.text(
            0.02,
            0.92,
            rf"$n={current_n}$",
            transform=ax.transAxes,
            fontsize=LEGEND_SIZE + 2,
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "0.80"},
        )
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_aux_axis_2c(ax, title: str, current_n: int | None = None) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlim(M_MIN_C - 0.5, M_MAX_C + 0.5)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(M_MIN_C, M_MAX_C + 1, 2))
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel(r"Auxiliary index $m$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.axvline(0.0, color="0.65", lw=1.0, ls="--")
    if current_n is not None:
        ax.text(
            0.02,
            0.92,
            rf"$n={current_n}$",
            transform=ax.transAxes,
            fontsize=LEGEND_SIZE + 2,
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "0.80"},
        )
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_output_axis(ax, title: str, current_n: int | None = None) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlim(N_MIN - 0.5, N_MAX + 0.5)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(N_MIN, N_MAX + 1, 2))
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel(r"Sample index $n$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    if current_n is not None:
        ax.axvline(current_n, color=ACTIVE_RED, alpha=0.45, lw=2.0, ls="--", zorder=1)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_output_axis_2c(ax, title: str, current_n: int | None = None) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlim(N_MIN_C - 0.5, N_MAX_C + 0.5)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(N_MIN_C, N_MAX_C + 1, 2))
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel(r"Sample index $n$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    if current_n is not None:
        ax.axvline(current_n, color=ACTIVE_RED, alpha=0.45, lw=2.0, ls="--", zorder=1)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_legend(ax, handles) -> None:
    ax.legend(
        handles=handles,
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
    )


def add_output_legend(ax, sum_label: str, signal_label: str) -> None:
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_BLUE, lw=2.5, label=signal_label),
            plt.Line2D([0], [0], color=ACTIVE_RED, lw=3.0, label=sum_label),
        ],
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="0.75",
        framealpha=0.95,
        fontsize=LEGEND_SIZE,
    )


def create_figure() -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes]]:
    fig, axes = plt.subplots(2, 1, figsize=FIGSIZE)
    fig.subplots_adjust(left=0.055, right=0.992, bottom=0.105, top=0.94, hspace=0.48)
    return fig, axes


def plot_empty_output_axis(ax) -> None:
    style_output_axis(ax, r"$x[n]$")


def plot_empty_output_axis_2c(ax) -> None:
    style_output_axis_2c(ax, r"$y[n]$")


def draw_product_sample(ax, position: int, value: float) -> None:
    if value == 0.0:
        ax.plot(position, 0, marker="o", ms=8.5, color=ACTIVE_RED, zorder=8)
    else:
        stem_sequence(
            ax,
            np.array([position]),
            np.array([value]),
            color=ACTIVE_RED,
            marker_size=9.0,
            line_width=3.2,
            zorder=7,
        )


def draw_product_sequence(ax, indices: np.ndarray, values: np.ndarray) -> None:
    active = np.abs(values) > 1e-10
    if np.any(active):
        stem_sequence(
            ax,
            indices[active],
            values[active],
            color=ACTIVE_RED,
            marker_size=8.5,
            line_width=3.0,
            zorder=7,
        )


def draw_selected_input_sample(ax, input_index: int, input_value: float) -> None:
    stem_sequence(
        ax,
        np.array([input_index]),
        np.array([input_value]),
        color=ACTIVE_RED,
        marker_size=9.0,
        line_width=3.2,
        zorder=7,
    )


def draw_output_sum_sample(ax, current_n: int, current_value: float) -> None:
    if current_value != 0.0:
        stem_sequence(
            ax,
            np.array([current_n]),
            np.array([current_value]),
            color=ACTIVE_RED,
            marker_size=9.0,
            line_width=3.2,
            zorder=7,
        )
    else:
        ax.plot(current_n, 0, marker="o", ms=8.5, color=ACTIVE_RED, zorder=7)


def export_input_only(x_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID, x_samples)

    stem_sequence(ax_top, M_GRID, x_values, color=SIGNAL_BLACK)
    style_aux_axis(ax_top, r"Input sequence $x[m]$")
    add_legend(ax_top, [plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$")])
    plot_empty_output_axis(ax_bottom)
    save_figure(fig, "01_input_sequence_x_m.png")


def export_input_only_2c(x_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID_C, x_samples)

    stem_sequence(ax_top, M_GRID_C, x_values, color=SIGNAL_BLACK)
    style_aux_axis_2c(ax_top, r"Input sequence $x[m]$")
    add_legend(ax_top, [plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$")])
    plot_empty_output_axis_2c(ax_bottom)
    save_figure(fig, "01_input_sequence_x_m.png")


def export_fixed_dirac_and_input(x_samples: dict[int, float], *, title: str, filename: str) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    h_values = fixed_dirac_values(M_GRID)
    x_values = sequence_values(M_GRID, x_samples)

    stem_sequence(ax_top, M_GRID, x_values, color=SIGNAL_BLACK, alpha=0.88)
    stem_sequence(ax_top, M_GRID, h_values, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    style_aux_axis(ax_top, title)
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$\delta[m]$"),
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$"),
        ],
    )
    plot_empty_output_axis(ax_bottom)
    save_figure(fig, filename)


def export_fixed_lowpass_and_input(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    h_values = sequence_values(M_GRID_C, h_samples)
    x_values = sequence_values(M_GRID_C, x_samples)

    stem_sequence(ax_top, M_GRID_C, x_values, color=SIGNAL_BLACK, alpha=0.88)
    stem_sequence(ax_top, M_GRID_C, h_values, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    style_aux_axis_2c(ax_top, r"Low-pass impulse response $h[m]$ and input sequence $x[m]$")
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$h[m]$"),
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$"),
        ],
    )
    plot_empty_output_axis_2c(ax_bottom)
    save_figure(fig, "02_fixed_lowpass_h_and_x_m.png")


def export_flipped_input(x_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    h_values = fixed_dirac_values(M_GRID)
    flipped_values = shifted_flipped_x_values(M_GRID, 0, x_samples)

    stem_sequence(ax_top, M_GRID, h_values, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    stem_sequence(ax_top, M_GRID, flipped_values, color=SIGNAL_BLACK)
    style_aux_axis(ax_top, r"Flipped input sequence $x[-m]$")
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$\delta[m]$"),
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[-m]$"),
        ],
    )
    plot_empty_output_axis(ax_bottom)
    save_figure(fig, "03_flipped_input_sequence_x_minus_m.png")


def export_flipped_input_2c(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    h_values = sequence_values(M_GRID_C, h_samples)
    flipped_values = shifted_flipped_x_values(M_GRID_C, 0, x_samples)

    stem_sequence(ax_top, M_GRID_C, h_values, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    stem_sequence(ax_top, M_GRID_C, flipped_values, color=SIGNAL_BLACK)
    style_aux_axis_2c(ax_top, r"Flipped input sequence $x[-m]$")
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$h[m]$"),
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[-m]$"),
        ],
    )
    plot_empty_output_axis_2c(ax_bottom)
    save_figure(fig, "03_flipped_input_sequence_x_minus_m.png")


def export_flipped_dirac(x_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID, x_samples)
    flipped_h = shifted_flipped_h_values(M_GRID, 0)

    stem_sequence(ax_top, M_GRID, x_values, color=SIGNAL_BLACK, alpha=0.88)
    stem_sequence(ax_top, M_GRID, flipped_h, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    style_aux_axis(ax_top, r"Flipped Dirac $\delta[-m]$")
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$"),
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$\delta[-m]$"),
        ],
    )
    plot_empty_output_axis(ax_bottom)
    save_figure(fig, "03_flipped_dirac_delta_minus_m.png")


def plot_output_panel(ax_bottom, x_samples: dict[int, float], current_n: int, sum_label: str) -> None:
    current_value = x_value(current_n, x_samples)
    full_y = output_values(x_samples)
    partial_y = partial_output_values(x_samples, current_n)

    stem_sequence(ax_bottom, N_GRID, full_y, color=FUTURE_GREY, alpha=0.45, marker_size=7.0, line_width=2.0, zorder=1)
    stem_sequence(ax_bottom, N_GRID, partial_y, color=SYSTEM_BLUE)
    draw_output_sum_sample(ax_bottom, current_n, current_value)
    style_output_axis(ax_bottom, r"$x[n]$", current_n=current_n)
    add_output_legend(ax_bottom, sum_label, r"reconstructed $x[n]$")


def plot_output_panel_2c(
    ax_bottom,
    x_samples: dict[int, float],
    h_samples: dict[int, float],
    current_n: int,
) -> None:
    full_y = lowpass_output_values(x_samples, h_samples)
    partial_y = lowpass_partial_output_values(x_samples, h_samples, current_n)
    current_value = sum(
        h_lowpass_value(int(m), h_samples) * x_value(current_n - int(m), x_samples)
        for m in M_GRID_C
    )

    stem_sequence(ax_bottom, N_GRID_C, full_y, color=FUTURE_GREY, alpha=0.45, marker_size=7.0, line_width=2.0, zorder=1)
    stem_sequence(ax_bottom, N_GRID_C, partial_y, color=SYSTEM_BLUE)
    draw_output_sum_sample(ax_bottom, current_n, current_value)
    style_output_axis_2c(ax_bottom, r"$y[n]$", current_n=current_n)
    add_output_legend(ax_bottom, r"$\sum_m h[m]x[n-m]$", r"computed $y[n]$")


def build_shift_figure_2a(x_samples: dict[int, float], shift_position: int) -> plt.Figure:
    current_n = shift_position_to_output_index_for_2a(shift_position, x_samples)
    current_value = x_value(current_n, x_samples)

    fig, (ax_top, ax_bottom) = create_figure()
    h_values = fixed_dirac_values(M_GRID)
    moving_x = shifted_flipped_x_values(M_GRID, current_n, x_samples)

    stem_sequence(ax_top, M_GRID, h_values, color=SYSTEM_GREEN, alpha=0.95, marker_size=8.5, line_width=3.0)
    stem_sequence(ax_top, M_GRID, moving_x, color=SIGNAL_BLACK)
    draw_product_sample(ax_top, 0, current_value)
    style_aux_axis(ax_top, rf"Shifted sequence $x[{current_n}-m]$", current_n=current_n)
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$\delta[m]$"),
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=rf"$x[{current_n}-m]$"),
            plt.Line2D([0], [0], color=ACTIVE_RED, lw=3.0, label=r"$\delta[m]\,x[n-m]$"),
        ],
    )
    plot_output_panel(ax_bottom, x_samples, current_n, r"$x[n]=\sum_m \delta[m]x[n-m]$")
    return fig


def build_shift_figure_2b(x_samples: dict[int, float], shift_position: int) -> plt.Figure:
    current_n = shift_position
    current_value = x_value(current_n, x_samples)

    fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID, x_samples)
    moving_h = shifted_flipped_h_values(M_GRID, current_n)

    stem_sequence(ax_top, M_GRID, x_values, color=SIGNAL_BLACK, alpha=0.88)
    stem_sequence(ax_top, M_GRID, moving_h, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    draw_product_sample(ax_top, current_n, current_value)
    style_aux_axis(ax_top, rf"Shifted Dirac $\delta[{current_n}-m]$", current_n=current_n)
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$"),
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=rf"$\delta[{current_n}-m]$"),
            plt.Line2D([0], [0], color=ACTIVE_RED, lw=3.0, label=r"$x[m]\,\delta[n-m]$"),
        ],
    )
    plot_output_panel(ax_bottom, x_samples, current_n, r"$x[n]=\sum_m x[m]\delta[n-m]$")
    return fig


def build_shift_figure_2c(
    x_samples: dict[int, float],
    h_samples: dict[int, float],
    current_n: int,
) -> plt.Figure:
    fig, (ax_top, ax_bottom) = create_figure()
    h_values = sequence_values(M_GRID_C, h_samples)
    moving_x = shifted_flipped_x_values(M_GRID_C, current_n, x_samples)
    product = h_values * moving_x

    stem_sequence(ax_top, M_GRID_C, h_values, color=SYSTEM_GREEN, alpha=0.95, marker_size=8.5, line_width=3.0)
    stem_sequence(ax_top, M_GRID_C, moving_x, color=SIGNAL_BLACK)
    draw_product_sequence(ax_top, M_GRID_C, product)
    style_aux_axis_2c(ax_top, rf"Shifted sequence $x[{current_n}-m]$", current_n=current_n)
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$h[m]$"),
            plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=rf"$x[{current_n}-m]$"),
            plt.Line2D([0], [0], color=ACTIVE_RED, lw=3.0, label=r"$h[m]\,x[n-m]$"),
        ],
    )
    plot_output_panel_2c(ax_bottom, x_samples, h_samples, current_n)
    return fig


def build_copy_figure_2d(
    x_samples: dict[int, float],
    h_samples: dict[int, float],
    copy_count: int,
    *,
    final_frame: bool = False,
    input_items_override: list[tuple[int, float]] | None = None,
) -> plt.Figure:
    input_items = active_input_items(x_samples) if input_items_override is None else input_items_override
    selected_items = input_items[:copy_count]
    current_item = selected_items[-1] if selected_items and not final_frame else None

    fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID_C, x_samples)

    stem_sequence(ax_top, M_GRID_C, x_values, color=SIGNAL_BLACK, alpha=0.88)
    if current_item is not None:
        draw_selected_input_sample(ax_top, current_item[0], current_item[1])

    if current_item is None:
        top_title = r"Input sequence $x[m]$"
    else:
        input_index, input_value = current_item
        copy_label = rf"x[{input_index}]h[n]" if input_index == 0 else rf"x[{input_index}]h[n-{input_index}]"
        if input_value == 0.0:
            top_title = rf"Sample $x[{input_index}]={input_value:.2f}$ gives zero copy ${copy_label}$"
        else:
            top_title = rf"Sample $x[{input_index}]={input_value:.2f}$ starts ${copy_label}$"
    style_aux_axis_2c(ax_top, top_title)
    top_legend_handles = [plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$")]
    if current_item is not None:
        top_legend_handles.append(plt.Line2D([0], [0], color=ACTIVE_RED, lw=3.0, label=rf"$x[{input_index}]$"))
    add_legend(ax_top, top_legend_handles)

    previous_items = selected_items if final_frame else selected_items[:-1]
    for input_index, input_value in previous_items:
        copy_values = shifted_scaled_h_values(input_index, input_value, h_samples)
        stem_sequence(
            ax_bottom,
            N_GRID_C,
            copy_values,
            color=COPY_LIGHT_BLUE,
            alpha=0.85,
            marker_size=7.0,
            line_width=2.3,
            zorder=1,
        )

    if current_item is not None:
        input_index, input_value = current_item
        current_shifted_h = shifted_h_values(input_index, h_samples)
        current_copy = shifted_scaled_h_values(input_index, input_value, h_samples)
        stem_sequence(
            ax_bottom,
            N_GRID_C,
            current_shifted_h,
            color=SYSTEM_GREEN,
            alpha=0.78,
            marker_size=7.5,
            line_width=2.5,
            zorder=3,
        )
        stem_sequence(
            ax_bottom,
            N_GRID_C,
            current_copy,
            color=ACTIVE_RED,
            marker_size=8.5,
            line_width=3.0,
            zorder=5,
        )

    if final_frame:
        partial_sum = summed_shifted_scaled_h_values(selected_items, h_samples)
        stem_sequence(ax_bottom, N_GRID_C, partial_sum, color=SYSTEM_BLUE, marker_size=7.5, line_width=2.7, zorder=4)
    style_output_axis_2c(ax_bottom, r"$y[n]$")

    legend_handles = []
    if previous_items:
        legend_handles.append(plt.Line2D([0], [0], color=COPY_LIGHT_BLUE, lw=2.5, label=copy_index_label(previous_items)))
    if current_item is not None:
        input_index, _ = current_item
        legend_handles.extend(
            [
                plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=2.5, label=rf"${shifted_h_formula(input_index)}$"),
                plt.Line2D([0], [0], color=ACTIVE_RED, lw=3.0, label=rf"${copy_formula(input_index)}$"),
            ]
        )
    if final_frame:
        legend_handles = [
            plt.Line2D([0], [0], color=COPY_LIGHT_BLUE, lw=2.5, label=copy_index_label(selected_items)),
            plt.Line2D([0], [0], color=SYSTEM_BLUE, lw=2.7, label=r"$y[n]=\sum_m x[m]h[n-m]$"),
        ]
    add_legend(ax_bottom, legend_handles)
    return fig


def export_static_shift_frames_2a(x_samples: dict[int, float]) -> None:
    for file_index, shift_position in enumerate(STATIC_SHIFT_POSITIONS, start=4):
        filename = f"{file_index:02d}_shift_m_{shift_position_slug(shift_position)}.png"
        fig = build_shift_figure_2a(x_samples, shift_position)
        save_figure(fig, filename)


def export_static_shift_frames_2b(x_samples: dict[int, float]) -> None:
    for file_index, shift_position in enumerate(STATIC_SHIFT_POSITIONS, start=4):
        filename = f"{file_index:02d}_shift_m_{shift_position_slug(shift_position)}.png"
        fig = build_shift_figure_2b(x_samples, shift_position)
        save_figure(fig, filename)


def export_static_shift_frames_2c(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    for file_index, current_n in enumerate(STATIC_SHIFT_POSITIONS_C, start=4):
        filename = f"{file_index:02d}_shift_n_{shift_position_slug(current_n)}.png"
        fig = build_shift_figure_2c(x_samples, h_samples, current_n)
        save_figure(fig, filename)


def export_gif(x_samples: dict[int, float], build_shift_figure) -> None:
    frames = []
    durations = []
    for shift_position in GIF_SHIFT_POSITIONS:
        fig = build_shift_figure(x_samples, shift_position)
        frames.append(gif_compatible_frame(render_figure(fig)))
        durations.append(650)

    durations[0] = 950
    durations[-1] = 1300
    frames[0].save(
        CURRENT_OUTPUT_DIR / GIF_NAME,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def export_gif_2c(
    x_samples: dict[int, float],
    h_samples: dict[int, float],
    positions: list[int],
    filename: str,
) -> None:
    frames = []
    durations = []
    for current_n in positions:
        fig = build_shift_figure_2c(x_samples, h_samples, current_n)
        frames.append(gif_compatible_frame(render_figure(fig)))
        durations.append(650)

    durations[0] = 950
    durations[-1] = 1300
    frames[0].save(
        CURRENT_OUTPUT_DIR / filename,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def export_shift_m_max(x_samples: dict[int, float], build_shift_figure) -> None:
    fig = build_shift_figure(x_samples, M_MAX)
    save_figure(fig, "10_shift_m_max.png")


def export_shift_n_max_2c(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    fig = build_shift_figure_2c(x_samples, h_samples, N_MAX_C)
    save_figure(fig, "12_shift_n_max.png")


def export_shift_n_split_2c(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    fig = build_shift_figure_2c(x_samples, h_samples, SPLIT_FRAME_C)
    save_figure(fig, "09_shift_n_8.png")


def export_input_only_2d(x_samples: dict[int, float]) -> None:
    fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID_C, x_samples)

    stem_sequence(ax_top, M_GRID_C, x_values, color=SIGNAL_BLACK)
    style_aux_axis_2c(ax_top, r"Input sequence $x[m]$")
    add_legend(ax_top, [plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$")])
    plot_empty_output_axis_2c(ax_bottom)
    save_figure(fig, "01_input_sequence_x_m.png")


def build_impulse_response_reference_2d(h_samples: dict[int, float]) -> plt.Figure:
    fig, (ax_top, ax_bottom) = create_figure()
    h_values = sequence_values(N_GRID_C, h_samples)

    stem_sequence(ax_top, N_GRID_C, h_values, color=SYSTEM_GREEN, marker_size=8.5, line_width=3.0)
    style_output_axis_2c(ax_top, r"Impulse response $h[n]$")
    add_legend(
        ax_top,
        [
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$h[n]$"),
        ],
    )
    plot_empty_output_axis_2c(ax_bottom)
    return fig


def export_impulse_response_reference_2d(h_samples: dict[int, float]) -> None:
    fig = build_impulse_response_reference_2d(h_samples)
    save_figure(fig, "02_impulse_response_h_n.png")


def export_zero_copy_frame_2d(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    fig = build_copy_figure_2d(
        x_samples,
        h_samples,
        1,
        input_items_override=[(0, x_value(0, x_samples))],
    )
    save_figure(fig, "02_copy_m_0.png")


def export_static_copy_frames_2d(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    filenames = [
        "03_first_copy.png",
        "04_second_copy.png",
        "05_third_copy.png",
        "06_fourth_copy.png",
    ]
    for copy_count, filename in enumerate(filenames, start=1):
        fig = build_copy_figure_2d(x_samples, h_samples, copy_count)
        save_figure(fig, filename)

    fig = build_copy_figure_2d(x_samples, h_samples, len(active_input_items(x_samples)), final_frame=True)
    save_figure(fig, "07_final_sum_y_n.png")


def export_m_series_2d(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    set_output_dir(OUTPUT_DIR_D_M_SERIES)
    for frame_index, input_index in enumerate(M_SERIES_2D, start=1):
        input_value = x_value(input_index, x_samples)
        previous_items = [
            (previous_index, x_value(previous_index, x_samples))
            for previous_index in M_SERIES_2D
            if previous_index < input_index and x_value(previous_index, x_samples) != 0.0
        ]
        input_items = previous_items + [(input_index, input_value)]
        fig = build_copy_figure_2d(
            x_samples,
            h_samples,
            len(input_items),
            input_items_override=input_items,
        )
        save_figure(fig, f"{frame_index:02d}_copy_m_{input_index:02d}.png")


def export_gif_2d(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    frames = []
    durations = []

    input_fig, (ax_top, ax_bottom) = create_figure()
    x_values = sequence_values(M_GRID_C, x_samples)
    stem_sequence(ax_top, M_GRID_C, x_values, color=SIGNAL_BLACK)
    style_aux_axis_2c(ax_top, r"Input sequence $x[m]$")
    add_legend(ax_top, [plt.Line2D([0], [0], color=SIGNAL_BLACK, lw=2.5, label=r"$x[m]$")])
    plot_empty_output_axis_2c(ax_bottom)
    frames.append(gif_compatible_frame(render_figure(input_fig)))
    durations.append(950)

    zero_copy_fig = build_copy_figure_2d(
        x_samples,
        h_samples,
        1,
        input_items_override=[(0, x_value(0, x_samples))],
    )
    frames.append(gif_compatible_frame(render_figure(zero_copy_fig)))
    durations.append(950)

    for copy_count in range(1, len(active_input_items(x_samples)) + 1):
        fig = build_copy_figure_2d(x_samples, h_samples, copy_count)
        frames.append(gif_compatible_frame(render_figure(fig)))
        durations.append(800)

    fig = build_copy_figure_2d(x_samples, h_samples, len(active_input_items(x_samples)), final_frame=True)
    frames.append(gif_compatible_frame(render_figure(fig)))
    durations.append(1400)

    frames[0].save(
        CURRENT_OUTPUT_DIR / GIF_NAME_D,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def export_series_2a(x_samples: dict[int, float]) -> None:
    set_output_dir(OUTPUT_DIR_A)
    export_input_only(x_samples)
    export_fixed_dirac_and_input(
        x_samples,
        title=r"Fixed Dirac $\delta[m]$ and input sequence $x[m]$",
        filename="02_fixed_dirac_and_x_m.png",
    )
    export_flipped_input(x_samples)
    export_static_shift_frames_2a(x_samples)
    export_gif(x_samples, build_shift_figure_2a)
    export_shift_m_max(x_samples, build_shift_figure_2a)


def export_series_2b(x_samples: dict[int, float]) -> None:
    set_output_dir(OUTPUT_DIR_B)
    export_input_only(x_samples)
    export_fixed_dirac_and_input(
        x_samples,
        title=r"Fixed input $x[m]$ and Dirac $\delta[m]$",
        filename="02_fixed_x_and_dirac_m.png",
    )
    export_flipped_dirac(x_samples)
    export_static_shift_frames_2b(x_samples)
    export_gif(x_samples, build_shift_figure_2b)
    export_shift_m_max(x_samples, build_shift_figure_2b)


def export_series_2c(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    set_output_dir(OUTPUT_DIR_C)
    export_input_only_2c(x_samples)
    export_fixed_lowpass_and_input(x_samples, h_samples)
    export_flipped_input_2c(x_samples, h_samples)
    export_static_shift_frames_2c(x_samples, h_samples)
    export_shift_n_split_2c(x_samples, h_samples)
    export_gif_2c(x_samples, h_samples, list(range(1, SPLIT_FRAME_C + 1)), GIF_NAME_C_FIRST)
    export_gif_2c(x_samples, h_samples, list(range(SPLIT_FRAME_C, N_MAX_C + 1)), GIF_NAME_C_SECOND)
    export_shift_n_max_2c(x_samples, h_samples)


def export_series_2d(x_samples: dict[int, float], h_samples: dict[int, float]) -> None:
    set_output_dir(OUTPUT_DIR_D)
    export_input_only_2d(x_samples)
    export_zero_copy_frame_2d(x_samples, h_samples)
    export_static_copy_frames_2d(x_samples, h_samples)
    export_gif_2d(x_samples, h_samples)
    export_m_series_2d(x_samples, h_samples)


def main() -> None:
    clear_output_dirs()
    x_samples = example_input()
    h_samples = lowpass_samples()
    h_samples_display = display_scaled_samples(h_samples)
    export_series_2a(x_samples)
    export_series_2b(x_samples)
    export_series_2c(x_samples, h_samples_display)
    export_series_2d(x_samples, h_samples_display)
    print(f"PNG figures and GIFs exported to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
