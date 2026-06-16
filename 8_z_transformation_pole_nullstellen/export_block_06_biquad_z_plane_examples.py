from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "06_biquad_filter_z_ebene"

DPI = 160
IR_DPI = 200
FIGSIZE_FREQ = (10.5, 4.2)
FIGSIZE_SURFACE = (8.8, 6.2)
FIGSIZE_Z_ONLY = (5.2, 5.2)
FS_HZ = 48_000.0
NYQUIST_HZ = FS_HZ / 2.0
LOG_FREQ_MIN_HZ = 20.0
LOG_FREQ_MAX_HZ = 20_000.0

TITLE_SIZE = 18
LABEL_SIZE = 18
TICK_SIZE = 14
CROP_THRESHOLD = 250
CROP_PAD = 8
FREQ_LEFT_INCH = FIGSIZE_FREQ[0] * 0.10
FREQ_RIGHT_INCH = FIGSIZE_FREQ[0] * (1.0 - 0.98)
FREQ_BOTTOM = 0.19
FREQ_TOP = 0.82

BLACK = "0.10"
GREEN = "#66b77a"
LIGHT_GREY = "0.84"
UNIT_GREEN = "#3d9f5f"
POLE_RED = "#b84a4a"

Z_LIMIT = 1.25
SURFACE_LIMIT = 1.35
SURFACE_MIN_DB = -25.0
SURFACE_MAX_DB = 25.0
FREQ_MIN_DB = -12.0
FREQ_MAX_DB = 12.0

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class BiquadCoefficients:
    b0: float
    b1: float
    b2: float
    a1: float
    a2: float


@dataclass(frozen=True)
class BiquadExample:
    folder: str
    title: str
    kind: str
    frequency_hz: float
    q: float = 1.0 / np.sqrt(2.0)
    gain_db: float = 0.0
    shelf_slope: float = 1.0


