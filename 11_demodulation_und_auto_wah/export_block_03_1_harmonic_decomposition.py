from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.ticker import MultipleLocator
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
    / "03B_harmonic_decomposition"
)

PHASOR_FIGSIZE = (6.9, 6.9)
REFERENCE_PHASOR_FIGSIZE = (6.5, 6.3)
REFERENCE_HELIX_FIGSIZE = (9.47, 6.3)
HELIX_FIGSIZE = REFERENCE_HELIX_FIGSIZE
FIG_DPI = 100
ANIMATION_FPS = 24
ANIMATION_FRAMES = 384
ANIMATION_END_N = 8.0

SIGNAL_BLACK = "0.10"
OUTPUT_BLUE = "#2b7bbb"
COMPONENT_COLORS = [
    "#0b6b3a",
    "#1b7f4a",
    "#2ca25f",
    "#49b65f",
    "#66bd63",
    "#8acb63",
    "#a6d96a",
    "#c7e77f",
]
REFERENCE_GREY = "0.64"
LIGHT_GREY = "0.86"
CLIP_ORANGE = "#d98c2f"

TITLE_SIZE = 19
LABEL_SIZE = 20
TICK_SIZE = 16

NUM_SAMPLES = 24
OMEGA = np.pi / 4.0
OMEGA_LABEL = r"\pi/4"
DELAY_SAMPLES = 1
CLIP_THRESHOLD = 0.75
HARMONIC_INDICES = [1, -3, 5, -7, 9, -11, 13, -15]
CURRENT_N = 5.35
ZOOM_XLIM = (-0.96, -0.54)
ZOOM_YLIM = (-0.43, -0.08)
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


def delayed_signal(n_values: np.ndarray | float) -> np.ndarray | complex:
    return np.exp(1j * theta_from_n(n_values))


def hard_clip_complex(values: np.ndarray | complex) -> np.ndarray | complex:
    return np.clip(np.real(values), -CLIP_THRESHOLD, CLIP_THRESHOLD) + 1j * np.clip(
        np.imag(values),
        -CLIP_THRESHOLD,
        CLIP_THRESHOLD,
    )


def nonlinear_output(n_values: np.ndarray | float) -> np.ndarray | complex:
    return hard_clip_complex(delayed_signal(n_values))


def clipped_unit_circle(theta_values: np.ndarray) -> np.ndarray:
    return np.clip(np.cos(theta_values), -CLIP_THRESHOLD, CLIP_THRESHOLD) + 1j * np.clip(
        np.sin(theta_values),
        -CLIP_THRESHOLD,
        CLIP_THRESHOLD,
    )


def compute_fourier_coefficients(max_harmonic: int = 17) -> dict[int, complex]:
    theta_values = np.linspace(0.0, 2 * np.pi, 200_000, endpoint=False)
    values = clipped_unit_circle(theta_values)
    coefficients: dict[int, complex] = {}
    for harmonic in range(-max_harmonic, max_harmonic + 1):
        coefficients[harmonic] = np.mean(values * np.exp(-1j * harmonic * theta_values))
    return coefficients


COEFFS = compute_fourier_coefficients()


def component_signal(harmonic: int, n_values: np.ndarray | float) -> np.ndarray | complex:
    return COEFFS[harmonic] * np.exp(1j * harmonic * theta_from_n(n_values))


def component_sum(harmonics: list[int], n_values: np.ndarray | float) -> np.ndarray | complex:
    result = np.zeros_like(np.asarray(n_values, dtype=float), dtype=complex)
    for harmonic in harmonics:
        result = result + component_signal(harmonic, n_values)
    if np.isscalar(n_values):
        return complex(result)
    return result


def component_chain(harmonics: list[int], n_value: float) -> tuple[list[tuple[complex, complex]], complex]:
    current_sum = 0.0 + 0.0j
    segments: list[tuple[complex, complex]] = []
    for harmonic in harmonics:
        next_sum = current_sum + component_signal(harmonic, n_value)
        segments.append((current_sum, next_sum))
        current_sum = next_sum
    return segments, current_sum


