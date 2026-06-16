from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import MultipleLocator
from PIL import Image, ImageChops, ImageSequence


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "02_komplexe_exponentialsignale_lti"
    / "02B_phasenfaktor_multiplikation"
)

FPS = 8
FRAMES_PER_SAMPLE = 6
FIGSIZE = (17.2, 6.9)
FIG_DPI = 100
SUBPLOT_SPLIT_X = 650

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#26a043"
OUTPUT_BLUE = "#2b7bbb"
REFERENCE_GREY = "0.70"
LIGHT_GREY = "0.84"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"

TITLE_SIZE = 19
LABEL_SIZE = 20
TICK_SIZE = 16
INFO_TEXT_SIZE = 16
HELIX_BOX_ASPECT = (3.9, 1.55, 1.55)

NUM_SAMPLES = 16
DEFAULT_DELAY = 1

FREQUENCY_CASES = (
    {
        "key": "half_nyquist",
        "title": "Half Nyquist",
        "omega": 0.5 * np.pi,
        "omega_label": r"\pi/2",
    },
    {
        "key": "nyquist",
        "title": "Nyquist",
        "omega": np.pi,
        "omega_label": r"\pi",
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


def signal_value(n_values: np.ndarray | float, omega: float) -> np.ndarray | complex:
    return np.exp(1j * omega * n_values)


def output_value(n_values: np.ndarray | float, omega: float, delay: int) -> np.ndarray | complex:
    return np.exp(-1j * delay * omega) * signal_value(n_values, omega)


def setup_unit_circle_axis(ax, title: str, label: str) -> None:
    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 720)
    ax.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color=LIGHT_GREY, lw=2.2)
    ax.axhline(0.0, color="0.76", lw=0.9)
    ax.axvline(0.0, color="0.76", lw=0.9)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=0.18)
    ax.set_xlabel(rf"Re$\{{{label}\}}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(rf"Im$\{{{label}\}}$", fontsize=LABEL_SIZE)
    ax.set_title(title, pad=12, fontsize=TITLE_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def setup_helix_axis(ax, title: str, label: str) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("n", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel(rf"Re$\{{{label}\}}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=12)
    ax.set_zlabel(rf"Im$\{{{label}\}}$", color=SIGNAL_BLACK, fontsize=LABEL_SIZE, labelpad=6)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.tick_params(axis="x", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="z", colors=SIGNAL_BLACK, labelsize=TICK_SIZE)
    ax.set_title(title, y=1.035, pad=0, fontsize=TITLE_SIZE)
    ax.view_init(elev=22, azim=-62)


def draw_arrow(ax, value: complex, color: str, alpha: float = 1.0, linewidth: float = 2.8) -> None:
    ax.annotate(
        "",
        xy=(value.real, value.imag),
        xytext=(0.0, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=linewidth, mutation_scale=16, alpha=alpha),
        zorder=6,
    )
    ax.scatter(
        [value.real],
        [value.imag],
        s=82,
        color=color,
        edgecolor="white",
        linewidth=0.9,
        alpha=alpha,
        zorder=7,
    )


def build_arc(start_angle: float, delta_angle: float) -> tuple[np.ndarray, np.ndarray]:
    if np.isclose(delta_angle, 0.0):
        return np.array([]), np.array([])
    radius = 1.12
    theta = np.linspace(start_angle, start_angle + delta_angle, 100)
    return radius * np.cos(theta), radius * np.sin(theta)


def update_arc_arrow(arrow: FancyArrowPatch, arc_x: np.ndarray, arc_y: np.ndarray) -> None:
    if arc_x.size < 2:
        arrow.set_visible(False)
        return
    arrow.set_visible(True)
    arrow.set_positions((arc_x[-2], arc_y[-2]), (arc_x[-1], arc_y[-1]))


def build_complex_stem_segments(
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


def create_base_figure(case: dict, mode: str, delay: int = DEFAULT_DELAY):
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI, facecolor="white")
    grid = fig.add_gridspec(1, 2, width_ratios=[0.72, 2.95])
    ax_complex = fig.add_subplot(grid[0, 0])
    try:
        ax_helix = fig.add_subplot(grid[0, 1], projection="3d", computed_zorder=False)
    except TypeError:
        ax_helix = fig.add_subplot(grid[0, 1], projection="3d")

    fig.subplots_adjust(left=0.038, right=0.995, top=0.91, bottom=0.08, wspace=0.00)
    ax_complex.set_position([0.070, 0.115, 0.300, 0.720])
    ax_helix.set_position([0.280, 0.045, 0.715, 0.855])
    try:
        ax_helix.set_box_aspect(HELIX_BOX_ASPECT, zoom=1.35)
    except TypeError:
        ax_helix.set_box_aspect(HELIX_BOX_ASPECT)

    for axis in (ax_helix.xaxis, ax_helix.yaxis, ax_helix.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))

    if mode == "input":
        setup_unit_circle_axis(
            ax_complex,
            r"Input signal $x[n]=e^{j\Omega n}$",
            "x[n]",
        )
        setup_helix_axis(
            ax_helix,
            rf"Normalized angular frequency: $\Omega=2\pi f/f_s={case['omega_label']}$ rad/sample",
            "x[n]",
        )
    else:
        output_title = (
            r"Output signal $y[n]=e^{-j\Omega}x[n]$"
            if delay == 1
            else rf"Output signal $y[n]=e^{{-j{delay}\Omega}}x[n]$"
        )
        helix_title = (
            rf"One-sample delay: $y[n]=e^{{-j\Omega}}x[n]$, $\Omega=2\pi f/f_s={case['omega_label']}$ rad/sample"
            if delay == 1
            else rf"{delay}-sample delay: $y[n]=e^{{-j{delay}\Omega}}x[n]$, $\Omega=2\pi f/f_s={case['omega_label']}$ rad/sample"
        )
        setup_unit_circle_axis(
            ax_complex,
            output_title,
            "y[n]",
        )
        setup_helix_axis(
            ax_helix,
            helix_title,
            "y[n]",
        )

    return fig, ax_complex, ax_helix


def create_input_figure(case: dict):
    omega = case["omega"]
    frame_progress = np.linspace(0.0, float(NUM_SAMPLES), NUM_SAMPLES * FRAMES_PER_SAMPLE)
    frame_indices = np.floor(frame_progress).astype(int)
    frame_indices[-1] = NUM_SAMPLES
    sample_indices = np.arange(NUM_SAMPLES + 1, dtype=float)
    sample_values = signal_value(sample_indices, omega)

    fig, ax_complex, ax_helix = create_base_figure(case, "input")

    ax_complex.plot(sample_values.real, sample_values.imag, "o", color=REFERENCE_GREY, alpha=0.34, ms=5)
    phasor_trace, = ax_complex.plot([], [], color=SIGNAL_BLACK, lw=1.5, ls="--", alpha=0.85)
    phasor_line, = ax_complex.plot([], [], color=SIGNAL_BLACK, lw=2.8)
    phasor_tip, = ax_complex.plot([], [], "o", color=SIGNAL_BLACK, ms=8)
    omega_arc_line, = ax_complex.plot([], [], color=SIGNAL_BLACK, lw=2.3, alpha=0.95, zorder=10)
    omega_arc_arrow = FancyArrowPatch(
        (0.0, 0.0),
        (0.0, 0.0),
        arrowstyle="-|>",
        mutation_scale=18,
        color=SIGNAL_BLACK,
        lw=2.3,
        alpha=0.95,
        visible=False,
        zorder=11,
    )
    ax_complex.add_patch(omega_arc_arrow)
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

    ax_helix.plot(sample_indices, sample_values.real, sample_values.imag, "o", color=SIGNAL_BLACK, alpha=0.22, ms=4)
    sample_stems, = ax_helix.plot([], [], [], color=SIGNAL_BLACK, lw=1.7, alpha=0.80, zorder=29, clip_on=False)
    sample_points, = ax_helix.plot([], [], [], "o", color=SIGNAL_BLACK, ms=5, zorder=31, clip_on=False)
    helix_history, = ax_helix.plot([], [], [], color=SIGNAL_BLACK, lw=1.5, ls="--", zorder=30, clip_on=False)
    helix_point, = ax_helix.plot([], [], [], "o", color=SIGNAL_BLACK, ms=7, zorder=32, clip_on=False)
    helix_stem, = ax_helix.plot([], [], [], color=SIGNAL_BLACK, lw=2.0, alpha=0.95, zorder=31, clip_on=False)
    re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=1.9, alpha=0.85, zorder=28, clip_on=False)
    im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=1.9, alpha=0.85, zorder=28, clip_on=False)
    re_point, = ax_helix.plot([], [], [], "o", color=RE_COLOR, ms=5, zorder=29, clip_on=False)
    im_point, = ax_helix.plot([], [], [], "o", color=IM_COLOR, ms=5, zorder=29, clip_on=False)

    def draw_state(frame_index: int):
        current_n = int(frame_indices[frame_index])
        current_value = signal_value(current_n, omega)
        continuous_n = np.linspace(0.0, current_n, max(2, int(90 * current_n) + 2))
        continuous_values = signal_value(continuous_n, omega)
        past_indices = sample_indices[: current_n + 1]
        past_values = sample_values[: current_n + 1]
        stem_x, stem_y, stem_z = build_complex_stem_segments(past_indices, past_values)

        phasor_trace.set_data(continuous_values.real, continuous_values.imag)
        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_tip.set_data([current_value.real], [current_value.imag])
        arc_x, arc_y = build_arc(np.angle(current_value), omega)
        omega_arc_line.set_data(arc_x, arc_y)
        update_arc_arrow(omega_arc_arrow, arc_x, arc_y)
        sample_text.set_text(f"n = {current_n}")

        sample_stems.set_data_3d(stem_x, stem_y, stem_z)
        sample_points.set_data_3d(past_indices, past_values.real, past_values.imag)
        helix_history.set_data_3d(continuous_n, continuous_values.real, continuous_values.imag)
        helix_point.set_data_3d([current_n], [current_value.real], [current_value.imag])
        helix_stem.set_data_3d([current_n, current_n], [0.0, current_value.real], [0.0, current_value.imag])
        re_stem.set_data_3d([current_n, current_n], [0.0, current_value.real], [0.0, 0.0])
        im_stem.set_data_3d([current_n, current_n], [0.0, 0.0], [0.0, current_value.imag])
        re_point.set_data_3d([current_n], [current_value.real], [0.0])
        im_point.set_data_3d([current_n], [0.0], [current_value.imag])

        return (
            phasor_trace,
            phasor_line,
            phasor_tip,
            omega_arc_line,
            omega_arc_arrow,
            sample_text,
            sample_stems,
            sample_points,
            helix_history,
            helix_point,
            helix_stem,
            re_stem,
            im_stem,
            re_point,
            im_point,
        )

    return fig, frame_indices, draw_state


def create_output_figure(case: dict, delay: int = DEFAULT_DELAY):
    omega = case["omega"]
    phase_factor = np.exp(-1j * delay * omega)
    factor_angle = -delay * omega
    frame_progress = np.linspace(0.0, float(NUM_SAMPLES), NUM_SAMPLES * FRAMES_PER_SAMPLE)
    frame_indices = np.floor(frame_progress).astype(int)
    frame_indices[-1] = NUM_SAMPLES
    sample_indices = np.arange(NUM_SAMPLES + 1, dtype=float)
    input_samples = signal_value(sample_indices, omega)
    output_samples = output_value(sample_indices, omega, delay)

    fig, ax_complex, ax_helix = create_base_figure(case, "output", delay=delay)

    draw_arrow(ax_complex, phase_factor, SYSTEM_GREEN, alpha=0.86, linewidth=2.6)
    input_reference_points, = ax_complex.plot([], [], "o", color=SIGNAL_BLACK, alpha=0.30, ms=5, zorder=5)
    output_trace, = ax_complex.plot([], [], color=OUTPUT_BLUE, lw=1.5, ls="--", alpha=0.85, zorder=7)
    input_line, = ax_complex.plot([], [], color=SIGNAL_BLACK, lw=2.6, alpha=0.88, zorder=8)
    input_tip, = ax_complex.plot([], [], "o", color=SIGNAL_BLACK, ms=8, alpha=0.88, zorder=9)
    output_line, = ax_complex.plot([], [], color=OUTPUT_BLUE, lw=3.4, zorder=11)
    output_tip, = ax_complex.plot([], [], "o", color=OUTPUT_BLUE, ms=8, zorder=12)
    arc_line, = ax_complex.plot([], [], color=SYSTEM_GREEN, lw=2.5, alpha=0.95, zorder=10)
    arc_arrow = FancyArrowPatch(
        (0.0, 0.0),
        (0.0, 0.0),
        arrowstyle="-|>",
        mutation_scale=18,
        color=SYSTEM_GREEN,
        lw=2.5,
        alpha=0.95,
        visible=False,
        zorder=11,
    )
    ax_complex.add_patch(arc_arrow)
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

    ax_helix.plot(sample_indices, output_samples.real, output_samples.imag, "o", color=OUTPUT_BLUE, alpha=0.22, ms=4)
    input_reference_history, = ax_helix.plot([], [], [], color=SIGNAL_BLACK, lw=1.5, alpha=0.62, ls="--", zorder=8)
    input_reference_points_3d, = ax_helix.plot([], [], [], "o", color=SIGNAL_BLACK, alpha=0.28, ms=4, zorder=9)

    output_sample_stems, = ax_helix.plot([], [], [], color=OUTPUT_BLUE, lw=1.7, alpha=0.80, zorder=29, clip_on=False)
    output_sample_points, = ax_helix.plot([], [], [], "o", color=OUTPUT_BLUE, ms=5, zorder=31, clip_on=False)
    output_history, = ax_helix.plot([], [], [], color=OUTPUT_BLUE, lw=1.5, ls="--", zorder=30, clip_on=False)
    output_point, = ax_helix.plot([], [], [], "o", color=OUTPUT_BLUE, ms=7, zorder=32, clip_on=False)
    output_stem, = ax_helix.plot([], [], [], color=OUTPUT_BLUE, lw=2.0, alpha=0.95, zorder=31, clip_on=False)
    re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=1.9, alpha=0.85, zorder=28, clip_on=False)
    im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=1.9, alpha=0.85, zorder=28, clip_on=False)
    re_point, = ax_helix.plot([], [], [], "o", color=RE_COLOR, ms=5, zorder=29, clip_on=False)
    im_point, = ax_helix.plot([], [], [], "o", color=IM_COLOR, ms=5, zorder=29, clip_on=False)

    def draw_state(frame_index: int):
        current_n = int(frame_indices[frame_index])
        current_input = signal_value(current_n, omega)
        current_output = output_value(current_n, omega, delay)
        continuous_n = np.linspace(0.0, current_n, max(2, int(90 * current_n) + 2))
        continuous_input = signal_value(continuous_n, omega)
        continuous_output = output_value(continuous_n, omega, delay)
        past_indices = sample_indices[: current_n + 1]
        past_inputs = input_samples[: current_n + 1]
        past_outputs = output_samples[: current_n + 1]
        stem_x, stem_y, stem_z = build_complex_stem_segments(past_indices, past_outputs)

        input_line.set_data([0.0, current_input.real], [0.0, current_input.imag])
        input_tip.set_data([current_input.real], [current_input.imag])
        if current_n == 0:
            input_reference_points.set_data([], [])
            input_reference_history.set_data_3d([], [], [])
            input_reference_points_3d.set_data_3d([], [], [])
        else:
            input_reference_points.set_data(past_inputs.real, past_inputs.imag)
            input_reference_history.set_data_3d(continuous_n, continuous_input.real, continuous_input.imag)
            input_reference_points_3d.set_data_3d(past_indices, past_inputs.real, past_inputs.imag)
        output_line.set_data([0.0, current_output.real], [0.0, current_output.imag])
        output_tip.set_data([current_output.real], [current_output.imag])
        output_trace.set_data(continuous_output.real, continuous_output.imag)
        arc_x, arc_y = build_arc(np.angle(current_input), factor_angle)
        arc_line.set_data(arc_x, arc_y)
        update_arc_arrow(arc_arrow, arc_x, arc_y)
        sample_text.set_text(f"n = {current_n}")

        output_sample_stems.set_data_3d(stem_x, stem_y, stem_z)
        output_sample_points.set_data_3d(past_indices, past_outputs.real, past_outputs.imag)
        output_history.set_data_3d(continuous_n, continuous_output.real, continuous_output.imag)
        output_point.set_data_3d([current_n], [current_output.real], [current_output.imag])
        output_stem.set_data_3d(
            [current_n, current_n],
            [0.0, current_output.real],
            [0.0, current_output.imag],
        )
        re_stem.set_data_3d([current_n, current_n], [0.0, current_output.real], [0.0, 0.0])
        im_stem.set_data_3d([current_n, current_n], [0.0, 0.0], [0.0, current_output.imag])
        re_point.set_data_3d([current_n], [current_output.real], [0.0])
        im_point.set_data_3d([current_n], [0.0], [current_output.imag])

        return (
            input_line,
            input_tip,
            input_reference_points,
            output_trace,
            output_line,
            output_tip,
            arc_line,
            arc_arrow,
            sample_text,
            input_reference_history,
            input_reference_points_3d,
            output_sample_stems,
            output_sample_points,
            output_history,
            output_point,
            output_stem,
            re_stem,
            im_stem,
            re_point,
            im_point,
        )

    return fig, frame_indices, draw_state


