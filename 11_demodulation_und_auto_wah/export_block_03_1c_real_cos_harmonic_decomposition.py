from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d.art3d import Line3D
from PIL import Image, ImageSequence

from export_block_03_1_delay_clipper_helix import (
    FIGSIZE as REFERENCE_LAYOUT_FIGSIZE,
    REFERENCE_EXPORT_SIZE,
    SUBPLOT_SPLIT_X,
)


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "03_nonlinear_processing_intro"
    / "03C_real_cos_harmonic_decomposition"
)

FIG_DPI = 100
PHASOR_FIGSIZE = (6.9, 6.9)
REFERENCE_PHASOR_FIGSIZE = (6.5, 6.3)
REFERENCE_HELIX_FIGSIZE = (9.47, 6.3)
HELIX_FIGSIZE = REFERENCE_HELIX_FIGSIZE
TIME_DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
ANIMATION_FPS = 24
ANIMATION_FRAMES = 384
ANIMATION_END_N = 8.0

SIGNAL_BLACK = "0.10"
OUTPUT_BLUE = "#2b7bbb"
REFERENCE_GREY = "0.64"
LIGHT_GREY = "0.86"
CLIP_ORANGE = "#d98c2f"
PAIR_COLORS = [
    "#0b6b3a",
    "#1b7f4a",
    "#2ca25f",
    "#49b65f",
    "#66bd63",
    "#8acb63",
    "#a6d96a",
    "#c7e77f",
]

TITLE_SIZE = 19
LABEL_SIZE = 20
TICK_SIZE = 16
TIME_TITLE_SIZE = 24
TIME_LABEL_SIZE = 20
TIME_TICK_SIZE = 17

NUM_SAMPLES = 24
OMEGA = np.pi / 4.0
DELAY_SAMPLES = 1
CLIP_THRESHOLD = 0.75
POSITIVE_HARMONICS = [1, 3, 5, 7, 9, 11, 13, 15]
CURRENT_N = 5.35
PHASOR_LIM = (-1.25, 1.25)
ZOOM_WIDTH = 0.78
ZOOM_HEIGHT = 0.48
HELIX_BOX_ASPECT = (3.9, 1.55, 1.55)
FIXED_REFERENCE_CROP = (18, 65, 1615, 690)
FIXED_REFERENCE_TOP_PAD = 2

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_file in OUTPUT_DIR.rglob("*.png"):
        output_file.unlink()
    for output_file in OUTPUT_DIR.rglob("*.gif"):
        output_file.unlink()


def theta_from_n(n_values: np.ndarray | float) -> np.ndarray | float:
    return OMEGA * (n_values - DELAY_SAMPLES)


def real_input(n_values: np.ndarray | float) -> np.ndarray | float:
    return np.cos(theta_from_n(n_values))


def nonlinear_output(n_values: np.ndarray | float) -> np.ndarray | float:
    return np.clip(real_input(n_values), -CLIP_THRESHOLD, CLIP_THRESHOLD)


def compute_fourier_coefficients(max_harmonic: int = 17) -> dict[int, complex]:
    theta_values = np.linspace(0.0, 2 * np.pi, 240_000, endpoint=False)
    values = np.clip(np.cos(theta_values), -CLIP_THRESHOLD, CLIP_THRESHOLD)
    coefficients: dict[int, complex] = {}
    for harmonic in range(-max_harmonic, max_harmonic + 1):
        coefficients[harmonic] = np.mean(values * np.exp(-1j * harmonic * theta_values))
    return coefficients


COEFFS = compute_fourier_coefficients()


def component_signal(harmonic: int, n_values: np.ndarray | float) -> np.ndarray | complex:
    return COEFFS[harmonic] * np.exp(1j * harmonic * theta_from_n(n_values))


def pair_signal(harmonic: int, n_values: np.ndarray | float) -> np.ndarray | float:
    values = component_signal(harmonic, n_values) + component_signal(-harmonic, n_values)
    if np.isscalar(n_values):
        return float(np.real(values))
    return np.real(values)


def component_sum(harmonics: list[int], n_values: np.ndarray | float) -> np.ndarray | float:
    result = np.zeros_like(np.asarray(n_values, dtype=float), dtype=float)
    for harmonic in harmonics:
        result = result + pair_signal(harmonic, n_values)
    if np.isscalar(n_values):
        return float(result)
    return result


def pair_chain(harmonics: list[int], n_value: float) -> tuple[list[tuple[float, complex, complex, float]], float]:
    current_sum = 0.0
    segments: list[tuple[float, complex, complex, float]] = []
    for harmonic in harmonics:
        positive = component_signal(harmonic, n_value)
        negative = component_signal(-harmonic, n_value)
        next_sum = current_sum + float(np.real(positive + negative))
        segments.append((current_sum, positive, negative, next_sum))
        current_sum = next_sum
    return segments, current_sum


