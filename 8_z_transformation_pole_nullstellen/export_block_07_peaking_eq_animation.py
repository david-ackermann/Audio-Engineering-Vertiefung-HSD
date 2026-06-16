from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageSequence


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "07_peaking_eq_animation"

DPI = 160
IR_DPI = 200
FPS = 8
FRAME_COUNT = 72
FIGSIZE_FREQ = (10.5, 4.2)
FIGSIZE_SURFACE = (8.8, 6.2)
FIGSIZE_Z_ONLY = (5.2, 5.2)
FS_HZ = 48_000.0
LOG_FREQ_MIN_HZ = 20.0
LOG_FREQ_MAX_HZ = 20_000.0

TITLE_SIZE = 18
LABEL_SIZE = 18
TICK_SIZE = 14
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
TARGET_Z_2D_SIZE = (962, 960)
TARGET_Z_3D_SIZE = (921, 761)

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
class SweepState:
    frequency_hz: float
    q: float
    gain_db: float


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_file in OUTPUT_DIR.rglob("*"):
        if output_file.is_file() and output_file.suffix.lower() in {".png", ".gif"}:
            output_file.unlink()


def logarithmic_frequency_progress(t: float) -> float:
    curve = 9.0
    return float(np.log1p(curve * t) / np.log1p(curve))


def sweep_states() -> list[SweepState]:
    states: list[SweepState] = []
    for frame_index in range(FRAME_COUNT):
        t = frame_index / (FRAME_COUNT - 1)
        frequency_progress = logarithmic_frequency_progress(t)
        envelope = np.sin(np.pi * t) ** 1.35
        frequency_hz = 80.0 * (12_000.0 / 80.0) ** frequency_progress
        q = 0.30 + 7.70 * envelope
        gain_db = -5.0 + 15.0 * envelope
        states.append(SweepState(frequency_hz=frequency_hz, q=q, gain_db=gain_db))
    return states


def design_peaking_eq(state: SweepState) -> BiquadCoefficients:
    omega = 2.0 * np.pi * state.frequency_hz / FS_HZ
    sin_omega = np.sin(omega)
    cos_omega = np.cos(omega)
    alpha = sin_omega / (2.0 * state.q)
    amplitude = 10.0 ** (state.gain_db / 40.0)

    b0 = 1.0 + alpha * amplitude
    b1 = -2.0 * cos_omega
    b2 = 1.0 - alpha * amplitude
    a0 = 1.0 + alpha / amplitude
    a1 = -2.0 * cos_omega
    a2 = 1.0 - alpha / amplitude
    return BiquadCoefficients(b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def coefficient_arrays(coefficients: BiquadCoefficients) -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray((coefficients.b0, coefficients.b1, coefficients.b2), dtype=float),
        np.asarray((1.0, coefficients.a1, coefficients.a2), dtype=float),
    )


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


