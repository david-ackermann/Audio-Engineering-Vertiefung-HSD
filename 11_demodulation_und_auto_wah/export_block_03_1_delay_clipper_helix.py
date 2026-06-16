from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import MultipleLocator
from PIL import Image, ImageChops, ImageSequence


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "03_nonlinear_processing_intro"
    / "03A_delay_clipper_helix"
)

FPS = 12
FRAMES_PER_SAMPLE = 4
FIGSIZE = (17.2, 6.9)
PHASOR_FIGSIZE = (7.6, 7.6)
FIG_DPI = 100
SUBPLOT_SPLIT_X = 650
REFERENCE_EXPORT_SIZE = (1597, 630)

SIGNAL_BLACK = "0.10"
OUTPUT_BLUE = "#2b7bbb"
SYSTEM_GREEN = "#26a043"
CLIP_ORANGE = "#d98c2f"
REFERENCE_GREY = "0.64"
LIGHT_GREY = "0.84"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"

TITLE_SIZE = 19
LABEL_SIZE = 20
TICK_SIZE = 16
INFO_TEXT_SIZE = 16

NUM_SAMPLES = 24
OMEGA = np.pi / 4.0
OMEGA_LABEL = r"\pi/4"
DELAY_SAMPLES = 1
CLIP_THRESHOLD = 0.75
HELIX_BOX_ASPECT = (3.9, 1.55, 1.55)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_file in OUTPUT_DIR.glob("*.png"):
        output_file.unlink()
    for output_file in OUTPUT_DIR.glob("*.gif"):
        output_file.unlink()


def image_content_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    rgb_image = image.convert("RGB")
    background = Image.new("RGB", rgb_image.size, (255, 255, 255))
    diff = ImageChops.difference(rgb_image, background)
    diff = diff.convert("L").point(lambda value: 255 if value > 12 else 0)
    return diff.getbbox()


def expand_bbox(
    bbox: tuple[int, int, int, int],
    image_size: tuple[int, int],
    padding_px: int,
) -> tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    width, height = image_size
    return (
        max(0, left - padding_px),
        max(0, top - padding_px),
        min(width, right + padding_px),
        min(height, bottom + padding_px),
    )


def union_bbox(
    first: tuple[int, int, int, int] | None,
    second: tuple[int, int, int, int] | None,
) -> tuple[int, int, int, int] | None:
    if first is None:
        return second
    if second is None:
        return first
    return (
        min(first[0], second[0]),
        min(first[1], second[1]),
        max(first[2], second[2]),
        max(first[3], second[3]),
    )


def crop_png_margins(path: Path, padding_px: int = 12) -> None:
    image = Image.open(path).convert("RGB")
    bbox = image_content_bbox(image)
    if bbox is None:
        return
    image.crop(expand_bbox(bbox, image.size, padding_px)).save(path)


def crop_gif_margins(path: Path, padding_px: int = 12) -> None:
    image = Image.open(path)
    frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(image)]
    if not frames:
        return
    bbox = None
    for frame in frames:
        bbox = union_bbox(bbox, image_content_bbox(frame))
    if bbox is None:
        return
    crop_box = expand_bbox(bbox, frames[0].size, padding_px)
    durations = [frame.info.get("duration", image.info.get("duration", round(1000 / FPS))) for frame in ImageSequence.Iterator(image)]
    cropped_frames = [frame.crop(crop_box) for frame in frames]
    cropped_frames[0].save(
        path,
        save_all=True,
        append_images=cropped_frames[1:],
        duration=durations,
        loop=image.info.get("loop", 0),
        disposal=2,
    )


def pad_image_to_size(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    output = Image.new("RGBA", target_size, (255, 255, 255, 255))
    image = image.convert("RGBA")
    output.alpha_composite(image, ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2))
    return output