def export_series(case: dict, mode: str, figure_number: int, delay: int = DEFAULT_DELAY) -> int:
    if mode == "input":
        fig, frame_values, draw_state = create_input_figure(case)
    else:
        fig, frame_values, draw_state = create_output_figure(case, delay=delay)

    delay_suffix = "" if mode == "input" or delay == DEFAULT_DELAY else f"_d{delay}"
    start_path = OUTPUT_DIR / f"{figure_number:02d}_{case['key']}_{mode}{delay_suffix}_start_n0.png"
    gif_path = OUTPUT_DIR / f"{figure_number + 1:02d}_{case['key']}_{mode}{delay_suffix}_motion.gif"
    end_path = OUTPUT_DIR / f"{figure_number + 2:02d}_{case['key']}_{mode}{delay_suffix}_end_n16.png"

    draw_state(0)
    fig.canvas.draw()
    fig.canvas.print_png(str(start_path.resolve()))

    draw_state(len(frame_values) - 1)
    fig.canvas.draw()
    fig.canvas.print_png(str(end_path.resolve()))
    crop_box = crop_png_margins(end_path, padding_px=12)
    crop_png_to_box(start_path, crop_box)

    animation = FuncAnimation(
        fig,
        lambda idx: draw_state(idx),
        frames=len(frame_values),
        interval=1000 / FPS,
        blit=False,
    )
    writer = PillowWriter(fps=FPS)
    animation.save(str(gif_path.resolve()), writer=writer)
    crop_gif_to_box(
        gif_path,
        crop_box,
        int(round(len(frame_values) * 1000 / FPS)),
    )
    plt.close(fig)
    return figure_number + 3


def main() -> None:
    clear_output_dir()
    figure_number = 1
    for case in FREQUENCY_CASES:
        figure_number = export_series(case, "input", figure_number)
        figure_number = export_series(case, "output", figure_number)
    for case in FREQUENCY_CASES:
        figure_number = export_series(case, "output", figure_number, delay=2)
    normalize_export_sizes()
    split_export_subplots()
    print(f"PNG/GIF figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
