from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image, ImageSequence


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_systemfunktion_fir_iir"
)

DPI = 160
IR_DPI = 200
FIGSIZE_IR = (10.5, 4.2)
FIGSIZE_FREQ = (10.5, 4.2)
FIGSIZE_SURFACE = (8.8, 6.2)
FIGSIZE_Z_PLANE_2D = (6.2, 5.6)
NUM_SAMPLES = 15
FREQ_SAMPLE_COUNT = 121
FULL_FREQ_SAMPLE_COUNT = 241
ANIMATION_FPS = 12

TITLE_SIZE = 18
LABEL_SIZE = 18
TICK_SIZE = 14
SURFACE_TITLE_SIZE = 18
SURFACE_LABEL_SIZE = 18
SURFACE_TICK_SIZE = 14
CROP_THRESHOLD = 250
CROP_PAD = 8

BLACK = "0.10"
GREEN = "#66b77a"
BLUE = "#2b7bbb"
ORANGE = "#d98c2f"
GREY = "0.58"
LIGHT_GREY = "0.84"
VERY_LIGHT_GREY = "0.90"
POLE_RED = "#b84a4a"

SURFACE_LIMIT = 1.35
SURFACE_MIN_DB = -25.0
SURFACE_MAX_DB = 25.0
RADIUS_CURVES = (1.0, 0.8, 0.6, 0.4, 0.2, 0.0)
RADIUS_STEP_FILENAMES = {
    0.8: "11_frequency_response_radius_r_0_8.png",
    0.6: "12_frequency_response_radius_r_0_6.png",
    0.4: "13_frequency_response_radius_r_0_4.png",
    0.2: "14_frequency_response_radius_r_0_2.png",
    0.0: "15_frequency_response_radius_r_0_0.png",
}
RADIUS_EPSILON = 1.0e-6

FREQ_LEFT_INCH = FIGSIZE_FREQ[0] * 0.10
FREQ_AXIS_WIDTH_INCH = FIGSIZE_FREQ[0] * (0.98 - 0.10)
FREQ_RIGHT_INCH = FIGSIZE_FREQ[0] * (1.0 - 0.98)
FREQ_BOTTOM = 0.19
FREQ_TOP = 0.82

FIR_NOTCH_B = np.array([0.5, 0.0, 0.5])
FIR_VARIANT_B = np.array([1.0, -0.6, 0.36])
FIR_A = np.array([1.0])
FIR_DELAY_POLE_2D = (0.0 + 0.0j,)

IIR_R = 0.90
IIR_OMEGA0 = np.pi / 3.0
IIR_B = np.array([1.00])
IIR_A = np.array([1.0, -2.0 * IIR_R * np.cos(IIR_OMEGA0), IIR_R**2])

BIQUAD_HP_B = np.array([0.68930617, -1.37861234, 0.68930617])
BIQUAD_HP_A = np.array([1.0, -1.27963242, 0.47759225])

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class SystemCase:
    folder: str
    ir_title: str
    surface_title: str
    b: np.ndarray
    a: np.ndarray
    zeros: tuple[complex, ...]
    poles: tuple[complex, ...]
    y_limits: tuple[float, float]
    y_ticks: tuple[float, ...]


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_file in OUTPUT_DIR.rglob("*"):
        if output_file.is_file() and output_file.suffix.lower() in {".png", ".gif"}:
            output_file.unlink()
    for output_dir in sorted(OUTPUT_DIR.rglob("*"), reverse=True):
        if output_dir.is_dir():
            try:
                output_dir.rmdir()
            except OSError:
                pass


def impulse_response(b: np.ndarray, a: np.ndarray, num_samples: int) -> np.ndarray:
    x_values = np.zeros(num_samples + 1)
    y_values = np.zeros(num_samples + 1)
    x_values[0] = 1.0

    for n_value in range(num_samples + 1):
        acc = 0.0
        for k, b_value in enumerate(b):
            if n_value - k >= 0:
                acc += b_value * x_values[n_value - k]
        for r_value in range(1, len(a)):
            if n_value - r_value >= 0:
                acc -= a[r_value] * y_values[n_value - r_value]
        y_values[n_value] = acc
    return y_values