def normalize_export_group(paths: list[Path]) -> None:
    if not paths:
        return

    for path in paths:
        if path.suffix.lower() == ".png":
            crop_png_margins(path)
        elif path.suffix.lower() == ".gif":
            crop_gif_margins(path)

    sizes = []
    for path in paths:
        with Image.open(path) as image:
            sizes.append(image.size)
    target_size = (max(width for width, _ in sizes), max(height for _, height in sizes))

    for path in paths:
        with Image.open(path) as image:
            if image.size == target_size:
                continue
            if path.suffix.lower() == ".gif":
                frames = []
                durations = []
                loop = image.info.get("loop", 0)
                for frame in ImageSequence.Iterator(image):
                    frames.append(pad_image_to_size(frame, target_size))
                    durations.append(frame.info.get("duration", image.info.get("duration", round(1000 / FPS))))
                frames[0].save(
                    path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=loop,
                    disposal=2,
                )
            else:
                pad_image_to_size(image, target_size).convert("RGB").save(path)


def post_process_exports() -> None:
    output_files = sorted(list(OUTPUT_DIR.glob("*.png")) + list(OUTPUT_DIR.glob("*.gif")))
    normalize_export_group([path for path in output_files if "helix" in path.name])
    normalize_export_group([path for path in output_files if "phasor" in path.name])


def input_signal(n_values: np.ndarray | float) -> np.ndarray | complex:
    return np.exp(1j * OMEGA * n_values)


def delayed_signal(n_values: np.ndarray | float) -> np.ndarray | complex:
    return np.exp(-1j * DELAY_SAMPLES * OMEGA) * input_signal(n_values)


def hard_clip_complex(values: np.ndarray | complex) -> np.ndarray | complex:
    return np.clip(np.real(values), -CLIP_THRESHOLD, CLIP_THRESHOLD) + 1j * np.clip(
        np.imag(values),
        -CLIP_THRESHOLD,
        CLIP_THRESHOLD,
    )


def nonlinear_output(n_values: np.ndarray | float) -> np.ndarray | complex:
    return hard_clip_complex(delayed_signal(n_values))


def build_stem_segments(
    n_values: np.ndarray,
    values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_segments = []
    y_segments = []
    z_segments = []
    for n_value, value in zip(n_values, values):
        x_segments.extend([n_value, n_value, np.nan])
        y_segments.extend([0.0, value.real, np.nan])
        z_segments.extend([0.0, value.imag, np.nan])
    return np.array(x_segments), np.array(y_segments), np.array(z_segments)


def setup_helix_axis(ax, *, title: str, output_math: str) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("n", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel(r"$\mathrm{Re}\{" + output_math + r"\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=12)
    ax.set_zlabel(r"$\mathrm{Im}\{" + output_math + r"\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=8)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="x", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="z", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.set_title(title, y=1.03, pad=0, fontsize=TITLE_SIZE)
    ax.view_init(elev=22, azim=-62)
    try:
        ax.set_box_aspect(HELIX_BOX_ASPECT, zoom=1.30)
    except TypeError:
        ax.set_box_aspect(HELIX_BOX_ASPECT)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))


def draw_clip_guides(ax) -> None:
    n_line = np.array([0.0, NUM_SAMPLES])
    for threshold in (-CLIP_THRESHOLD, CLIP_THRESHOLD):
        ax.plot(
            n_line,
            [threshold, threshold],
            [-1.08, -1.08],
            color=CLIP_ORANGE,
            lw=1.4,
            ls=":",
            alpha=0.55,
            zorder=3,
        )
        ax.plot(
            n_line,
            [1.08, 1.08],
            [threshold, threshold],
            color=CLIP_ORANGE,
            lw=1.4,
            ls=":",
            alpha=0.55,
            zorder=3,
        )


def create_figure(*, title: str, output_math: str) -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI, facecolor="white")
    ax = fig.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.03, right=0.93, top=0.91, bottom=0.10)
    ax.set_position([0.04, 0.10, 0.89, 0.78])
    setup_helix_axis(ax, title=title, output_math=output_math)
    return fig, ax


