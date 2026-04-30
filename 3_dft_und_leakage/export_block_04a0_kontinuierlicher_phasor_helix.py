from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import FixedLocator, MultipleLocator
from PIL import Image, ImageChops, ImageSequence


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_diskrete_kreisfrequenz"
    / "04A"
    / "04A1_kontinuierlicher_phasor_helix"
)

FIGSIZE = (17.2, 6.9)
FIG_DPI = 100
FPS = 8
FRAMES_PER_SAMPLE = 6
SYNC_SAMPLE_COUNT = 16
FRAMES = SYNC_SAMPLE_COUNT * FRAMES_PER_SAMPLE
SYNC_FRAME_DURATION_PATTERN_MS = (120, 130, 120, 130, 120, 130)
REFERENCE_FREQUENCY_HZ = 1.0
OBSERVATION_TIME = 1.0 / REFERENCE_FREQUENCY_HZ
X_AXIS_LEFT_PAD_FRACTION = 0.0
X_AXIS_RIGHT_PAD_FRACTION = 0.16
HELIX_VIEW_ELEV = 24
HELIX_VIEW_AZIM = -62
EXPORT_GIFS = True

PHASOR_GREEN = "#26a043"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
TITLE_SIZE = 18
LABEL_SIZE = 20
TICK_SIZE = 16
HELIX_BOX_ASPECT = (3.9, 1.55, 1.55)


EXPORT_CASES = [
    {
        "file_index": 1,
        "label": "f1hz_continuous",
        "frequency_hz": 1.0,
    },
    {
        "file_index": 2,
        "label": "f4hz_continuous",
        "frequency_hz": 4.0,
    },
    {
        "file_index": 3,
        "label": "f7hz_continuous",
        "frequency_hz": 7.0,
    },
    {
        "file_index": 4,
        "label": "f9hz_continuous",
        "frequency_hz": 9.0,
    },
    {
        "file_index": 5,
        "label": "f16hz_continuous",
        "frequency_hz": 16.0,
    },
    {
        "file_index": 6,
        "label": "f3p46hz_continuous",
        "frequency_hz": float(np.sqrt(12.0)),
        "frequency_label": f"{np.sqrt(12.0):.2f}",
    },
]


def number_label(value: float) -> str:
    if np.isclose(value, round(value)):
        return str(int(round(value)))
    return f"{value:g}"


def frequency_label(case: dict) -> str:
    return case.get("frequency_label", number_label(case["frequency_hz"]))


def build_paths(case: dict) -> tuple[Path, Path, Path]:
    stem = f"{case['file_index']:02d}_{case['label']}"
    return OUTPUT_DIR / f"{stem}.gif", OUTPUT_DIR / f"{stem}.png", OUTPUT_DIR / f"{stem}_t0.png"


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


def sync_frame_durations(frame_count: int) -> list[int]:
    return [SYNC_FRAME_DURATION_PATTERN_MS[index % len(SYNC_FRAME_DURATION_PATTERN_MS)] for index in range(frame_count)]


def crop_gif_to_box(
    path: Path,
    crop_box: tuple[int, int, int, int] | None,
    durations_override: list[int] | None = None,
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

    if durations_override is not None and len(durations_override) == len(frames):
        durations = durations_override

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=image.info.get("loop", 0),
        disposal=2,
    )


