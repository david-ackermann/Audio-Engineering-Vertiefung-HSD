from pathlib import Path
from fractions import Fraction

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
    / "04_diskrete_kreisfrequenz"
    / "04A"
    / "04A2_dft_basis_als_diskreter_phasor"
)

FPS = 8
FRAMES_PER_SAMPLE = 6
FIGSIZE = (17.2, 6.9)
FIG_DPI = 100
EXPORT_GIFS = True

PHASOR_GREEN = "#26a043"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
TITLE_SIZE = 18
LABEL_SIZE = 20
TICK_SIZE = 16
INFO_TEXT_SIZE = 16
HELIX_BOX_ASPECT = (3.9, 1.55, 1.55)


EXPORT_CASES = [
    {
        "file_index": 0,
        "label": "general_f3p46hz_n16",
        "k": float(np.sqrt(12.0)),
        "n": 16,
        "frequency_hz": float(np.sqrt(12.0)),
        "sample_rate_hz": 16,
        "frequency_label": f"{np.sqrt(12.0):.2f}",
        "k_label": f"{np.sqrt(12.0):.2f}",
        "omega_label": r"0.43\pi",
        "is_dft_bin": False,
    },
    {
        "file_index": 1,
        "label": "k1_n16",
        "k": 1,
        "n": 16,
        "title": "Fixed N = 16: k = 1",
    },
    {
        "file_index": 2,
        "label": "k4_n16",
        "k": 4,
        "n": 16,
        "title": "Fixed N = 16: k = 4",
    },
    {
        "file_index": 3,
        "label": "k7_n16",
        "k": 7,
        "n": 16,
        "title": "Fixed N = 16: k = 7",
    },
    {
        "file_index": 4,
        "label": "k9_n16",
        "k": 9,
        "n": 16,
        "title": "Fixed N = 16: k = 9",
    },
    {
        "file_index": 5,
        "label": "k16_n16",
        "k": 16,
        "n": 16,
        "title": "Fixed N = 16: k = 16",
    },
    {
        "file_index": 6,
        "label": "k16_n32",
        "k": 16,
        "n": 32,
        "title": "Fixed N = 32: k = 16",
    },
]


def n_tick_step(block_length: int) -> int:
    if block_length <= 8:
        return 1
    if block_length <= 16:
        return 2
    return 4


def build_paths(case: dict) -> tuple[Path, Path, Path]:
    stem = f"{case['file_index']:02d}_{case['label']}"
    gif_path = OUTPUT_DIR / f"{stem}.gif"
    preview_path = OUTPUT_DIR / f"{stem}_preview.png"
    preview_n0_path = OUTPUT_DIR / f"{stem}_preview_n0.png"
    return gif_path, preview_path, preview_n0_path


def build_endpoint_preview_path(case: dict, endpoint_index: int) -> Path:
    stem = f"{case['file_index']:02d}_{case['label']}"
    return OUTPUT_DIR / f"{stem}_preview_n{endpoint_index}.png"


def number_label(value: float) -> str:
    if np.isclose(value, round(value)):
        return str(int(round(value)))
    return f"{value:g}"


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
        x_values, y_start_values, y_end_values, z_start_values, z_end_values
    ):
        x_segments.extend([x_value, x_value, np.nan])
        y_segments.extend([y_start, y_end, np.nan])
        z_segments.extend([z_start, z_end, np.nan])

    return np.array(x_segments), np.array(y_segments), np.array(z_segments)


def omega_fraction_latex(k: float, n: int) -> str:
    frac = Fraction(2.0 * k / n).limit_denominator(128)
    numerator = frac.numerator
    denominator = frac.denominator
    sign = "-" if numerator < 0 else ""
    numerator = abs(numerator)

    if numerator == 0:
        return "0"
    if denominator == 1:
        if numerator == 1:
            return rf"{sign}\pi"
        return rf"{sign}{numerator}\pi"
    if numerator == 1:
        return rf"{sign}\frac{{\pi}}{{{denominator}}}"
    return rf"{sign}\frac{{{numerator}\pi}}{{{denominator}}}"