def setup_phasor_axis(ax, *, title: str, output_math: str) -> None:
    unit_angle = np.linspace(0.0, 2 * np.pi, 721)
    ax.plot(np.cos(unit_angle), np.sin(unit_angle), color=LIGHT_GREY, lw=1.5, zorder=1)
    ax.axhline(0.0, color=LIGHT_GREY, lw=1.0, zorder=0)
    ax.axvline(0.0, color=LIGHT_GREY, lw=1.0, zorder=0)
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.12)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$\mathrm{Re}\{" + output_math + r"\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$\mathrm{Im}\{" + output_math + r"\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="both", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.grid(True, color="0.90", lw=0.8)
    ax.set_title(title, pad=14, fontsize=22)


def draw_phasor_clip_guides(ax) -> None:
    for threshold in (-CLIP_THRESHOLD, CLIP_THRESHOLD):
        ax.axvline(threshold, color=CLIP_ORANGE, lw=1.4, ls=":", alpha=0.70, zorder=2)
        ax.axhline(threshold, color=CLIP_ORANGE, lw=1.4, ls=":", alpha=0.70, zorder=2)


def create_phasor_figure(*, title: str, output_math: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=PHASOR_FIGSIZE, dpi=FIG_DPI, facecolor="white")
    fig.subplots_adjust(left=0.15, right=0.96, top=0.88, bottom=0.14)
    setup_phasor_axis(ax, title=title, output_math=output_math)
    return fig, ax


def export_phasor_series(
    *,
    title: str,
    output_math: str,
    output_legend: str,
    output_function,
    output_color: str,
    output_formula: str,
    preview_filename: str,
    gif_filename: str,
    reference_function=None,
    reference_label: str | None = None,
    show_clip_guides: bool = False,
) -> list[Path]:
    sample_indices = np.arange(NUM_SAMPLES + 1, dtype=float)
    dense_n_full = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 160 + 1)
    output_samples = output_function(sample_indices)
    output_dense = output_function(dense_n_full)
    frame_progress = np.linspace(0.0, float(NUM_SAMPLES), NUM_SAMPLES * FRAMES_PER_SAMPLE + 1)

    fig, ax = create_phasor_figure(title=title, output_math=output_math)
    if show_clip_guides:
        draw_phasor_clip_guides(ax)

    reference_line = None
    reference_point = None
    reference_vector = None
    if reference_function is not None:
        reference_dense = reference_function(dense_n_full)
        reference_line, = ax.plot(
            reference_dense.real,
            reference_dense.imag,
            color=REFERENCE_GREY,
            lw=1.6,
            ls="--",
            alpha=0.60,
            zorder=3,
            label=reference_label,
        )
        reference_vector, = ax.plot([], [], color=REFERENCE_GREY, lw=2.0, alpha=0.58, zorder=8)
        reference_point, = ax.plot([], [], "o", color=REFERENCE_GREY, ms=6.0, alpha=0.75, zorder=9)

    ax.plot(
        output_samples.real,
        output_samples.imag,
        "o",
        color=output_color,
        alpha=0.20,
        ms=4.8,
        zorder=5,
    )
    history_line, = ax.plot([], [], color=output_color, lw=2.0, ls="--", alpha=0.85, zorder=6)
    current_vector, = ax.plot([], [], color=output_color, lw=3.0, zorder=10)
    current_point, = ax.plot([], [], "o", color=output_color, ms=8.0, zorder=11)

    info_text = ax.text(
        0.035,
        0.965,
        "",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=INFO_TEXT_SIZE,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="0.80", alpha=0.94),
    )
    legend_handles = []
    legend_labels = []
    if reference_function is not None:
        legend_handles.append(reference_line)
        legend_labels.append(reference_label or "reference")
    legend_handles.append(plt.Line2D([0], [0], color=output_color, lw=2.8))
    legend_labels.append(output_legend)
    if show_clip_guides:
        legend_handles.append(plt.Line2D([0], [0], color=CLIP_ORANGE, lw=1.8, ls=":"))
        legend_labels.append(r"$\pm T$")
    legend = ax.legend(
        legend_handles,
        legend_labels,
        loc="lower right",
        frameon=True,
        fontsize=15,
        borderpad=0.45,
        labelspacing=0.35,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.92)

    def draw_state(frame_index: int):
        current_n = frame_progress[frame_index]
        current_value = output_function(current_n)
        dense_keep = dense_n_full <= current_n + 1e-9
        dense_values = output_dense[dense_keep]

        history_line.set_data(dense_values.real, dense_values.imag)
        current_vector.set_data([0.0, current_value.real], [0.0, current_value.imag])
        current_point.set_data([current_value.real], [current_value.imag])
        info_text.set_text(f"n = {int(np.floor(current_n + 1e-9))}")

        artists = [history_line, current_vector, current_point, info_text, legend]
        if reference_function is not None:
            reference_value = reference_function(current_n)
            reference_vector.set_data([0.0, reference_value.real], [0.0, reference_value.imag])
            reference_point.set_data([reference_value.real], [reference_value.imag])
            artists.extend([reference_line, reference_vector, reference_point])
        return tuple(artists)

    draw_state(len(frame_progress) - 1)
    preview_path = OUTPUT_DIR / preview_filename
    fig.savefig(preview_path, dpi=FIG_DPI, facecolor="white")

    animation = FuncAnimation(
        fig,
        draw_state,
        frames=len(frame_progress),
        interval=1000 / FPS,
        blit=False,
    )
    gif_path = OUTPUT_DIR / gif_filename
    animation.save(gif_path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    return [preview_path, gif_path]


def export_helix_series(
    *,
    title: str,
    output_math: str,
    output_legend: str,
    output_function,
    output_color: str,
    output_formula: str,
    preview_filename: str,
    gif_filename: str,
    reference_function=None,
    reference_label: str | None = None,
    show_clip_guides: bool = False,
) -> list[Path]:
    sample_indices = np.arange(NUM_SAMPLES + 1, dtype=float)
    dense_n_full = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 160 + 1)
    output_samples = output_function(sample_indices)
    output_dense = output_function(dense_n_full)

    frame_progress = np.linspace(0.0, float(NUM_SAMPLES), NUM_SAMPLES * FRAMES_PER_SAMPLE + 1)

    fig, ax = create_figure(title=title, output_math=output_math)
    if show_clip_guides:
        draw_clip_guides(ax)

    reference_line = None
    reference_points = None
    if reference_function is not None:
        reference_dense = reference_function(dense_n_full)
        reference_samples = reference_function(sample_indices)
        reference_line, = ax.plot(
            dense_n_full,
            reference_dense.real,
            reference_dense.imag,
            color=REFERENCE_GREY,
            lw=1.6,
            ls="--",
            alpha=0.62,
            zorder=4,
            label=reference_label,
        )
        reference_points, = ax.plot(
            sample_indices,
            reference_samples.real,
            reference_samples.imag,
            "o",
            color=REFERENCE_GREY,
            alpha=0.28,
            ms=4.5,
            zorder=5,
        )

    ax.plot(
        sample_indices,
        output_samples.real,
        output_samples.imag,
        "o",
        color=output_color,
        alpha=0.18,
        ms=4.5,
        zorder=6,
    )

    sample_stems, = ax.plot([], [], [], color=output_color, lw=1.7, alpha=0.80, zorder=29, clip_on=False)
    sample_points, = ax.plot([], [], [], "o", color=output_color, ms=5.2, zorder=31, clip_on=False)
    history_line, = ax.plot([], [], [], color=output_color, lw=1.6, ls="--", zorder=30, clip_on=False)
    current_point, = ax.plot([], [], [], "o", color=output_color, ms=7.5, zorder=33, clip_on=False)
    current_stem, = ax.plot([], [], [], color=output_color, lw=2.2, alpha=0.95, zorder=32, clip_on=False)
    re_stem, = ax.plot([], [], [], color=RE_COLOR, lw=1.9, alpha=0.82, zorder=27, clip_on=False)
    im_stem, = ax.plot([], [], [], color=IM_COLOR, lw=1.9, alpha=0.82, zorder=27, clip_on=False)
    re_point, = ax.plot([], [], [], "o", color=RE_COLOR, ms=5, zorder=28, clip_on=False)
    im_point, = ax.plot([], [], [], "o", color=IM_COLOR, ms=5, zorder=28, clip_on=False)

    info_text = ax.text2D(
        0.03,
        0.93,
        "",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=INFO_TEXT_SIZE,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="0.80", alpha=0.94),
    )
    def draw_state(frame_index: int):
        current_n = frame_progress[frame_index]
        current_value = output_function(current_n)
        dense_keep = dense_n_full <= current_n + 1e-9
        dense_n = dense_n_full[dense_keep]
        dense_values = output_dense[dense_keep]
        sample_keep = sample_indices <= np.floor(current_n + 1e-9)
        past_indices = sample_indices[sample_keep]
        past_values = output_samples[sample_keep]
        stem_x, stem_y, stem_z = build_stem_segments(past_indices, past_values)

        sample_stems.set_data_3d(stem_x, stem_y, stem_z)
        sample_points.set_data_3d(past_indices, past_values.real, past_values.imag)
        history_line.set_data_3d(dense_n, dense_values.real, dense_values.imag)
        current_point.set_data_3d([current_n], [current_value.real], [current_value.imag])
        current_stem.set_data_3d([current_n, current_n], [0.0, current_value.real], [0.0, current_value.imag])
        re_stem.set_data_3d([current_n, current_n], [0.0, current_value.real], [0.0, 0.0])
        im_stem.set_data_3d([current_n, current_n], [0.0, 0.0], [0.0, current_value.imag])
        re_point.set_data_3d([current_n], [current_value.real], [0.0])
        im_point.set_data_3d([current_n], [0.0], [current_value.imag])
        info_text.set_text(f"n = {int(np.floor(current_n + 1e-9))}")

        return (
            sample_stems,
            sample_points,
            history_line,
            current_point,
            current_stem,
            re_stem,
            im_stem,
            re_point,
            im_point,
            info_text,
            reference_line,
            reference_points,
        )

    draw_state(len(frame_progress) - 1)
    preview_path = OUTPUT_DIR / preview_filename
    fig.savefig(preview_path, dpi=FIG_DPI, facecolor="white")

    animation = FuncAnimation(
        fig,
        draw_state,
        frames=len(frame_progress),
        interval=1000 / FPS,
        blit=False,
    )
    gif_path = OUTPUT_DIR / gif_filename
    animation.save(gif_path, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    return [preview_path, gif_path]


def fit_image_to_reference_size(image: Image.Image) -> Image.Image:
    target_width, target_height = REFERENCE_EXPORT_SIZE
    source = image.convert("RGBA")

    bbox = image_content_bbox(source)
    if bbox is not None:
        source = source.crop(expand_bbox(bbox, source.size, padding_px=12))

    if source.width > target_width:
        left = (source.width - target_width) // 2
        source = source.crop((left, 0, left + target_width, source.height))
    if source.height > target_height:
        top = (source.height - target_height) // 2
        source = source.crop((0, top, source.width, top + target_height))

    if source.size == REFERENCE_EXPORT_SIZE:
        return source

    output = Image.new("RGBA", REFERENCE_EXPORT_SIZE, (255, 255, 255, 255))
    left = (target_width - source.width) // 2
    top = (target_height - source.height) // 2
    output.alpha_composite(source, (left, top))
    return output


def split_reference_image(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    fitted = fit_image_to_reference_size(image)
    phasor = fitted.crop((0, 0, SUBPLOT_SPLIT_X, REFERENCE_EXPORT_SIZE[1]))
    helix = fitted.crop((SUBPLOT_SPLIT_X, 0, REFERENCE_EXPORT_SIZE[0], REFERENCE_EXPORT_SIZE[1]))
    return phasor, helix


def setup_reference_complex_axis(ax, *, title: str, output_math: str, show_clip_guides: bool) -> None:
    unit_angle = np.linspace(0.0, 2.0 * np.pi, 600)
    ax.plot(np.cos(unit_angle), np.sin(unit_angle), color="0.82", lw=2.2)
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.axvline(0.0, color="0.75", lw=0.9)
    if show_clip_guides:
        draw_phasor_clip_guides(ax)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.18)
    ax.set_xlabel(r"$\mathrm{Re}\{" + output_math + r"\}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$\mathrm{Im}\{" + output_math + r"\}$", fontsize=LABEL_SIZE)
    ax.set_title(title, pad=12, fontsize=TITLE_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def setup_reference_helix_axis(ax, *, title: str, output_math: str, show_clip_guides: bool) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("n", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel(r"$\mathrm{Re}\{" + output_math + r"\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=12)
    ax.set_zlabel(r"$\mathrm{Im}\{" + output_math + r"\}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=6)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="x", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="z", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.set_title(title, y=1.035, pad=0, fontsize=TITLE_SIZE)
    ax.view_init(elev=22, azim=-62)
    if show_clip_guides:
        draw_clip_guides(ax)


def create_reference_combined_figure(
    *,
    phasor_title: str,
    helix_title: str,
    output_math: str,
    output_function,
    output_color: str,
    reference_function=None,
    show_clip_guides: bool = False,
) -> tuple[plt.Figure, list[float], callable]:
    sample_indices = np.arange(NUM_SAMPLES + 1, dtype=float)
    dense_n_full = np.linspace(0.0, NUM_SAMPLES, NUM_SAMPLES * 160 + 1)
    output_samples = output_function(sample_indices)
    output_dense = output_function(dense_n_full)
    frame_progress = np.linspace(0.0, float(NUM_SAMPLES), NUM_SAMPLES * FRAMES_PER_SAMPLE + 1)

    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI, facecolor="white")
    grid = fig.add_gridspec(1, 2, width_ratios=[0.62, 2.95])
    ax_complex = fig.add_subplot(grid[0, 0])
    try:
        ax_helix = fig.add_subplot(grid[0, 1], projection="3d", computed_zorder=False)
    except TypeError:
        ax_helix = fig.add_subplot(grid[0, 1], projection="3d")

    fig.subplots_adjust(left=0.038, right=0.995, top=0.91, bottom=0.08, wspace=0.00)
    ax_complex.set_position([0.070, 0.115, 0.300, 0.720])
    ax_helix.set_position([0.280, 0.045, 0.715, 0.855])
    ax_complex.set_facecolor("white")
    ax_helix.set_facecolor("white")
    try:
        ax_helix.set_box_aspect(HELIX_BOX_ASPECT, zoom=1.35)
    except TypeError:
        ax_helix.set_box_aspect(HELIX_BOX_ASPECT)

    for axis in (ax_helix.xaxis, ax_helix.yaxis, ax_helix.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))

    setup_reference_complex_axis(
        ax_complex,
        title=phasor_title,
        output_math=output_math,
        show_clip_guides=show_clip_guides,
    )
    setup_reference_helix_axis(
        ax_helix,
        title=helix_title,
        output_math=output_math,
        show_clip_guides=show_clip_guides,
    )

    if reference_function is not None:
        reference_dense = reference_function(dense_n_full)
        reference_samples = reference_function(sample_indices)
        ax_complex.plot(
            reference_dense.real,
            reference_dense.imag,
            color=REFERENCE_GREY,
            lw=1.5,
            ls="--",
            alpha=0.58,
            zorder=3,
        )
        ax_complex.plot(
            reference_samples.real,
            reference_samples.imag,
            "o",
            color=REFERENCE_GREY,
            alpha=0.42,
            ms=5.6,
            zorder=4,
        )
        ax_helix.plot(
            dense_n_full,
            reference_dense.real,
            reference_dense.imag,
            color=REFERENCE_GREY,
            lw=1.5,
            ls="--",
            alpha=0.58,
            zorder=4,
        )
        ax_helix.plot(
            sample_indices,
            reference_samples.real,
            reference_samples.imag,
            "o",
            color=REFERENCE_GREY,
            alpha=0.26,
            ms=4,
            zorder=5,
        )

    ax_complex.plot(
        output_samples.real,
        output_samples.imag,
        "o",
        color="0.75",
        ms=6,
        alpha=0.55,
        zorder=5,
    )
    phasor_line, = ax_complex.plot([], [], color=output_color, lw=2.7)
    phasor_tip, = ax_complex.plot([], [], "o", color=output_color, ms=8)
    phasor_trace, = ax_complex.plot([], [], color=output_color, lw=1.6)
    sample_text = ax_complex.text(
        0.04,
        0.95,
        "",
        transform=ax_complex.transAxes,
        ha="left",
        va="top",
        fontsize=INFO_TEXT_SIZE,
        color="0.20",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="0.80", alpha=0.95),
    )

    zeros = np.zeros_like(sample_indices)
    re_stem_x, re_stem_y, re_stem_z = build_stem_segments(sample_indices, output_samples.real + 0j)
    im_stem_x, im_stem_y, im_stem_z = build_stem_segments(sample_indices, 1j * output_samples.imag)
    ax_helix.plot(re_stem_x, re_stem_y, re_stem_z, color=RE_COLOR, lw=1.0, alpha=0.18, zorder=5)
    ax_helix.plot(im_stem_x, im_stem_y, im_stem_z, color=IM_COLOR, lw=1.0, alpha=0.18, zorder=5)
    ax_helix.plot(sample_indices, output_samples.real, zeros, "o", color=RE_COLOR, alpha=0.24, ms=4, zorder=6)
    ax_helix.plot(sample_indices, zeros, output_samples.imag, "o", color=IM_COLOR, alpha=0.24, ms=4, zorder=6)

    re_point, = ax_helix.plot([], [], [], "o", color=RE_COLOR, ms=5, zorder=28, clip_on=False)
    im_point, = ax_helix.plot([], [], [], "o", color=IM_COLOR, ms=5, zorder=28, clip_on=False)
    re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=2.0, alpha=0.95, zorder=27, clip_on=False)
    im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=2.0, alpha=0.95, zorder=27, clip_on=False)
    helix_stem_history, = ax_helix.plot([], [], [], color=output_color, lw=1.7, zorder=30, clip_on=False)
    helix_history_line, = ax_helix.plot([], [], [], color=output_color, lw=1.4, zorder=31, clip_on=False)
    helix_trace, = ax_helix.plot([], [], [], linestyle="None", marker="o", color=output_color, ms=5, zorder=32, clip_on=False)
    helix_point, = ax_helix.plot([], [], [], "o", color=output_color, ms=6, zorder=34, clip_on=False)
    helix_stem, = ax_helix.plot([], [], [], color=output_color, lw=2.0, alpha=0.95, zorder=33, clip_on=False)

    def draw_state(frame_index: int):
        current_n = frame_progress[frame_index]
        current_value = output_function(current_n)
        dense_keep = dense_n_full <= current_n + 1e-9
        dense_n = dense_n_full[dense_keep]
        dense_values = output_dense[dense_keep]
        sample_keep = sample_indices <= np.floor(current_n + 1e-9)
        past_indices = sample_indices[sample_keep]
        past_values = output_samples[sample_keep]
        stem_x, stem_y, stem_z = build_stem_segments(past_indices, past_values)

        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_tip.set_data([current_value.real], [current_value.imag])
        phasor_trace.set_data(dense_values.real, dense_values.imag)
        sample_text.set_text(f"n = {int(np.floor(current_n + 1e-9))}")

        helix_stem_history.set_data_3d(stem_x, stem_y, stem_z)
        helix_history_line.set_data_3d(dense_n, dense_values.real, dense_values.imag)
        helix_trace.set_data_3d(past_indices, past_values.real, past_values.imag)
        helix_point.set_data_3d([current_n], [current_value.real], [current_value.imag])
        re_point.set_data_3d([current_n], [current_value.real], [0.0])
        im_point.set_data_3d([current_n], [0.0], [current_value.imag])
        helix_stem.set_data_3d(
            [current_n, current_n],
            [0.0, current_value.real],
            [0.0, current_value.imag],
        )
        re_stem.set_data_3d([current_n, current_n], [0.0, current_value.real], [0.0, 0.0])
        im_stem.set_data_3d([current_n, current_n], [0.0, 0.0], [0.0, current_value.imag])

        return (
            phasor_line,
            phasor_tip,
            phasor_trace,
            sample_text,
            helix_stem_history,
            helix_history_line,
            helix_trace,
            helix_point,
            re_point,
            im_point,
            helix_stem,
            re_stem,
            im_stem,
        )

    return fig, list(range(len(frame_progress))), draw_state


