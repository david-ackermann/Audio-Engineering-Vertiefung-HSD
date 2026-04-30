from pathlib import Path
import os
import shutil

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "06_idft_rekonstruktion"

DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 21
TICK_SIZE = 17

TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (11.0, 4.8)
PHASOR_FIGSIZE = (6.8, 6.8)

REFERENCE_TIME_EXPORT_SIZE = (2106, 926)
REFERENCE_PHASOR_EXPORT_SIZE = (1417, 1313)
REFERENCE_MAG_EXPORT_SIZE = (1924, 988)
REFERENCE_PHASE_EXPORT_SIZE = (1974, 988)

DISPLAY_FREQ_MIN_HZ = -7.0
DISPLAY_FREQ_MAX_HZ = 7.0
DISPLAY_FREQ_COUNT = 2601
SPECTRUM_TICKS_HZ = (-7.0, -5.0, -2.0, 0.0, 2.0, 5.0, 7.0)
WEIGHT_TICKS = np.arange(-1.0, 1.01, 0.5)
PHASE_Y_TICKS = np.arange(-180.0, 181.0, 90.0)

LEFT_MARGIN = 0.095
RIGHT_MARGIN = 0.985
BOTTOM_MARGIN = 0.16
TOP_MARGIN = 0.89

BASELINE_COLOR = "0.78"
GRID_ALPHA = 0.25
SIGNAL_BLACK = "0.15"
SIGNAL_LIGHT_BLUE = "#bddcf3"
RE_COLOR = "#2b7bbb"
IM_COLOR = "#d97a27"
ACTIVE_RED = "#d7263d"
SPECTRUM_GREY = "0.70"

FS_HZ = 16.0
N = 16
SNAPSHOT_INDICES = (3, 1, 0)

COMPONENTS = (
    (2.0, 1.00, np.pi / 4.0),
    (5.0, 0.85, -np.pi / 2.0),
)

SAMPLE_INDICES = np.arange(N, dtype=float)
DENSE_INDICES = np.linspace(0.0, N - 1, 2400)
DISPLAY_FREQS = np.linspace(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ, DISPLAY_FREQ_COUNT)


def build_signal(sample_positions: np.ndarray) -> np.ndarray:
    signal_values = np.zeros_like(sample_positions, dtype=float)
    for frequency_hz, amplitude, phase_rad in COMPONENTS:
        signal_values += amplitude * np.cos(2.0 * np.pi * frequency_hz * sample_positions / FS_HZ + phase_rad)
    return signal_values


SIGNAL_VALUES = build_signal(SAMPLE_INDICES)
SIGNAL_DENSE = build_signal(DENSE_INDICES)
FULL_FREQUENCIES_HZ = np.fft.fftfreq(N, d=1.0 / FS_HZ)
FULL_COEFFICIENTS = np.fft.fft(SIGNAL_VALUES)
FULL_RECONSTRUCTED_SEQUENCE = np.array(
    [
        (1.0 / N)
        * np.sum(FULL_COEFFICIENTS * np.exp(1j * 2.0 * np.pi * FULL_FREQUENCIES_HZ * sample_index / FS_HZ))
        for sample_index in SAMPLE_INDICES
    ],
    dtype=complex,
)
GLOBAL_COMPLEX_LIMIT = 1.15 * max(
    0.2,
    np.max(np.abs(np.real(FULL_RECONSTRUCTED_SEQUENCE))),
    np.max(np.abs(np.imag(FULL_RECONSTRUCTED_SEQUENCE))),
)


def symmetric_ticks(limit: float, step: float) -> np.ndarray:
    max_tick = step * np.floor(limit / step)
    return np.arange(-max_tick, max_tick + 0.5 * step, step)


def positive_ticks(limit: float, step: float) -> np.ndarray:
    max_tick = step * np.floor(limit / step)
    return np.arange(0.0, max_tick + 0.5 * step, step)