def zoom_limits(center: float) -> tuple[tuple[float, float], tuple[float, float]]:
    xlim = (center - ZOOM_WIDTH / 2, center + ZOOM_WIDTH / 2)
    ylim = (-ZOOM_HEIGHT / 2, ZOOM_HEIGHT / 2)
    return xlim, ylim


def setup_phasor_axis(ax, title: str, *, zoom: bool = False) -> None:
    angle = np.linspace(0.0, 2 * np.pi, 721)
    ax.plot(np.cos(angle), np.sin(angle), color="0.82", lw=2.2, zorder=1)
    ax.axhline(0.0, color="0.75", lw=0.9, zorder=0)
    ax.axvline(0.0, color="0.75", lw=0.9, zorder=0)
    for threshold in (-CLIP_THRESHOLD, CLIP_THRESHOLD):
        ax.axvline(threshold, color=CLIP_ORANGE, lw=1.1, ls=":", alpha=0.58, zorder=2)
    if zoom:
        ax.set_xlim(-1.0, -0.2)
        ax.set_ylim(-0.25, 0.25)
        ax.xaxis.set_major_locator(MultipleLocator(0.2))
        ax.yaxis.set_major_locator(MultipleLocator(0.1))
    else:
        ax.set_xlim(*PHASOR_LIM)
        ax.set_ylim(*PHASOR_LIM)
        ax.xaxis.set_major_locator(MultipleLocator(0.5))
        ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$\mathrm{Re}\{\cdot\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$\mathrm{Im}\{\cdot\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.grid(alpha=0.18)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=12)


def setup_helix_axis(ax, title: str) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("n", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel(r"$\mathrm{Re}\{y[n]\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=12)
    ax.set_zlabel(r"$\mathrm{Im}\{y[n]\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=6)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="x", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="z", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.set_title(title, fontsize=TITLE_SIZE, y=1.035, pad=0)
    ax.view_init(elev=22, azim=-62)
    try:
        ax.set_box_aspect(HELIX_BOX_ASPECT, zoom=1.35)
    except TypeError:
        ax.set_box_aspect(HELIX_BOX_ASPECT)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))


def setup_sequence_axis(ax, title: str) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("n", color=SIGNAL_BLACK, fontsize=TIME_LABEL_SIZE)
    ax.set_ylabel("Amplitude", color=SIGNAL_BLACK, fontsize=TIME_LABEL_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="both", colors=SIGNAL_BLACK, labelsize=TIME_TICK_SIZE)
    ax.grid(True, color="0.75", alpha=0.25)
    ax.axhline(0.0, color="0.55", lw=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title(title, fontsize=TIME_TITLE_SIZE, pad=14)


def make_vector_patch(
    color: str,
    *,
    dashed: bool = False,
    zoom: bool = False,
    label: str | None = None,
) -> FancyArrowPatch:
    patch = FancyArrowPatch(
        (0.0, 0.0),
        (0.0, 0.0),
        arrowstyle="-|>",
        mutation_scale=6 if zoom else 14,
        linewidth=1.05 if zoom else 2.2,
        color=color,
        alpha=0.94,
        label=label,
        zorder=14,
    )
    if dashed:
        patch.set_linestyle("--")
        patch.set_alpha(0.78)
    return patch


def update_vector_patch(patch: FancyArrowPatch, start: complex, end: complex) -> None:
    patch.set_positions((start.real, start.imag), (end.real, end.imag))


def draw_arrow(
    ax,
    start: complex,
    end: complex,
    color: str,
    *,
    dashed: bool = False,
    alpha: float = 0.94,
    linewidth: float | None = None,
    zoom: bool = False,
    label: str | None = None,
) -> None:
    delta = end - start
    arrow = ax.arrow(
        start.real,
        start.imag,
        delta.real,
        delta.imag,
        length_includes_head=True,
        head_width=0.006 if zoom else 0.035,
        head_length=0.010 if zoom else 0.055,
        linewidth=(1.05 if zoom else 2.2) if linewidth is None else linewidth,
        color=color,
        alpha=alpha,
        zorder=12,
        label=label,
    )
    if dashed:
        arrow.set_linestyle("--")


def draw_pair_vectors(
    ax,
    harmonics: list[int],
    n_value: float,
    *,
    zoom: bool = False,
    label_vectors: bool = False,
) -> float:
    segments, current_sum = pair_chain(harmonics, n_value)
    for index, (start, positive, negative, next_sum) in enumerate(segments):
        color = PAIR_COLORS[index]
        start_c = complex(start, 0.0)
        draw_arrow(
            ax,
            start_c,
            start_c + positive,
            color,
            zoom=zoom,
            label=rf"$+{harmonics[index]}\Omega$" if label_vectors else None,
        )
        draw_arrow(
            ax,
            start_c,
            start_c + negative,
            color,
            dashed=True,
            alpha=0.75,
            zoom=zoom,
            label=rf"$-{harmonics[index]}\Omega$" if label_vectors else None,
        )
        ax.plot([start, next_sum], [0.0, 0.0], color=color, lw=1.05 if zoom else 2.2, alpha=0.72, zorder=11)
    return current_sum


def export_phasor_page(
    *,
    filename: str,
    title: str,
    included_harmonics: list[int],
    show_sum: bool,
    show_output_only: bool = False,
    zoom: bool = False,
) -> Path:
    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    y_nl_dense = nonlinear_output(dense_n)
    y_current = nonlinear_output(CURRENT_N)

    fig_size = PHASOR_FIGSIZE if zoom else REFERENCE_PHASOR_FIGSIZE
    fig, ax = plt.subplots(figsize=fig_size, dpi=FIG_DPI, facecolor="white")
    if zoom:
        fig.subplots_adjust(left=0.15, right=0.98, top=0.90, bottom=0.13)
    else:
        fig.subplots_adjust(left=0.17, right=0.938, top=0.918, bottom=0.13)
    setup_phasor_axis(ax, title, zoom=zoom)

    ax.plot(real_input(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.4, ls="--", alpha=0.42, zorder=3)
    ax.plot(
        y_nl_dense,
        np.zeros_like(dense_n),
        color=OUTPUT_BLUE if show_output_only else REFERENCE_GREY,
        lw=2.4,
        alpha=0.95 if show_output_only else 0.60,
        zorder=5,
    )
    ax.plot([y_current], [0.0], "o", color=OUTPUT_BLUE, ms=7, zorder=14)

    if not zoom:
        xlim, ylim = zoom_limits(float(y_current))
        ax.add_patch(
            Rectangle(
                (xlim[0], ylim[0]),
                xlim[1] - xlim[0],
                ylim[1] - ylim[0],
                fill=False,
                edgecolor=OUTPUT_BLUE,
                linewidth=1.6,
                alpha=0.78,
                zorder=16,
            )
        )

    if included_harmonics:
        for index, harmonic in enumerate(included_harmonics):
            positive = component_signal(harmonic, dense_n)
            negative = component_signal(-harmonic, dense_n)
            ax.plot(positive.real, positive.imag, color=PAIR_COLORS[index], lw=1.2, ls=":", alpha=0.46, zorder=6)
            ax.plot(negative.real, negative.imag, color=PAIR_COLORS[index], lw=1.2, ls=":", alpha=0.46, zorder=6)
        approximation = component_sum(included_harmonics, dense_n)
        ax.plot(
            approximation,
            np.zeros_like(dense_n),
            color=OUTPUT_BLUE,
            lw=1.6,
            ls="--" if zoom else "-",
            alpha=0.88,
            zorder=8,
        )
        current_sum = draw_pair_vectors(
            ax,
            included_harmonics,
            CURRENT_N,
            zoom=zoom,
            label_vectors=(not zoom and len(included_harmonics) <= 2),
        )
        ax.plot([current_sum], [0.0], "o", color=OUTPUT_BLUE, ms=7, zorder=15)
        if show_sum:
            draw_arrow(
                ax,
                0.0 + 0.0j,
                complex(current_sum, 0.0),
                OUTPUT_BLUE,
                alpha=0.94,
                linewidth=1.15 if zoom else 2.4,
                zoom=zoom,
            )

    subdir = OUTPUT_DIR / ("phasor_zoom" if zoom else "phasor")
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / filename
    if zoom:
        fig.savefig(path, dpi=FIG_DPI, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    else:
        fig.savefig(path, dpi=FIG_DPI, facecolor="white")
    plt.close(fig)
    return path


def export_helix_page(
    *,
    filename: str,
    title: str,
    included_harmonics: list[int],
    show_sum: bool,
    show_output_only: bool = False,
) -> Path:
    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)

    fig = plt.figure(figsize=HELIX_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    ax = fig.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.015, right=0.985, top=0.90, bottom=0.04)
    ax.set_position([-0.11, 0.025, 1.12, 0.950])
    setup_helix_axis(ax, title)

    ax.plot(dense_n, real_input(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.3, ls="--", alpha=0.34, zorder=3)
    ax.plot(
        dense_n,
        nonlinear_output(dense_n),
        np.zeros_like(dense_n),
        color=OUTPUT_BLUE if show_output_only else REFERENCE_GREY,
        lw=2.2,
        alpha=0.96 if show_output_only else 0.62,
        zorder=5,
    )

    if included_harmonics:
        for index, harmonic in enumerate(included_harmonics):
            positive = component_signal(harmonic, dense_n)
            negative = component_signal(-harmonic, dense_n)
            ax.plot(dense_n, positive.real, positive.imag, color=PAIR_COLORS[index], lw=1.4, ls=":", alpha=0.88, zorder=6 + index)
            ax.plot(dense_n, negative.real, negative.imag, color=PAIR_COLORS[index], lw=1.4, ls="--", alpha=0.60, zorder=6 + index)
        if show_sum:
            approximation = component_sum(included_harmonics, dense_n)
            ax.plot(dense_n, approximation, np.zeros_like(dense_n), color=OUTPUT_BLUE, lw=2.4, alpha=0.94, zorder=18)

    subdir = OUTPUT_DIR / "helix"
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / filename
    fig.savefig(path, dpi=FIG_DPI, facecolor="white")
    plt.close(fig)
    return path


def create_reference_layout_axes(phasor_title: str, helix_title: str) -> tuple[plt.Figure, plt.Axes, plt.Axes]:
    fig = plt.figure(figsize=REFERENCE_LAYOUT_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    grid = fig.add_gridspec(1, 2, width_ratios=[0.62, 2.95])
    ax_phasor = fig.add_subplot(grid[0, 0])
    ax_helix = fig.add_subplot(grid[0, 1], projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.038, right=0.995, top=0.91, bottom=0.08, wspace=0.00)
    ax_phasor.set_position([0.070, 0.115, 0.300, 0.720])
    ax_helix.set_position([0.280, 0.045, 0.715, 0.855])
    ax_phasor.set_facecolor("white")
    ax_helix.set_facecolor("white")
    setup_phasor_axis(ax_phasor, phasor_title, zoom=False)
    setup_helix_axis(ax_helix, helix_title)
    return fig, ax_phasor, ax_helix


def save_reference_split_png(fig: plt.Figure, phasor_path: Path, helix_path: Path) -> None:
    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    rgba = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(height, width, 4)
    image = Image.fromarray(rgba, mode="RGBA")
    phasor, helix = split_fixed_reference_image(image)
    phasor_path.parent.mkdir(parents=True, exist_ok=True)
    helix_path.parent.mkdir(parents=True, exist_ok=True)
    phasor.convert("RGB").save(phasor_path)
    helix.convert("RGB").save(helix_path)


def split_fixed_reference_image(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    fitted = Image.new("RGBA", REFERENCE_EXPORT_SIZE, (255, 255, 255, 255))
    fitted.alpha_composite(image.convert("RGBA").crop(FIXED_REFERENCE_CROP), (0, FIXED_REFERENCE_TOP_PAD))
    phasor = fitted.crop((0, 0, SUBPLOT_SPLIT_X, REFERENCE_EXPORT_SIZE[1]))
    helix = fitted.crop((SUBPLOT_SPLIT_X, 0, REFERENCE_EXPORT_SIZE[0], REFERENCE_EXPORT_SIZE[1]))
    return phasor, helix


def save_reference_helix_png(fig: plt.Figure, helix_path: Path) -> None:
    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    rgba = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(height, width, 4)
    image = Image.fromarray(rgba, mode="RGBA")
    _phasor, helix = split_fixed_reference_image(image)
    helix_path.parent.mkdir(parents=True, exist_ok=True)
    helix.convert("RGB").save(helix_path)


def save_reference_helix_gif(temp_path: Path, helix_path: Path) -> None:
    image = Image.open(temp_path)
    helix_frames: list[Image.Image] = []
    durations: list[int] = []
    for frame in ImageSequence.Iterator(image):
        _phasor, helix = split_fixed_reference_image(frame.convert("RGBA"))
        helix_frames.append(helix)
        durations.append(frame.info.get("duration", image.info.get("duration", round(1000 / ANIMATION_FPS))))

    helix_frames[0].save(
        helix_path,
        save_all=True,
        append_images=helix_frames[1:],
        duration=durations,
        loop=image.info.get("loop", 0),
        disposal=2,
    )


def export_reference_layout_page(
    *,
    base_name: str,
    title: str,
    included_harmonics: list[int],
    show_sum: bool,
    show_output_only: bool = False,
) -> list[Path]:
    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    y_nl_dense = nonlinear_output(dense_n)
    y_current = nonlinear_output(CURRENT_N)

    phasor_path = OUTPUT_DIR / "phasor" / f"{base_name}_phasor.png"
    helix_path = OUTPUT_DIR / "helix" / f"{base_name}_helix.png"
    fig, ax_phasor, ax_helix = create_reference_layout_axes(f"Phasor: {title}", f"Helix: {title}")

    ax_phasor.plot(real_input(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.4, ls="--", alpha=0.42, zorder=3)
    ax_phasor.plot(
        y_nl_dense,
        np.zeros_like(dense_n),
        color=OUTPUT_BLUE if show_output_only else REFERENCE_GREY,
        lw=2.4,
        alpha=0.95 if show_output_only else 0.60,
        zorder=5,
    )
    ax_phasor.plot([y_current], [0.0], "o", color=OUTPUT_BLUE, ms=7, zorder=14)
    xlim, ylim = zoom_limits(float(y_current))
    ax_phasor.add_patch(
        Rectangle(
            (xlim[0], ylim[0]),
            xlim[1] - xlim[0],
            ylim[1] - ylim[0],
            fill=False,
            edgecolor=OUTPUT_BLUE,
            linewidth=1.6,
            alpha=0.78,
            zorder=16,
        )
    )

    ax_helix.plot(dense_n, real_input(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.3, ls="--", alpha=0.34, zorder=3)
    ax_helix.plot(
        dense_n,
        nonlinear_output(dense_n),
        np.zeros_like(dense_n),
        color=OUTPUT_BLUE if show_output_only else REFERENCE_GREY,
        lw=2.2,
        alpha=0.96 if show_output_only else 0.62,
        zorder=5,
    )

    if included_harmonics:
        for index, harmonic in enumerate(included_harmonics):
            positive = component_signal(harmonic, dense_n)
            negative = component_signal(-harmonic, dense_n)
            ax_phasor.plot(positive.real, positive.imag, color=PAIR_COLORS[index], lw=1.2, ls=":", alpha=0.46, zorder=6)
            ax_phasor.plot(negative.real, negative.imag, color=PAIR_COLORS[index], lw=1.2, ls=":", alpha=0.46, zorder=6)
            ax_helix.plot(dense_n, positive.real, positive.imag, color=PAIR_COLORS[index], lw=1.4, ls=":", alpha=0.88, zorder=6 + index)
            ax_helix.plot(dense_n, negative.real, negative.imag, color=PAIR_COLORS[index], lw=1.4, ls="--", alpha=0.60, zorder=6 + index)

        approximation = component_sum(included_harmonics, dense_n)
        ax_phasor.plot(
            approximation,
            np.zeros_like(dense_n),
            color=OUTPUT_BLUE,
            lw=1.6,
            ls="-",
            alpha=0.88,
            zorder=8,
        )
        current_sum = draw_pair_vectors(
            ax_phasor,
            included_harmonics,
            CURRENT_N,
            zoom=False,
            label_vectors=(len(included_harmonics) <= 2),
        )
        ax_phasor.plot([current_sum], [0.0], "o", color=OUTPUT_BLUE, ms=7, zorder=15)
        if show_sum:
            draw_arrow(
                ax_phasor,
                0.0 + 0.0j,
                complex(current_sum, 0.0),
                OUTPUT_BLUE,
                alpha=0.94,
                linewidth=2.4,
                zoom=False,
            )
            ax_helix.plot(dense_n, approximation, np.zeros_like(dense_n), color=OUTPUT_BLUE, lw=2.4, alpha=0.94, zorder=18)

    save_reference_split_png(fig, phasor_path, helix_path)
    plt.close(fig)
    return [phasor_path, helix_path]


def export_sequence_page(
    *,
    filename: str,
    title: str,
    included_harmonics: list[int],
    show_sum: bool,
    show_output_only: bool = False,
) -> Path:
    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    sample_n = np.arange(0, NUM_SAMPLES + 1)

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE, dpi=TIME_DPI, facecolor="white")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    setup_sequence_axis(ax, title)

    ax.plot(dense_n, real_input(dense_n), color=SIGNAL_BLACK, lw=1.4, ls="--", alpha=0.38, zorder=3)
    ax.plot(
        dense_n,
        nonlinear_output(dense_n),
        color=OUTPUT_BLUE if show_output_only else REFERENCE_GREY,
        lw=2.2,
        alpha=0.95 if show_output_only else 0.60,
        zorder=5,
    )
    ax.plot(sample_n, nonlinear_output(sample_n), "o", color=OUTPUT_BLUE, ms=4.5, alpha=0.88, zorder=8)

    if included_harmonics and show_sum:
        approximation = component_sum(included_harmonics, dense_n)
        sample_approximation = component_sum(included_harmonics, sample_n)
        ax.plot(dense_n, approximation, color=OUTPUT_BLUE, lw=2.4, ls="--", alpha=0.94, zorder=10)
        ax.plot(sample_n, sample_approximation, "o", color=OUTPUT_BLUE, ms=4.0, zorder=12)

    subdir = OUTPUT_DIR / "sequence"
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / filename
    fig.savefig(path, dpi=TIME_DPI, facecolor="white")
    plt.close(fig)
    return path


def pad_image_to_size(path: Path, target_size: tuple[int, int]) -> None:
    image = Image.open(path).convert("RGBA")
    if image.size == target_size:
        return
    output = Image.new("RGBA", target_size, (255, 255, 255, 255))
    output.alpha_composite(image, ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2))
    output.convert("RGB").save(path)


def normalize_subdir_images(subdir: Path) -> None:
    paths = sorted(subdir.glob("*.png"))
    if not paths:
        return
    sizes = [Image.open(path).size for path in paths]
    target_size = (max(width for width, _ in sizes), max(height for _, height in sizes))
    for path in paths:
        pad_image_to_size(path, target_size)


def export_rotating_phasor_animation() -> list[Path]:
    harmonics = POSITIVE_HARMONICS
    animation_dir = OUTPUT_DIR / "phasor_animation"
    animation_dir.mkdir(parents=True, exist_ok=True)

    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    frame_n = np.linspace(CURRENT_N, CURRENT_N + ANIMATION_END_N, ANIMATION_FRAMES)
    approximation_dense = component_sum(harmonics, dense_n)

    def setup_animation_axis(ax, title: str, *, zoom: bool = False) -> None:
        setup_phasor_axis(ax, title, zoom=False)
        if zoom:
            ax.xaxis.set_major_locator(MultipleLocator(0.2))
            ax.yaxis.set_major_locator(MultipleLocator(0.1))
        ax.plot(real_input(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.2, ls="--", alpha=0.34, zorder=3)
        ax.plot(nonlinear_output(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.9, alpha=0.52, zorder=4)
        ax.plot(
            approximation_dense,
            np.zeros_like(dense_n),
            color=OUTPUT_BLUE,
            lw=1.7 if not zoom else 1.25,
            ls="--" if zoom else "-",
            alpha=0.88,
            zorder=7,
        )
        for index, harmonic in enumerate(harmonics):
            positive = component_signal(harmonic, dense_n)
            negative = component_signal(-harmonic, dense_n)
            ax.plot(positive.real, positive.imag, color=PAIR_COLORS[index], lw=0.95, ls=":", alpha=0.32, zorder=6)
            ax.plot(negative.real, negative.imag, color=PAIR_COLORS[index], lw=0.95, ls=":", alpha=0.32, zorder=6)

    def add_artists(ax, *, zoom: bool = False):
        positive_vectors = []
        negative_vectors = []
        pair_lines = []
        for index, harmonic in enumerate(harmonics):
            positive = make_vector_patch(
                PAIR_COLORS[index],
                zoom=zoom,
                label=rf"$+{harmonic}\Omega$" if index == 0 and not zoom else None,
            )
            negative = make_vector_patch(
                PAIR_COLORS[index],
                dashed=True,
                zoom=zoom,
                label=rf"$-{harmonic}\Omega$" if index == 0 and not zoom else None,
            )
            ax.add_patch(positive)
            ax.add_patch(negative)
            pair_line, = ax.plot([], [], color=PAIR_COLORS[index], lw=1.05 if zoom else 2.1, alpha=0.70, zorder=11)
            positive_vectors.append(positive)
            negative_vectors.append(negative)
            pair_lines.append(pair_line)
        sum_vector = make_vector_patch(OUTPUT_BLUE, zoom=zoom, label=r"$y[n]$" if not zoom else None)
        sum_vector.set_linewidth(1.15 if zoom else 2.5)
        sum_vector.set_mutation_scale(6 if zoom else 15)
        ax.add_patch(sum_vector)
        sum_point, = ax.plot([], [], "o", color=OUTPUT_BLUE, ms=6.5, zorder=16)
        time_text = ax.text(
            0.035,
            0.955,
            "",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=14,
            color="0.20",
            bbox=dict(boxstyle="round,pad=0.24", facecolor="white", edgecolor="0.82", alpha=0.94),
            zorder=20,
        )
        return positive_vectors, negative_vectors, pair_lines, sum_vector, sum_point, time_text

    main_fig, main_ax = plt.subplots(figsize=REFERENCE_PHASOR_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    main_fig.subplots_adjust(left=0.17, right=0.939, top=0.919, bottom=0.13)
    setup_animation_axis(main_ax, r"Phasor: $|h|\leq 15$")
    main_artists = add_artists(main_ax, zoom=False)
    zoom_rect = Rectangle((0, 0), ZOOM_WIDTH, ZOOM_HEIGHT, fill=False, edgecolor=OUTPUT_BLUE, linewidth=1.5, zorder=18)
    main_ax.add_patch(zoom_rect)

    zoom_fig, zoom_ax = plt.subplots(figsize=PHASOR_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    zoom_fig.subplots_adjust(left=0.15, right=0.98, top=0.90, bottom=0.13)
    setup_animation_axis(zoom_ax, r"Zoom: $|h|\leq 15$", zoom=True)
    zoom_artists = add_artists(zoom_ax, zoom=True)

    def update_artist_group(artists, n_value: float):
        positive_vectors, negative_vectors, pair_lines, sum_vector, sum_point, time_text = artists
        segments, current_sum = pair_chain(harmonics, n_value)
        for positive_patch, negative_patch, pair_line, (start, positive, negative, next_sum) in zip(
            positive_vectors,
            negative_vectors,
            pair_lines,
            segments,
        ):
            start_c = complex(start, 0.0)
            update_vector_patch(positive_patch, start_c, start_c + positive)
            update_vector_patch(negative_patch, start_c, start_c + negative)
            pair_line.set_data([start, next_sum], [0.0, 0.0])
        update_vector_patch(sum_vector, 0.0 + 0.0j, complex(current_sum, 0.0))
        sum_point.set_data([current_sum], [0.0])
        time_text.set_text(f"n = {int(np.floor(n_value + 1e-9))}")
        return current_sum

    def draw_state(frame_index: int):
        n_value = frame_n[frame_index]
        current_sum = update_artist_group(main_artists, n_value)
        xlim, ylim = zoom_limits(current_sum)
        zoom_rect.set_xy((xlim[0], ylim[0]))
        zoom_rect.set_width(xlim[1] - xlim[0])
        zoom_rect.set_height(ylim[1] - ylim[0])
        update_artist_group(zoom_artists, n_value)
        zoom_ax.set_xlim(*xlim)
        zoom_ax.set_ylim(*ylim)
        return (*main_artists[0], *main_artists[1], *main_artists[2], main_artists[3], main_artists[4], main_artists[5], zoom_rect)

    draw_state(0)
    main_preview = animation_dir / "07_rotating_real_cos_phasors_preview.png"
    zoom_preview = animation_dir / "09_rotating_real_cos_phasors_zoom_preview.png"
    main_fig.savefig(main_preview, dpi=FIG_DPI, facecolor="white")
    zoom_fig.savefig(zoom_preview, dpi=FIG_DPI, facecolor="white", bbox_inches="tight", pad_inches=0.06)

    main_animation = FuncAnimation(main_fig, draw_state, frames=len(frame_n), interval=1000 / ANIMATION_FPS, blit=False)
    zoom_animation = FuncAnimation(zoom_fig, draw_state, frames=len(frame_n), interval=1000 / ANIMATION_FPS, blit=False)
    main_gif = animation_dir / "08_rotating_real_cos_phasors_motion.gif"
    zoom_gif = animation_dir / "10_rotating_real_cos_phasors_zoom_motion.gif"
    main_animation.save(main_gif, writer=PillowWriter(fps=ANIMATION_FPS))
    zoom_animation.save(zoom_gif, writer=PillowWriter(fps=ANIMATION_FPS))
    plt.close(main_fig)
    plt.close(zoom_fig)
    return [main_preview, main_gif, zoom_preview, zoom_gif]


def export_rotating_helix_animation() -> list[Path]:
    harmonics = POSITIVE_HARMONICS
    animation_dir = OUTPUT_DIR / "helix_animation"
    animation_dir.mkdir(parents=True, exist_ok=True)

    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    frame_n = np.linspace(CURRENT_N, CURRENT_N + ANIMATION_END_N, ANIMATION_FRAMES)
    approximation_dense = component_sum(harmonics, dense_n)

    fig, _ax_phasor, ax = create_reference_layout_axes(r"Phasor: $|h|\leq 15$", r"Helix: $|h|\leq 15$")

    ax.plot(dense_n, real_input(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.2, ls="--", alpha=0.26, zorder=3)
    ax.plot(dense_n, nonlinear_output(dense_n), np.zeros_like(dense_n), color=REFERENCE_GREY, lw=1.8, alpha=0.46, zorder=5)
    for index, harmonic in enumerate(harmonics):
        positive = component_signal(harmonic, dense_n)
        negative = component_signal(-harmonic, dense_n)
        ax.plot(dense_n, positive.real, positive.imag, color=PAIR_COLORS[index], lw=1.15, ls=":", alpha=0.72, zorder=6 + index)
        ax.plot(dense_n, negative.real, negative.imag, color=PAIR_COLORS[index], lw=1.15, ls="--", alpha=0.52, zorder=6 + index)
    ax.plot(dense_n, approximation_dense, np.zeros_like(dense_n), color=OUTPUT_BLUE, lw=2.2, alpha=0.92, zorder=18)

    current_stem = Line3D([], [], [], color=OUTPUT_BLUE, lw=2.3, alpha=0.95, zorder=24)
    ax.add_line(current_stem)
    current_point, = ax.plot([], [], [], "o", color=OUTPUT_BLUE, ms=7.0, zorder=25, clip_on=False)
    exact_point, = ax.plot([], [], [], "o", color=REFERENCE_GREY, ms=5.0, alpha=0.80, zorder=23, clip_on=False)
    component_points = [
        ax.plot([], [], [], "o", color=PAIR_COLORS[index], ms=4.0, alpha=0.86, zorder=22, clip_on=False)[0]
        for index, _harmonic in enumerate(harmonics)
    ]
    time_text = ax.text2D(
        0.035,
        0.945,
        "",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.24", facecolor="white", edgecolor="0.82", alpha=0.94),
    )

    def draw_state(frame_index: int):
        n_value = frame_n[frame_index]
        current_value = component_sum(harmonics, n_value)
        exact_value = nonlinear_output(n_value)
        current_stem.set_data_3d([n_value, n_value], [0.0, current_value], [0.0, 0.0])
        current_point.set_data_3d([n_value], [current_value], [0.0])
        exact_point.set_data_3d([n_value], [exact_value], [0.0])
        for point, harmonic in zip(component_points, harmonics):
            value = pair_signal(harmonic, n_value)
            point.set_data_3d([n_value], [value], [0.0])
        time_text.set_text(f"n = {int(np.floor(n_value + 1e-9))}")
        return (current_stem, current_point, exact_point, *component_points, time_text)

    draw_state(0)
    preview_path = animation_dir / "11_rotating_real_cos_helix_preview.png"
    gif_path = animation_dir / "12_rotating_real_cos_helix_motion.gif"
    save_reference_helix_png(fig, preview_path)

    animation = FuncAnimation(fig, draw_state, frames=len(frame_n), interval=1000 / ANIMATION_FPS, blit=False)
    temp_gif_path = animation_dir / "__tmp_rotating_real_cos_helix_motion.gif"
    animation.save(temp_gif_path, writer=PillowWriter(fps=ANIMATION_FPS))
    save_reference_helix_gif(temp_gif_path, gif_path)
    temp_gif_path.unlink(missing_ok=True)
    plt.close(fig)
    return [preview_path, gif_path]


def export_rotating_sequence_animation() -> list[Path]:
    harmonics = POSITIVE_HARMONICS
    animation_dir = OUTPUT_DIR / "sequence_animation"
    animation_dir.mkdir(parents=True, exist_ok=True)

    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    frame_n = np.linspace(CURRENT_N, CURRENT_N + ANIMATION_END_N, ANIMATION_FRAMES)
    approximation_dense = component_sum(harmonics, dense_n)

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE, dpi=TIME_DPI, facecolor="white")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    setup_sequence_axis(ax, r"Sequence: $|h|\leq 15$")
    ax.plot(dense_n, real_input(dense_n), color=SIGNAL_BLACK, lw=1.2, ls="--", alpha=0.26, zorder=3)
    ax.plot(dense_n, nonlinear_output(dense_n), color=REFERENCE_GREY, lw=1.8, alpha=0.46, zorder=5)
    ax.plot(dense_n, approximation_dense, color=OUTPUT_BLUE, lw=2.2, ls="--", alpha=0.92, zorder=9)

    current_line = ax.axvline(CURRENT_N, color=OUTPUT_BLUE, lw=1.7, alpha=0.75, zorder=14)
    current_point, = ax.plot([], [], "o", color=OUTPUT_BLUE, ms=7.0, zorder=16)
    exact_point, = ax.plot([], [], "o", color=REFERENCE_GREY, ms=5.0, alpha=0.80, zorder=15)
    time_text = ax.text(
        0.035,
        0.945,
        "",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.24", facecolor="white", edgecolor="0.82", alpha=0.94),
        zorder=20,
    )

    def draw_state(frame_index: int):
        n_value = frame_n[frame_index]
        current_value = component_sum(harmonics, n_value)
        exact_value = nonlinear_output(n_value)
        current_line.set_xdata([n_value, n_value])
        current_point.set_data([n_value], [current_value])
        exact_point.set_data([n_value], [exact_value])
        time_text.set_text(f"n = {int(np.floor(n_value + 1e-9))}")
        return current_line, current_point, exact_point, time_text

    draw_state(0)
    preview_path = animation_dir / "13_rotating_real_cos_sequence_preview.png"
    gif_path = animation_dir / "14_rotating_real_cos_sequence_motion.gif"
    fig.savefig(preview_path, dpi=TIME_DPI, facecolor="white")

    animation = FuncAnimation(fig, draw_state, frames=len(frame_n), interval=1000 / ANIMATION_FPS, blit=False)
    animation.save(gif_path, writer=PillowWriter(fps=ANIMATION_FPS))
    plt.close(fig)
    return [preview_path, gif_path]


def main() -> None:
    clear_output_dir()
    pages = [
        dict(
            filename="01_clipped_real_cos_reference.png",
            title="output",
            included_harmonics=[],
            show_sum=False,
            show_output_only=True,
        )
    ]
    stage_counts = [1, 2, 3, 4, len(POSITIVE_HARMONICS)]
    for page_number, stage_index in enumerate(stage_counts, start=2):
        stage_harmonics = POSITIVE_HARMONICS[:stage_index]
        last_harmonic = stage_harmonics[-1]
        if stage_index == 1:
            title = r"$h=\pm1$"
            stem = f"{page_number:02d}_partial_sum_to_h01"
        else:
            title = rf"$|h|\leq {last_harmonic}$"
            stem = f"{page_number:02d}_partial_sum_to_h{last_harmonic:02d}"
        pages.append(
            dict(
                filename=f"{stem}.png",
                title=title,
                included_harmonics=stage_harmonics,
                show_sum=True,
            )
        )

    paths: list[Path] = []
    for page in pages:
        base_name = page["filename"].replace(".png", "")
        title = page["title"]
        page_kwargs = {key: value for key, value in page.items() if key not in {"filename", "title"}}
        paths.extend(export_reference_layout_page(**page_kwargs, base_name=base_name, title=title))
        paths.append(
            export_phasor_page(
                **page_kwargs,
                filename=f"{base_name}_phasor_zoom.png",
                title=f"Zoom: {title}",
                zoom=True,
            )
        )
        paths.append(export_sequence_page(**page_kwargs, filename=f"{base_name}_sequence.png", title=f"Sequence: {title}"))

    for subdir in ("phasor", "phasor_zoom", "helix", "sequence"):
        normalize_subdir_images(OUTPUT_DIR / subdir)

    paths.extend(export_rotating_phasor_animation())
    paths.extend(export_rotating_helix_animation())
    paths.extend(export_rotating_sequence_animation())

    for path in paths:
        print(path.relative_to(LECTURE_DIR))


if __name__ == "__main__":
    main()
