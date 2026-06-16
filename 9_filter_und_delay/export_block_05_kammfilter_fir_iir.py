from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "05_kammfilter_fir_iir"

DPI = 200
FIGSIZE = (11.5, 4.8)
FIGSIZE_SURFACE = (8.8, 6.2)
FIGSIZE_Z_PLANE_2D = (6.2, 5.6)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18
SURFACE_TITLE_SIZE = 18
SURFACE_LABEL_SIZE = 18
SURFACE_TICK_SIZE = 14

SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.70"
DARK_GREY = "0.35"
BLACK = "0.10"
LIGHT_GREY = "0.84"
POLE_RED = "#b84a4a"

FS_HZ = 48_000.0
MAGNITUDE_LIMITS_DB = (-18.0, 8.0)
MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]
NORMALIZED_OMEGA_TICKS = [0.0, 0.25, 0.5, 0.75, 1.0]
NORMALIZED_OMEGA_TICKLABELS = ["0", "0.25", "0.5", "0.75", "1"]
Z_LIMIT = 1.35
SURFACE_LIMIT = 1.35
SURFACE_MIN_DB = -25.0
SURFACE_MAX_DB = 25.0

FIR_COEFFICIENTS = (0.70, -0.70)
IIR_FEEDBACK_COEFFICIENTS = (0.70, -0.70)
Z_PLANE_COEFFICIENT = 0.70

INITIAL_DELAY_SAMPLES = 6
SECOND_DELAY_SAMPLES = 10

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class CombDelay:
    label: str
    samples: int

    @property
    def normalized_comb_spacing(self) -> float:
        return 2.0 / self.samples


INITIAL_DELAY = CombDelay("initial delay", INITIAL_DELAY_SAMPLES)
SECOND_DELAY = CombDelay("new delay", SECOND_DELAY_SAMPLES)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.glob("*.png"):
        image_file.unlink()


def save_figure(fig, filename: str) -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def normalized_omega_grid() -> np.ndarray:
    return np.linspace(0.0, 1.0, 4096)


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def magnitude_db_clipped(response: np.ndarray) -> np.ndarray:
    return np.clip(20.0 * np.log10(np.maximum(np.abs(response), 1e-9)), SURFACE_MIN_DB, SURFACE_MAX_DB)


def fir_comb_response(normalized_omega: np.ndarray, delay_samples: int, coefficient: float) -> np.ndarray:
    omega = normalized_omega * np.pi
    normalization = 1.0 + abs(coefficient)
    return (1.0 + coefficient * np.exp(-1j * omega * delay_samples)) / normalization


def iir_comb_response(normalized_omega: np.ndarray, delay_samples: int, coefficient: float) -> np.ndarray:
    omega = normalized_omega * np.pi
    blend = 1.0 - abs(coefficient)
    return blend / (1.0 - coefficient * np.exp(-1j * omega * delay_samples))


def response_at_z(z_values: np.ndarray, kind: str, delay_samples: int, coefficient: float) -> np.ndarray:
    z_power = z_values**delay_samples
    if kind == "fir":
        return (z_power + coefficient) / ((1.0 + abs(coefficient)) * z_power)
    return (1.0 - abs(coefficient)) * z_power / (z_power - coefficient)


def roots_of_power(value: complex, delay_samples: int) -> np.ndarray:
    radius = abs(value) ** (1.0 / delay_samples)
    angle = np.angle(value)
    indices = np.arange(delay_samples)
    return radius * np.exp(1j * (angle + 2.0 * np.pi * indices) / delay_samples)


def roots_for_comb(kind: str, delay_samples: int, coefficient: float) -> tuple[np.ndarray, np.ndarray]:
    origin_roots = np.zeros(delay_samples, dtype=complex)
    if kind == "fir":
        zeros = roots_of_power(-coefficient, delay_samples)
        poles = origin_roots
    else:
        zeros = origin_roots
        poles = roots_of_power(coefficient, delay_samples)
    return zeros, poles


def unique_complex_values(values: np.ndarray, precision: int = 6) -> np.ndarray:
    rounded = np.round(values.real, precision) + 1j * np.round(values.imag, precision)
    _, unique_indices = np.unique(rounded, return_index=True)
    return values[np.sort(unique_indices)]