SHIFTED_FREQUENCIES_HZ = np.fft.fftshift(FULL_FREQUENCIES_HZ)
SHIFTED_COEFFICIENTS = np.fft.fftshift(FULL_COEFFICIENTS)
VISIBLE_SPECTRUM_MASK = (SHIFTED_FREQUENCIES_HZ >= DISPLAY_FREQ_MIN_HZ) & (SHIFTED_FREQUENCIES_HZ <= DISPLAY_FREQ_MAX_HZ)
VISIBLE_LINE_FREQS = SHIFTED_FREQUENCIES_HZ[VISIBLE_SPECTRUM_MASK]
VISIBLE_LINE_COEFFS = SHIFTED_COEFFICIENTS[VISIBLE_SPECTRUM_MASK]
VISIBLE_LINE_MAGNITUDES = np.abs(VISIBLE_LINE_COEFFS)
VISIBLE_LINE_PHASES_RAD = np.angle(VISIBLE_LINE_COEFFS)

GLOBAL_SIGNAL_LIMIT = 1.15 * max(1.0, np.max(np.abs(SIGNAL_VALUES)))
GLOBAL_SPECTRUM_LIMIT = 1.15 * max(1.0, np.max(VISIBLE_LINE_MAGNITUDES))

_global_contribution_peak = 1.0
for _snapshot_index in SNAPSHOT_INDICES:
    _base_phase = 2.0 * np.pi * VISIBLE_LINE_FREQS * _snapshot_index / FS_HZ
    _real_product = VISIBLE_LINE_MAGNITUDES * np.cos(_base_phase + VISIBLE_LINE_PHASES_RAD)
    _imag_product = VISIBLE_LINE_MAGNITUDES * np.sin(_base_phase + VISIBLE_LINE_PHASES_RAD)
    _snapshot_complex = (1.0 / N) * np.sum(FULL_COEFFICIENTS * np.exp(1j * 2.0 * np.pi * FULL_FREQUENCIES_HZ * _snapshot_index / FS_HZ))
    _global_contribution_peak = max(
        _global_contribution_peak,
        np.max(np.abs(_real_product)),
        np.max(np.abs(_imag_product)),
        abs(_snapshot_complex.real),
        abs(_snapshot_complex.imag),
    )
GLOBAL_CONTRIBUTION_LIMIT = 1.15 * _global_contribution_peak

SEQUENCE_Y_TICKS = symmetric_ticks(GLOBAL_SIGNAL_LIMIT, 1.0)
SPECTRUM_Y_TICKS = positive_ticks(GLOBAL_SPECTRUM_LIMIT, 2.0)
CONTRIBUTION_Y_TICKS = symmetric_ticks(GLOBAL_CONTRIBUTION_LIMIT, 4.0)
COMPLEX_TICKS = symmetric_ticks(GLOBAL_COMPLEX_LIMIT, 0.5)


def snapshot_dir(snapshot_index: int) -> Path:
    return OUTPUT_ROOT / f"06A_idft_storyboard_n{snapshot_index}"


def handle_remove_readonly(function, path, _excinfo) -> None:
    os.chmod(path, 0o666)
    function(path)


def clear_output_root() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for child in OUTPUT_ROOT.iterdir():
        if child.is_dir():
            shutil.rmtree(child, onerror=handle_remove_readonly)
        else:
            child.unlink()


def create_time_figure():
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    return fig, ax


def create_spectrum_figure():
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.90, bottom=0.17, top=0.89)
    return fig, ax


def create_overlay_spectrum_figure():
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.84, bottom=0.17, top=0.89)
    return fig, ax


def create_square_figure():
    fig, ax = plt.subplots(figsize=PHASOR_FIGSIZE)
    fig.subplots_adjust(left=0.15, right=0.97, bottom=0.15, top=0.91)
    return fig, ax