def plot_labels(case: dict, omega_label: str) -> tuple[str, str, str, str, str, str]:
    block_length = case["n"]
    bin_index = case["k"]
    is_dft_bin = case.get("is_dft_bin", True)

    if is_dft_bin:
        complex_title = r"DFT basis $b_k[n] = e^{-j \Omega_k n}$"
        helix_title = rf"Fixed $N = {block_length}$: $k = {bin_index}$, $\Omega_k = {omega_label}$"
        re_label = r"Re$\{b_k[n]\}$"
        im_label = r"Im$\{b_k[n]\}$"
        helix_re_label = r"Re$\{b_k[n]\}$"
        helix_im_label = r"Im$\{b_k[n]\}$"
    else:
        frequency_hz = case["frequency_hz"]
        sample_rate_hz = case["sample_rate_hz"]
        frequency_label = case.get("frequency_label", number_label(frequency_hz))
        k_label = case.get("k_label", number_label(bin_index))
        complex_title = r"General discrete circular motion $b_\Omega[n] = e^{-j\Omega n}$"
        helix_title = (
            rf"$f={frequency_label}\,\mathrm{{Hz}}$, "
            rf"$f_s={number_label(sample_rate_hz)}\,\mathrm{{Hz}}$, "
            rf"$N={block_length}$, $k_\mathrm{{eff}}={k_label}$, "
            rf"$\Omega={omega_label}$"
        )
        re_label = r"Re$\{b_\Omega[n]\}$"
        im_label = r"Im$\{b_\Omega[n]\}$"
        helix_re_label = r"Re$\{b_\Omega[n]\}$"
        helix_im_label = r"Im$\{b_\Omega[n]\}$"

    return complex_title, helix_title, re_label, im_label, helix_re_label, helix_im_label