def response_at_z(z_values: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    numerator = coefficients.b0 * z_values**2 + coefficients.b1 * z_values + coefficients.b2
    denominator = z_values**2 + coefficients.a1 * z_values + coefficients.a2
    with np.errstate(divide="ignore", invalid="ignore"):
        return numerator / denominator


def magnitude_db(values: np.ndarray, minimum: float, maximum: float) -> np.ndarray:
    magnitude = 20.0 * np.log10(np.maximum(np.abs(values), 1.0e-9))
    return np.clip(magnitude, minimum, maximum)


def format_frequency(value_hz: float) -> str:
    if value_hz >= 1_000.0:
        return f"{value_hz / 1_000.0:.2g} kHz"
    return f"{value_hz:.0f} Hz"


def parameter_text(state: SweepState) -> str:
    return rf"$f_0={format_frequency(state.frequency_hz)}$, $Q={state.q:.2g}$, $G={state.gain_db:+.1f}\,\mathrm{{dB}}$"


def coefficient_text(coefficients: BiquadCoefficients) -> str:
    return (
        rf"$b_0={coefficients.b0:+.3f}$" + "\n"
        + rf"$b_1={coefficients.b1:+.3f}$" + "\n"
        + rf"$b_2={coefficients.b2:+.3f}$" + "\n"
        + rf"$a_1={coefficients.a1:+.3f}$" + "\n"
        + rf"$a_2={coefficients.a2:+.3f}$"
    )


def add_coefficient_box(ax, coefficients: BiquadCoefficients) -> None:
    label = ax.text(
        0.985,
        0.955,
        coefficient_text(coefficients),
        transform=ax.transAxes,
        fontsize=13,
        color=BLACK,
        ha="right",
        va="top",
        zorder=10,
        bbox={
            "boxstyle": "square,pad=0.18",
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 1.0,
        },
    )
    label.set_path_effects([path_effects.withStroke(linewidth=1.2, foreground="white")])


def adjust_frequency_figure(fig) -> None:
    width, _ = fig.get_size_inches()
    fig.subplots_adjust(
        left=FREQ_LEFT_INCH / width,
        right=1.0 - FREQ_RIGHT_INCH / width,
        bottom=FREQ_BOTTOM,
        top=FREQ_TOP,
    )


def render_figure_to_image(fig) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def setup_spectrum_axis(ax, state: SweepState) -> None:
    ax.set_title(f"Peaking-EQ: sweep | {parameter_text(state)}", fontsize=22, pad=10)
    ax.set_xscale("log")
    ax.set_xlim(LOG_FREQ_MIN_HZ, LOG_FREQ_MAX_HZ)
    ax.set_ylim(FREQ_MIN_DB, FREQ_MAX_DB)
    ax.set_xticks([20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax.set_yticks([-12.0, -6.0, 0.0, 6.0, 12.0])
    ax.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=24)
    ax.set_ylabel("Magnitude in dB", fontsize=24)
    ax.grid(alpha=0.25, which="both")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def render_spectrum_frame(state: SweepState, coefficients: BiquadCoefficients) -> Image.Image:
    frequency_hz = np.geomspace(LOG_FREQ_MIN_HZ, LOG_FREQ_MAX_HZ, 460)
    omega_values = 2.0 * np.pi * frequency_hz / FS_HZ
    response_db = magnitude_db(response_at_z(np.exp(1j * omega_values), coefficients), FREQ_MIN_DB, FREQ_MAX_DB)

    fig, ax = plt.subplots(figsize=FIGSIZE_FREQ, dpi=IR_DPI, facecolor="white")
    adjust_frequency_figure(fig)
    ax.plot(frequency_hz, response_db, color=GREEN, lw=3.2, zorder=2)
    setup_spectrum_axis(ax, state)
    add_coefficient_box(ax, coefficients)
    return render_figure_to_image(fig)


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


def setup_z_2d_axis(ax) -> None:
    ax.set_title("z-plane", fontsize=22, pad=10)
    ax.set_xlim(-Z_LIMIT, Z_LIMIT)
    ax.set_ylim(-Z_LIMIT, Z_LIMIT)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel(r"Re$\{z\}$", fontsize=24)
    ax.set_ylabel(r"Im$\{z\}$", fontsize=24)
    ax.grid(alpha=0.20)
    ax.tick_params(labelsize=18)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def render_z_plane_2d_frame(coefficients: BiquadCoefficients) -> Image.Image:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    fig, ax = plt.subplots(figsize=FIGSIZE_Z_ONLY, dpi=IR_DPI, facecolor="white")
    fig.subplots_adjust(left=0.18, right=0.95, bottom=0.16, top=0.86)
    ax.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    ax.axhline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax.axvline(0.0, color=BLACK, lw=1.1, zorder=0)
    plot_poles_zeros_2d(ax, coefficients)
    setup_z_2d_axis(ax)
    return render_figure_to_image(fig)


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


def setup_surface_axis(ax) -> None:
    ax.set_title("z-plane", fontsize=TITLE_SIZE, y=1.005, pad=0)
    ax.set_xlabel(r"Re$\{z\}$", fontsize=LABEL_SIZE, labelpad=8)
    ax.set_ylabel(r"Im$\{z\}$", fontsize=LABEL_SIZE, labelpad=8)
    ax.set_zlabel(r"$|H(z)|$ in dB", fontsize=LABEL_SIZE, labelpad=8)
    ax.set_xlim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax.set_ylim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax.set_zlim(SURFACE_MIN_DB, SURFACE_MAX_DB)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_zticks([-25.0, 0.0, 25.0])
    ax.tick_params(labelsize=TICK_SIZE)
    ax.view_init(elev=25, azim=-58)
    try:
        ax.set_box_aspect((1.9, 1.9, 1.25), zoom=1.08)
    except TypeError:
        ax.set_box_aspect((1.9, 1.9, 1.25))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))


def render_z_plane_3d_frame(coefficients: BiquadCoefficients) -> Image.Image:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    omega = np.linspace(0.0, np.pi, 420)
    unit_circle = np.exp(1j * theta)
    active_path = np.exp(1j * omega)
    active_response = magnitude_db(response_at_z(active_path, coefficients), SURFACE_MIN_DB, SURFACE_MAX_DB)

    real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 150)
    imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, 150)
    real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
    z_grid = real_grid + 1j * imag_grid
    denominator = z_grid**2 + coefficients.a1 * z_grid + coefficients.a2
    response_db = magnitude_db(response_at_z(z_grid, coefficients), SURFACE_MIN_DB, SURFACE_MAX_DB)
    response_db[np.abs(denominator) < 0.006] = np.nan

    fig = plt.figure(figsize=FIGSIZE_SURFACE, dpi=DPI, facecolor="white")
    ax = fig.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.04, top=0.82)
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
    ax.plot(active_path.real, active_path.imag, active_response, color=GREEN, lw=3.2, alpha=0.96, zorder=5)
    plot_poles_zeros_3d(ax, coefficients)
    setup_surface_axis(ax)
    return render_figure_to_image(fig)