def normalize_png_canvas(target_path: Path, target_size) -> None:
    image = Image.open(target_path).convert("RGBA")
    current_width, current_height = image.size
    target_width, target_height = target_size

    if current_width > target_width or current_height > target_height:
        scale_factor = min(target_width / current_width, target_height / current_height)
        resized_width = int(round(current_width * scale_factor))
        resized_height = int(round(current_height * scale_factor))
        image = image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
        current_width, current_height = image.size

    normalized = Image.new("RGBA", target_size, (255, 255, 255, 255))
    paste_x = max(0, (target_width - current_width) // 2)
    paste_y = max(0, (target_height - current_height) // 2)
    normalized.paste(image, (paste_x, paste_y))
    normalized.save(target_path)


def save_figure(fig, target_path: Path, target_size=None) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.10)
    plt.close(fig)
    if target_size is not None:
        normalize_png_canvas(target_path, target_size)


def finalize_frequency_axis(ax, title: str, y_limits, y_label: str, y_ticks=None) -> None:
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ)
    ax.set_ylim(*y_limits)
    ax.set_xticks(SPECTRUM_TICKS_HZ)
    if y_ticks is not None:
        ax.set_yticks(y_ticks)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def finalize_sequence_axis(ax, title: str, y_limits, y_label: str = "Amplitude", y_ticks=None) -> None:
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-0.35, N - 0.65)
    ax.set_ylim(*y_limits)
    ax.set_xticks(np.arange(0, N, 2))
    if y_ticks is not None:
        ax.set_yticks(y_ticks)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_discrete_spectrum(ax, line_freqs, values, color) -> None:
    ax.vlines(line_freqs, 0.0, values, color=color, lw=2.4)
    ax.plot(line_freqs, values, "o", color=color, ms=7)


def prepare_context(snapshot_index: int):
    line_freqs = VISIBLE_LINE_FREQS
    line_coeffs = VISIBLE_LINE_COEFFS
    line_magnitudes = np.abs(line_coeffs)
    line_phases_rad = np.angle(line_coeffs)
    line_phases_deg = np.degrees(line_phases_rad)

    base_phase_display = 2.0 * np.pi * DISPLAY_FREQS * snapshot_index / FS_HZ
    base_phase_lines = 2.0 * np.pi * line_freqs * snapshot_index / FS_HZ

    pure_real_weight = np.cos(base_phase_display)
    pure_imag_weight = np.sin(base_phase_display)
    pure_real_weight_lines = np.cos(base_phase_lines)
    pure_imag_weight_lines = np.sin(base_phase_lines)
    real_weight_lines = np.cos(base_phase_lines + line_phases_rad)
    imag_weight_lines = np.sin(base_phase_lines + line_phases_rad)
    real_product_lines = line_magnitudes * real_weight_lines
    imag_product_lines = line_magnitudes * imag_weight_lines

    complex_weight_full = np.exp(1j * 2.0 * np.pi * FULL_FREQUENCIES_HZ * snapshot_index / FS_HZ)
    snapshot_complex = (1.0 / N) * np.sum(FULL_COEFFICIENTS * complex_weight_full)

    reconstructed_sequence = FULL_RECONSTRUCTED_SEQUENCE

    return {
        "snapshot_index": snapshot_index,
        "line_freqs": line_freqs,
        "line_coeffs": line_coeffs,
        "line_magnitudes": line_magnitudes,
        "line_phases_deg": line_phases_deg,
        "pure_real_weight": pure_real_weight,
        "pure_imag_weight": pure_imag_weight,
        "pure_real_weight_lines": pure_real_weight_lines,
        "pure_imag_weight_lines": pure_imag_weight_lines,
        "real_weight_lines": real_weight_lines,
        "imag_weight_lines": imag_weight_lines,
        "real_product_lines": real_product_lines,
        "imag_product_lines": imag_product_lines,
        "real_sum": snapshot_complex.real,
        "imag_sum": snapshot_complex.imag,
        "snapshot_complex": snapshot_complex,
        "reconstructed_sequence": np.real(reconstructed_sequence),
        "signal_limit": GLOBAL_SIGNAL_LIMIT,
        "spectrum_limit": GLOBAL_SPECTRUM_LIMIT,
        "contribution_limit": GLOBAL_CONTRIBUTION_LIMIT,
        "complex_limit": GLOBAL_COMPLEX_LIMIT,
    }


def export_magnitude(context, output_dir: Path) -> None:
    fig, ax = create_spectrum_figure()
    draw_discrete_spectrum(ax, context["line_freqs"], context["line_magnitudes"], SPECTRUM_GREY)
    finalize_frequency_axis(ax, r"$|X[k]|$", (0.0, context["spectrum_limit"]), r"$|X[k]|$", SPECTRUM_Y_TICKS)
    save_figure(fig, output_dir / "01_two_sided_magnitude_spectrum.png", REFERENCE_MAG_EXPORT_SIZE)


