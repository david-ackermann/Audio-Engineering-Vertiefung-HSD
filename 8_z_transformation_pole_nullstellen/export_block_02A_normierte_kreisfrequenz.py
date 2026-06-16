from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import MultipleLocator
from PIL import Image, ImageChops, ImageSequence


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "02_komplexe_exponentialsignale_lti"
    / "02A_normierte_kreisfrequenz"
)

FPS = 8
FRAMES_PER_SAMPLE = 6
FIGSIZE = (17.2, 6.9)
FIG_DPI = 100
SUBPLOT_SPLIT_X = 650

SIGNAL_BLACK = "0.10"
OUTPUT_BLUE = "#2b7bbb"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
TITLE_SIZE = 19
LABEL_SIZE = 20
TICK_SIZE = 16
INFO_TEXT_SIZE = 16
HELIX_BOX_ASPECT = (3.9, 1.55, 1.55)

NUM_SAMPLES = 16
OMEGA = 0.5 * np.pi
OMEGA_LABEL = r"\frac{\pi}{2}"

SERIES = (
    {
        "prefix": "x_input",
        "title": r"Input signal $x[n]=e^{j\Omega n}$",
        "helix_title": rf"Normalized angular frequency: $\Omega=2\pi f/f_s={OMEGA_LABEL}$ rad/sample",
        "signal_label": "x",
        "sample_shift": 0,
        "start_file": "01_x_input_start_n0.png",
        "gif_file": "02_x_input_motion.gif",
        "end_file": "03_x_input_end_n16.png",
    },
    {
        "prefix": "y_delay",
        "title": r"Output signal $y[n]=x[n-1]$",
        "helix_title": rf"One-sample delay: $y[n]=x[n-1]$, $\Omega=2\pi f/f_s={OMEGA_LABEL}$ rad/sample",
        "signal_label": "y",
        "sample_shift": -1,
        "initial_rest": True,
        "start_file": "04_y_delay_start_n0.png",
        "gif_file": "05_y_delay_motion.gif",
        "end_file": "06_y_delay_end_n16.png",
    },
)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.rglob("*.png"):
        image_file.unlink()
    for gif_file in OUTPUT_DIR.rglob("*.gif"):
        gif_file.unlink()


def crop_png_margins(path: Path, padding_px: int = 18) -> tuple[int, int, int, int] | None:
    image = Image.open(path).convert("RGB")
    background = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, background)
    diff = diff.convert("L").point(lambda value: 255 if value > 12 else 0)
    bbox = diff.getbbox()
    if bbox is None:
        return None

    left, top, right, bottom = bbox
    crop_box = (
        max(0, left - padding_px),
        max(0, top - padding_px),
        min(image.width, right + padding_px),
        min(image.height, bottom + padding_px),
    )
    image.crop(crop_box).save(path)
    return crop_box


def crop_png_to_box(path: Path, crop_box: tuple[int, int, int, int] | None) -> None:
    if crop_box is None:
        return
    image = Image.open(path).convert("RGB")
    image.crop(crop_box).save(path)


def normalize_duration_sum(durations: list[int], total_duration_ms: int) -> list[int]:
    if not durations:
        return durations
    durations = list(durations)
    durations[-1] = max(10, durations[-1] + total_duration_ms - sum(durations))
    return durations


def crop_gif_to_box(
    path: Path,
    crop_box: tuple[int, int, int, int] | None,
    total_duration_ms: int | None = None,
) -> None:
    if crop_box is None:
        return

    image = Image.open(path)
    frames = []
    durations = []
    for frame in ImageSequence.Iterator(image):
        frames.append(frame.convert("RGBA").crop(crop_box))
        durations.append(frame.info.get("duration", image.info.get("duration", round(1000 / FPS))))

    if not frames:
        return

    if total_duration_ms is not None:
        durations = normalize_duration_sum(durations, total_duration_ms)

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=image.info.get("loop", 0),
        disposal=2,
    )