def save_split_png_from_figure(fig: plt.Figure, phasor_path: Path, helix_path: Path) -> None:
    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    rgba = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape(height, width, 4)
    image = Image.fromarray(rgba, mode="RGBA")
    phasor, helix = split_reference_image(image)
    phasor.convert("RGB").save(phasor_path)
    helix.convert("RGB").save(helix_path)


def split_reference_gif(temp_path: Path, phasor_path: Path, helix_path: Path) -> None:
    image = Image.open(temp_path)
    phasor_frames: list[Image.Image] = []
    helix_frames: list[Image.Image] = []
    durations: list[int] = []
    for frame in ImageSequence.Iterator(image):
        phasor, helix = split_reference_image(frame.convert("RGBA"))
        phasor_frames.append(phasor)
        helix_frames.append(helix)
        durations.append(frame.info.get("duration", image.info.get("duration", round(1000 / FPS))))

    save_kwargs = {
        "save_all": True,
        "duration": durations,
        "loop": image.info.get("loop", 0),
        "disposal": 2,
    }
    phasor_frames[0].save(phasor_path, append_images=phasor_frames[1:], **save_kwargs)
    helix_frames[0].save(helix_path, append_images=helix_frames[1:], **save_kwargs)


def export_reference_layout_series(
    *,
    phasor_title: str,
    helix_title: str,
    output_math: str,
    output_function,
    output_color: str,
    helix_preview_filename: str,
    helix_gif_filename: str,
    phasor_preview_filename: str,
    phasor_gif_filename: str,
    reference_function=None,
    show_clip_guides: bool = False,
) -> list[Path]:
    fig, frame_indices, draw_state = create_reference_combined_figure(
        phasor_title=phasor_title,
        helix_title=helix_title,
        output_math=output_math,
        output_function=output_function,
        output_color=output_color,
        reference_function=reference_function,
        show_clip_guides=show_clip_guides,
    )

    helix_preview_path = OUTPUT_DIR / helix_preview_filename
    helix_gif_path = OUTPUT_DIR / helix_gif_filename
    phasor_preview_path = OUTPUT_DIR / phasor_preview_filename
    phasor_gif_path = OUTPUT_DIR / phasor_gif_filename

    draw_state(frame_indices[-1])
    save_split_png_from_figure(fig, phasor_preview_path, helix_preview_path)

    temp_gif_path = OUTPUT_DIR / f"__tmp_combined_{phasor_gif_filename}"
    animation = FuncAnimation(
        fig,
        lambda idx: draw_state(idx),
        frames=len(frame_indices),
        interval=1000 / FPS,
        blit=False,
    )
    animation.save(temp_gif_path, writer=PillowWriter(fps=FPS))
    split_reference_gif(temp_gif_path, phasor_gif_path, helix_gif_path)
    temp_gif_path.unlink(missing_ok=True)
    plt.close(fig)

    return [helix_preview_path, helix_gif_path, phasor_preview_path, phasor_gif_path]