def export_phase(context, output_dir: Path) -> None:
    fig, ax = create_spectrum_figure()
    draw_discrete_spectrum(ax, context["line_freqs"], context["line_phases_deg"], SPECTRUM_GREY)
    finalize_frequency_axis(ax, "Phase", (-190.0, 190.0), "Phase [deg]", PHASE_Y_TICKS)
    save_figure(fig, output_dir / "02_two_sided_phase_spectrum.png", REFERENCE_PHASE_EXPORT_SIZE)


def export_weighting_overlay(
    context,
    output_dir: Path,
    weight_curve,
    line_values,
    color,
    title: str,
    right_label: str,
    filename: str,
):
    fig, ax_mag = create_overlay_spectrum_figure()
    draw_discrete_spectrum(ax_mag, context["line_freqs"], context["line_magnitudes"], SPECTRUM_GREY)
    finalize_frequency_axis(ax_mag, title, (0.0, context["spectrum_limit"]), r"$|X[k]|$", SPECTRUM_Y_TICKS)

    ax_weight = ax_mag.twinx()
    ax_weight.plot(DISPLAY_FREQS, weight_curve, color=color, lw=2.0, ls="--")
    ax_weight.vlines(context["line_freqs"], 0.0, line_values, color=color, lw=2.1)
    ax_weight.plot(context["line_freqs"], line_values, "o", color=color, ms=6)
    ax_weight.axhline(0.0, color=color, lw=0.9, alpha=0.55)
    ax_weight.set_ylim(-1.1, 1.1)
    ax_weight.set_yticks(WEIGHT_TICKS)
    ax_weight.set_ylabel(right_label, fontsize=LABEL_SIZE - 1, color=color, labelpad=6)
    ax_weight.tick_params(axis="y", colors=color, labelsize=TICK_SIZE)
    save_figure(fig, output_dir / filename, REFERENCE_PHASE_EXPORT_SIZE)


def export_contribution(
    context,
    output_dir: Path,
    values,
    color,
    title: str,
    filename: str,
    sum_line=None,
):
    fig, ax = create_spectrum_figure()
    draw_discrete_spectrum(ax, context["line_freqs"], values, color)
    if sum_line is not None:
        ax.plot([DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ], [sum_line, sum_line], color=color, lw=2.0, ls="--")
    finalize_frequency_axis(
        ax,
        title,
        (-context["contribution_limit"], context["contribution_limit"]),
        "Contribution",
        CONTRIBUTION_Y_TICKS,
    )
    save_figure(fig, output_dir / filename, REFERENCE_MAG_EXPORT_SIZE)


def export_complex_sample(context, output_dir: Path) -> None:
    value = context["snapshot_complex"]

    fig, ax = create_square_figure()
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.plot([0.0, value.real], [0.0, value.imag], color=ACTIVE_RED, lw=3.0)
    ax.plot([value.real], [value.imag], "o", color=ACTIVE_RED, ms=9)
    ax.plot([0.0, value.real], [0.0, 0.0], color=RE_COLOR, lw=1.6, alpha=0.90)
    ax.plot([value.real, value.real], [0.0, value.imag], color=IM_COLOR, lw=1.6, alpha=0.90)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-context["complex_limit"], context["complex_limit"])
    ax.set_ylim(-context["complex_limit"], context["complex_limit"])
    ax.set_xticks(COMPLEX_TICKS)
    ax.set_yticks(COMPLEX_TICKS)
    ax.grid(alpha=0.22)
    ax.set_xlabel(r"Re$\{x[n_0]\}$", fontsize=LABEL_SIZE, color=RE_COLOR)
    ax.set_ylabel(r"Im$\{x[n_0]\}$", fontsize=LABEL_SIZE, color=IM_COLOR)
    ax.set_title(f"Complex sample, n = {context['snapshot_index']}", pad=10, fontsize=TITLE_SIZE)
    ax.tick_params(axis="x", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=IM_COLOR, labelsize=TICK_SIZE)
    save_figure(fig, output_dir / "11_complex_sample.png", REFERENCE_PHASOR_EXPORT_SIZE)