def response_z(b: np.ndarray, a: np.ndarray, z_values: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        numerator = np.zeros_like(z_values, dtype=complex)
        denominator = np.ones_like(z_values, dtype=complex)
        for k, b_value in enumerate(b):
            numerator += b_value * z_values ** (-k)
        for r_value in range(1, len(a)):
            denominator += a[r_value] * z_values ** (-r_value)
        return numerator / denominator


def magnitude_db(values: np.ndarray) -> np.ndarray:
    magnitude = np.abs(values)
    magnitude = np.where(np.isfinite(magnitude), magnitude, np.nan)
    return np.clip(20.0 * np.log10(np.maximum(magnitude, 1.0e-9)), SURFACE_MIN_DB, SURFACE_MAX_DB)


def export_impulse_response(system_case: SystemCase) -> None:
    output_dir = OUTPUT_DIR / system_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    n_values = np.arange(NUM_SAMPLES + 1)
    h_values = impulse_response(system_case.b, system_case.a, NUM_SAMPLES)

    fig_ir, ax_ir = plt.subplots(figsize=FIGSIZE_IR, dpi=IR_DPI, facecolor="white")
    fig_ir.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    ax_ir.vlines(n_values, 0.0, h_values, color=GREEN, lw=2.2, alpha=1.0, zorder=3)
    ax_ir.scatter(
        n_values,
        h_values,
        s=7.0**2,
        color=GREEN,
        edgecolor="white",
        linewidth=0.9,
        zorder=4,
        alpha=1.0,
        clip_on=False,
    )
    ax_ir.axhline(0.0, color=BLACK, lw=1.2)
    ax_ir.set_axisbelow(True)
    ax_ir.set_xlim(-0.5, NUM_SAMPLES + 0.5)
    ax_ir.set_ylim(*system_case.y_limits)
    ax_ir.set_xticks([0, 3, 6, 9, 12, 15])
    ax_ir.set_yticks(list(system_case.y_ticks))
    ax_ir.set_xlabel("Sample index n", fontsize=24)
    ax_ir.set_ylabel(r"$h[n]$", fontsize=24)
    ax_ir.set_title(system_case.ir_title, fontsize=22, pad=10)
    ax_ir.grid(alpha=0.25)
    ax_ir.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_ir.spines[spine].set_visible(False)
    fig_ir.savefig(output_dir / "01_impulse_response.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_ir)


def nyquist_frequency_response(system_case: SystemCase) -> tuple[np.ndarray, np.ndarray]:
    omega_values = np.linspace(0.0, np.pi, FREQ_SAMPLE_COUNT)
    z_values = np.exp(1j * omega_values)
    response_db = magnitude_db(response_z(system_case.b, system_case.a, z_values))
    return omega_values, response_db


def nyquist_linear_frequency_response(system_case: SystemCase) -> tuple[np.ndarray, np.ndarray]:
    omega_values = np.linspace(0.0, np.pi, FREQ_SAMPLE_COUNT)
    z_values = np.exp(1j * omega_values)
    response_linear = np.abs(response_z(system_case.b, system_case.a, z_values))
    response_linear = np.where(np.isfinite(response_linear), response_linear, np.nan)
    return omega_values, response_linear


def full_frequency_response(system_case: SystemCase) -> tuple[np.ndarray, np.ndarray]:
    omega_values = np.linspace(0.0, 2.0 * np.pi, FULL_FREQ_SAMPLE_COUNT)
    z_values = np.exp(1j * omega_values)
    response_db = magnitude_db(response_z(system_case.b, system_case.a, z_values))
    return omega_values, response_db


def frequency_figure_width(normalized_span: float) -> float:
    return FREQ_LEFT_INCH + normalized_span * FREQ_AXIS_WIDTH_INCH + FREQ_RIGHT_INCH


def adjust_frequency_figure(fig, normalized_span: float) -> None:
    width, _ = fig.get_size_inches()
    fig.subplots_adjust(
        left=FREQ_LEFT_INCH / width,
        right=1.0 - FREQ_RIGHT_INCH / width,
        bottom=FREQ_BOTTOM,
        top=FREQ_TOP,
    )


def setup_frequency_axis(ax_freq, title: str, *, normalized_span: float = 1.0) -> None:
    ax_freq.set_title(title, fontsize=22, pad=10)
    ax_freq.set_xlim(0.0, normalized_span)
    ax_freq.set_ylim(SURFACE_MIN_DB, SURFACE_MAX_DB)
    if np.isclose(normalized_span, 1.0):
        ax_freq.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    else:
        ax_freq.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0])
    ax_freq.set_yticks([-25.0, 0.0, 25.0])
    ax_freq.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=24)
    ax_freq.set_ylabel("Magnitude [dB]", fontsize=24)
    ax_freq.grid(alpha=0.25)
    ax_freq.set_axisbelow(True)
    ax_freq.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_freq.spines[spine].set_visible(False)


def setup_linear_frequency_axis(ax_freq, title: str, response_linear: np.ndarray) -> None:
    y_max = float(np.nanmax(response_linear))
    if y_max <= 1.05:
        y_limit = 1.05
        y_ticks = [0.0, 0.5, 1.0]
    else:
        y_limit = float(np.ceil(y_max * 1.08))
        y_ticks = [0.0, 0.5 * y_limit, y_limit]

    ax_freq.set_title(title, fontsize=22, pad=10)
    ax_freq.set_xlim(0.0, 1.0)
    ax_freq.set_ylim(0.0, y_limit)
    ax_freq.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax_freq.set_yticks(y_ticks)
    ax_freq.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=24)
    ax_freq.set_ylabel(r"$|H(e^{j\Omega})|$", fontsize=24)
    ax_freq.grid(alpha=0.25)
    ax_freq.set_axisbelow(True)
    ax_freq.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_freq.spines[spine].set_visible(False)


def plot_full_frequency_response_2d(ax_freq, normalized_frequency: np.ndarray, response_db: np.ndarray) -> None:
    positive = normalized_frequency <= 1.0
    negative = normalized_frequency >= 1.0
    ax_freq.plot(normalized_frequency[positive], response_db[positive], color=GREEN, lw=3.0)
    ax_freq.plot(normalized_frequency[negative], response_db[negative], color=BLUE, lw=3.0)