def draw_case(case: dict):
    frequency_hz = case["frequency_hz"]
    observation_time = OBSERVATION_TIME
    current_time = observation_time
    dense_times = np.linspace(0.0, observation_time, 2000)
    output_times = np.linspace(0.0, observation_time, FRAMES)

    dense_values = np.exp(-1j * 2.0 * np.pi * frequency_hz * dense_times)

    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI, facecolor="white")
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(1.0)
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

    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax_complex.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.82", lw=2.2)
    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)
    phasor_trace, = ax_complex.plot([], [], color=PHASOR_GREEN, lw=1.6, alpha=0.55)
    phasor_line, = ax_complex.plot([], [], color=PHASOR_GREEN, lw=2.7)
    phasor_tip, = ax_complex.plot([], [], "o", color=PHASOR_GREEN, ms=8)
    phasor_re_line, = ax_complex.plot([], [], color=RE_COLOR, lw=2.0, alpha=0.95)
    phasor_im_line, = ax_complex.plot([], [], color=IM_COLOR, lw=2.0, alpha=0.95)

    ax_complex.set_xlim(-1.25, 1.25)
    ax_complex.set_ylim(-1.25, 1.25)
    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.grid(alpha=0.18)
    ax_complex.set_xlabel(r"Re$\{x_c(t)\}$", fontsize=LABEL_SIZE)
    ax_complex.set_ylabel(r"Im$\{x_c(t)\}$", fontsize=LABEL_SIZE)
    ax_complex.set_title(r"Continuous analysis phasor $e^{-j2\pi f t}$", pad=12, fontsize=TITLE_SIZE)
    ax_complex.tick_params(labelsize=TICK_SIZE)

    # Keep the visible reference ticks at 0...1 s, but give the 3D renderer
    # room on both sides so neither the first nor the last helix arc is clipped.
    ax_helix.set_xlim(
        -observation_time * X_AXIS_LEFT_PAD_FRACTION,
        observation_time * (1.0 + X_AXIS_RIGHT_PAD_FRACTION),
    )
    ax_helix.set_ylim(-1.1, 1.1)
    ax_helix.set_zlim(-1.1, 1.1)
    ax_helix.set_xlabel(r"$t$ [s]", fontsize=LABEL_SIZE, labelpad=10)
    ax_helix.set_ylabel(r"Re$\{x_c(t)\}$", color=RE_COLOR, fontsize=LABEL_SIZE, labelpad=12)
    ax_helix.set_zlabel(r"Im$\{x_c(t)\}$", color=IM_COLOR, fontsize=LABEL_SIZE, labelpad=6)
    ax_helix.xaxis.set_major_locator(FixedLocator(np.linspace(0.0, observation_time, 5)))
    ax_helix.yaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.zaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.tick_params(axis="x", labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="y", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="z", colors=IM_COLOR, labelsize=TICK_SIZE)

    ax_helix.set_title(
        rf"Complex signal as 3D helix, $f={frequency_label(case)}\,\mathrm{{Hz}}$",
        y=1.035,
        pad=0,
        fontsize=TITLE_SIZE,
    )
    ax_helix.view_init(elev=HELIX_VIEW_ELEV, azim=HELIX_VIEW_AZIM)

    helix_background, = ax_helix.plot(
        dense_times,
        dense_values.real,
        dense_values.imag,
        color="0.85",
        lw=1.6,
        zorder=10,
        clip_on=False,
    )
    helix_trace, = ax_helix.plot([], [], [], color=PHASOR_GREEN, lw=2.1, zorder=30, clip_on=False)
    helix_point, = ax_helix.plot([], [], [], "o", color=PHASOR_GREEN, ms=6, zorder=32, clip_on=False)
    helix_re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=2.0, alpha=0.95, zorder=31, clip_on=False)
    helix_im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=2.0, alpha=0.95, zorder=31, clip_on=False)

    def draw_state(time_value: float):
        current_value = np.exp(-1j * 2.0 * np.pi * frequency_hz * time_value)
        past_times = np.linspace(0.0, time_value, max(2, int(900 * max(time_value, 0.001) / observation_time)))
        past_values = np.exp(-1j * 2.0 * np.pi * frequency_hz * past_times)

        phasor_trace.set_data(past_values.real, past_values.imag)
        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_tip.set_data([current_value.real], [current_value.imag])
        phasor_re_line.set_data([0.0, current_value.real], [0.0, 0.0])
        phasor_im_line.set_data([current_value.real, current_value.real], [0.0, current_value.imag])

        helix_trace.set_data_3d(past_times, past_values.real, past_values.imag)
        helix_point.set_data_3d([time_value], [current_value.real], [current_value.imag])
        helix_re_stem.set_data_3d([time_value, time_value], [0.0, current_value.real], [0.0, 0.0])
        helix_im_stem.set_data_3d(
            [time_value, time_value],
            [current_value.real, current_value.real],
            [0.0, current_value.imag],
        )

        return (
            phasor_trace,
            phasor_line,
            phasor_tip,
            phasor_re_line,
            phasor_im_line,
            helix_trace,
            helix_point,
            helix_re_stem,
            helix_im_stem,
        )

    draw_state(current_time)

    return fig, output_times, draw_state


def export_case(case: dict) -> tuple[Path | None, Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    gif_path, png_path, t0_path = build_paths(case)
    fig, output_times, draw_state = draw_case(case)

    draw_state(0.0)
    fig.canvas.draw()
    fig.canvas.print_png(str(t0_path.resolve()))
    crop_png_margins(t0_path)

    draw_state(OBSERVATION_TIME)
    fig.canvas.draw()
    fig.canvas.print_png(str(png_path.resolve()))
    crop_box = crop_png_margins(png_path)

    if EXPORT_GIFS:
        animation = FuncAnimation(
            fig,
            lambda frame_index: draw_state(output_times[frame_index]),
            frames=len(output_times),
            interval=1000 / FPS,
            blit=False,
        )
        animation.save(str(gif_path.resolve()), writer=PillowWriter(fps=FPS))
        crop_gif_to_box(gif_path, crop_box, sync_frame_durations(len(output_times)))
    else:
        gif_path = None

    plt.close(fig)
    return gif_path, png_path, t0_path


def main():
    exported_items = []
    for case in EXPORT_CASES:
        gif_path, png_path, t0_path = export_case(case)
        exported_items.append((case["frequency_hz"], gif_path, png_path, t0_path))

    print("Saved 4A0 continuous phasor/helix cases:")
    for frequency_hz, gif_path, png_path, t0_path in exported_items:
        print(f"  f = {number_label(frequency_hz)} Hz")
        if gif_path is not None:
            print(f"    GIF: {gif_path}")
        else:
            print("    GIF: skipped")
        print(f"    PNG: {png_path}")
        print(f"    PNG t=0: {t0_path}")


if __name__ == "__main__":
    main()