def draw_case(case: dict):
    block_length = case["n"]
    bin_index = case["k"]
    is_dft_bin = case.get("is_dft_bin", True)
    show_block_endpoint = not is_dft_bin or case.get("show_block_endpoint", False)
    omega_label = case.get("omega_label", omega_fraction_latex(bin_index, block_length))
    complex_title, helix_title, re_label, im_label, helix_re_label, helix_im_label = plot_labels(
        case,
        omega_label,
    )

    sample_count = block_length + 1 if show_block_endpoint else block_length
    sample_indices = np.arange(sample_count, dtype=float)
    if show_block_endpoint:
        frame_progress = np.linspace(0.0, float(block_length), block_length * FRAMES_PER_SAMPLE)
        frame_indices = np.floor(frame_progress).astype(int)
        frame_indices[-1] = block_length
    else:
        frame_indices = np.repeat(np.arange(block_length), FRAMES_PER_SAMPLE)

    sample_values = np.exp(-1j * 2.0 * np.pi * bin_index * sample_indices / block_length)
    zero_values = np.zeros_like(sample_indices)

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
    ax_complex.plot(sample_values.real, sample_values.imag, "o", color="0.75", ms=6)
    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)
    phasor_line, = ax_complex.plot([], [], color=PHASOR_GREEN, lw=2.7)
    phasor_tip, = ax_complex.plot([], [], "o", color=PHASOR_GREEN, ms=8)
    phasor_trace, = ax_complex.plot([], [], color=PHASOR_GREEN, lw=1.6, ls="--")
    phasor_re_line, = ax_complex.plot([], [], color=RE_COLOR, lw=2.0, alpha=0.95)
    phasor_im_line, = ax_complex.plot([], [], color=IM_COLOR, lw=2.0, alpha=0.95)
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
    ax_complex.set_xlim(-1.25, 1.25)
    ax_complex.set_ylim(-1.25, 1.25)
    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.grid(alpha=0.18)
    ax_complex.set_xlabel(re_label, fontsize=LABEL_SIZE)
    ax_complex.set_ylabel(im_label, fontsize=LABEL_SIZE)
    ax_complex.set_title(complex_title, pad=12, fontsize=TITLE_SIZE)
    ax_complex.tick_params(labelsize=TICK_SIZE)

    helix_stem_x, helix_stem_y, helix_stem_z = build_stem_segments(
        sample_indices,
        zero_values,
        sample_values.real,
        zero_values,
        sample_values.imag,
    )
    re_stem_x, re_stem_y, re_stem_z = build_stem_segments(
        sample_indices,
        zero_values,
        sample_values.real,
        zero_values,
        zero_values,
    )
    im_stem_x, im_stem_y, im_stem_z = build_stem_segments(
        sample_indices,
        zero_values,
        zero_values,
        zero_values,
        sample_values.imag,
    )

    ax_helix.plot(re_stem_x, re_stem_y, re_stem_z, color=RE_COLOR, lw=1.0, alpha=0.18, zorder=5)
    ax_helix.plot(im_stem_x, im_stem_y, im_stem_z, color=IM_COLOR, lw=1.0, alpha=0.18, zorder=5)
    ax_helix.plot(sample_indices, sample_values.real, zero_values, "o", color=RE_COLOR, alpha=0.24, ms=4, zorder=6)
    ax_helix.plot(sample_indices, zero_values, sample_values.imag, "o", color=IM_COLOR, alpha=0.24, ms=4, zorder=6)

    re_point, = ax_helix.plot([], [], [], "o", color=RE_COLOR, ms=5, zorder=28, clip_on=False)
    im_point, = ax_helix.plot([], [], [], "o", color=IM_COLOR, ms=5, zorder=28, clip_on=False)
    re_stem, = ax_helix.plot([], [], [], color=RE_COLOR, lw=2.0, alpha=0.95, zorder=27, clip_on=False)
    im_stem, = ax_helix.plot([], [], [], color=IM_COLOR, lw=2.0, alpha=0.95, zorder=27, clip_on=False)
    helix_stem_history, = ax_helix.plot([], [], [], color=PHASOR_GREEN, lw=1.7, zorder=30, clip_on=False)
    helix_history_line, = ax_helix.plot([], [], [], color=PHASOR_GREEN, lw=1.4, ls="--", zorder=31, clip_on=False)
    helix_trace, = ax_helix.plot([], [], [], linestyle="None", marker="o", color=PHASOR_GREEN, ms=5, zorder=32, clip_on=False)
    helix_point, = ax_helix.plot([], [], [], "o", color=PHASOR_GREEN, ms=6, zorder=34, clip_on=False)
    helix_stem, = ax_helix.plot([], [], [], color=PHASOR_GREEN, lw=2.0, alpha=0.95, zorder=33, clip_on=False)

    ax_helix.set_xlim(0.0, sample_indices[-1])
    ax_helix.set_ylim(-1.1, 1.1)
    ax_helix.set_zlim(-1.1, 1.1)
    ax_helix.set_xlabel("n", fontsize=LABEL_SIZE, labelpad=10)
    ax_helix.set_ylabel(helix_re_label, color=RE_COLOR, fontsize=LABEL_SIZE, labelpad=12)
    ax_helix.set_zlabel(helix_im_label, color=IM_COLOR, fontsize=LABEL_SIZE, labelpad=6)
    ax_helix.xaxis.set_major_locator(MultipleLocator(n_tick_step(block_length)))
    ax_helix.yaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.zaxis.set_major_locator(MultipleLocator(0.5))
    ax_helix.tick_params(axis="x", labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="y", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax_helix.tick_params(axis="z", colors=IM_COLOR, labelsize=TICK_SIZE)
    ax_helix.set_title(
        helix_title,
        y=1.035,
        pad=0,
        fontsize=TITLE_SIZE,
    )
    ax_helix.view_init(elev=24, azim=-62)

    def draw_state(frame_index: int):
        sample_index = int(frame_indices[frame_index])
        current_value = sample_values[sample_index]

        past_indices = sample_indices[: sample_index + 1]
        past_re_values = sample_values.real[: sample_index + 1]
        past_im_values = sample_values.imag[: sample_index + 1]

        continuous_n = np.linspace(0.0, float(sample_index), max(2, 40 * (sample_index + 1)))
        continuous_values = np.exp(-1j * 2.0 * np.pi * bin_index * continuous_n / block_length)

        phasor_line.set_data([0.0, current_value.real], [0.0, current_value.imag])
        phasor_tip.set_data([current_value.real], [current_value.imag])
        phasor_trace.set_data(continuous_values.real, continuous_values.imag)
        phasor_re_line.set_data([0.0, current_value.real], [0.0, 0.0])
        phasor_im_line.set_data([current_value.real, current_value.real], [0.0, current_value.imag])
        sample_text.set_text(f"n = {sample_index}")

        zeros_past = np.zeros_like(past_indices)
        past_helix_stem_x, past_helix_stem_y, past_helix_stem_z = build_stem_segments(
            past_indices,
            zeros_past,
            past_re_values,
            zeros_past,
            past_im_values,
        )

        helix_stem_history.set_data_3d(past_helix_stem_x, past_helix_stem_y, past_helix_stem_z)
        helix_history_line.set_data_3d(
            continuous_n,
            continuous_values.real,
            continuous_values.imag,
        )
        helix_trace.set_data_3d(past_indices, past_re_values, past_im_values)
        helix_point.set_data_3d([sample_index], [current_value.real], [current_value.imag])
        re_point.set_data_3d([sample_index], [current_value.real], [0.0])
        im_point.set_data_3d([sample_index], [0.0], [current_value.imag])
        helix_stem.set_data_3d([sample_index, sample_index], [0.0, current_value.real], [0.0, current_value.imag])
        re_stem.set_data_3d([sample_index, sample_index], [0.0, current_value.real], [0.0, 0.0])
        im_stem.set_data_3d([sample_index, sample_index], [0.0, 0.0], [0.0, current_value.imag])

        return (
            phasor_line,
            phasor_tip,
            phasor_trace,
            phasor_re_line,
            phasor_im_line,
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


def sync_total_duration_ms(block_length: int) -> int:
    return int(round(block_length * FRAMES_PER_SAMPLE * 1000 / FPS))


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


def export_case(case: dict) -> tuple[Path | None, Path, Path]:
    gif_path, preview_path, preview_n0_path = build_paths(case)
    fig, frame_indices, draw_state = draw_case(case)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    draw_state(0)
    fig.canvas.draw()
    fig.canvas.print_png(str(preview_n0_path.resolve()))
    crop_png_margins(preview_n0_path)

    draw_state(len(frame_indices) - 1)
    fig.canvas.draw()
    fig.canvas.print_png(str(preview_path.resolve()))
    crop_box = crop_png_margins(preview_path)

    if EXPORT_GIFS:
        animation = FuncAnimation(
            fig,
            lambda idx: draw_state(idx),
            frames=len(frame_indices),
            interval=1000 / FPS,
            blit=False,
        )
        writer = PillowWriter(fps=FPS)
        animation.save(str(gif_path.resolve()), writer=writer)
        crop_gif_to_box(gif_path, crop_box, sync_total_duration_ms(case["n"]))
    else:
        gif_path = None
    plt.close(fig)
    return gif_path, preview_path, preview_n0_path


def export_endpoint_preview(case: dict, endpoint_index: int) -> Path:
    endpoint_case = dict(case)
    endpoint_case["show_block_endpoint"] = True

    output_path = build_endpoint_preview_path(case, endpoint_index)
    fig, frame_indices, draw_state = draw_case(endpoint_case)
    draw_state(len(frame_indices) - 1)
    fig.canvas.draw()
    fig.canvas.print_png(str(output_path.resolve()))
    crop_png_margins(output_path)
    plt.close(fig)
    return output_path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    exported_items = []
    for case in EXPORT_CASES:
        gif_path, preview_path, preview_n0_path = export_case(case)
        exported_items.append((case["k"], case["n"], gif_path, preview_path, preview_n0_path))

    k4_case = next(case for case in EXPORT_CASES if case["label"] == "k4_n16")
    k4_endpoint_path = export_endpoint_preview(k4_case, endpoint_index=16)

    print("Saved 4A comparison cases:")
    for bin_index, block_length, gif_path, preview_path, preview_n0_path in exported_items:
        print(f"  k = {number_label(bin_index)}, N = {block_length}")
        if gif_path is not None:
            print(f"    GIF: {gif_path}")
        else:
            print("    GIF: skipped")
        print(f"    PNG: {preview_path}")
        print(f"    PNG n=0: {preview_n0_path}")
    print(f"  k = 4, N = 16 endpoint PNG: {k4_endpoint_path}")


if __name__ == "__main__":
    main()