def style_axis(ax, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(NORMALIZED_OMEGA_TICKS)
    ax.set_xticklabels(NORMALIZED_OMEGA_TICKLABELS)
    ax.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax.set_yticks(MAGNITUDE_TICKS_DB)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|H(e^{j\Omega})|$ in dB", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def delay_text(delay: CombDelay) -> str:
    return rf"$M={delay.samples},\ \Delta(\Omega/\pi)={delay.normalized_comb_spacing:.2f}$"


def add_delay_annotation(ax, delay: CombDelay, color: str, y_position: float) -> None:
    ax.text(
        0.02,
        y_position,
        delay_text(delay),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
        color=color,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
    )


def add_coefficient_legend(ax) -> None:
    coefficient_handles = [
        Line2D([0], [0], color=DARK_GREY, lw=2.6, ls="-", label="positive coefficient"),
        Line2D([0], [0], color=DARK_GREY, lw=2.6, ls="--", label="negative coefficient"),
    ]
    coefficient_legend = ax.legend(handles=coefficient_handles, loc="upper right", fontsize=14, frameon=True)
    coefficient_legend.get_frame().set_facecolor("white")
    coefficient_legend.get_frame().set_edgecolor("none")
    coefficient_legend.get_frame().set_alpha(0.95)


def export_initial_response(kind: str, response_function, filename: str, title: str) -> None:
    normalized_omega = normalized_omega_grid()

    fig, ax = plt.subplots(figsize=FIGSIZE)
    coefficients = FIR_COEFFICIENTS if kind == "fir" else IIR_FEEDBACK_COEFFICIENTS
    for coefficient in coefficients:
        response = response_function(normalized_omega, INITIAL_DELAY.samples, coefficient)
        ax.plot(
            normalized_omega,
            magnitude_db(response),
            color=SYSTEM_GREEN,
            lw=3.0,
            ls="-" if coefficient > 0.0 else "--",
            zorder=3,
        )
    style_axis(ax, title)
    add_delay_annotation(ax, INITIAL_DELAY, SYSTEM_GREEN, 0.96)
    add_coefficient_legend(ax)
    save_figure(fig, filename)


def export_comparison_response(kind: str, response_function, filename: str, title: str) -> None:
    normalized_omega = normalized_omega_grid()

    fig, ax = plt.subplots(figsize=FIGSIZE)
    coefficients = FIR_COEFFICIENTS if kind == "fir" else IIR_FEEDBACK_COEFFICIENTS
    for coefficient in coefficients:
        second_response = response_function(normalized_omega, SECOND_DELAY.samples, coefficient)
        line_style = "-" if coefficient > 0.0 else "--"
        ax.plot(
            normalized_omega,
            magnitude_db(second_response),
            color=SYSTEM_GREEN,
            lw=3.0,
            ls=line_style,
            zorder=3,
        )
    style_axis(ax, title)
    add_delay_annotation(ax, SECOND_DELAY, SYSTEM_GREEN, 0.96)
    add_coefficient_legend(ax)
    save_figure(fig, filename)


def setup_z_plane_2d(ax) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    ax.set_title("z-Plane", fontsize=22, pad=10)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-Z_LIMIT, Z_LIMIT)
    ax.set_ylim(-Z_LIMIT, Z_LIMIT)
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel(r"Re$\{z\}$", fontsize=24)
    ax.set_ylabel(r"Im$\{z\}$", fontsize=24)
    ax.grid(alpha=0.20)
    ax.tick_params(labelsize=18)
    ax.axhline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax.axvline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_pole_zero_count_annotation(ax, zero_count: int, pole_count: int) -> None:
    ax.text(
        0.04,
        0.96,
        f"Zeros: {zero_count}\nPoles: {pole_count}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
        color=DARK_GREY,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        zorder=20,
    )


def plot_poles_zeros_2d(ax, kind: str, delay_samples: int, coefficient: float) -> None:
    zeros, poles = roots_for_comb(kind, delay_samples, coefficient)
    add_pole_zero_count_annotation(ax, len(zeros), len(poles))
    zeros = unique_complex_values(zeros)
    poles = unique_complex_values(poles)
    ax.scatter(
        zeros.real,
        zeros.imag,
        s=10.5**2,
        marker="o",
        facecolors="white",
        edgecolors=SYSTEM_GREEN,
        linewidth=2.3,
        zorder=8,
        clip_on=False,
    )
    ax.scatter(
        poles.real,
        poles.imag,
        s=9.5**2,
        marker="x",
        color=POLE_RED,
        linewidth=2.4,
        zorder=8,
        clip_on=False,
    )