def pad_image_to_size(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    target_width, target_height = target_size
    image = image.convert("RGBA")
    output = Image.new("RGBA", target_size, (255, 255, 255, 255))
    left = (target_width - image.width) // 2
    top = (target_height - image.height) // 2
    output.alpha_composite(image, (left, top))
    return output


def normalize_export_sizes() -> None:
    export_files = sorted(
        list(OUTPUT_DIR.glob("*.png")) + list(OUTPUT_DIR.glob("*.gif")),
        key=lambda path: path.name,
    )
    if not export_files:
        return

    sizes = []
    for path in export_files:
        with Image.open(path) as image:
            sizes.append(image.size)

    target_size = (max(width for width, _ in sizes), max(height for _, height in sizes))

    for path in export_files:
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


def split_png_subplots(path: Path, split_x: int = SUBPLOT_SPLIT_X) -> None:
    image = Image.open(path).convert("RGB")
    phasor_dir = path.parent / "phasor"
    helix_dir = path.parent / "helix"
    phasor_dir.mkdir(exist_ok=True)
    helix_dir.mkdir(exist_ok=True)
    image.crop((0, 0, split_x, image.height)).save(phasor_dir / path.name)
    image.crop((split_x, 0, image.width, image.height)).save(helix_dir / path.name)


def split_gif_subplots(path: Path, split_x: int = SUBPLOT_SPLIT_X) -> None:
    image = Image.open(path)
    phasor_dir = path.parent / "phasor"
    helix_dir = path.parent / "helix"
    phasor_dir.mkdir(exist_ok=True)
    helix_dir.mkdir(exist_ok=True)

    phasor_frames = []
    helix_frames = []
    durations = []
    for frame in ImageSequence.Iterator(image):
        frame_rgba = frame.convert("RGBA")
        phasor_frames.append(frame_rgba.crop((0, 0, split_x, frame_rgba.height)))
        helix_frames.append(frame_rgba.crop((split_x, 0, frame_rgba.width, frame_rgba.height)))
        durations.append(frame.info.get("duration", image.info.get("duration", round(1000 / FPS))))

    if not phasor_frames:
        return

    save_kwargs = {
        "save_all": True,
        "duration": durations,
        "loop": image.info.get("loop", 0),
        "disposal": 2,
    }
    phasor_frames[0].save(phasor_dir / path.name, append_images=phasor_frames[1:], **save_kwargs)
    helix_frames[0].save(helix_dir / path.name, append_images=helix_frames[1:], **save_kwargs)


def split_export_subplots() -> None:
    for output_file in sorted(OUTPUT_DIR.glob("*.png")):
        split_png_subplots(output_file)
    for output_file in sorted(OUTPUT_DIR.glob("*.gif")):
        split_gif_subplots(output_file)


def build_stem_segments(
    x_values: np.ndarray,
    y_start_values: np.ndarray,
    y_end_values: np.ndarray,
    z_start_values: np.ndarray,
    z_end_values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_segments = []
    y_segments = []
    z_segments = []

    for x_value, y_start, y_end, z_start, z_end in zip(
        x_values,
        y_start_values,
        y_end_values,
        z_start_values,
        z_end_values,
    ):
        x_segments.extend([x_value, x_value, np.nan])
        y_segments.extend([y_start, y_end, np.nan])
        z_segments.extend([z_start, z_end, np.nan])

    return np.array(x_segments), np.array(y_segments), np.array(z_segments)


def signal_values(sample_indices: np.ndarray, sample_shift: int) -> np.ndarray:
    return np.exp(1j * OMEGA * (sample_indices + sample_shift))


def series_values(sample_indices: np.ndarray, series: dict) -> np.ndarray:
    values = signal_values(sample_indices, series["sample_shift"])
    if series.get("initial_rest", False):
        values = values.astype(complex, copy=True)
        values[sample_indices < 1.0] = 0.0
    return values


def series_color(series: dict) -> str:
    return OUTPUT_BLUE if series["signal_label"] == "y" else SIGNAL_BLACK


def setup_complex_axis(ax, series: dict) -> None:
    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 600)
    ax.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.82", lw=2.2)
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.axvline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.18)
    label = series["signal_label"]
    ax.set_xlabel(rf"Re$\{{{label}[n]\}}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(rf"Im$\{{{label}[n]\}}$", fontsize=LABEL_SIZE)
    ax.set_title(series["title"], pad=12, fontsize=TITLE_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def setup_helix_axis(ax, series: dict) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    label = series["signal_label"]
    ax.set_xlabel("n", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel(rf"Re$\{{{label}[n]\}}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=12)
    ax.set_zlabel(rf"Im$\{{{label}[n]\}}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=6)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="x", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="z", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.set_title(series["helix_title"], y=1.035, pad=0, fontsize=TITLE_SIZE)
    ax.view_init(elev=22, azim=-62)


def create_figure(series: dict):
    sample_indices = np.arange(NUM_SAMPLES + 1, dtype=float)
    values = series_values(sample_indices, series)
    zeros = np.zeros_like(sample_indices)
    frame_progress = np.linspace(0.0, float(NUM_SAMPLES), NUM_SAMPLES * FRAMES_PER_SAMPLE)
    frame_indices = np.floor(frame_progress).astype(int)
    frame_indices[-1] = NUM_SAMPLES

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

    setup_complex_axis(ax_complex, series)
    setup_helix_axis(ax_helix, series)

    active_color = series_color(series)
    ax_complex.plot(values.real, values.imag, "o", color="0.75", ms=6)
    phasor_line, = ax_complex.plot([], [], color=active_color, lw=2.7)
    phasor_tip, = ax_complex.plot([], [], "o", color=active_color, ms=8)
    phasor_trace, = ax_complex.plot([], [], color=active_color, lw=1.6, ls="--")
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

    re_stem_x, re_stem_y, re_stem_z = build_stem_segments(
        sample_indices,
        zeros,
        values.real,
        zeros,
        zeros,
    )
    im_stem_x, im_stem_y, im_stem_z = build_stem_segments(
        sample_indices,
        zeros,
        zeros,
        zeros,
        values.imag,
    )

    ax_helix.plot(re_stem_x, re_stem_y, re_stem_z, color=RE_COLOR, lw=1.0, alpha=0.18, zorder=5)
    ax_helix.plot(im_stem_x, im_stem_y, im_stem_z, color=IM_COLOR, lw=1.0, alpha=0.18, zorder=5)
    ax_helix.plot(sample_indices, values.real, zeros, "o", color=RE_COLOR, alpha=0.24, ms=4, zorder=6)
    ax_helix.plot(sample_indices, zeros, values.imag, "o", color=IM_COLOR, alpha=0.24, ms=4, zorder=6)

    re_point, = ax_helix.plot([], [], [], "o", color=RE_COLOR, ms=5, zorder=28, clip_on=False)
    im_point, = ax_helix.plot([], [], [], "o", color=IM_COLOR, ms=5, zorder=28, clip_on=False)
    re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=2.0, alpha=0.95, zorder=27, clip_on=False)
    im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=2.0, alpha=0.95, zorder=27, clip_on=False)
    helix_stem_history, = ax_helix.plot([], [], [], color=active_color, lw=1.7, zorder=30, clip_on=False)
    helix_history_line, = ax_helix.plot([], [], [], color=active_color, lw=1.4, ls="--", zorder=31, clip_on=False)
    helix_trace, = ax_helix.plot([], [], [], linestyle="None", marker="o", color=active_color, ms=5, zorder=32, clip_on=False)
    helix_point, = ax_helix.plot([], [], [], "o", color=active_color, ms=6, zorder=34, clip_on=False)
    helix_stem, = ax_helix.plot([], [], [], color=active_color, lw=2.0, alpha=0.95, zorder=33, clip_on=False)

    def draw_state(frame_index: int):
        sample_index = int(frame_indices[frame_index])
        current_value = values[sample_index]

        past_indices = sample_indices[: sample_index + 1]
        past_values = values[: sample_index + 1]
        continuous_n = np.linspace(0.0, float(sample_index), max(2, 40 * (sample_index + 1)))
        continuous_values = series_values(continuous_n, series)

        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_tip.set_data([current_value.real], [current_value.imag])
        phasor_trace.set_data(continuous_values.real, continuous_values.imag)
        sample_text.set_text(f"n = {sample_index}")

        zeros_past = np.zeros_like(past_indices)
        past_helix_stem_x, past_helix_stem_y, past_helix_stem_z = build_stem_segments(
            past_indices,
            zeros_past,
            past_values.real,
            zeros_past,
            past_values.imag,
        )

        helix_stem_history.set_data_3d(past_helix_stem_x, past_helix_stem_y, past_helix_stem_z)
        helix_history_line.set_data_3d(
            continuous_n,
            continuous_values.real,
            continuous_values.imag,
        )
        helix_trace.set_data_3d(past_indices, past_values.real, past_values.imag)
        helix_point.set_data_3d([sample_index], [current_value.real], [current_value.imag])
        re_point.set_data_3d([sample_index], [current_value.real], [0.0])
        im_point.set_data_3d([sample_index], [0.0], [current_value.imag])
        helix_stem.set_data_3d(
            [sample_index, sample_index],
            [0.0, current_value.real],
            [0.0, current_value.imag],
        )
        re_stem.set_data_3d([sample_index, sample_index], [0.0, current_value.real], [0.0, 0.0])
        im_stem.set_data_3d([sample_index, sample_index], [0.0, 0.0], [0.0, current_value.imag])

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

    return fig, frame_indices, draw_state


def export_series(series: dict) -> None:
    start_path = OUTPUT_DIR / series["start_file"]
    gif_path = OUTPUT_DIR / series["gif_file"]
    end_path = OUTPUT_DIR / series["end_file"]

    fig, frame_indices, draw_state = create_figure(series)

    draw_state(0)
    fig.canvas.draw()
    fig.canvas.print_png(str(start_path.resolve()))

    draw_state(len(frame_indices) - 1)
    fig.canvas.draw()
    fig.canvas.print_png(str(end_path.resolve()))
    crop_box = crop_png_margins(end_path, padding_px=12)
    crop_png_to_box(start_path, crop_box)

    animation = FuncAnimation(
        fig,
        lambda idx: draw_state(idx),
        frames=len(frame_indices),
        interval=1000 / FPS,
        blit=False,
    )
    writer = PillowWriter(fps=FPS)
    animation.save(str(gif_path.resolve()), writer=writer)
    crop_gif_to_box(
        gif_path,
        crop_box,
        int(round(NUM_SAMPLES * FRAMES_PER_SAMPLE * 1000 / FPS)),
    )
    plt.close(fig)


def main() -> None:
    clear_output_dir()
    for series in SERIES:
        export_series(series)
    normalize_export_sizes()
    split_export_subplots()
    print(f"PNG/GIF figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
