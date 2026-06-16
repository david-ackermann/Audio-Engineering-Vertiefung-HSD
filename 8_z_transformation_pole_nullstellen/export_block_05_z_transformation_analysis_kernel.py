from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "05_z_transformation_analysekern"
)

DPI = 160
IR_DPI = 200
FIGSIZE = (13.8, 6.4)
FIGSIZE_FREQ = (10.5, 4.2)
FIGSIZE_IR = (10.5, 4.2)
FIGSIZE_SURFACE = (8.8, 6.2)
FIGSIZE_Z_ONLY = (5.2, 5.2)
NUM_SAMPLES = 16
TIME_DENSE = np.linspace(0.0, NUM_SAMPLES, 1100)
SAMPLE_INDICES = np.arange(NUM_SAMPLES + 1)

TITLE_SIZE = 18
LABEL_SIZE = 18
TICK_SIZE = 14
CROP_THRESHOLD = 250
CROP_PAD = 8
FREQ_LEFT_INCH = FIGSIZE_FREQ[0] * 0.10
FREQ_AXIS_WIDTH_INCH = FIGSIZE_FREQ[0] * (0.98 - 0.10)
FREQ_RIGHT_INCH = FIGSIZE_FREQ[0] * (1.0 - 0.98)
FREQ_BOTTOM = 0.19
FREQ_TOP = 0.82

BLACK = "0.10"
GREEN = "#66b77a"
GREY = "0.58"
LIGHT_GREY = "0.84"
RE_COLOR = BLACK
IM_COLOR = BLACK
UNIT_GREEN = "#3d9f5f"
DECAY_BLUE = "#2b7bbb"
GROWTH_ORANGE = "#d98c2f"
POLE_RED = "#b84a4a"

HELIX_LIMIT = 3.75
Z_LIMIT = 1.25
SURFACE_LIMIT = 1.35
SURFACE_MIN_DB = -25.0
SURFACE_MAX_DB = 25.0
FS_HZ = 48_000.0
KNOWN_POSITIVE_POLE = 0.50
KNOWN_POSITIVE_GAIN = 0.50
KNOWN_NEGATIVE_POLE = -0.50
KNOWN_NEGATIVE_GAIN = 1.50
BIQUAD_HP_B = np.array([0.68930617, -1.37861234, 0.68930617])
BIQUAD_HP_A = np.array([1.0, -1.27963242, 0.47759225])
BIQUAD_HP_ZEROS = np.roots(BIQUAD_HP_B)
BIQUAD_HP_POLES = np.roots([1.0, BIQUAD_HP_A[1], BIQUAD_HP_A[2]])
BIQUAD_HP_POLE = complex(BIQUAD_HP_POLES[np.argmax(np.imag(BIQUAD_HP_POLES))])
BIQUAD_HP_POLE_RADIUS = float(abs(BIQUAD_HP_POLE))
BIQUAD_HP_POLE_OMEGA = float(np.angle(BIQUAD_HP_POLE))

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class RadiusCase:
    folder: str
    title: str
    radius: float
    color: str
    explanation: str


@dataclass(frozen=True)
class FrequencyCase:
    slug: str
    title: str
    omega: float
    omega_label: str
    frequency_hz: float


RADIUS_CASES = (
    RadiusCase(
        "05A_r_1_unit_circle",
        "Unit circle: stationary",
        1.00,
        UNIT_GREEN,
        r"$r=1$: constant envelope",
    ),
    RadiusCase(
        "05B_r_less_1_decay",
        "Inside the unit circle: decay",
        0.86,
        UNIT_GREEN,
        r"$r<1$: decaying envelope",
    ),
    RadiusCase(
        "05C_r_greater_1_growth",
        "Outside the unit circle: growth",
        1.08,
        UNIT_GREEN,
        r"$r>1$: growing envelope",
    ),
    RadiusCase(
        "05D_r_pole_radius",
        "Pole radius: biquad mode",
        BIQUAD_HP_POLE_RADIUS,
        UNIT_GREEN,
        r"$r=|p|$: pole radius",
    ),
)