def white_crop_box(image: Image.Image, threshold: int = 250, padding: int = 8) -> tuple[int, int, int, int] | None:
    rgb = image.convert("RGB")
    array = np.asarray(rgb)
    mask = np.any(array < threshold, axis=2)
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if rows.size == 0 or cols.size == 0:
        return None
    left = max(int(cols[0]) - padding, 0)
    top = max(int(rows[0]) - padding, 0)
    right = min(int(cols[-1]) + padding + 1, image.width)
    bottom = min(int(rows[-1]) + padding + 1, image.height)
    return left, top, right, bottom


def union_crop_box(frames: list[Image.Image]) -> tuple[int, int, int, int] | None:
    boxes = [box for frame in frames if (box := white_crop_box(frame)) is not None]
    if not boxes:
        return None
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def normalize_frame_size(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    target_width, target_height = target_size
    image = image.convert("RGB")
    if image.width > target_width or image.height > target_height:
        left = max((image.width - target_width) // 2, 0)
        top = max((image.height - target_height) // 2, 0)
        image = image.crop((left, top, left + min(target_width, image.width), top + min(target_height, image.height)))

    output = Image.new("RGB", target_size, (255, 255, 255))
    left = (target_width - image.width) // 2
    top = (target_height - image.height) // 2
    output.paste(image, (left, top))
    return output


def crop_and_normalize_frames(frames: list[Image.Image], target_size: tuple[int, int]) -> list[Image.Image]:
    crop_box = union_crop_box(frames)
    normalized_frames: list[Image.Image] = []
    for frame in frames:
        cropped = frame.crop(crop_box) if crop_box is not None else frame
        normalized_frames.append(normalize_frame_size(cropped, target_size))
    return normalized_frames


def save_gif(frames: list[Image.Image], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),
        loop=0,
        disposal=2,
        optimize=False,
    )


def save_first_last(frames: list[Image.Image], prefix: str) -> None:
    frames[0].save(OUTPUT_DIR / f"{prefix}_start.png")
    frames[-1].save(OUTPUT_DIR / f"{prefix}_end.png")


def write_readme() -> None:
    (OUTPUT_DIR / "README.md").write_text(
        """# Block 7: Peaking-EQ Sweep

Der Block enthaelt drei framegenau synchrone Animationen desselben
Peaking-EQ-Verlaufs:

- `01_spectrum_motion.gif`: Spektrum mit logarithmischer Frequenzachse und
  Betrag in dB und aktuellen Biquad-Koeffizienten
- `02_z_plane_2d_motion.gif`: Pol-Nullstellen-Bewegung in der 2D-z-Ebene
- `03_z_plane_3d_motion.gif`: zugehoerige 3D-z-Ebenenflaeche

Alle drei GIFs nutzen dieselbe Parameterfolge, dieselbe Framezahl und dieselbe
Bildrate. Der Peaking-EQ wandert mit logarithmisch gebremstem
Frequenzfortschritt von tiefen zu hohen Frequenzen; Gain und Guete steigen in
der Mitte deutlich an und sinken danach wieder. Der Gain wechselt dabei von
Cut zu Boost und zurueck zu Cut.
""",
        encoding="utf-8",
    )


def export_animation() -> None:
    clear_output_dir()
    states = sweep_states()
    coefficients = [design_peaking_eq(state) for state in states]

    spectrum_frames = [render_spectrum_frame(state, coeff) for state, coeff in zip(states, coefficients)]
    z_2d_frames = [render_z_plane_2d_frame(coeff) for coeff in coefficients]
    z_3d_frames = [render_z_plane_3d_frame(coeff) for coeff in coefficients]

    z_2d_frames = crop_and_normalize_frames(z_2d_frames, TARGET_Z_2D_SIZE)
    z_3d_frames = crop_and_normalize_frames(z_3d_frames, TARGET_Z_3D_SIZE)

    save_gif(spectrum_frames, OUTPUT_DIR / "01_spectrum_motion.gif")
    save_gif(z_2d_frames, OUTPUT_DIR / "02_z_plane_2d_motion.gif")
    save_gif(z_3d_frames, OUTPUT_DIR / "03_z_plane_3d_motion.gif")

    save_first_last(spectrum_frames, "01_spectrum")
    save_first_last(z_2d_frames, "02_z_plane_2d")
    save_first_last(z_3d_frames, "03_z_plane_3d")
    write_readme()
    print(f"Peaking-EQ animation exported to: {OUTPUT_DIR}")


def main() -> None:
    export_animation()


if __name__ == "__main__":
    main()