def plot_poles_zeros_3d(ax, kind: str, delay_samples: int, coefficient: float) -> None:
    zeros, poles = roots_for_comb(kind, delay_samples, coefficient)
    zeros = unique_complex_values(zeros)
    poles = unique_complex_values(poles)
    ax.scatter(
        zeros.real,
        zeros.imag,
        np.full(zeros.shape, SURFACE_MIN_DB),
        s=88,
        marker="o",
        facecolors="white",
        edgecolors=SYSTEM_GREEN,
        linewidth=2.3,
        depthshade=False,
        zorder=8,
    )
    ax.scatter(
        poles.real,
        poles.imag,
        np.full(poles.shape, SURFACE_MIN_DB),
        s=92,
        marker="x",
        color=POLE_RED,
        linewidth=2.4,
        depthshade=False,
        zorder=8,
    )


def setup_surface_axis(ax_surface) -> None:
    ax_surface.set_title("z-Plane", fontsize=SURFACE_TITLE_SIZE, y=1.005, pad=0)
    ax_surface.set_xlabel(r"Re$\{z\}$", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_ylabel(r"Im$\{z\}$", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_zlabel(r"$|H(z)|$ in dB", fontsize=SURFACE_LABEL_SIZE, labelpad=3)
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


def export_z_plane_2d(kind: str, filename: str, delay: CombDelay = SECOND_DELAY, show_delay: bool = False) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE_Z_PLANE_2D, dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.16, right=0.96, bottom=0.15, top=0.86)
    setup_z_plane_2d(ax)
    plot_poles_zeros_2d(ax, kind, delay.samples, Z_PLANE_COEFFICIENT)
    if show_delay:
        add_delay_annotation(ax, delay, DARK_GREY, 0.14)
    save_figure(fig, filename)


def export_z_plane_3d(kind: str, filename: str) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    omega = np.linspace(0.0, np.pi, 520)
    unit_circle = np.exp(1j * theta)
    active_path = np.exp(1j * omega)
    active_response = magnitude_db_clipped(response_at_z(active_path, kind, SECOND_DELAY.samples, Z_PLANE_COEFFICIENT))

    real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
    imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
    real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
    z_grid = real_grid + 1j * imag_grid
    response = response_at_z(z_grid, kind, SECOND_DELAY.samples, Z_PLANE_COEFFICIENT)
    response_db = magnitude_db_clipped(response)
    if kind == "fir":
        response_db[np.abs(z_grid) < 0.035] = np.nan
    else:
        response_db[np.abs(z_grid**SECOND_DELAY.samples - Z_PLANE_COEFFICIENT) < 0.006] = np.nan

    fig = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
    ax = fig.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.02, right=0.91, bottom=0.04, top=0.82)
    ax.plot(
        unit_circle.real,
        unit_circle.imag,
        np.full_like(theta, SURFACE_MIN_DB),
        color=LIGHT_GREY,
        lw=2.2,
        alpha=0.78,
        zorder=0,
    )
    ax.plot_surface(
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
    ax.plot(
        active_path.real,
        active_path.imag,
        active_response,
        color=SYSTEM_GREEN,
        lw=3.2,
        alpha=0.96,
        zorder=5,
    )
    plot_poles_zeros_3d(ax, kind, SECOND_DELAY.samples, Z_PLANE_COEFFICIENT)
    setup_surface_axis(ax)
    save_figure(fig, filename)


def main() -> None:
    clear_output_dir()
    export_initial_response(
        "fir",
        fir_comb_response,
        "01_fir_comb_initial_delay.png",
        "FIR comb filter magnitude response",
    )
    export_comparison_response(
        "fir",
        fir_comb_response,
        "02_fir_comb_delay_comparison.png",
        "FIR comb filter magnitude response",
    )
    export_initial_response(
        "iir",
        iir_comb_response,
        "03_iir_comb_initial_delay.png",
        "IIR comb filter magnitude response",
    )
    export_comparison_response(
        "iir",
        iir_comb_response,
        "04_iir_comb_delay_comparison.png",
        "IIR comb filter magnitude response",
    )
    export_z_plane_2d("fir", "05_fir_comb_z_plane_2d.png", INITIAL_DELAY, show_delay=True)
    export_z_plane_3d("fir", "06_fir_comb_z_plane_3d.png")
    export_z_plane_2d("iir", "07_iir_comb_z_plane_2d.png", INITIAL_DELAY, show_delay=True)
    export_z_plane_3d("iir", "08_iir_comb_z_plane_3d.png")
    export_z_plane_2d("fir", "09_fir_comb_dense_z_plane_2d.png", SECOND_DELAY, show_delay=True)
    export_z_plane_2d("iir", "10_iir_comb_dense_z_plane_2d.png", SECOND_DELAY, show_delay=True)


if __name__ == "__main__":
    main()