def export_reconstructed_block(context, output_dir: Path) -> None:
    snapshot_index = context["snapshot_index"]
    sample_value = context["reconstructed_sequence"][snapshot_index]

    fig, ax = create_time_figure()
    ax.plot(DENSE_INDICES, SIGNAL_DENSE, color=SIGNAL_LIGHT_BLUE, lw=1.8, zorder=1)
    ax.vlines(SAMPLE_INDICES, 0.0, context["reconstructed_sequence"], color=SIGNAL_BLACK, lw=2.0, zorder=2)
    ax.scatter(SAMPLE_INDICES, context["reconstructed_sequence"], s=65, color=SIGNAL_BLACK, edgecolor="white", linewidth=1.0, zorder=3)
    ax.vlines(snapshot_index, 0.0, sample_value, color=ACTIVE_RED, lw=2.6, zorder=4)
    ax.scatter([snapshot_index], [sample_value], s=80, color=ACTIVE_RED, edgecolor="white", linewidth=1.0, zorder=5)
    finalize_sequence_axis(
        ax,
        f"Reconstructed block, n = {snapshot_index}",
        (-context["signal_limit"], context["signal_limit"]),
        y_ticks=SEQUENCE_Y_TICKS,
    )
    save_figure(fig, output_dir / "12_reconstructed_block.png", REFERENCE_TIME_EXPORT_SIZE)


def export_snapshot_series(snapshot_index: int) -> None:
    context = prepare_context(snapshot_index)
    output_dir = snapshot_dir(snapshot_index)
    output_dir.mkdir(parents=True, exist_ok=True)

    export_magnitude(context, output_dir)
    export_phase(context, output_dir)
    export_weighting_overlay(
        context,
        output_dir,
        context["pure_real_weight"],
        context["pure_real_weight_lines"],
        RE_COLOR,
        f"|X[k]| and cos, n = {snapshot_index}",
        r"$\cos(\Omega_k n)$",
        "03_magnitude_with_cos_weight.png",
    )
    export_weighting_overlay(
        context,
        output_dir,
        context["pure_real_weight"],
        context["real_weight_lines"],
        RE_COLOR,
        f"Real weight, n = {snapshot_index}",
        r"$\cos(\Omega_k n + \varphi(\Omega_k))$",
        "04_real_weighting.png",
    )
    export_contribution(
        context,
        output_dir,
        context["real_product_lines"],
        RE_COLOR,
        f"Real contribution, n = {snapshot_index}",
        "05_real_contribution.png",
    )
    export_contribution(
        context,
        output_dir,
        context["real_product_lines"],
        RE_COLOR,
        f"Real sum, n = {snapshot_index}",
        "06_real_sum.png",
        sum_line=context["real_sum"],
    )
    export_weighting_overlay(
        context,
        output_dir,
        context["pure_imag_weight"],
        context["pure_imag_weight_lines"],
        IM_COLOR,
        f"|X[k]| and sin, n = {snapshot_index}",
        r"$\sin(\Omega_k n)$",
        "07_magnitude_with_sin_weight.png",
    )
    export_weighting_overlay(
        context,
        output_dir,
        context["pure_imag_weight"],
        context["imag_weight_lines"],
        IM_COLOR,
        f"Imag weight, n = {snapshot_index}",
        r"$\sin(\Omega_k n + \varphi(\Omega_k))$",
        "08_imag_weighting.png",
    )
    export_contribution(
        context,
        output_dir,
        context["imag_product_lines"],
        IM_COLOR,
        f"Imag contribution, n = {snapshot_index}",
        "09_imag_contribution.png",
    )
    export_contribution(
        context,
        output_dir,
        context["imag_product_lines"],
        IM_COLOR,
        f"Imag sum, n = {snapshot_index}",
        "10_imag_sum.png",
        sum_line=context["imag_sum"],
    )
    export_complex_sample(context, output_dir)
    export_reconstructed_block(context, output_dir)


def main() -> None:
    clear_output_root()
    for snapshot_index in SNAPSHOT_INDICES:
        export_snapshot_series(snapshot_index)
    print(f"PNG storyboard exported to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