BIQUAD_EXAMPLES = (
    BiquadExample("06A_low_pass", "Low-pass: higher cutoff", "lowpass", 4_000.0),
    BiquadExample("06B_high_pass", "High-pass: thin sound", "highpass", 1_000.0),
    BiquadExample("06C_notch", "Notch: moved center", "notch", 4_000.0, q=1.0),
    BiquadExample("06D_band_pass", "Band-pass: higher band", "bandpass", 4_000.0, q=1.0),
    BiquadExample("06E_low_shelf", "Low-shelf: higher corner", "lowshelf", 500.0, gain_db=6.0),
    BiquadExample("06F_high_shelf", "High-shelf: brightness boost", "highshelf", 4_000.0, gain_db=6.0),
    BiquadExample("06G_peaking_eq", "Peaking-EQ: moved boost", "peaking", 4_000.0, q=1.0, gain_db=6.0),
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


def normalize_biquad(b0: float, b1: float, b2: float, a0: float, a1: float, a2: float) -> BiquadCoefficients:
    return BiquadCoefficients(b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def design_biquad(example: BiquadExample) -> BiquadCoefficients:
    omega = 2.0 * np.pi * example.frequency_hz / FS_HZ
    cos_omega = np.cos(omega)
    sin_omega = np.sin(omega)
    alpha = sin_omega / (2.0 * example.q)

    if example.kind == "lowpass":
        b0 = (1.0 - cos_omega) / 2.0
        b1 = 1.0 - cos_omega
        b2 = (1.0 - cos_omega) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "highpass":
        b0 = (1.0 + cos_omega) / 2.0
        b1 = -(1.0 + cos_omega)
        b2 = (1.0 + cos_omega) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "bandpass":
        b0 = alpha
        b1 = 0.0
        b2 = -alpha
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "notch":
        b0 = 1.0
        b1 = -2.0 * cos_omega
        b2 = 1.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "peaking":
        amplitude = 10.0 ** (example.gain_db / 40.0)
        b0 = 1.0 + alpha * amplitude
        b1 = -2.0 * cos_omega
        b2 = 1.0 - alpha * amplitude
        a0 = 1.0 + alpha / amplitude
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha / amplitude
    elif example.kind in {"lowshelf", "highshelf"}:
        amplitude = 10.0 ** (example.gain_db / 40.0)
        shelf_alpha = (
            sin_omega
            / 2.0
            * np.sqrt((amplitude + 1.0 / amplitude) * (1.0 / example.shelf_slope - 1.0) + 2.0)
        )
        root_amplitude = np.sqrt(amplitude)
        if example.kind == "lowshelf":
            b0 = amplitude * (
                (amplitude + 1.0) - (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha
            )
            b1 = 2.0 * amplitude * ((amplitude - 1.0) - (amplitude + 1.0) * cos_omega)
            b2 = amplitude * (
                (amplitude + 1.0) - (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha
            )
            a0 = (amplitude + 1.0) + (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha
            a1 = -2.0 * ((amplitude - 1.0) + (amplitude + 1.0) * cos_omega)
            a2 = (amplitude + 1.0) + (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha
        else:
            b0 = amplitude * (
                (amplitude + 1.0) + (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha
            )
            b1 = -2.0 * amplitude * ((amplitude - 1.0) + (amplitude + 1.0) * cos_omega)
            b2 = amplitude * (
                (amplitude + 1.0) + (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha
            )
            a0 = (amplitude + 1.0) - (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha
            a1 = 2.0 * ((amplitude - 1.0) - (amplitude + 1.0) * cos_omega)
            a2 = (amplitude + 1.0) - (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha
    else:
        raise ValueError(f"Unknown biquad kind: {example.kind}")

    return normalize_biquad(b0, b1, b2, a0, a1, a2)


def coefficient_arrays(coefficients: BiquadCoefficients) -> tuple[np.ndarray, np.ndarray]:
    b = np.asarray((coefficients.b0, coefficients.b1, coefficients.b2), dtype=float)
    a = np.asarray((1.0, coefficients.a1, coefficients.a2), dtype=float)
    return b, a


def roots_from_biquad(coefficients: BiquadCoefficients) -> tuple[np.ndarray, np.ndarray]:
    b, a = coefficient_arrays(coefficients)
    zeros = np.roots(b)
    poles = np.roots(a)
    zeros[np.abs(zeros) < 1.0e-12] = 0.0
    poles[np.abs(poles) < 1.0e-12] = 0.0
    return zeros, poles


def unique_complex_values(values: np.ndarray, precision: int = 6) -> np.ndarray:
    rounded = np.round(values.real, precision) + 1j * np.round(values.imag, precision)
    _, unique_indices = np.unique(rounded, return_index=True)
    return values[np.sort(unique_indices)]


def response_on_unit_circle(omega_values: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    z = np.exp(1j * omega_values)
    return response_at_z(z, coefficients)


def response_at_z(z_values: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    numerator = coefficients.b0 * z_values**2 + coefficients.b1 * z_values + coefficients.b2
    denominator = z_values**2 + coefficients.a1 * z_values + coefficients.a2
    with np.errstate(divide="ignore", invalid="ignore"):
        return numerator / denominator


def magnitude_db(values: np.ndarray) -> np.ndarray:
    return np.clip(20.0 * np.log10(np.maximum(np.abs(values), 1.0e-9)), SURFACE_MIN_DB, SURFACE_MAX_DB)


def format_frequency(value_hz: float) -> str:
    if value_hz >= 1_000.0:
        return f"{value_hz / 1_000.0:g} kHz"
    return f"{value_hz:g} Hz"


def parameter_text(example: BiquadExample) -> str:
    parts = [rf"$f_0={format_frequency(example.frequency_hz)}$"]
    if example.kind in {"lowpass", "highpass", "bandpass", "notch", "peaking"}:
        parts.append(rf"$Q={example.q:.2g}$")
    if example.kind in {"lowshelf", "highshelf", "peaking"}:
        parts.append(rf"$G={example.gain_db:+.1f}\,\mathrm{{dB}}$")
    return ", ".join(parts)


def spectrum_title(example: BiquadExample) -> str:
    return f"{example.title} | {parameter_text(example)}"


def coefficient_text(coefficients: BiquadCoefficients) -> str:
    return (
        rf"$b_0={coefficients.b0:+.3f}$" + "\n"
        + rf"$b_1={coefficients.b1:+.3f}$" + "\n"
        + rf"$b_2={coefficients.b2:+.3f}$" + "\n"
        + rf"$a_1={coefficients.a1:+.3f}$" + "\n"
        + rf"$a_2={coefficients.a2:+.3f}$"
    )


def coefficient_box_location(example: BiquadExample) -> str:
    if example.folder == "06F_high_shelf":
        return "lower_left"
    return "upper_right"


def add_coefficient_box(ax, coefficients: BiquadCoefficients, location: str = "upper_right") -> None:
    if location == "lower_left":
        x_position = 0.035
        y_position = 0.055
        horizontal_alignment = "left"
        vertical_alignment = "bottom"
    else:
        x_position = 0.985
        y_position = 0.955
        horizontal_alignment = "right"
        vertical_alignment = "top"

    label = ax.text(
        x_position,
        y_position,
        coefficient_text(coefficients),
        transform=ax.transAxes,
        fontsize=13,
        color=BLACK,
        ha=horizontal_alignment,
        va=vertical_alignment,
        zorder=10,
        bbox={
            "boxstyle": "square,pad=0.18",
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 1.0,
        },
    )
    label.set_path_effects([path_effects.withStroke(linewidth=1.2, foreground="white")])


def plot_poles_zeros_2d(ax, coefficients: BiquadCoefficients) -> None:
    zeros, poles = roots_from_biquad(coefficients)
    zeros = unique_complex_values(zeros)
    poles = unique_complex_values(poles)
    ax.scatter(
        zeros.real,
        zeros.imag,
        s=10.5**2,
        marker="o",
        facecolors="white",
        edgecolors=UNIT_GREEN,
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


def plot_poles_zeros_3d(ax, coefficients: BiquadCoefficients) -> None:
    zeros, poles = roots_from_biquad(coefficients)
    zeros = unique_complex_values(zeros)
    poles = unique_complex_values(poles)
    ax.scatter(
        zeros.real,
        zeros.imag,
        np.full(zeros.shape, SURFACE_MIN_DB),
        s=88,
        marker="o",
        facecolors="white",
        edgecolors=UNIT_GREEN,
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


def export_z_plane_2d(output_dir: Path, coefficients: BiquadCoefficients) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    fig_z, ax_z = plt.subplots(figsize=FIGSIZE_Z_ONLY, dpi=IR_DPI, facecolor="white")
    fig_z.subplots_adjust(left=0.18, right=0.95, bottom=0.16, top=0.86)

    ax_z.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    ax_z.axhline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax_z.axvline(0.0, color=BLACK, lw=1.1, zorder=0)
    plot_poles_zeros_2d(ax_z, coefficients)

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

    fig_z.savefig(output_dir / "01_z_plane_2d.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_z)


def setup_surface_axis(ax_surface, title: str) -> None:
    ax_surface.set_title(title, fontsize=TITLE_SIZE, y=1.005, pad=0)
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


def export_z_plane_3d(output_dir: Path, example: BiquadExample, coefficients: BiquadCoefficients) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    omega = np.linspace(0.0, np.pi, 520)
    unit_circle = np.exp(1j * theta)
    active_path = np.exp(1j * omega)
    active_response = magnitude_db(response_on_unit_circle(omega, coefficients))

    real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
    imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 230)
    real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
    z_grid = real_grid + 1j * imag_grid
    denominator = z_grid**2 + coefficients.a1 * z_grid + coefficients.a2
    response_db = magnitude_db(response_at_z(z_grid, coefficients))
    response_db[np.abs(denominator) < 0.006] = np.nan

    fig_surface = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
    ax_surface = fig_surface.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig_surface.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)

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
        zorder=1,
    )
    ax_surface.plot(
        active_path.real,
        active_path.imag,
        active_response,
        color=GREEN,
        lw=3.2,
        alpha=0.96,
        zorder=5,
    )
    plot_poles_zeros_3d(ax_surface, coefficients)

    setup_surface_axis(ax_surface, example.title)
    fig_surface.savefig(output_dir / "02_z_plane_3d.png", dpi=DPI, facecolor="white")
    plt.close(fig_surface)


def adjust_frequency_figure(fig) -> None:
    width, _ = fig.get_size_inches()
    fig.subplots_adjust(
        left=FREQ_LEFT_INCH / width,
        right=1.0 - FREQ_RIGHT_INCH / width,
        bottom=FREQ_BOTTOM,
        top=FREQ_TOP,
    )


def setup_frequency_axis(ax_freq, response_linear: np.ndarray, title: str) -> None:
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


def frequency_y_limits(response_linear: np.ndarray) -> tuple[float, list[float]]:
    y_max = float(np.nanmax(response_linear))
    if y_max <= 1.05:
        return 1.05, [0.0, 0.5, 1.0]
    y_limit = float(np.ceil(y_max * 1.08))
    return y_limit, [0.0, 0.5 * y_limit, y_limit]


def setup_log_frequency_axis(ax_freq, response_linear: np.ndarray, title: str) -> None:
    y_limit, y_ticks = frequency_y_limits(response_linear)
    ax_freq.set_title(title, fontsize=22, pad=10)
    ax_freq.set_xscale("log")
    ax_freq.set_xlim(LOG_FREQ_MIN_HZ, LOG_FREQ_MAX_HZ)
    ax_freq.set_ylim(0.0, y_limit)
    ax_freq.set_xticks([20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0])
    ax_freq.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax_freq.set_yticks(y_ticks)
    ax_freq.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=24)
    ax_freq.set_ylabel(r"$|H(e^{j\Omega})|$", fontsize=24)
    ax_freq.grid(alpha=0.25, which="both")
    ax_freq.set_axisbelow(True)
    ax_freq.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_freq.spines[spine].set_visible(False)


def setup_log_frequency_db_axis(ax_freq, title: str) -> None:
    ax_freq.set_title(title, fontsize=22, pad=10)
    ax_freq.set_xscale("log")
    ax_freq.set_xlim(LOG_FREQ_MIN_HZ, LOG_FREQ_MAX_HZ)
    ax_freq.set_ylim(FREQ_MIN_DB, FREQ_MAX_DB)
    ax_freq.set_xticks([20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0])
    ax_freq.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax_freq.set_yticks([-12.0, -6.0, 0.0, 6.0, 12.0])
    ax_freq.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=24)
    ax_freq.set_ylabel("Magnitude in dB", fontsize=24)
    ax_freq.grid(alpha=0.25, which="both")
    ax_freq.set_axisbelow(True)
    ax_freq.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax_freq.spines[spine].set_visible(False)


def export_frequency_response(output_dir: Path, example: BiquadExample, coefficients: BiquadCoefficients) -> None:
    omega_values = np.linspace(0.0, np.pi, 121)
    response_linear = np.abs(response_on_unit_circle(omega_values, coefficients))
    response_linear = np.where(np.isfinite(response_linear), response_linear, np.nan)
    normalized_frequency = omega_values / np.pi
    title = spectrum_title(example)
    box_location = coefficient_box_location(example)

    fig_freq, ax_freq = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_freq)
    ax_freq.plot(normalized_frequency, response_linear, color=GREEN, lw=3.2, zorder=2)
    setup_frequency_axis(ax_freq, response_linear, title)
    add_coefficient_box(ax_freq, coefficients, box_location)
    fig_freq.savefig(output_dir / "03_frequency_response.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_freq)

    log_frequency_hz = np.geomspace(LOG_FREQ_MIN_HZ, LOG_FREQ_MAX_HZ, 360)
    log_omega_values = 2.0 * np.pi * log_frequency_hz / FS_HZ
    log_response_linear = np.abs(response_on_unit_circle(log_omega_values, coefficients))
    log_response_linear = np.where(np.isfinite(log_response_linear), log_response_linear, np.nan)

    fig_log, ax_log = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_log)
    ax_log.plot(log_frequency_hz, log_response_linear, color=GREEN, lw=3.2, zorder=2)
    setup_log_frequency_axis(ax_log, log_response_linear, title)
    add_coefficient_box(ax_log, coefficients, box_location)
    fig_log.savefig(output_dir / "04_frequency_response_log.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_log)

    log_response_db = 20.0 * np.log10(np.maximum(log_response_linear, 1.0e-9))

    fig_log_db, ax_log_db = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig_log_db)
    ax_log_db.plot(log_frequency_hz, log_response_db, color=GREEN, lw=3.2, zorder=2)
    setup_log_frequency_db_axis(ax_log_db, title)
    add_coefficient_box(ax_log_db, coefficients, box_location)
    fig_log_db.savefig(output_dir / "05_frequency_response_log_db.png", dpi=IR_DPI, facecolor="white")
    plt.close(fig_log_db)


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
            image.crop(crop_box).save(png_file)


def crop_outputs() -> None:
    z_plane_files = sorted(OUTPUT_DIR.rglob("01_z_plane_2d.png"))
    surface_files = sorted(OUTPUT_DIR.rglob("02_z_plane_3d.png"))
    crop_png_group(z_plane_files)
    crop_png_group(surface_files)


def write_readme() -> None:
    readme = OUTPUT_DIR / "README.md"
    readme.write_text(
        """# Block 6: Biquad-Filter in der z-Ebene

Jeder Unterblock enthaelt genau fuenf Einzelabbildungen:

- `01_z_plane_2d.png`: Pol-Nullstellen-Diagramm in der 2D-z-Ebene
- `02_z_plane_3d.png`: Auswertung von `|H(z)|` in der 3D-z-Ebene
- `03_frequency_response.png`: Frequenzgang auf dem Einheitskreis mit
  normierter linearer Frequenzachse
- `04_frequency_response_log.png`: derselbe Frequenzgang mit logarithmischer
  Frequenzachse in Hz
- `05_frequency_response_log_db.png`: logarithmische Frequenzachse und Betrag
  in dB

Die Layout-Konstanten entsprechen Block 5. Die Spektren verwenden die
Titel- und Koeffizientenbox-Logik aus der 7. Vorlesung.
""",
        encoding="utf-8",
    )


def export_example(example: BiquadExample) -> None:
    coefficients = design_biquad(example)
    output_dir = OUTPUT_DIR / example.folder
    output_dir.mkdir(parents=True, exist_ok=True)
    export_z_plane_2d(output_dir, coefficients)
    export_z_plane_3d(output_dir, example, coefficients)
    export_frequency_response(output_dir, example, coefficients)


def main() -> None:
    clear_output_dir()
    for example in BIQUAD_EXAMPLES:
        export_example(example)
    crop_outputs()
    write_readme()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