def export_frequency_response(system_case: SystemCase) -> None:
    output_dir = OUTPUT_DIR / system_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    omega_linear, response_linear = nyquist_linear_frequency_response(system_case)
    normalized_linear = omega_linear / np.pi
    fig_linear, ax_linear = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_linear, 1.0)
    ax_linear.plot(normalized_linear, response_linear, color=GREEN, lw=3.0)
    setup_linear_frequency_axis(ax_linear, "Frequency response", response_linear)
    fig_linear.savefig(output_dir / "02_frequency_response_linear.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_linear)

    omega_values, response_db = nyquist_frequency_response(system_case)
    normalized_frequency = omega_values / np.pi

    fig_freq, ax_freq = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_freq, 1.0)
    ax_freq.plot(normalized_frequency, response_db, color=GREEN, lw=3.0)
    setup_frequency_axis(ax_freq, "Frequency response")
    fig_freq.savefig(output_dir / "03_frequency_response_full.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_freq)

    fig_gif, ax_gif = plt.subplots(figsize=FIGSIZE_FREQ, dpi=DPI, facecolor="white")
    adjust_frequency_figure(fig_gif, 1.0)
    ax_gif.plot(normalized_frequency, response_db, color=LIGHT_GREY, lw=3.0, zorder=1)
    (active_line,) = ax_gif.plot([], [], color=GREEN, lw=3.2, zorder=2)
    active_dot = ax_gif.scatter(
        [],
        [],
        s=7.5**2,
        color=GREEN,
        edgecolor="white",
        linewidth=0.9,
        zorder=3,
        clip_on=False,
    )
    setup_frequency_axis(ax_gif, "Frequency response")

    def update(frame_index: int):
        active_line.set_data(normalized_frequency[: frame_index + 1], response_db[: frame_index + 1])
        active_dot.set_offsets([[normalized_frequency[frame_index], response_db[frame_index]]])
        return active_line, active_dot

    update(0)
    fig_gif.savefig(output_dir / "04_frequency_response_build_start.png", dpi=DPI, facecolor="white")
    animation = FuncAnimation(fig_gif, update, frames=len(omega_values), interval=1000 / ANIMATION_FPS, blit=True)
    animation.save(output_dir / "05_frequency_response_build.gif", writer=PillowWriter(fps=ANIMATION_FPS))
    plt.close(fig_gif)

    omega_full, response_full_db = full_frequency_response(system_case)
    normalized_full = omega_full / np.pi
    extended_width = frequency_figure_width(2.0)
    fig_full, ax_full = plt.subplots(figsize=(extended_width, FIGSIZE_FREQ[1]), dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_full, 2.0)
    plot_full_frequency_response_2d(ax_full, normalized_full, response_full_db)
    setup_frequency_axis(ax_full, "Frequency response", normalized_span=2.0)
    fig_full.savefig(output_dir / "06_frequency_response_full_two_periods.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_full)


def setup_surface_axis(ax_surface, title: str = "z-Plane") -> None:
    ax_surface.set_title("z-Plane", fontsize=SURFACE_TITLE_SIZE, y=1.005, pad=0)
    ax_surface.set_xlabel(r"Re$\{z\}$", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_ylabel(r"Im$\{z\}$", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_zlabel(r"$|H(z)|$ in dB", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_xlim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax_surface.set_ylim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax_surface.set_zlim(SURFACE_MIN_DB, SURFACE_MAX_DB)
    ax_surface.set_xticks([-1.0, 0.0, 1.0])
    ax_surface.set_yticks([-1.0, 0.0, 1.0])
    ax_surface.set_zticks([-25.0, 0.0, 25.0])
    ax_surface.tick_params(labelsize=SURFACE_TICK_SIZE)
    ax_surface.view_init(elev=25, azim=-58)
    for axis in (ax_surface.xaxis, ax_surface.yaxis, ax_surface.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
        axis._axinfo["grid"]["color"] = (0.82, 0.82, 0.82, 0.75)
    try:
        ax_surface.set_box_aspect((1.9, 1.9, 1.25), zoom=1.08)
    except (TypeError, AttributeError):
        ax_surface.set_box_aspect((1.9, 1.9, 1.25))


def export_unit_circle_response_gif(system_case: SystemCase) -> None:
    output_dir = OUTPUT_DIR / system_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    omega_values, response_db = nyquist_frequency_response(system_case)
    unit_circle = np.exp(1j * omega_values)
    theta_reference = np.linspace(0.0, 2.0 * np.pi, 900)
    reference_circle = np.exp(1j * theta_reference)

    fig_curve = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
    ax_curve = fig_curve.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig_curve.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)

    ax_curve.plot(
        reference_circle.real,
        reference_circle.imag,
        np.full_like(theta_reference, SURFACE_MIN_DB),
        color=LIGHT_GREY,
        lw=2.2,
        alpha=0.82,
        zorder=0,
    )
    ax_curve.plot(
        unit_circle.real,
        unit_circle.imag,
        response_db,
        color=LIGHT_GREY,
        lw=3.0,
        alpha=0.86,
        zorder=1,
    )
    (active_projection,) = ax_curve.plot([], [], [], color=ORANGE, lw=3.0, alpha=0.96, zorder=2)
    active_projection_point = ax_curve.scatter(
        [],
        [],
        [],
        s=7.5**2,
        color=ORANGE,
        edgecolor="white",
        linewidth=0.9,
        zorder=3,
    )
    (active_projection_vector,) = ax_curve.plot([], [], [], color=ORANGE, lw=3.0, alpha=0.98, zorder=4)
    (active_projection_head_left,) = ax_curve.plot([], [], [], color=ORANGE, lw=3.0, alpha=0.98, zorder=4)
    (active_projection_head_right,) = ax_curve.plot([], [], [], color=ORANGE, lw=3.0, alpha=0.98, zorder=4)
    (active_curve,) = ax_curve.plot([], [], [], color=GREEN, lw=3.3, zorder=3)
    active_point = ax_curve.scatter([], [], [], s=7.5**2, color=GREEN, edgecolor="white", linewidth=0.9, zorder=4)

    setup_surface_axis(ax_curve, "Frequency response on the unit circle")

    def update(frame_index: int) -> None:
        current_x = float(unit_circle.real[frame_index])
        current_y = float(unit_circle.imag[frame_index])
        active_projection.set_data(unit_circle.real[: frame_index + 1], unit_circle.imag[: frame_index + 1])
        active_projection.set_3d_properties(np.full(frame_index + 1, SURFACE_MIN_DB))
        active_projection_point._offsets3d = (
            [current_x],
            [current_y],
            [SURFACE_MIN_DB],
        )
        vector_length = max(np.hypot(current_x, current_y), 1.0e-9)
        unit_x = current_x / vector_length
        unit_y = current_y / vector_length
        normal_x = -unit_y
        normal_y = unit_x
        head_length = 0.15
        head_width = 0.075
        head_base_x = current_x - head_length * unit_x
        head_base_y = current_y - head_length * unit_y
        head_left_x = head_base_x + head_width * normal_x
        head_left_y = head_base_y + head_width * normal_y
        head_right_x = head_base_x - head_width * normal_x
        head_right_y = head_base_y - head_width * normal_y

        active_projection_vector.set_data([0.0, current_x], [0.0, current_y])
        active_projection_vector.set_3d_properties([SURFACE_MIN_DB, SURFACE_MIN_DB])
        active_projection_head_left.set_data([head_left_x, current_x], [head_left_y, current_y])
        active_projection_head_left.set_3d_properties([SURFACE_MIN_DB, SURFACE_MIN_DB])
        active_projection_head_right.set_data([head_right_x, current_x], [head_right_y, current_y])
        active_projection_head_right.set_3d_properties([SURFACE_MIN_DB, SURFACE_MIN_DB])
        active_curve.set_data(unit_circle.real[: frame_index + 1], unit_circle.imag[: frame_index + 1])
        active_curve.set_3d_properties(response_db[: frame_index + 1])
        active_point._offsets3d = (
            [current_x],
            [current_y],
            [response_db[frame_index]],
        )

    frames: list[Image.Image] = []
    for frame_index in range(len(omega_values)):
        update(frame_index)
        fig_curve.canvas.draw()
        width, height = fig_curve.canvas.get_width_height()
        rgba = np.array(fig_curve.canvas.buffer_rgba(), dtype=np.uint8).reshape((height, width, 4))
        if frame_index == 0:
            Image.fromarray(rgba.copy()).convert("RGB").save(
                output_dir / "07_frequency_response_unit_circle_start.png"
            )
        if frame_index == len(omega_values) - 1:
            Image.fromarray(rgba.copy()).convert("RGB").save(
                output_dir / "09_frequency_response_unit_circle_end.png"
            )
        # Prevent GIF encoders from merging visually identical clipped frames.
        rgba[0:2, 0:2, :3] = (
            frame_index % 256,
            (frame_index * 37) % 256,
            (frame_index * 73) % 256,
        )
        frames.append(Image.fromarray(rgba).convert("RGB"))

    frames[0].save(
        output_dir / "08_frequency_response_unit_circle_build.gif",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / ANIMATION_FPS),
        loop=0,
        disposal=2,
        optimize=False,
    )
    plt.close(fig_curve)


def plot_split_3d_curve(
    ax_surface,
    z_values: np.ndarray,
    curve_db: np.ndarray,
    omega_values: np.ndarray,
    *,
    lw: float,
    alpha: float,
    zorder: int,
) -> None:
    positive = omega_values <= np.pi
    negative = omega_values >= np.pi
    ax_surface.plot(
        z_values.real[positive],
        z_values.imag[positive],
        curve_db[positive],
        color=GREEN,
        lw=lw,
        alpha=alpha,
        zorder=zorder,
    )
    ax_surface.plot(
        z_values.real[negative],
        z_values.imag[negative],
        curve_db[negative],
        color=BLUE,
        lw=lw,
        alpha=alpha,
        zorder=zorder,
    )


def radius_projection(
    radius: float,
    omega_values: np.ndarray,
) -> np.ndarray:
    return radius * np.exp(1j * omega_values)


def draw_radius_projection_circle(
    ax_surface,
    radius: float,
    omega_values: np.ndarray,
    *,
    color: str,
    lw: float,
    alpha: float,
    zorder: int,
) -> None:
    if radius == 0.0:
        ax_surface.scatter(
            [0.0],
            [0.0],
            [SURFACE_MIN_DB],
            s=58,
            color=color,
            edgecolor="white",
            linewidth=0.8,
            alpha=alpha,
            zorder=zorder,
        )
        return

    projection = radius_projection(radius, omega_values)
    ax_surface.plot(
        projection.real,
        projection.imag,
        np.full_like(omega_values, SURFACE_MIN_DB),
        color=color,
        lw=lw,
        alpha=alpha,
        zorder=zorder,
    )


def response_db_for_radius(
    system_case: SystemCase,
    radius: float,
    omega_values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    eval_radius = max(radius, RADIUS_EPSILON)
    eval_z = radius_projection(eval_radius, omega_values)
    plot_z = radius_projection(radius, omega_values)
    radius_response_db = magnitude_db(response_z(system_case.b, system_case.a, eval_z))
    return plot_z, radius_response_db


def export_full_circle_response_frames(system_case: SystemCase) -> None:
    output_dir = OUTPUT_DIR / system_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    omega_values, unit_response_db = full_frequency_response(system_case)
    unit_circle = np.exp(1j * omega_values)

    def export_curve_frame(filename: str, *, include_radius_curves: bool) -> None:
        fig_curve = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
        ax_curve = fig_curve.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
        fig_curve.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)

        for radius in ([1.0, *RADIUS_CURVES[1:]] if include_radius_curves else [1.0]):
            if include_radius_curves:
                circle_color = VERY_LIGHT_GREY if radius < 1.0 else LIGHT_GREY
                circle_lw = 1.4 if radius < 1.0 else 2.2
                circle_alpha = 0.70 if radius < 1.0 else 0.82
            else:
                circle_color = ORANGE
                circle_lw = 3.0
                circle_alpha = 0.96
            draw_radius_projection_circle(
                ax_curve,
                radius,
                omega_values,
                color=circle_color,
                lw=circle_lw,
                alpha=circle_alpha,
                zorder=0,
            )

        if include_radius_curves:
            for radius in RADIUS_CURVES[1:]:
                plot_z, radius_response_db = response_db_for_radius(system_case, radius, omega_values)
                if radius == 0.0:
                    ax_curve.scatter(
                        [0.0],
                        [0.0],
                        [radius_response_db[0]],
                        s=54,
                        color=GREY,
                        edgecolor="white",
                        linewidth=0.8,
                        alpha=0.78,
                        zorder=2,
                    )
                else:
                    plot_split_3d_curve(
                        ax_curve,
                        plot_z,
                        radius_response_db,
                        omega_values,
                        lw=2.1,
                        alpha=0.52,
                        zorder=2,
                    )

        plot_split_3d_curve(
            ax_curve,
            unit_circle,
            unit_response_db,
            omega_values,
            lw=3.35,
            alpha=1.0,
            zorder=5,
        )
        setup_surface_axis(ax_curve, "z-Plane")
        fig_curve.savefig(output_dir / filename, dpi=DPI, facecolor="white")
        plt.close(fig_curve)

    export_curve_frame("10_frequency_response_full_unit_circle.png", include_radius_curves=False)

    for active_radius, filename in RADIUS_STEP_FILENAMES.items():
        fig_radius = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
        ax_radius = fig_radius.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
        fig_radius.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)

        active_index = RADIUS_CURVES.index(active_radius)
        shown_radii = RADIUS_CURVES[: active_index + 1]
        previous_radii = shown_radii[:-1]

        for radius in previous_radii:
            draw_radius_projection_circle(
                ax_radius,
                radius,
                omega_values,
                color=ORANGE,
                lw=1.8,
                alpha=0.18,
                zorder=0,
            )
            plot_z, radius_response_db = response_db_for_radius(system_case, radius, omega_values)
            if radius == 0.0:
                ax_radius.scatter(
                    [0.0],
                    [0.0],
                    [radius_response_db[0]],
                    s=46,
                    color=ORANGE,
                    edgecolor="white",
                    linewidth=0.8,
                    alpha=0.24,
                    zorder=1,
                )
            else:
                plot_split_3d_curve(
                    ax_radius,
                    plot_z,
                    radius_response_db,
                    omega_values,
                    lw=2.0,
                    alpha=0.20,
                    zorder=1,
                )

        draw_radius_projection_circle(
            ax_radius,
            active_radius,
            omega_values,
            color=ORANGE,
            lw=3.0,
            alpha=0.96,
            zorder=3,
        )

        plot_z, radius_response_db = response_db_for_radius(system_case, active_radius, omega_values)
        if active_radius == 0.0:
            ax_radius.scatter(
                [0.0],
                [0.0],
                [radius_response_db[0]],
                s=64,
                color=ORANGE,
                edgecolor="white",
                linewidth=0.8,
                zorder=5,
            )
        else:
            plot_split_3d_curve(
                ax_radius,
                plot_z,
                radius_response_db,
                omega_values,
                lw=3.15,
                alpha=0.95,
                zorder=5,
            )

        setup_surface_axis(ax_radius, "z-Plane")
        fig_radius.savefig(output_dir / filename, dpi=DPI, facecolor="white")
        plt.close(fig_radius)

    export_curve_frame("16_frequency_response_radius_curves.png", include_radius_curves=True)


def export_surface_frames(system_case: SystemCase) -> None:
    output_dir = OUTPUT_DIR / system_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
    imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
    real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
    z_grid = real_grid + 1j * imag_grid
    response_grid = response_z(system_case.b, system_case.a, z_grid)
    response_db = magnitude_db(response_grid)
    response_db[np.abs(z_grid) < 0.035] = np.nan

    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    unit_circle = np.exp(1j * theta)
    unit_response_db = magnitude_db(response_z(system_case.b, system_case.a, unit_circle))

    def export_surface_frame(
        filename: str,
        *,
        show_unit_projection: bool,
        show_response_curve: bool,
        show_markers: bool,
    ) -> None:
        fig_surface = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
        ax_surface = fig_surface.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
        fig_surface.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)

        if show_unit_projection:
            ax_surface.plot(
                unit_circle.real,
                unit_circle.imag,
                np.full_like(theta, SURFACE_MIN_DB),
                color=LIGHT_GREY,
                lw=2.2,
                alpha=0.78,
                zorder=0,
            )

        ax_surface.plot_surface(
            real_grid,
            imag_grid,
            response_db,
            cmap="viridis",
            vmin=SURFACE_MIN_DB,
            vmax=SURFACE_MAX_DB,
            linewidth=0.0,
            antialiased=True,
            alpha=0.94,
        )

        if show_response_curve:
            plot_split_3d_curve(
                ax_surface,
                unit_circle,
                unit_response_db,
                theta,
                lw=3.2,
                alpha=1.0,
                zorder=5,
            )

        if show_markers:
            if system_case.zeros:
                zeros = np.asarray(system_case.zeros)
                ax_surface.scatter(
                    zeros.real,
                    zeros.imag,
                    np.full(zeros.shape, SURFACE_MIN_DB),
                    color=GREEN,
                    marker="o",
                    s=92,
                    linewidth=1.5,
                    edgecolor="white",
                    zorder=6,
                )
            if system_case.poles:
                poles = np.asarray(system_case.poles)
                ax_surface.scatter(
                    poles.real,
                    poles.imag,
                    np.full(poles.shape, SURFACE_MIN_DB),
                    color=POLE_RED,
                    marker="x",
                    s=105,
                    linewidth=2.6,
                    zorder=7,
                )

        setup_surface_axis(ax_surface, system_case.surface_title)
        fig_surface.savefig(output_dir / filename, dpi=DPI, facecolor="white")
        plt.close(fig_surface)

    export_surface_frame(
        "17_z_plane_surface.png",
        show_unit_projection=True,
        show_response_curve=False,
        show_markers=False,
    )
    export_surface_frame(
        "18_frequency_response_on_surface.png",
        show_unit_projection=True,
        show_response_curve=True,
        show_markers=False,
    )
    export_surface_frame(
        "19_surface_with_poles_zeros.png",
        show_unit_projection=True,
        show_response_curve=True,
        show_markers=True,
    )


def setup_z_plane_2d(ax_z) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    ax_z.set_title("z-Plane", fontsize=22, pad=10)
    ax_z.set_aspect("equal", adjustable="box")
    ax_z.set_xlim(-1.35, 1.35)
    ax_z.set_ylim(-1.35, 1.35)
    ax_z.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax_z.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax_z.set_xlabel(r"Re$\{z\}$", fontsize=24)
    ax_z.set_ylabel(r"Im$\{z\}$", fontsize=24)
    ax_z.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    ax_z.axhline(0.0, color=BLACK, lw=1.15, zorder=0)
    ax_z.axvline(0.0, color=BLACK, lw=1.15, zorder=0)
    ax_z.grid(alpha=0.24)
    ax_z.set_axisbelow(True)
    ax_z.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_z.spines[spine].set_visible(False)


def export_poles_zeros_2d(system_case: SystemCase) -> None:
    output_dir = OUTPUT_DIR / system_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)
    display_poles = system_case.poles
    if system_case.folder.startswith("04A"):
        display_poles = display_poles + FIR_DELAY_POLE_2D

    fig_z, ax_z = plt.subplots(figsize=FIGSIZE_Z_PLANE_2D, dpi=IR_DPI, facecolor="white")
    fig_z.subplots_adjust(left=0.17, right=0.96, bottom=0.16, top=0.86)
    setup_z_plane_2d(ax_z)

    if system_case.zeros:
        zeros = np.asarray(system_case.zeros, dtype=complex)
        unique_zeros: list[complex] = []
        zero_counts: list[int] = []
        for zero in zeros:
            for idx, unique_zero in enumerate(unique_zeros):
                if np.isclose(zero.real, unique_zero.real) and np.isclose(zero.imag, unique_zero.imag):
                    zero_counts[idx] += 1
                    break
            else:
                unique_zeros.append(zero)
                zero_counts.append(1)

        for point_idx, (zero, count) in enumerate(zip(unique_zeros, zero_counts)):
            for multiplicity_idx in reversed(range(count)):
                ax_z.scatter(
                    [zero.real],
                    [zero.imag],
                    marker="o",
                    s=180 + 420 * multiplicity_idx,
                    facecolor="white" if multiplicity_idx == 0 else "none",
                    edgecolor=GREEN,
                    linewidth=3.0,
                    zorder=5 + multiplicity_idx,
                    label="zeros" if point_idx == 0 and multiplicity_idx == 0 else None,
                )
    if display_poles:
        poles = np.asarray(display_poles)
        ax_z.scatter(
            poles.real,
            poles.imag,
            marker="x",
            s=180,
            color=POLE_RED,
            linewidth=3.1,
            zorder=6,
            label="poles",
        )

    if system_case.zeros or display_poles:
        legend = ax_z.legend(loc="lower right", fontsize=14, frameon=True)
        legend.get_frame().set_facecolor("white")
        legend.get_frame().set_edgecolor("none")
        legend.get_frame().set_alpha(0.92)

    fig_z.savefig(output_dir / "20_z_plane_poles_zeros_2d.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_z)


def white_crop_box(image: Image.Image) -> tuple[int, int, int, int] | None:
    rgb = image.convert("RGB")
    array = np.asarray(rgb)
    mask = np.any(array < CROP_THRESHOLD, axis=2)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if rows.size == 0 or cols.size == 0:
        return None

    left = max(int(cols[0]) - CROP_PAD, 0)
    upper = max(int(rows[0]) - CROP_PAD, 0)
    right = min(int(cols[-1]) + CROP_PAD + 1, image.width)
    lower = min(int(rows[-1]) + CROP_PAD + 1, image.height)
    return left, upper, right, lower


def combined_crop_box(png_files: list[Path]) -> tuple[int, int, int, int] | None:
    boxes: list[tuple[int, int, int, int]] = []
    for png_file in png_files:
        with Image.open(png_file) as image:
            box = white_crop_box(image)
            if box is not None:
                boxes.append(box)
    if not boxes:
        return None

    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def crop_png_to_box(path: Path, crop_box: tuple[int, int, int, int]) -> None:
    with Image.open(path) as image:
        image.crop(crop_box).save(path)


def crop_gif_to_box(path: Path, crop_box: tuple[int, int, int, int]) -> None:
    with Image.open(path) as source:
        durations = [
            frame.info.get("duration", source.info.get("duration", int(1000 / ANIMATION_FPS)))
            for frame in ImageSequence.Iterator(source)
        ]
        frames: list[Image.Image] = []
        for frame_index, frame in enumerate(ImageSequence.Iterator(source)):
            cropped = frame.convert("RGB").crop(crop_box)
            marker_color = (
                frame_index % 256,
                (frame_index * 37) % 256,
                (frame_index * 73) % 256,
            )
            for x_value in range(2):
                for y_value in range(2):
                    cropped.putpixel((x_value, y_value), marker_color)
            frames.append(cropped)

        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=source.info.get("loop", 0),
            disposal=2,
            optimize=False,
        )


def crop_3d_outputs(system_cases: tuple[SystemCase, ...]) -> None:
    png_names = [
        "07_frequency_response_unit_circle_start.png",
        "09_frequency_response_unit_circle_end.png",
        "10_frequency_response_full_unit_circle.png",
        *RADIUS_STEP_FILENAMES.values(),
        "16_frequency_response_radius_curves.png",
        "17_z_plane_surface.png",
        "18_frequency_response_on_surface.png",
        "19_surface_with_poles_zeros.png",
    ]
    png_files = [
        OUTPUT_DIR / system_case.folder / png_name
        for system_case in system_cases
        for png_name in png_names
    ]
    crop_box = combined_crop_box(png_files)
    if crop_box is None:
        return

    for png_file in png_files:
        crop_png_to_box(png_file, crop_box)
    for system_case in system_cases:
        crop_gif_to_box(
            OUTPUT_DIR / system_case.folder / "08_frequency_response_unit_circle_build.gif",
            crop_box,
        )


def write_readme() -> None:
    readme = OUTPUT_DIR / "README.md"
    readme.write_text(
        r"""# Block 4: Systemfunktion aus FIR und IIR

Block 4 zeigt, was man mit einer bereits hergeleiteten Systemfunktion machen
kann.

- `04A1_fir_three_tap_notch`: Drei-Tap-FIR-Notch mit
  \(H(z)=0.5+0.5z^{-2}\). Die Nullstellen liegen bei
  \(z=e^{\pm j\pi/2}\), also bei \(f=f_s/4\).
- `04A2_fir_three_tap_inside_zeros`: Drei-Tap-FIR mit
  \(H(z)=1-0.6z^{-1}+0.36z^{-2}\). Die Nullstellen liegen bei
  \(z=0.6e^{\pm j\pi/3}\), also innerhalb des Einheitskreises.
- `04C_iir_two_delay_resonator`: rein rekursiver Resonator mit
  \(H(z)=1/(1-0.9z^{-1}+0.81z^{-2})\). Die Pole liegen bei
  \(z=0.9e^{\pm j\pi/3}\).
- `04D_biquad_highpass`: Highpass-Biquad mit
  \(H(z)=(0.68931-1.37861z^{-1}+0.68931z^{-2})/
  (1-1.27963z^{-1}+0.47759z^{-2})\). Die Nullstellen liegen doppelt
  bei \(z=1\), die Pole bei \(z\approx0.6398\pm j0.2612\).

Die erste Abbildung zeigt jeweils die Impulsantwort in Gruen. Danach wird
zuerst \(z=e^{j\Omega}\) eingesetzt: Der Frequenzgang bis Nyquist wird
zunaechst linear und danach in dB gezeigt. Der dB-Frequenzgang wird als GIF
aufgebaut; das Startbild des GIFs liegt als eigenes PNG vor. Anschliessend
wird der Frequenzgang auf \(0\leq\Omega/\pi\leq2\) erweitert; der Bereich
oberhalb von Nyquist ist blau.

Danach wird derselbe Frequenzgang in der z-Ebene gezeigt: erst als GIF bis
Nyquist, dann als Standbild ueber den ganzen Einheitskreis. Im GIF bleibt der
vollstaendige Einheitskreis unten grau, der abgefahrene Abschnitt wird orange
aufgebaut; zusaetzlich zeigt ein orangefarbener Zeiger die aktuelle Projektion
auf den Einheitskreis.
Im Standbild ist der \(r=1\)-Kreis unten orange hervorgehoben. Anschliessend
folgt eine Serie mit kleiner werdendem Radius \(r=0.8,0.6,0.4,0.2,0\); der
aktuell zugehoerige Kreis ist unten in der z-Ebene orange hervorgehoben,
bereits gezeigte Werte bleiben transparent sichtbar. Ein weiteres Standbild
fasst die Radiuskurven zusammen. Erst danach wird \(|H(z)|\) in der ganzen
z-Ebene als Flaeche gezeigt. Die gruene und blaue Kurve auf der Flaeche ist
derselbe Ausdruck auf dem Einheitskreis, also der Frequenzgang. Abschliessend
zeigt eine 2D-z-Ebene beim FIR die Nullstellen plus den formalen Delay-Pol
bei \(z=0\), beim IIR die Polstellen.
""",
        encoding="utf-8",
    )


def main() -> None:
    fir_notch_zeros = tuple(np.roots(FIR_NOTCH_B))
    fir_variant_zeros = tuple(np.roots(FIR_VARIANT_B))
    iir_poles = tuple(np.roots([1.0, IIR_A[1], IIR_A[2]]))
    iir_zeros = (0.0 + 0.0j, 0.0 + 0.0j)
    biquad_zeros = tuple(np.roots(BIQUAD_HP_B))
    biquad_poles = tuple(np.roots([1.0, BIQUAD_HP_A[1], BIQUAD_HP_A[2]]))
    cases = (
        SystemCase(
            "04A1_fir_three_tap_notch",
            r"Impulse response: 3-tap FIR notch",
            r"FIR notch: $|H(z)|$",
            FIR_NOTCH_B,
            FIR_A,
            fir_notch_zeros,
            (),
            (-1.15, 1.15),
            (-1.0, -0.5, 0.0, 0.5, 1.0),
        ),
        SystemCase(
            "04A2_fir_three_tap_inside_zeros",
            r"Impulse response: 3-tap FIR",
            r"FIR inside zeros: $|H(z)|$",
            FIR_VARIANT_B,
            FIR_A,
            fir_variant_zeros,
            (),
            (-1.15, 1.15),
            (-1.0, -0.5, 0.0, 0.5, 1.0),
        ),
        SystemCase(
            "04C_iir_two_delay_resonator",
            r"Impulse response: 2-delay IIR resonator",
            r"IIR resonator: $|H(z)|$",
            IIR_B,
            IIR_A,
            iir_zeros,
            iir_poles,
            (-1.15, 1.15),
            (-1.0, -0.5, 0.0, 0.5, 1.0),
        ),
        SystemCase(
            "04D_biquad_highpass",
            r"Impulse response: highpass biquad",
            r"Highpass biquad: $|H(z)|$",
            BIQUAD_HP_B,
            BIQUAD_HP_A,
            biquad_zeros,
            biquad_poles,
            (-1.15, 1.15),
            (-1.0, -0.5, 0.0, 0.5, 1.0),
        ),
    )

    clear_output_dir()
    for system_case in cases:
        export_impulse_response(system_case)
        export_frequency_response(system_case)
        export_unit_circle_response_gif(system_case)
        export_full_circle_response_frames(system_case)
        export_surface_frames(system_case)
        export_poles_zeros_2d(system_case)
    crop_3d_outputs(cases)
    write_readme()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