def zoom_limits(center: complex) -> tuple[tuple[float, float], tuple[float, float]]:
    width = ZOOM_XLIM[1] - ZOOM_XLIM[0]
    height = ZOOM_YLIM[1] - ZOOM_YLIM[0]
    return (
        (center.real - width / 2, center.real + width / 2),
        (center.imag - height / 2, center.imag + height / 2),
    )


def draw_phasor_clip_guides(ax) -> None:
    for threshold in (-CLIP_THRESHOLD, CLIP_THRESHOLD):
        ax.axvline(threshold, color=CLIP_ORANGE, lw=1.2, ls=":", alpha=0.60, zorder=2)
        ax.axhline(threshold, color=CLIP_ORANGE, lw=1.2, ls=":", alpha=0.60, zorder=2)


def setup_phasor_axis(ax, title: str, *, zoom: bool = False) -> None:
    angle = np.linspace(0.0, 2 * np.pi, 721)
    ax.plot(np.cos(angle), np.sin(angle), color="0.82", lw=2.2, zorder=1)
    ax.axhline(0.0, color="0.75", lw=0.9, zorder=0)
    ax.axvline(0.0, color="0.75", lw=0.9, zorder=0)
    draw_phasor_clip_guides(ax)
    if zoom:
        ax.set_xlim(*ZOOM_XLIM)
        ax.set_ylim(*ZOOM_YLIM)
    else:
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$\mathrm{Re}\{\cdot\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$\mathrm{Im}\{\cdot\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(0.5 if not zoom else 0.1))
    ax.yaxis.set_major_locator(MultipleLocator(0.5 if not zoom else 0.1))
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


def draw_arrow(
    ax,
    start: complex,
    end: complex,
    color: str,
    label: str | None = None,
    alpha: float = 1.0,
    linewidth: float = 2.2,
    head_width: float = 0.035,
    head_length: float = 0.055,
):
    delta = end - start
    ax.arrow(
        start.real,
        start.imag,
        delta.real,
        delta.imag,
        length_includes_head=True,
        head_width=head_width,
        head_length=head_length,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        zorder=12,
        label=label,
    )


def draw_component_vectors(ax, harmonics: list[int], *, zoom: bool = False, label_vectors: bool = True) -> complex:
    current_sum = 0.0 + 0.0j
    linewidth = 1.05 if zoom else 2.2
    head_width = 0.006 if zoom else 0.035
    head_length = 0.010 if zoom else 0.055
    for index, harmonic in enumerate(harmonics):
        value = component_signal(harmonic, CURRENT_N)
        next_sum = current_sum + value
        draw_arrow(
            ax,
            current_sum,
            next_sum,
            COMPONENT_COLORS[index],
            rf"$h={harmonic}$" if label_vectors else None,
            alpha=0.95,
            linewidth=linewidth,
            head_width=head_width,
            head_length=head_length,
        )
        current_sum = next_sum
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
    y_nl_current = nonlinear_output(CURRENT_N)
    delayed_dense = delayed_signal(dense_n)

    fig_size = PHASOR_FIGSIZE if zoom else REFERENCE_PHASOR_FIGSIZE
    fig, ax_phasor = plt.subplots(figsize=fig_size, dpi=FIG_DPI, facecolor="white")
    if zoom:
        fig.subplots_adjust(left=0.15, right=0.98, top=0.90, bottom=0.13)
    else:
        fig.subplots_adjust(left=0.17, right=0.938, top=0.918, bottom=0.13)
    setup_phasor_axis(ax_phasor, title, zoom=zoom)

    ax_phasor.plot(
        delayed_dense.real,
        delayed_dense.imag,
        color=REFERENCE_GREY,
        lw=1.4,
        ls="--",
        alpha=0.45,
        label=r"$x[n-1]$",
        zorder=3,
    )
    ax_phasor.plot(
        y_nl_dense.real,
        y_nl_dense.imag,
        color=REFERENCE_GREY if not show_output_only else OUTPUT_BLUE,
        lw=2.2,
        alpha=0.70 if not show_output_only else 0.95,
        label=r"$y_\mathrm{NL}[n]$",
        zorder=5,
    )
    ax_phasor.plot([y_nl_current.real], [y_nl_current.imag], "o", color=OUTPUT_BLUE, ms=7, zorder=13)
    if not zoom:
        ax_phasor.add_patch(
            Rectangle(
                (ZOOM_XLIM[0], ZOOM_YLIM[0]),
                ZOOM_XLIM[1] - ZOOM_XLIM[0],
                ZOOM_YLIM[1] - ZOOM_YLIM[0],
                fill=False,
                edgecolor=OUTPUT_BLUE,
                linewidth=1.6,
                linestyle="-",
                alpha=0.78,
                zorder=16,
            )
        )

    if included_harmonics:
        approximation_dense = component_sum(included_harmonics, dense_n)
        ax_phasor.plot(
            approximation_dense.real,
            approximation_dense.imag,
            color=OUTPUT_BLUE,
            lw=1.6 if not zoom else 1.2,
            ls="--" if zoom else "-",
            alpha=0.88,
            zorder=9,
            label="partial sum" if not zoom else None,
        )
        phasor_sum = draw_component_vectors(
            ax_phasor,
            included_harmonics,
            zoom=zoom,
            label_vectors=(len(included_harmonics) <= 4),
        )
        ax_phasor.plot([phasor_sum.real], [phasor_sum.imag], "o", color=OUTPUT_BLUE, ms=7, zorder=14)

        if show_sum:
            approximation_current = component_sum(included_harmonics, CURRENT_N)
            sum_linewidth = 1.15 if zoom else 2.5
            sum_head_width = 0.007 if zoom else 0.04
            sum_head_length = 0.012 if zoom else 0.065
            ax_phasor.arrow(
                0.0,
                0.0,
                approximation_current.real,
                approximation_current.imag,
                length_includes_head=True,
                head_width=sum_head_width,
                head_length=sum_head_length,
                linewidth=sum_linewidth,
                color=OUTPUT_BLUE,
                alpha=0.95,
                zorder=15,
                label=None,
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
    y_nl_dense = nonlinear_output(dense_n)
    delayed_dense = delayed_signal(dense_n)

    fig = plt.figure(figsize=HELIX_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    ax_helix = fig.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.015, right=0.985, top=0.90, bottom=0.04)
    ax_helix.set_position([-0.11, 0.025, 1.12, 0.950])
    setup_helix_axis(ax_helix, title)

    ax_helix.plot(
        dense_n,
        delayed_dense.real,
        delayed_dense.imag,
        color=REFERENCE_GREY,
        lw=1.3,
        ls="--",
        alpha=0.34,
        zorder=3,
    )
    ax_helix.plot(
        dense_n,
        y_nl_dense.real,
        y_nl_dense.imag,
        color=REFERENCE_GREY if not show_output_only else OUTPUT_BLUE,
        lw=2.2,
        alpha=0.68 if not show_output_only else 0.96,
        zorder=6,
    )

    if included_harmonics:
        for index, harmonic in enumerate(included_harmonics):
            values = component_signal(harmonic, dense_n)
            ax_helix.plot(
                dense_n,
                values.real,
                values.imag,
                color=COMPONENT_COLORS[index],
                lw=1.7,
                ls=":",
                alpha=0.90,
                zorder=8 + index,
            )

        if show_sum:
            approximation = component_sum(included_harmonics, dense_n)
            ax_helix.plot(
                dense_n,
                approximation.real,
                approximation.imag,
                color=OUTPUT_BLUE,
                lw=2.4,
                alpha=0.94,
                zorder=18,
            )

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
    y_nl_current = nonlinear_output(CURRENT_N)
    delayed_dense = delayed_signal(dense_n)

    phasor_path = OUTPUT_DIR / "phasor" / f"{base_name}_phasor.png"
    helix_path = OUTPUT_DIR / "helix" / f"{base_name}_helix.png"
    fig, ax_phasor, ax_helix = create_reference_layout_axes(f"Phasor: {title}", f"Helix: {title}")

    ax_phasor.plot(
        delayed_dense.real,
        delayed_dense.imag,
        color=REFERENCE_GREY,
        lw=1.4,
        ls="--",
        alpha=0.45,
        zorder=3,
    )
    ax_phasor.plot(
        y_nl_dense.real,
        y_nl_dense.imag,
        color=REFERENCE_GREY if not show_output_only else OUTPUT_BLUE,
        lw=2.2,
        alpha=0.70 if not show_output_only else 0.95,
        zorder=5,
    )
    ax_phasor.plot([y_nl_current.real], [y_nl_current.imag], "o", color=OUTPUT_BLUE, ms=7, zorder=13)
    ax_phasor.add_patch(
        Rectangle(
            (ZOOM_XLIM[0], ZOOM_YLIM[0]),
            ZOOM_XLIM[1] - ZOOM_XLIM[0],
            ZOOM_YLIM[1] - ZOOM_YLIM[0],
            fill=False,
            edgecolor=OUTPUT_BLUE,
            linewidth=1.6,
            linestyle="-",
            alpha=0.78,
            zorder=16,
        )
    )

    ax_helix.plot(
        dense_n,
        delayed_dense.real,
        delayed_dense.imag,
        color=REFERENCE_GREY,
        lw=1.3,
        ls="--",
        alpha=0.34,
        zorder=3,
    )
    ax_helix.plot(
        dense_n,
        y_nl_dense.real,
        y_nl_dense.imag,
        color=REFERENCE_GREY if not show_output_only else OUTPUT_BLUE,
        lw=2.2,
        alpha=0.68 if not show_output_only else 0.96,
        zorder=6,
    )

    if included_harmonics:
        approximation_dense = component_sum(included_harmonics, dense_n)
        ax_phasor.plot(
            approximation_dense.real,
            approximation_dense.imag,
            color=OUTPUT_BLUE,
            lw=1.6,
            ls="-",
            alpha=0.88,
            zorder=9,
        )
        phasor_sum = draw_component_vectors(
            ax_phasor,
            included_harmonics,
            zoom=False,
            label_vectors=(len(included_harmonics) <= 4),
        )
        ax_phasor.plot([phasor_sum.real], [phasor_sum.imag], "o", color=OUTPUT_BLUE, ms=7, zorder=14)

        if show_sum:
            approximation_current = component_sum(included_harmonics, CURRENT_N)
            ax_phasor.arrow(
                0.0,
                0.0,
                approximation_current.real,
                approximation_current.imag,
                length_includes_head=True,
                head_width=0.04,
                head_length=0.065,
                linewidth=2.5,
                color=OUTPUT_BLUE,
                alpha=0.95,
                zorder=15,
            )
            ax_helix.plot(
                dense_n,
                approximation_dense.real,
                approximation_dense.imag,
                color=OUTPUT_BLUE,
                lw=2.4,
                alpha=0.94,
                zorder=18,
            )

        for index, harmonic in enumerate(included_harmonics):
            values = component_signal(harmonic, dense_n)
            ax_helix.plot(
                dense_n,
                values.real,
                values.imag,
                color=COMPONENT_COLORS[index],
                lw=1.7,
                ls=":",
                alpha=0.90,
                zorder=8 + index,
            )

    save_reference_split_png(fig, phasor_path, helix_path)
    plt.close(fig)
    return [phasor_path, helix_path]


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


def make_vector_patch(color: str, *, zoom: bool = False, label: str | None = None) -> FancyArrowPatch:
    return FancyArrowPatch(
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


def update_vector_patch(patch: FancyArrowPatch, start: complex, end: complex) -> None:
    patch.set_positions((start.real, start.imag), (end.real, end.imag))


def export_rotating_phasor_animation() -> list[Path]:
    harmonics = HARMONIC_INDICES
    animation_dir = OUTPUT_DIR / "phasor_animation"
    animation_dir.mkdir(parents=True, exist_ok=True)

    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    y_nl_dense = nonlinear_output(dense_n)
    delayed_dense = delayed_signal(dense_n)
    approximation_dense = component_sum(harmonics, dense_n)
    frame_n = np.linspace(CURRENT_N, CURRENT_N + ANIMATION_END_N, ANIMATION_FRAMES)

    def setup_animation_axis(ax, title: str, *, zoom: bool = False) -> None:
        setup_phasor_axis(ax, title, zoom=False)
        if zoom:
            ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
            ax.xaxis.set_major_locator(MultipleLocator(0.1))
            ax.yaxis.set_major_locator(MultipleLocator(0.1))
        ax.plot(
            delayed_dense.real,
            delayed_dense.imag,
            color=REFERENCE_GREY,
            lw=1.2,
            ls="--",
            alpha=0.35,
            zorder=3,
            label=r"$x[n-1]$",
        )
        ax.plot(
            y_nl_dense.real,
            y_nl_dense.imag,
            color=REFERENCE_GREY,
            lw=1.9,
            alpha=0.52,
            zorder=4,
            label=r"$y_\mathrm{NL}[n]$",
        )
        ax.plot(
            approximation_dense.real,
            approximation_dense.imag,
            color=OUTPUT_BLUE,
            lw=1.7 if not zoom else 1.25,
            ls="--" if zoom else "-",
            alpha=0.88,
            zorder=7,
            label="partial sum",
        )

    main_fig, main_ax = plt.subplots(figsize=REFERENCE_PHASOR_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    main_fig.subplots_adjust(left=0.17, right=0.939, top=0.919, bottom=0.13)
    setup_animation_axis(main_ax, r"Phasor: $|h|\leq 15$")

    main_vectors = [
        make_vector_patch(COMPONENT_COLORS[index], label=rf"$h={harmonic}$")
        for index, harmonic in enumerate(harmonics)
    ]
    for patch in main_vectors:
        main_ax.add_patch(patch)

    main_sum_vector = make_vector_patch(OUTPUT_BLUE, label=r"$\sum c_h e^{jh\Omega n}$")
    main_sum_vector.set_linewidth(2.5)
    main_sum_vector.set_mutation_scale(15)
    main_ax.add_patch(main_sum_vector)
    main_sum_point, = main_ax.plot([], [], "o", color=OUTPUT_BLUE, ms=6.5, zorder=16)
    zoom_rect = Rectangle((0, 0), 0.1, 0.1, fill=False, edgecolor=OUTPUT_BLUE, linewidth=1.5, zorder=18)
    main_ax.add_patch(zoom_rect)
    main_time_text = main_ax.text(
        0.035,
        0.955,
        "",
        transform=main_ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.24", facecolor="white", edgecolor="0.82", alpha=0.94),
        zorder=20,
    )
    zoom_fig, zoom_ax = plt.subplots(figsize=PHASOR_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    zoom_fig.subplots_adjust(left=0.15, right=0.98, top=0.90, bottom=0.13)
    setup_animation_axis(zoom_ax, r"Zoom: $|h|\leq 15$", zoom=True)

    zoom_vectors = [
        make_vector_patch(COMPONENT_COLORS[index], zoom=False)
        for index, _harmonic in enumerate(harmonics)
    ]
    for patch in zoom_vectors:
        zoom_ax.add_patch(patch)
    zoom_sum_vector = make_vector_patch(OUTPUT_BLUE, zoom=False)
    zoom_sum_vector.set_visible(False)
    zoom_ax.add_patch(zoom_sum_vector)
    zoom_sum_point, = zoom_ax.plot([], [], "o", color=OUTPUT_BLUE, ms=6.5, zorder=16)
    zoom_time_text = zoom_ax.text(
        0.035,
        0.955,
        "",
        transform=zoom_ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.24", facecolor="white", edgecolor="0.82", alpha=0.94),
        zorder=20,
    )

    def draw_state(frame_index: int):
        n_value = frame_n[frame_index]
        segments, current_sum = component_chain(harmonics, n_value)
        xlim, ylim = zoom_limits(current_sum)

        for patch, (start, end) in zip(main_vectors, segments):
            update_vector_patch(patch, start, end)
        update_vector_patch(main_sum_vector, 0.0 + 0.0j, current_sum)
        main_sum_point.set_data([current_sum.real], [current_sum.imag])
        zoom_rect.set_xy((xlim[0], ylim[0]))
        zoom_rect.set_width(xlim[1] - xlim[0])
        zoom_rect.set_height(ylim[1] - ylim[0])
        main_time_text.set_text(f"n = {int(np.floor(n_value + 1e-9))}")

        for patch, (start, end) in zip(zoom_vectors, segments):
            update_vector_patch(patch, start, end)
        update_vector_patch(zoom_sum_vector, 0.0 + 0.0j, current_sum)
        zoom_sum_point.set_data([current_sum.real], [current_sum.imag])
        zoom_ax.set_xlim(*xlim)
        zoom_ax.set_ylim(*ylim)
        zoom_time_text.set_text(f"n = {int(np.floor(n_value + 1e-9))}")

        return (
            *main_vectors,
            main_sum_vector,
            main_sum_point,
            zoom_rect,
            main_time_text,
            *zoom_vectors,
            zoom_sum_vector,
            zoom_sum_point,
            zoom_time_text,
        )

    draw_state(0)
    main_preview = animation_dir / "07_rotating_harmonic_phasors_preview.png"
    zoom_preview = animation_dir / "09_rotating_harmonic_phasors_zoom_preview.png"
    main_fig.savefig(main_preview, dpi=FIG_DPI, facecolor="white")
    zoom_fig.savefig(zoom_preview, dpi=FIG_DPI, facecolor="white", bbox_inches="tight", pad_inches=0.06)

    main_animation = FuncAnimation(
        main_fig,
        draw_state,
        frames=len(frame_n),
        interval=1000 / ANIMATION_FPS,
        blit=False,
    )
    zoom_animation = FuncAnimation(
        zoom_fig,
        draw_state,
        frames=len(frame_n),
        interval=1000 / ANIMATION_FPS,
        blit=False,
    )
    main_gif = animation_dir / "08_rotating_harmonic_phasors_motion.gif"
    zoom_gif = animation_dir / "10_rotating_harmonic_phasors_zoom_motion.gif"
    main_animation.save(main_gif, writer=PillowWriter(fps=ANIMATION_FPS))
    zoom_animation.save(zoom_gif, writer=PillowWriter(fps=ANIMATION_FPS))
    plt.close(main_fig)
    plt.close(zoom_fig)
    return [main_preview, main_gif, zoom_preview, zoom_gif]


def export_rotating_helix_animation() -> list[Path]:
    harmonics = HARMONIC_INDICES
    animation_dir = OUTPUT_DIR / "helix_animation"
    animation_dir.mkdir(parents=True, exist_ok=True)

    dense_n = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 200 + 1)
    frame_n = np.linspace(CURRENT_N, CURRENT_N + ANIMATION_END_N, ANIMATION_FRAMES)
    y_nl_dense = nonlinear_output(dense_n)
    delayed_dense = delayed_signal(dense_n)
    approximation_dense = component_sum(harmonics, dense_n)

    fig, _ax_phasor, ax = create_reference_layout_axes(r"Phasor: $|h|\leq 15$", r"Helix: $|h|\leq 15$")

    ax.plot(
        dense_n,
        delayed_dense.real,
        delayed_dense.imag,
        color=REFERENCE_GREY,
        lw=1.2,
        ls="--",
        alpha=0.26,
        zorder=3,
    )
    ax.plot(
        dense_n,
        y_nl_dense.real,
        y_nl_dense.imag,
        color=REFERENCE_GREY,
        lw=1.8,
        alpha=0.46,
        zorder=5,
    )
    for index, harmonic in enumerate(harmonics):
        values = component_signal(harmonic, dense_n)
        ax.plot(
            dense_n,
            values.real,
            values.imag,
            color=COMPONENT_COLORS[index],
            lw=1.25,
            ls=":",
            alpha=0.72,
            zorder=6 + index,
        )
    ax.plot(
        dense_n,
        approximation_dense.real,
        approximation_dense.imag,
        color=OUTPUT_BLUE,
        lw=2.2,
        alpha=0.92,
        zorder=18,
    )

    current_stem, = ax.plot([], [], [], color=OUTPUT_BLUE, lw=2.3, alpha=0.95, zorder=24, clip_on=False)
    current_point, = ax.plot([], [], [], "o", color=OUTPUT_BLUE, ms=7.0, zorder=25, clip_on=False)
    exact_point, = ax.plot([], [], [], "o", color=REFERENCE_GREY, ms=5.0, alpha=0.80, zorder=23, clip_on=False)
    component_points = [
        ax.plot([], [], [], "o", color=COMPONENT_COLORS[index], ms=4.2, alpha=0.90, zorder=22, clip_on=False)[0]
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
        current_stem.set_data_3d([n_value, n_value], [0.0, current_value.real], [0.0, current_value.imag])
        current_point.set_data_3d([n_value], [current_value.real], [current_value.imag])
        exact_point.set_data_3d([n_value], [exact_value.real], [exact_value.imag])
        for point, harmonic in zip(component_points, harmonics):
            component_value = component_signal(harmonic, n_value)
            point.set_data_3d([n_value], [component_value.real], [component_value.imag])
        time_text.set_text(f"n = {int(np.floor(n_value + 1e-9))}")
        return (current_stem, current_point, exact_point, *component_points, time_text)

    draw_state(0)
    preview_path = animation_dir / "11_rotating_harmonic_helix_preview.png"
    gif_path = animation_dir / "12_rotating_harmonic_helix_motion.gif"
    save_reference_helix_png(fig, preview_path)

    animation = FuncAnimation(
        fig,
        draw_state,
        frames=len(frame_n),
        interval=1000 / ANIMATION_FPS,
        blit=False,
    )
    temp_gif_path = animation_dir / "__tmp_rotating_harmonic_helix_motion.gif"
    animation.save(temp_gif_path, writer=PillowWriter(fps=ANIMATION_FPS))
    save_reference_helix_gif(temp_gif_path, gif_path)
    temp_gif_path.unlink(missing_ok=True)
    plt.close(fig)
    return [preview_path, gif_path]


def main() -> None:
    clear_output_dir()
    pages = [
        dict(
            filename="01_clipped_output_reference.png",
            title="output",
            included_harmonics=[],
            show_sum=False,
            show_output_only=True,
        )
    ]
    stage_counts = [1, 2, 3, 4, len(HARMONIC_INDICES)]
    for page_number, stage_index in enumerate(stage_counts, start=2):
        stage_harmonics = HARMONIC_INDICES[:stage_index]
        last_harmonic = abs(stage_harmonics[-1])
        if stage_index == 1:
            title = r"$h=1$"
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
        phasor_title = f"Phasor: {title}"
        zoom_title = f"Zoom: {title}"
        page_kwargs = {key: value for key, value in page.items() if key not in {"filename", "title"}}
        paths.extend(export_reference_layout_page(**page_kwargs, base_name=base_name, title=title))
        paths.append(export_phasor_page(**page_kwargs, filename=f"{base_name}_phasor_zoom.png", title=zoom_title, zoom=True))
    for subdir in ("phasor", "phasor_zoom", "helix"):
        normalize_subdir_images(OUTPUT_DIR / subdir)
    paths.extend(export_rotating_phasor_animation())
    paths.extend(export_rotating_helix_animation())
    for path in paths:
        print(path.relative_to(LECTURE_DIR))


if __name__ == "__main__":
    main()