FREQUENCY_CASES = (
    FrequencyCase("dc", "DC", 0.0, "0", 0.0),
    FrequencyCase("quarter_nyquist", "Quarter Nyquist", 0.25 * np.pi, r"\pi/4", FS_HZ / 8.0),
    FrequencyCase("half_nyquist", "Half Nyquist", 0.5 * np.pi, r"\pi/2", FS_HZ / 4.0),
    FrequencyCase("nyquist", "Nyquist", np.pi, r"\pi", FS_HZ / 2.0),
    FrequencyCase(
        "biquad_pole_angle",
        "Biquad pole angle",
        BIQUAD_HP_POLE_OMEGA,
        r"0.1234\pi",
        BIQUAD_HP_POLE_OMEGA / np.pi * FS_HZ / 2.0,
    ),
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_file in OUTPUT_DIR.rglob("*.png"):
        output_file.unlink()
    for output_dir in sorted(OUTPUT_DIR.rglob("*"), reverse=True):
        if output_dir.is_dir():
            try:
                output_dir.rmdir()
            except OSError:
                pass


def format_frequency(value_hz: float) -> str:
    if value_hz == 0.0:
        return "0 Hz"
    if value_hz >= 1_000.0:
        return f"{value_hz / 1_000.0:g} kHz"
    return f"{value_hz:g} Hz"


def format_radius(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def z_value(radius: float, omega: float) -> complex:
    return radius * np.exp(1j * omega)


def z_mode(radius: float, omega: float, n_values: np.ndarray) -> np.ndarray:
    return (radius**n_values) * np.exp(1j * omega * n_values)


def one_pole_response(z_values: np.ndarray, pole: float, gain: float) -> np.ndarray:
    return gain * z_values / (z_values - pole)


def biquad_response(z_values: np.ndarray) -> np.ndarray:
    numerator = BIQUAD_HP_B[0] * z_values**2 + BIQUAD_HP_B[1] * z_values + BIQUAD_HP_B[2]
    denominator = z_values**2 + BIQUAD_HP_A[1] * z_values + BIQUAD_HP_A[2]
    with np.errstate(divide="ignore", invalid="ignore"):
        return numerator / denominator


def biquad_frequency_response_linear() -> tuple[np.ndarray, np.ndarray]:
    omega_values = np.linspace(0.0, np.pi, 121)
    response_linear = np.abs(biquad_response(np.exp(1j * omega_values)))
    response_linear = np.where(np.isfinite(response_linear), response_linear, np.nan)
    return omega_values, response_linear


def should_show_biquad_poles(radius_case: RadiusCase, active_index: int) -> bool:
    current_omega = FREQUENCY_CASES[active_index].omega
    if radius_case.folder == "05C_r_greater_1_growth":
        return True
    return radius_case.folder == "05D_r_pole_radius" and current_omega >= BIQUAD_HP_POLE_OMEGA


def unique_complex_values(values: np.ndarray, precision: int = 6) -> np.ndarray:
    rounded = np.round(values.real, precision) + 1j * np.round(values.imag, precision)
    _, unique_indices = np.unique(rounded, return_index=True)
    return values[np.sort(unique_indices)]


def plot_biquad_markers_2d(ax, *, show_poles: bool) -> None:
    zero_values = unique_complex_values(BIQUAD_HP_ZEROS)
    ax.scatter(
        zero_values.real,
        zero_values.imag,
        s=10.5**2,
        marker="o",
        facecolors="white",
        edgecolors=UNIT_GREEN,
        linewidth=2.3,
        zorder=8,
        clip_on=False,
    )
    if show_poles:
        ax.scatter(
            BIQUAD_HP_POLES.real,
            BIQUAD_HP_POLES.imag,
            s=9.5**2,
            marker="x",
            color=POLE_RED,
            linewidth=2.4,
            zorder=8,
            clip_on=False,
        )


def plot_biquad_markers_3d(ax_surface, *, show_poles: bool) -> None:
    zero_values = unique_complex_values(BIQUAD_HP_ZEROS)
    ax_surface.scatter(
        zero_values.real,
        zero_values.imag,
        np.full(zero_values.shape, SURFACE_MIN_DB),
        s=88,
        marker="o",
        facecolors="white",
        edgecolors=UNIT_GREEN,
        linewidth=2.3,
        depthshade=False,
        zorder=8,
    )
    if show_poles:
        ax_surface.scatter(
            BIQUAD_HP_POLES.real,
            BIQUAD_HP_POLES.imag,
            np.full(BIQUAD_HP_POLES.shape, SURFACE_MIN_DB),
            s=92,
            marker="x",
            color=POLE_RED,
            linewidth=2.4,
            depthshade=False,
            zorder=8,
        )


def magnitude_db(values: np.ndarray) -> np.ndarray:
    return np.clip(20.0 * np.log10(np.maximum(np.abs(values), 1.0e-9)), SURFACE_MIN_DB, SURFACE_MAX_DB)


def export_known_ir_surface(
    folder: str,
    pole: float,
    gain: float,
    ir_title: str,
    envelope_title: str,
    *,
    y_limits: tuple[float, float],
    y_ticks: list[float],
    show_lower_envelope: bool,
    time_num_samples: int = 7,
) -> None:
    output_dir = OUTPUT_DIR / folder
    output_dir.mkdir(parents=True, exist_ok=True)

    n_values = np.arange(time_num_samples + 1)
    impulse_response = gain * pole**n_values
    dense_n = np.linspace(0.0, time_num_samples, 500)
    envelope = abs(gain) * (abs(pole) ** dense_n)

    real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 210)
    imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 210)
    real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
    z_grid = real_grid + 1j * imag_grid
    response_grid = one_pole_response(z_grid, pole, gain)
    response_db = magnitude_db(response_grid)
    response_db[np.abs(z_grid - pole) < 0.030] = np.nan

    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    unit_circle = np.exp(1j * theta)
    unit_response_db = magnitude_db(one_pole_response(unit_circle, pole, gain))

    def export_ir_plot(filename: str, title: str, *, show_envelope: bool) -> None:
        fig_ir, ax_ir = plt.subplots(figsize=FIGSIZE_IR, dpi=IR_DPI, facecolor="white")
        fig_ir.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
        if show_envelope:
            ax_ir.plot(dense_n, envelope, color=GREEN, lw=3.0, alpha=0.58, zorder=2)
            if show_lower_envelope:
                ax_ir.plot(dense_n, -envelope, color=GREEN, lw=3.0, alpha=0.58, zorder=2)
        ax_ir.vlines(n_values, 0.0, impulse_response, color=GREEN, lw=2.2, alpha=1.0, zorder=3)
        ax_ir.scatter(
            n_values,
            impulse_response,
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
        ax_ir.set_xlim(-0.5, time_num_samples + 0.5)
        ax_ir.set_ylim(*y_limits)
        ax_ir.set_xticks(list(range(time_num_samples + 1)))
        ax_ir.set_yticks(y_ticks)
        ax_ir.set_xlabel("Sample index n", fontsize=24)
        ax_ir.set_ylabel(r"$h[n]$", fontsize=24)
        ax_ir.set_title(title, fontsize=22, pad=10)
        ax_ir.grid(alpha=0.25)
        ax_ir.tick_params(labelsize=18)
        for spine in ("top", "right"):
            ax_ir.spines[spine].set_visible(False)
        fig_ir.savefig(output_dir / filename, dpi=IR_DPI, facecolor="white")
        plt.close(fig_ir)

    export_ir_plot("01_known_ir.png", ir_title, show_envelope=False)
    export_ir_plot("02_known_ir_with_envelope.png", envelope_title, show_envelope=True)

    def setup_surface_axis(ax_surface) -> None:
        ax_surface.set_title(r"z-transform: $|H(z)|$", fontsize=TITLE_SIZE, y=1.005, pad=0)
        ax_surface.set_xlabel(r"Re$\{z\}$", fontsize=LABEL_SIZE, labelpad=8)
        ax_surface.set_ylabel(r"Im$\{z\}$", fontsize=LABEL_SIZE, labelpad=8)
        ax_surface.set_zlabel(r"$|H(z)|$ in dB", fontsize=LABEL_SIZE, labelpad=8)
        ax_surface.set_xlim(-SURFACE_LIMIT, SURFACE_LIMIT)
        ax_surface.set_ylim(-SURFACE_LIMIT, SURFACE_LIMIT)
        ax_surface.set_zlim(SURFACE_MIN_DB, SURFACE_MAX_DB)
        ax_surface.set_xticks([-1.0, 0.0, 1.0])
        ax_surface.set_yticks([-1.0, 0.0, 1.0])
        ax_surface.set_zticks([-25.0, 0.0, 25.0])
        ax_surface.tick_params(labelsize=TICK_SIZE)
        ax_surface.view_init(elev=25, azim=-58)
        try:
            ax_surface.set_box_aspect((1.9, 1.9, 1.25), zoom=1.08)
        except TypeError:
            ax_surface.set_box_aspect((1.9, 1.9, 1.25))
        for axis in (ax_surface.xaxis, ax_surface.yaxis, ax_surface.zaxis):
            axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
            axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))

    def export_surface_frame(
        filename: str,
        *,
        show_unit_projection: bool,
        show_response_curve: bool,
        show_pole: bool,
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
            ax_surface.plot(
                unit_circle.real,
                unit_circle.imag,
                unit_response_db,
                color=GREEN,
                lw=3.2,
                zorder=5,
            )

        if show_pole:
            ax_surface.scatter(
                [pole],
                [0.0],
                [SURFACE_MIN_DB],
                color=POLE_RED,
                marker="x",
                s=92,
                linewidth=2.4,
                zorder=6,
            )

        setup_surface_axis(ax_surface)
        fig_surface.savefig(output_dir / filename, dpi=DPI, facecolor="white")
        plt.close(fig_surface)

    export_surface_frame(
        "03_z_transform_unit_circle_projection.png",
        show_unit_projection=True,
        show_response_curve=False,
        show_pole=False,
    )
    export_surface_frame(
        "04_z_transform_frequency_response.png",
        show_unit_projection=True,
        show_response_curve=True,
        show_pole=False,
    )
    export_surface_frame(
        "05_z_transform_with_pole.png",
        show_unit_projection=True,
        show_response_curve=True,
        show_pole=True,
    )


def setup_z_axis(ax, radius_case: RadiusCase, active_index: int) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    current_omega = FREQUENCY_CASES[active_index].omega

    ax.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    if radius_case.radius != 1.0:
        ax.plot(
            radius_case.radius * np.cos(theta),
            radius_case.radius * np.sin(theta),
            color=LIGHT_GREY,
            lw=2.0,
            alpha=0.86,
            zorder=1,
        )

    if current_omega > 0.0:
        active_theta = np.linspace(0.0, current_omega, max(2, int(300 * current_omega / np.pi)))
        ax.plot(
            radius_case.radius * np.cos(active_theta),
            radius_case.radius * np.sin(active_theta),
            color=radius_case.color,
            lw=3.2,
            alpha=0.88,
            zorder=3,
        )

    ax.axhline(0.0, color=BLACK, lw=1.0, zorder=0)
    ax.axvline(0.0, color=BLACK, lw=1.0, zorder=0)

    point = z_value(radius_case.radius, current_omega)
    ax.annotate(
        "",
        xy=(point.real, point.imag),
        xytext=(0.0, 0.0),
        arrowprops={
            "arrowstyle": "-|>",
            "color": radius_case.color,
            "lw": 3.0,
            "mutation_scale": 18,
            "shrinkA": 0.0,
            "shrinkB": 0.0,
        },
        zorder=5,
    )
    plot_biquad_markers_2d(ax, show_poles=should_show_biquad_poles(radius_case, active_index))

    ax.set_title("z-plane", fontsize=TITLE_SIZE, pad=11)
    ax.set_xlim(-Z_LIMIT, Z_LIMIT)
    ax.set_ylim(-Z_LIMIT, Z_LIMIT)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel(r"Re$\{z\}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Im$\{z\}$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.20)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_biquad_poles_zeros_2d() -> None:
    output_dir = OUTPUT_DIR / "05E_biquad_poles_zeros_2d"
    output_dir.mkdir(parents=True, exist_ok=True)

    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    fig_z, ax_z = plt.subplots(figsize=FIGSIZE_Z_ONLY, dpi=IR_DPI, facecolor="white")
    fig_z.subplots_adjust(left=0.18, right=0.95, bottom=0.16, top=0.86)

    ax_z.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    ax_z.axhline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax_z.axvline(0.0, color=BLACK, lw=1.1, zorder=0)
    plot_biquad_markers_2d(ax_z, show_poles=True)

    ax_z.set_title("z-plane", fontsize=22, pad=10)
    ax_z.set_xlim(-Z_LIMIT, Z_LIMIT)
    ax_z.set_ylim(-Z_LIMIT, Z_LIMIT)
    ax_z.set_aspect("equal", adjustable="box")
    ax_z.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax_z.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax_z.set_xlabel(r"Re$\{z\}$", fontsize=24)
    ax_z.set_ylabel(r"Im$\{z\}$", fontsize=24)
    ax_z.grid(alpha=0.20)
    ax_z.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_z.spines[spine].set_visible(False)

    fig_z.savefig(output_dir / "01_biquad_poles_zeros_2d.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_z)


def build_stem_segments(n_values: np.ndarray, values: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_segments: list[float] = []
    y_segments: list[float] = []
    z_segments: list[float] = []
    for n_value, value in zip(n_values, values):
        x_segments.extend([float(n_value), float(n_value), np.nan])
        y_segments.extend([0.0, float(value.real), np.nan])
        z_segments.extend([0.0, float(value.imag), np.nan])
    return np.asarray(x_segments), np.asarray(y_segments), np.asarray(z_segments)


def setup_helix_axis(ax, radius_case: RadiusCase, frequency_case: FrequencyCase) -> None:
    ax.set_xlim(0.0, NUM_SAMPLES)
    ax.set_ylim(-HELIX_LIMIT, HELIX_LIMIT)
    ax.set_zlim(-HELIX_LIMIT, HELIX_LIMIT)
    ax.set_xlabel("n", color=BLACK, fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel(r"Re$\{x_z[n]\}$", color=BLACK, fontsize=LABEL_SIZE, labelpad=12)
    ax.set_zlabel(r"Im$\{x_z[n]\}$", color=BLACK, fontsize=LABEL_SIZE, labelpad=8)
    ax.tick_params(axis="x", colors=BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=BLACK, labelsize=TICK_SIZE)
    ax.tick_params(axis="z", colors=BLACK, labelsize=TICK_SIZE)
    ax.set_xticks([0, 4, 8, 12, 16])
    ax.set_yticks([-3.0, -1.5, 0.0, 1.5, 3.0])
    ax.set_zticks([-3.0, -1.5, 0.0, 1.5, 3.0])
    ax.set_title(
        rf"Analysis kernel: $r={format_radius(radius_case.radius)}$, "
        rf"$\Omega={frequency_case.omega_label}$",
        fontsize=TITLE_SIZE,
        y=0.94,
        pad=0,
    )
    ax.view_init(elev=22, azim=-62)
    try:
        ax.set_box_aspect((3.7, 1.55, 1.55), zoom=1.15)
    except TypeError:
        ax.set_box_aspect((3.7, 1.55, 1.55))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))


def setup_biquad_surface_axis(ax_surface, radius_case: RadiusCase, frequency_case: FrequencyCase) -> None:
    ax_surface.set_title(
        rf"Biquad: $r={format_radius(radius_case.radius)}$, "
        rf"$\Omega={frequency_case.omega_label}$",
        fontsize=TITLE_SIZE,
        y=1.005,
        pad=0,
    )
    ax_surface.set_xlabel(r"Re$\{z\}$", fontsize=LABEL_SIZE, labelpad=8)
    ax_surface.set_ylabel(r"Im$\{z\}$", fontsize=LABEL_SIZE, labelpad=8)
    ax_surface.set_zlabel(r"$|H(z)|$ in dB", fontsize=LABEL_SIZE, labelpad=8)
    ax_surface.set_xlim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax_surface.set_ylim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax_surface.set_zlim(SURFACE_MIN_DB, SURFACE_MAX_DB)
    ax_surface.set_xticks([-1.0, 0.0, 1.0])
    ax_surface.set_yticks([-1.0, 0.0, 1.0])
    ax_surface.set_zticks([-25.0, 0.0, 25.0])
    ax_surface.tick_params(labelsize=TICK_SIZE)
    ax_surface.view_init(elev=25, azim=-58)
    try:
        ax_surface.set_box_aspect((1.9, 1.9, 1.25), zoom=1.08)
    except TypeError:
        ax_surface.set_box_aspect((1.9, 1.9, 1.25))
    for axis in (ax_surface.xaxis, ax_surface.yaxis, ax_surface.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))


def adjust_frequency_figure(fig) -> None:
    width, _ = fig.get_size_inches()
    fig.subplots_adjust(
        left=FREQ_LEFT_INCH / width,
        right=1.0 - FREQ_RIGHT_INCH / width,
        bottom=FREQ_BOTTOM,
        top=FREQ_TOP,
    )


def setup_biquad_frequency_axis(ax_freq, response_linear: np.ndarray) -> None:
    y_max = float(np.nanmax(response_linear))
    if y_max <= 1.05:
        y_limit = 1.05
        y_ticks = [0.0, 0.5, 1.0]
    else:
        y_limit = float(np.ceil(y_max * 1.08))
        y_ticks = [0.0, 0.5 * y_limit, y_limit]

    ax_freq.set_title("Frequency response", fontsize=22, pad=10)
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


def export_biquad_frequency_response_frame(radius_case: RadiusCase, frequency_case: FrequencyCase, active_index: int) -> None:
    output_dir = OUTPUT_DIR / radius_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    omega_values, response_linear = biquad_frequency_response_linear()
    normalized_frequency = omega_values / np.pi

    fig_freq, ax_freq = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_freq)
    ax_freq.plot(normalized_frequency, response_linear, color=LIGHT_GREY, lw=3.0, zorder=1)

    if frequency_case.omega > 0.0:
        active_omega = np.linspace(0.0, frequency_case.omega, max(2, int(240 * frequency_case.omega / np.pi)))
        active_response = np.abs(biquad_response(np.exp(1j * active_omega)))
        active_response = np.where(np.isfinite(active_response), active_response, np.nan)
        active_normalized = active_omega / np.pi
        point_response = float(np.abs(biquad_response(np.asarray([np.exp(1j * frequency_case.omega)]))[0]))
        ax_freq.plot(active_normalized, active_response, color=GREEN, lw=3.2, zorder=2)
        ax_freq.scatter(
            [frequency_case.omega / np.pi],
            [point_response],
            s=7.5**2,
            color=GREEN,
            edgecolor="white",
            linewidth=0.9,
            zorder=3,
            clip_on=False,
        )

    setup_biquad_frequency_axis(ax_freq, response_linear)
    filename = f"{active_index + 6:02d}_biquad_frequency_response_{frequency_case.slug}.png"
    fig_freq.savefig(output_dir / filename, dpi=IR_DPI, facecolor="white")
    plt.close(fig_freq)


def export_biquad_surface_frame(
    radius_case: RadiusCase,
    frequency_case: FrequencyCase,
    active_index: int,
    *,
    include_surface: bool = False,
    filename: str | None = None,
) -> None:
    output_dir = OUTPUT_DIR / radius_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    current_omega = frequency_case.omega
    active_theta = np.linspace(0.0, current_omega, max(2, int(300 * max(current_omega, 0.02) / np.pi)))
    if current_omega == 0.0:
        active_theta = np.array([0.0])

    full_circle = np.exp(1j * theta)
    radius_circle = radius_case.radius * full_circle
    active_path = radius_case.radius * np.exp(1j * active_theta)
    active_response = magnitude_db(biquad_response(active_path))
    point = z_value(radius_case.radius, current_omega)
    point_response = magnitude_db(biquad_response(np.asarray([point])))[0]

    fig_surface = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
    ax_surface = fig_surface.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig_surface.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)

    ax_surface.plot(
        full_circle.real,
        full_circle.imag,
        np.full_like(theta, SURFACE_MIN_DB),
        color=LIGHT_GREY,
        lw=2.2,
        alpha=0.78,
        zorder=0,
    )
    if radius_case.radius != 1.0:
        ax_surface.plot(
            radius_circle.real,
            radius_circle.imag,
            np.full_like(theta, SURFACE_MIN_DB),
            color=LIGHT_GREY,
            lw=1.9,
            alpha=0.70,
            zorder=0,
        )

    if include_surface:
        real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
        imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
        real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
        z_grid = real_grid + 1j * imag_grid
        denominator = z_grid**2 + BIQUAD_HP_A[1] * z_grid + BIQUAD_HP_A[2]
        response_db = magnitude_db(biquad_response(z_grid))
        response_db[np.abs(denominator) < 0.006] = np.nan
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
            zorder=1,
        )

    if current_omega > 0.0:
        ax_surface.plot(
            active_path.real,
            active_path.imag,
            np.full_like(active_theta, SURFACE_MIN_DB),
            color=radius_case.color,
            lw=3.0,
            alpha=0.88,
            zorder=4,
        )
        ax_surface.plot(
            active_path.real,
            active_path.imag,
            active_response,
            color=radius_case.color,
            lw=3.2,
            alpha=0.96,
            zorder=5,
        )

    ax_surface.plot(
        [point.real, point.real],
        [point.imag, point.imag],
        [SURFACE_MIN_DB, point_response],
        color=radius_case.color,
        lw=2.2,
        alpha=0.74,
        zorder=6,
    )
    ax_surface.scatter(
        [point.real],
        [point.imag],
        [point_response],
        s=78,
        color=radius_case.color,
        edgecolor="white",
        linewidth=0.8,
        depthshade=False,
        zorder=7,
    )
    plot_biquad_markers_3d(ax_surface, show_poles=should_show_biquad_poles(radius_case, active_index))

    setup_biquad_surface_axis(ax_surface, radius_case, frequency_case)
    output_filename = filename or f"{active_index + 11:02d}_biquad_z_response_{frequency_case.slug}.png"
    fig_surface.savefig(output_dir / output_filename, dpi=DPI, facecolor="white")
    plt.close(fig_surface)