def main() -> None:
    clear_output_dir()

    paths: list[Path] = []
    paths.extend(
        export_reference_layout_series(
            phasor_title=rf"Linear delay: phasor, $\Omega={OMEGA_LABEL}$",
            helix_title=rf"Linear delay, $\Omega={OMEGA_LABEL}$",
            output_math=r"y_\mathrm{L}[n]",
            output_function=delayed_signal,
            output_color=OUTPUT_BLUE,
            helix_preview_filename="01_linear_delay_helix_preview.png",
            helix_gif_filename="02_linear_delay_helix_motion.gif",
            phasor_preview_filename="05_linear_delay_phasor_preview.png",
            phasor_gif_filename="06_linear_delay_phasor_motion.gif",
            reference_function=input_signal,
        )
    )
    paths.extend(
        export_reference_layout_series(
            phasor_title=rf"Delay + hard clipper: phasor, $\Omega={OMEGA_LABEL}$",
            helix_title=rf"Delay + hard clipper, $\Omega={OMEGA_LABEL}$",
            output_math=r"y_\mathrm{NL}[n]",
            output_function=nonlinear_output,
            output_color=OUTPUT_BLUE,
            helix_preview_filename="03_delay_hard_clipper_helix_preview.png",
            helix_gif_filename="04_delay_hard_clipper_helix_motion.gif",
            phasor_preview_filename="07_delay_hard_clipper_phasor_preview.png",
            phasor_gif_filename="08_delay_hard_clipper_phasor_motion.gif",
            reference_function=delayed_signal,
            show_clip_guides=True,
        )
    )

    for path in paths:
        print(path.relative_to(LECTURE_DIR))


if __name__ == "__main__":
    main()