def export_frame(radius_case: RadiusCase, frequency_case: FrequencyCase, active_index: int) -> None:
    output_dir = OUTPUT_DIR / radius_case.folder
    output_dir.mkdir(parents=True, exist_ok=True)

    dense_values = z_mode(radius_case.radius, frequency_case.omega, TIME_DENSE)
    sample_values = z_mode(radius_case.radius, frequency_case.omega, SAMPLE_INDICES)
    stem_x, stem_y, stem_z = build_stem_segments(SAMPLE_INDICES, sample_values)

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    grid = fig.add_gridspec(1, 2, width_ratios=[0.82, 2.65])
    ax_z = fig.add_subplot(grid[0, 0])
    ax_helix = fig.add_subplot(grid[0, 1], projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.095, right=0.985, bottom=0.09, top=0.88, wspace=0.02)

    setup_z_axis(ax_z, radius_case, active_index)
    setup_helix_axis(ax_helix, radius_case, frequency_case)

    ax_helix.plot(
        TIME_DENSE,
        dense_values.real,
        dense_values.imag,
        color=radius_case.color,
        lw=2.8,
        alpha=0.95,
        zorder=4,
    )
    ax_helix.plot(stem_x, stem_y, stem_z, color=GREY, lw=1.1, alpha=0.55, zorder=2)
    ax_helix.scatter(
        SAMPLE_INDICES,
        sample_values.real,
        sample_values.imag,
        s=38,
        color=radius_case.color,
        edgecolor="white",
        linewidth=0.7,
        zorder=5,
    )
    ax_helix.plot(
        TIME_DENSE,
        np.abs(dense_values),
        np.zeros_like(TIME_DENSE),
        color=UNIT_GREEN,
        lw=1.7,
        alpha=0.26,
        zorder=1,
    )
    ax_helix.plot(
        TIME_DENSE,
        -np.abs(dense_values),
        np.zeros_like(TIME_DENSE),
        color=UNIT_GREEN,
        lw=1.7,
        alpha=0.26,
        zorder=1,
    )

    filename = f"{active_index + 1:02d}_{frequency_case.slug}.png"
    fig.savefig(output_dir / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


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


def crop_png_group(png_files: list[Path]) -> None:
    boxes: list[tuple[int, int, int, int]] = []
    for png_file in png_files:
        with Image.open(png_file) as image:
            box = white_crop_box(image)
            if box is not None:
                boxes.append(box)
    if not boxes:
        return

    left = min(box[0] for box in boxes)
    upper = min(box[1] for box in boxes)
    right = max(box[2] for box in boxes)
    lower = max(box[3] for box in boxes)
    crop_box = (left, upper, right, lower)

    for png_file in png_files:
        with Image.open(png_file) as image:
            cropped = image.crop(crop_box)
            cropped.save(png_file)


def crop_all_outputs() -> None:
    png_files = sorted(
        png_file
        for png_file in OUTPUT_DIR.rglob("*.png")
        if png_file.name not in {"01_known_ir.png", "02_known_ir_with_envelope.png"}
        and "_biquad_frequency_response_" not in png_file.name
    )
    groups: dict[tuple[int, int], list[Path]] = {}
    for png_file in png_files:
        with Image.open(png_file) as image:
            key = image.size
        groups.setdefault(key, []).append(png_file)
    for group_files in groups.values():
        crop_png_group(sorted(group_files))


def write_readme() -> None:
    readme = OUTPUT_DIR / "README.md"
    readme.write_text(
        r"""# Block 5: z-Transformation als verallgemeinerte komplexe Schwingung

Diese Bildserie zeigt die Zeitfunktion

$$
x_z[n]=z^n=r^n e^{j\Omega n}
$$

fuer unterschiedliche Radien und Frequenzen.

- `05A_r_1_unit_circle`: stationaere Schwingungen auf dem Einheitskreis
- `05B_r_less_1_decay`: abklingende Schwingungen mit \(r<1\)
- `05C_r_greater_1_growth`: aufschwingende Schwingungen mit \(r>1\)
- `05D_r_pole_radius`: natuerlicher Biquad-Modus mit
  \(r=|p|\approx0.6911\)
- `05E_biquad_poles_zeros_2d`: reines Pol-Nullstellen-Diagramm des
  Biquad-Hochpasses in der 2D-z-Ebene, ohne Zeiger und ohne Helix

Die absolute Startamplitude ist in den Abbildungen \(A=1\). Der Radius \(r\)
beschreibt daher die Huelle pro Sample: \(r^n\). Die eigentliche
z-Transformationssumme nutzt den Kern \(z^{-n}\); fuer die Systemintuition ist
\(z^n\) die anschauliche Zeitfunktion, weil Pole und natuerliche Systemanteile
ebenfalls als \(p^n\) sichtbar werden.

In `05A_r_1_unit_circle` wird fuer jeden diskreten Analysekern die
Systemantwort des Biquad-Hochpasses aus Block 4D zunaechst als
2D-Frequenzgang wie in Block 4D gezeigt: vollstaendig grau, bis zur aktuellen
Zeigerposition gruen. Danach folgt fuer alle Radiusfaelle dieselbe Auswertung
als 3D-Kurve ohne Flaeche. Die Kurve liegt fuer \(r=1\) auf dem
Einheitskreis, fuer \(r=0.86\) innerhalb, fuer \(r=1.08\) ausserhalb und fuer
\(r=|p|\) auf dem Polradius. Beim Polwinkel \(\Omega\approx0.1234\pi\) trifft
die letzte Serie den Pol des Biquads.

Die z-Ebene markiert die doppelte Nullstelle des Biquad-Hochpasses bei
\(z=1\). In der \(r>1\)-Serie werden die konjugiert-komplexen Polstellen von
Anfang an mit gezeigt. In der Polradius-Serie werden sie erst eingeblendet,
sobald der aktive Zeiger den Polwinkel erreicht oder ueberschritten hat.
Dieselbe Logik gilt in der 2D-z-Ebene und unten in den 3D-Darstellungen.
""",
        encoding="utf-8",
    )


def main() -> None:
    clear_output_dir()
    export_biquad_poles_zeros_2d()
    for radius_case in RADIUS_CASES:
        for active_index, frequency_case in enumerate(FREQUENCY_CASES):
            export_frame(radius_case, frequency_case, active_index)
            if radius_case.folder == "05A_r_1_unit_circle":
                export_biquad_frequency_response_frame(radius_case, frequency_case, active_index)
            export_biquad_surface_frame(radius_case, frequency_case, active_index)
            if radius_case.folder == "05A_r_1_unit_circle" and frequency_case.slug == "nyquist":
                export_biquad_surface_frame(
                    radius_case,
                    frequency_case,
                    active_index,
                    include_surface=True,
                    filename="16_biquad_z_response_nyquist_surface.png",
                )
    crop_all_outputs()
    write_readme()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
