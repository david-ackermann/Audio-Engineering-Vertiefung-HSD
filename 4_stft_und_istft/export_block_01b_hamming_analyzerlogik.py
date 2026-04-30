from pathlib import Path
import os
import shutil

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from export_block_01a_offbin_analyzerlogik import (
    EXPORT_CASES as REFERENCE_7A_CASES,
    apply_global_limits as apply_7a_global_limits,
    prepare_case as prepare_7a_case,
)


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "01_leakage_und_fenstervergleich"
GROUP_ROOT = OUTPUT_ROOT / "01B_hamming_fenster"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
PHASOR_FIGSIZE = (6.8, 6.8)
SPECTRUM_FIGSIZE = (11.0, 4.8)

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17

REFERENCE_TIME_EXPORT_SIZE = (2106, 926)
REFERENCE_PHASOR_EXPORT_SIZE = (1417, 1313)
REFERENCE_MAG_EXPORT_SIZE = (1924, 988)
REFERENCE_PHASE_EXPORT_SIZE = (1974, 988)

LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
SIGNAL_ORANGE = "#d97a27"
ACTIVE_RED = "#d7263d"
INACTIVE_GREY = "0.72"
ACTIVE_LIGHT_RED = "#ef8895"
WINDOW_GREEN = "#66b77a"
WINDOW_LIGHT_GREEN = "#d7efde"

FS_HZ = 16.0
N = 16
DELTA_F_HZ = FS_HZ / N
NYQUIST_HZ = FS_HZ / 2.0
DISPLAY_FREQ_MIN_HZ = -17.0
DISPLAY_FREQ_MAX_HZ = 17.0
SPECTRUM_TICKS_HZ = (-16.0, -12.0, -8.0, -4.0, 0.0, 4.0, 8.0, 12.0, 16.0)
ONE_SIDED_TICKS_HZ = (0.0, 2.0, 4.0, 6.0, 8.0)
SEQUENCE_Y_LIMITS = (-2.2, 2.2)
SEQUENCE_Y_TICKS = np.arange(-2.0, 2.01, 1.0)
PHASOR_AXIS_LIMIT = 1.1
PHASOR_TICK_STEP = 2.0
PHASOR_DISPLAY_LIMIT = 10.0
DB_LEVEL_MIN = -60.0
DB_LEVEL_MAX = 0.0
DB_LEVEL_TICKS = np.arange(-60.0, 0.1, 10.0)

SAMPLE_INDICES = np.arange(N, dtype=float)
DENSE_INDICES = np.linspace(0.0, N - 1, 2400)
HAMMING_WINDOW_VALUES = np.hamming(N)
HAMMING_WINDOW_DENSE = np.interp(DENSE_INDICES, SAMPLE_INDICES, HAMMING_WINDOW_VALUES)
HAMMING_COHERENT_GAIN = float(np.mean(HAMMING_WINDOW_VALUES))

SIGNAL_AMPLITUDE = 1.0
SIGNAL_PHASE_RAD = np.pi / 4.0
DISPLAY_FREQS_HZ = np.linspace(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ, 6000)

EXPORT_CASES = [
    {
        "label": "01B_hamming_probe_2_hz_n16",
        "n": 16,
        "signal_frequency_hz": 2.5,
        "probe_frequency_hz": 2.0,
    },
    {
        "label": "01B_hamming_probe_2_hz_n32",
        "n": 32,
        "signal_frequency_hz": 2.5,
        "probe_frequency_hz": 2.0,
    },
    {
        "label": "01B_hamming_probe_2_hz_n64",
        "n": 64,
        "signal_frequency_hz": 2.5,
        "probe_frequency_hz": 2.0,
    },
    {
        "label": "01B_hamming_probe_2_hz_n128",
        "n": 128,
        "signal_frequency_hz": 2.5,
        "probe_frequency_hz": 2.0,
    },
]


def freq_slug(value: float) -> str:
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return text.replace(".", "p")


def freq_text(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def build_signal(sample_positions: np.ndarray, signal_frequency_hz: float) -> np.ndarray:
    return SIGNAL_AMPLITUDE * np.cos(
        2.0 * np.pi * signal_frequency_hz * sample_positions / FS_HZ + SIGNAL_PHASE_RAD
    )


def configure_runtime(n_value: int) -> None:
    global N, DELTA_F_HZ
    global SAMPLE_INDICES, DENSE_INDICES
    global HAMMING_WINDOW_VALUES, HAMMING_WINDOW_DENSE, HAMMING_COHERENT_GAIN

    N = n_value
    DELTA_F_HZ = FS_HZ / N
    SAMPLE_INDICES = np.arange(N, dtype=float)
    DENSE_INDICES = np.linspace(0.0, N - 1, 2400)
    HAMMING_WINDOW_VALUES = np.hamming(N)
    HAMMING_WINDOW_DENSE = np.interp(DENSE_INDICES, SAMPLE_INDICES, HAMMING_WINDOW_VALUES)
    HAMMING_COHERENT_GAIN = float(np.mean(HAMMING_WINDOW_VALUES))


def case_dir(case: dict) -> Path:
    return GROUP_ROOT / case["label"]


def handle_remove_readonly(function, path, _excinfo) -> None:
    os.chmod(path, 0o666)
    function(path)


def clear_output_root() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    if GROUP_ROOT.exists():
        shutil.rmtree(GROUP_ROOT, onerror=handle_remove_readonly)
    for child in OUTPUT_ROOT.iterdir():
        if child.is_dir() and child.name.startswith("01B_"):
            shutil.rmtree(child, onerror=handle_remove_readonly)


def create_time_figure():
    return plt.subplots(figsize=TIME_FIGSIZE)


def create_square_figure():
    return plt.subplots(figsize=PHASOR_FIGSIZE)


def create_spectrum_figure():
    return plt.subplots(figsize=SPECTRUM_FIGSIZE)


def normalize_png_canvas(target_path: Path, target_size) -> None:
    image = Image.open(target_path).convert("RGBA")
    current_width, current_height = image.size
    target_width, target_height = target_size

    crop_left = max(0, (current_width - target_width) // 2)
    crop_top = max(0, (current_height - target_height) // 2)
    crop_right = crop_left + min(current_width, target_width)
    crop_bottom = crop_top + min(current_height, target_height)
    cropped = image.crop((crop_left, crop_top, crop_right, crop_bottom))

    normalized = Image.new("RGBA", target_size, (255, 255, 255, 255))
    paste_x = max(0, (target_width - cropped.size[0]) // 2)
    paste_y = max(0, (target_height - cropped.size[1]) // 2)
    normalized.paste(cropped, (paste_x, paste_y))
    normalized.save(target_path)


def save_figure(fig, target_path: Path, target_size=None) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    if target_size is not None:
        normalize_png_canvas(target_path, target_size)


def style_sequence_axis(ax, title: str, y_limits, y_label: str = "Amplitude", y_ticks=None) -> None:
    ax.axhline(0.0, color="0.78", lw=0.9)
    ax.set_xlim(-0.35, N - 0.65)
    ax.set_ylim(*y_limits)
    ax.set_xticks(np.arange(0, N, sample_tick_step()))
    ax.set_yticks(SEQUENCE_Y_TICKS if y_ticks is None else y_ticks)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_spectrum_axis(ax, title: str, y_limits, y_label: str) -> None:
    ax.axhline(0.0, color="0.78", lw=0.9)
    ax.set_xlim(DISPLAY_FREQ_MIN_HZ, DISPLAY_FREQ_MAX_HZ)
    ax.set_ylim(*y_limits)
    ax.set_xticks(SPECTRUM_TICKS_HZ)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_one_sided_spectrum_axis(ax, title: str, y_limits, y_label: str) -> None:
    ax.axhline(0.0, color="0.78", lw=0.9)
    ax.set_xlim(0.0, NYQUIST_HZ)
    ax.set_ylim(*y_limits)
    ax.set_xticks(ONE_SIDED_TICKS_HZ)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_signal_block(ax, signal_dense, signal_values) -> None:
    ax.plot(DENSE_INDICES, signal_dense, color=SIGNAL_LIGHT_BLUE, lw=1.5, zorder=1)
    ax.vlines(SAMPLE_INDICES, 0.0, signal_values, color=SIGNAL_BLACK, lw=2.0, zorder=2)
    ax.scatter(SAMPLE_INDICES, signal_values, s=65, color=SIGNAL_BLACK, edgecolor="white", linewidth=1.0, zorder=3)


def draw_hamming_window_overlay(ax) -> None:
    ax.fill_between(
        DENSE_INDICES,
        0.0,
        HAMMING_WINDOW_DENSE,
        color=WINDOW_LIGHT_GREEN,
        alpha=0.16,
        zorder=0,
    )
    ax.plot(
        DENSE_INDICES,
        HAMMING_WINDOW_DENSE,
        color=WINDOW_GREEN,
        lw=1.7,
        zorder=1,
    )


def draw_basis(ax, dense_values, sample_values, color) -> None:
    ax.plot(DENSE_INDICES, dense_values, color=color, lw=2.1, ls="--", zorder=1)
    ax.vlines(SAMPLE_INDICES, 0.0, sample_values, color=color, lw=1.9, alpha=0.95, zorder=3)
    ax.scatter(SAMPLE_INDICES, sample_values, s=42, color=color, edgecolor="white", linewidth=0.8, zorder=4)


def draw_product(ax, product_values, color) -> None:
    ax.vlines(SAMPLE_INDICES, 0.0, product_values, color=color, lw=2.2, zorder=3)
    ax.scatter(SAMPLE_INDICES, product_values, s=55, color=color, edgecolor="white", linewidth=0.9, zorder=4)


def amplitude_to_db(values: np.ndarray) -> np.ndarray:
    floor_linear = 10.0 ** (DB_LEVEL_MIN / 20.0)
    return 20.0 * np.log10(np.maximum(values, floor_linear))


def sample_tick_step() -> int:
    if N <= 16:
        return 2
    if N <= 32:
        return 4
    if N <= 64:
        return 8
    return 16


def dft_scale() -> float:
    return 1.0


def phasor_ticks(limit: float) -> np.ndarray:
    tick_extent = np.ceil(limit / PHASOR_TICK_STEP) * PHASOR_TICK_STEP
    return np.arange(-tick_extent, tick_extent + 0.001, PHASOR_TICK_STEP)


def sum_ticks(limit: float) -> np.ndarray:
    tick_step = 2.0 if limit > 4.0 else 1.0
    tick_extent = np.ceil(limit / tick_step) * tick_step
    return np.arange(-tick_extent, tick_extent + 0.001, tick_step)


def repeated_spectrum_view(frequencies_hz, values):
    repeated_frequencies = []
    repeated_values = []
    for shift_hz in (-FS_HZ, 0.0, FS_HZ):
        shifted_frequencies = frequencies_hz + shift_hz
        visible_mask = (shifted_frequencies >= DISPLAY_FREQ_MIN_HZ - 1e-9) & (
            shifted_frequencies <= DISPLAY_FREQ_MAX_HZ + 1e-9
        )
        repeated_frequencies.append(shifted_frequencies[visible_mask])
        repeated_values.append(values[visible_mask])
    return np.concatenate(repeated_frequencies), np.concatenate(repeated_values)


def draw_fs_markers(ax, y_limits) -> None:
    for fs_marker_hz, label in ((-FS_HZ, r"$-f_s$"), (FS_HZ, r"$f_s$")):
        if not (DISPLAY_FREQ_MIN_HZ <= fs_marker_hz <= DISPLAY_FREQ_MAX_HZ):
            continue
        ax.axvline(fs_marker_hz, color="0.45", lw=1.4, ls="--", zorder=0)
        ax.text(
            fs_marker_hz,
            y_limits[1] * 0.96 if y_limits[0] >= 0.0 else y_limits[1] * 0.88,
            label,
            ha="center",
            va="top",
            fontsize=LABEL_SIZE + 1,
            color="0.35",
        )


def visible_periodic_copy_frequencies(reference_frequency_hz: float) -> list[float]:
    copy_frequencies_hz = []
    min_period_index = int(np.floor((DISPLAY_FREQ_MIN_HZ - reference_frequency_hz) / FS_HZ))
    max_period_index = int(np.ceil((DISPLAY_FREQ_MAX_HZ - reference_frequency_hz) / FS_HZ))

    for period_index in range(min_period_index, max_period_index + 1):
        if period_index == 0:
            continue
        shifted_frequency_hz = reference_frequency_hz + period_index * FS_HZ
        if DISPLAY_FREQ_MIN_HZ - 1e-9 <= shifted_frequency_hz <= DISPLAY_FREQ_MAX_HZ + 1e-9:
            copy_frequencies_hz.append(float(shifted_frequency_hz))

    return sorted(copy_frequencies_hz)


def one_sided_bin_frequency(probe_frequency_hz: float) -> float:
    if probe_frequency_hz <= NYQUIST_HZ:
        return probe_frequency_hz
    return FS_HZ - probe_frequency_hz


def one_sided_amplitude_curve(two_sided_curve: np.ndarray, frequency_values_hz: np.ndarray) -> np.ndarray:
    amplitudes = 2.0 * two_sided_curve / N
    endpoint_mask = np.isclose(frequency_values_hz, 0.0) | np.isclose(frequency_values_hz, NYQUIST_HZ)
    amplitudes[endpoint_mask] = two_sided_curve[endpoint_mask] / N
    return amplitudes


def periodic_dtft(signal_values: np.ndarray, frequency_values_hz: np.ndarray) -> np.ndarray:
    phase_matrix = np.exp(-1j * 2.0 * np.pi * frequency_values_hz[:, None] * SAMPLE_INDICES[None, :] / FS_HZ)
    return np.sum(signal_values[None, :] * phase_matrix, axis=1)


def prepare_case(case: dict):
    signal_frequency_hz = case["signal_frequency_hz"]
    probe_frequency_hz = case["probe_frequency_hz"]
    raw_signal_values = build_signal(SAMPLE_INDICES, signal_frequency_hz)
    raw_signal_dense = build_signal(DENSE_INDICES, signal_frequency_hz)
    signal_values = raw_signal_values * HAMMING_WINDOW_VALUES
    signal_dense = raw_signal_dense * HAMMING_WINDOW_DENSE

    fft_values = np.fft.fft(signal_values)
    spectrum_coefficients = np.fft.fftshift(fft_values)
    spectrum_frequencies_hz = np.fft.fftshift(np.fft.fftfreq(N, d=1.0 / FS_HZ))
    spectrum_magnitudes = np.abs(spectrum_coefficients)
    amplitude_magnitudes = spectrum_magnitudes / N
    window_normalized_amplitudes = amplitude_magnitudes / HAMMING_COHERENT_GAIN
    one_sided_frequencies_hz = np.fft.rfftfreq(N, d=1.0 / FS_HZ)
    one_sided_amplitudes = np.abs(fft_values[: N // 2 + 1]) / N
    if N > 2:
        one_sided_amplitudes[1:-1] *= 2.0
    spectrum_phases_deg = np.degrees(np.angle(spectrum_coefficients))
    envelope_magnitudes = np.abs(periodic_dtft(signal_values, DISPLAY_FREQS_HZ))
    envelope_amplitudes = envelope_magnitudes / N
    window_normalized_envelope_amplitudes = envelope_amplitudes / HAMMING_COHERENT_GAIN
    one_sided_envelope_frequencies_hz = np.linspace(0.0, NYQUIST_HZ, 2500)
    one_sided_envelope_magnitudes = np.abs(periodic_dtft(signal_values, one_sided_envelope_frequencies_hz))
    one_sided_envelope_amplitudes = one_sided_amplitude_curve(
        one_sided_envelope_magnitudes,
        one_sided_envelope_frequencies_hz,
    )
    max_complex = np.max(spectrum_magnitudes)

    bin_index = int(round(probe_frequency_hz / DELTA_F_HZ))
    basis_real_samples = np.cos(2.0 * np.pi * bin_index * SAMPLE_INDICES / N)
    basis_imag_samples = -np.sin(2.0 * np.pi * bin_index * SAMPLE_INDICES / N)
    basis_real_dense = np.cos(2.0 * np.pi * bin_index * DENSE_INDICES / N)
    basis_imag_dense = -np.sin(2.0 * np.pi * bin_index * DENSE_INDICES / N)

    real_product = signal_values * basis_real_samples
    imag_product = signal_values * basis_imag_samples
    scale = dft_scale()
    real_sum = scale * np.sum(real_product)
    imag_sum = scale * np.sum(imag_product)
    coefficient = real_sum + 1j * imag_sum

    max_complex = max(max_complex, abs(real_sum), abs(imag_sum), abs(coefficient))
    sum_limit = 1.15 * max(0.4, abs(real_sum), abs(imag_sum))
    spectrum_limit = 1.15 * max(0.35, np.max(spectrum_magnitudes), np.max(envelope_magnitudes))
    amplitude_limit = 1.15 * max(0.08, np.max(amplitude_magnitudes), np.max(envelope_amplitudes))
    one_sided_limit = 1.15 * max(0.08, np.max(one_sided_amplitudes), np.max(one_sided_envelope_amplitudes))
    phase_threshold = 0.02 * np.max(spectrum_magnitudes)

    return {
        "signal_frequency_hz": signal_frequency_hz,
        "probe_frequency_hz": probe_frequency_hz,
        "raw_signal_values": raw_signal_values,
        "raw_signal_dense": raw_signal_dense,
        "signal_values": signal_values,
        "signal_dense": signal_dense,
        "complex_limit": 1.15 * max(0.2, max_complex),
        "sum_limit": sum_limit,
        "spectrum_frequencies_hz": spectrum_frequencies_hz,
        "spectrum_coefficients": spectrum_coefficients,
        "spectrum_magnitudes": spectrum_magnitudes,
        "amplitude_magnitudes": amplitude_magnitudes,
        "window_normalized_amplitudes": window_normalized_amplitudes,
        "one_sided_frequencies_hz": one_sided_frequencies_hz,
        "one_sided_amplitudes": one_sided_amplitudes,
        "spectrum_phases_deg": spectrum_phases_deg,
        "envelope_frequencies_hz": DISPLAY_FREQS_HZ,
        "envelope_magnitudes": envelope_magnitudes,
        "envelope_amplitudes": envelope_amplitudes,
        "window_normalized_envelope_amplitudes": window_normalized_envelope_amplitudes,
        "one_sided_envelope_frequencies_hz": one_sided_envelope_frequencies_hz,
        "one_sided_envelope_amplitudes": one_sided_envelope_amplitudes,
        "spectrum_limit": spectrum_limit,
        "amplitude_limit": amplitude_limit,
        "one_sided_limit": one_sided_limit,
        "phase_threshold": phase_threshold,
        "n": N,
        "probe_data": {
            "bin_index": bin_index,
            "basis_real_samples": basis_real_samples,
            "basis_imag_samples": basis_imag_samples,
            "basis_real_dense": basis_real_dense,
            "basis_imag_dense": basis_imag_dense,
            "real_product": real_product,
            "imag_product": imag_product,
            "real_sum": real_sum,
            "imag_sum": imag_sum,
            "coefficient": coefficient,
            "magnitude": abs(coefficient),
            "amplitude_magnitude": abs(coefficient) / N,
            "window_normalized_amplitude": abs(coefficient) / (N * HAMMING_COHERENT_GAIN),
            "one_sided_frequency_hz": one_sided_bin_frequency(probe_frequency_hz),
            "one_sided_amplitude": (
                abs(coefficient) / N
                if probe_frequency_hz in (0.0, NYQUIST_HZ)
                else 2.0 * abs(coefficient) / N
            ),
            "phase_deg": np.degrees(np.angle(coefficient)),
            "copy_frequencies_hz": visible_periodic_copy_frequencies(probe_frequency_hz),
        },
    }


def export_signal_plot(context, output_dir: Path) -> None:
    fig, ax = create_time_figure()
    draw_signal_block(ax, context["raw_signal_dense"], context["raw_signal_values"])
    style_sequence_axis(
        ax,
        rf"$x[n]$, {freq_text(context['signal_frequency_hz'])} Hz",
        SEQUENCE_Y_LIMITS,
    )
    save_figure(fig, output_dir / "01_signalblock_x_n.png", target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_windowed_signal_plot(context, output_dir: Path) -> None:
    fig, ax = create_time_figure()
    draw_hamming_window_overlay(ax)
    draw_signal_block(ax, context["signal_dense"], context["signal_values"])
    style_sequence_axis(
        ax,
        rf"$x[n]\cdot w[n]$, Hamming window, {freq_text(context['signal_frequency_hz'])} Hz",
        SEQUENCE_Y_LIMITS,
    )
    save_figure(fig, output_dir / "02_signal_mit_hamming_fenster.png", target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_basis_plot(context, output_dir: Path, probe_data, part: str, *, show_window: bool, filename: str) -> None:
    if part == "real":
        basis_dense = probe_data["basis_real_dense"]
        basis_samples = probe_data["basis_real_samples"]
        color = SIGNAL_BLUE
        title = rf"$x[n]\cdot w[n]$ and $\cos$, {freq_text(context['probe_frequency_hz'])} Hz"
    else:
        basis_dense = probe_data["basis_imag_dense"]
        basis_samples = probe_data["basis_imag_samples"]
        color = SIGNAL_ORANGE
        title = rf"$x[n]\cdot w[n]$ and $-\sin$, {freq_text(context['probe_frequency_hz'])} Hz"

    fig, ax = create_time_figure()
    if show_window:
        draw_hamming_window_overlay(ax)
    draw_signal_block(ax, context["signal_dense"], context["signal_values"])
    draw_basis(ax, basis_dense, basis_samples, color)
    style_sequence_axis(ax, title, SEQUENCE_Y_LIMITS)
    save_figure(fig, output_dir / filename, target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_product_plot(context, output_dir: Path, probe_data, part: str) -> None:
    if part == "real":
        product_values = probe_data["real_product"]
        color = SIGNAL_BLUE
        title = rf"$x[n]\cdot w[n]\cos$, {freq_text(context['probe_frequency_hz'])} Hz"
        filename = "05_produkt_cos.png"
        ylabel = "Product"
    else:
        product_values = probe_data["imag_product"]
        color = SIGNAL_ORANGE
        title = rf"$x[n]\cdot w[n](-\sin)$, {freq_text(context['probe_frequency_hz'])} Hz"
        filename = "06_produkt_minus_sin.png"
        ylabel = "Product"

    fig, ax = create_time_figure()
    draw_product(ax, product_values, color)
    style_sequence_axis(
        ax,
        title,
        (-context["sum_limit"], context["sum_limit"]),
        y_label=ylabel,
        y_ticks=sum_ticks(context["sum_limit"]),
    )
    save_figure(fig, output_dir / filename, target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_sum_plot(context, output_dir: Path, probe_data, part: str) -> None:
    if part == "real":
        product_values = probe_data["real_product"]
        sum_value = probe_data["real_sum"]
        color = SIGNAL_BLUE
        title = rf"$\Re\{{X[k]\}}$, {freq_text(context['probe_frequency_hz'])} Hz"
        filename = "07_summe_cos.png"
    else:
        product_values = probe_data["imag_product"]
        sum_value = probe_data["imag_sum"]
        color = SIGNAL_ORANGE
        title = rf"$\Im\{{X[k]\}}$, {freq_text(context['probe_frequency_hz'])} Hz"
        filename = "08_summe_minus_sin.png"

    fig, ax = create_time_figure()
    draw_product(ax, product_values, color)
    ax.axhline(sum_value, color=color, lw=2.0, ls="--")
    style_sequence_axis(
        ax,
        title,
        (-context["sum_limit"], context["sum_limit"]),
        y_label="Weighted term",
        y_ticks=sum_ticks(context["sum_limit"]),
    )
    save_figure(fig, output_dir / filename, target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_phasor_plot(context, output_dir: Path, probe_data) -> None:
    coefficient = probe_data["coefficient"]
    phasor_title_size = TITLE_SIZE + 2
    phasor_label_size = LABEL_SIZE + 2
    phasor_tick_size = TICK_SIZE + 2

    fig, ax = create_square_figure()
    ax.axhline(0.0, color="0.78", lw=0.9)
    ax.axvline(0.0, color="0.78", lw=0.9)
    ax.plot([0.0, coefficient.real], [0.0, coefficient.imag], color=ACTIVE_RED, lw=3.0)
    ax.plot([coefficient.real], [coefficient.imag], "o", color=ACTIVE_RED, ms=9)
    ax.plot([0.0, coefficient.real], [0.0, 0.0], color=SIGNAL_BLUE, lw=1.5, alpha=0.90)
    ax.plot([coefficient.real, coefficient.real], [0.0, coefficient.imag], color=SIGNAL_ORANGE, lw=1.5, alpha=0.90)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-PHASOR_DISPLAY_LIMIT, PHASOR_DISPLAY_LIMIT)
    ax.set_ylim(-PHASOR_DISPLAY_LIMIT, PHASOR_DISPLAY_LIMIT)
    tick_values = phasor_ticks(PHASOR_DISPLAY_LIMIT)
    ax.set_xticks(tick_values)
    ax.set_yticks(tick_values)
    ax.grid(alpha=0.22)
    ax.set_xlabel(r"Re$\{X[k]\}$", fontsize=phasor_label_size, color=SIGNAL_BLUE)
    ax.set_ylabel(r"Im$\{X[k]\}$", fontsize=phasor_label_size, color=SIGNAL_ORANGE)
    ax.set_title(
        rf"$X[k]$, {freq_text(context['probe_frequency_hz'])} Hz",
        pad=10,
        fontsize=phasor_title_size,
    )
    ax.tick_params(axis="x", labelsize=phasor_tick_size, colors=SIGNAL_BLUE)
    ax.tick_params(axis="y", labelsize=phasor_tick_size, colors=SIGNAL_ORANGE)
    save_figure(fig, output_dir / "09_komplexer_bin_wert.png", target_size=REFERENCE_PHASOR_EXPORT_SIZE)


def export_spectrum_plot(context, output_dir: Path, probe_data, *, show_envelope: bool, filename: str) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    magnitudes = context["spectrum_magnitudes"]
    if show_envelope:
        ax.plot(
            context["envelope_frequencies_hz"],
            context["envelope_magnitudes"],
            color=WINDOW_GREEN,
            lw=2.4,
            zorder=2,
        )
    repeated_frequencies, repeated_magnitudes = repeated_spectrum_view(frequencies, magnitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_magnitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(repeated_frequencies, repeated_magnitudes, "o", color=INACTIVE_GREY, ms=7)
    if probe_data["copy_frequencies_hz"]:
        copy_magnitudes = np.full(len(probe_data["copy_frequencies_hz"]), probe_data["magnitude"])
        ax.vlines(probe_data["copy_frequencies_hz"], 0.0, copy_magnitudes, color=ACTIVE_LIGHT_RED, lw=2.6)
        ax.plot(probe_data["copy_frequencies_hz"], copy_magnitudes, "o", color=ACTIVE_LIGHT_RED, ms=8)
    ax.vlines(context["probe_frequency_hz"], 0.0, probe_data["magnitude"], color=ACTIVE_RED, lw=2.8)
    ax.plot([context["probe_frequency_hz"]], [probe_data["magnitude"]], "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        rf"$|X[k]|$, {freq_text(context['probe_frequency_hz'])} Hz",
        (0.0, context["spectrum_limit"]),
        r"$|X[k]|$",
    )
    draw_fs_markers(ax, (0.0, context["spectrum_limit"]))
    save_figure(fig, output_dir / filename, target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_phase_plot(context, output_dir: Path, probe_data) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    magnitudes = context["spectrum_magnitudes"]
    phases_deg = context["spectrum_phases_deg"]
    valid_mask = magnitudes >= context["phase_threshold"]

    repeated_frequencies, repeated_phases = repeated_spectrum_view(frequencies[valid_mask], phases_deg[valid_mask])
    ax.vlines(repeated_frequencies, 0.0, repeated_phases, color=INACTIVE_GREY, lw=2.4)
    ax.plot(repeated_frequencies, repeated_phases, "o", color=INACTIVE_GREY, ms=7)

    if probe_data["magnitude"] >= context["phase_threshold"]:
        if probe_data["copy_frequencies_hz"]:
            copy_phases = np.full(len(probe_data["copy_frequencies_hz"]), probe_data["phase_deg"])
            ax.vlines(probe_data["copy_frequencies_hz"], 0.0, copy_phases, color=ACTIVE_LIGHT_RED, lw=2.6)
            ax.plot(probe_data["copy_frequencies_hz"], copy_phases, "o", color=ACTIVE_LIGHT_RED, ms=8)
        ax.vlines(context["probe_frequency_hz"], 0.0, probe_data["phase_deg"], color=ACTIVE_RED, lw=2.8)
        ax.plot([context["probe_frequency_hz"]], [probe_data["phase_deg"]], "o", color=ACTIVE_RED, ms=8)
    else:
        ax.plot([context["probe_frequency_hz"]], [0.0], "o", color=ACTIVE_RED, ms=8)

    style_spectrum_axis(
        ax,
        f"Phase, {freq_text(context['probe_frequency_hz'])} Hz",
        (-190.0, 190.0),
        "Phase [deg]",
    )
    draw_fs_markers(ax, (-190.0, 190.0))

    save_figure(fig, output_dir / "12_dft_phasenspektrum.png", target_size=REFERENCE_PHASE_EXPORT_SIZE)


def export_amplitude_spectrum_plot(context, output_dir: Path, probe_data, *, show_envelope: bool, filename: str) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    amplitudes = context["amplitude_magnitudes"]
    if show_envelope:
        ax.plot(
            context["envelope_frequencies_hz"],
            context["envelope_amplitudes"],
            color=WINDOW_GREEN,
            lw=2.4,
            ls="--",
            zorder=2,
        )
    repeated_frequencies, repeated_amplitudes = repeated_spectrum_view(frequencies, amplitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_amplitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(repeated_frequencies, repeated_amplitudes, "o", color=INACTIVE_GREY, ms=7)
    if probe_data["copy_frequencies_hz"]:
        copy_amplitudes = np.full(len(probe_data["copy_frequencies_hz"]), probe_data["amplitude_magnitude"])
        ax.vlines(probe_data["copy_frequencies_hz"], 0.0, copy_amplitudes, color=ACTIVE_LIGHT_RED, lw=2.6)
        ax.plot(probe_data["copy_frequencies_hz"], copy_amplitudes, "o", color=ACTIVE_LIGHT_RED, ms=8)
    ax.vlines(context["probe_frequency_hz"], 0.0, probe_data["amplitude_magnitude"], color=ACTIVE_RED, lw=2.8)
    ax.plot([context["probe_frequency_hz"]], [probe_data["amplitude_magnitude"]], "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        rf"$A_k^{{(2)}}$, {freq_text(context['probe_frequency_hz'])} Hz",
        (0.0, context["amplitude_limit"]),
        r"$A_k^{(2)}$",
    )
    draw_fs_markers(ax, (0.0, context["amplitude_limit"]))
    save_figure(fig, output_dir / filename, target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_negative_frequency_amplitude_plot(context, output_dir: Path, *, show_envelope: bool, filename: str) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    amplitudes = context["amplitude_magnitudes"]

    if show_envelope:
        ax.plot(
            context["envelope_frequencies_hz"],
            context["envelope_amplitudes"],
            color=WINDOW_GREEN,
            lw=2.4,
            ls="--",
            zorder=2,
        )

    repeated_frequencies, repeated_amplitudes = repeated_spectrum_view(frequencies, amplitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_amplitudes, color=ACTIVE_RED, lw=2.6)
    ax.plot(repeated_frequencies, repeated_amplitudes, "o", color=ACTIVE_RED, ms=8)

    style_spectrum_axis(
        ax,
        rf"$A_k^{{(2)}}$, {freq_text(context['probe_frequency_hz'])} Hz",
        (0.0, context["amplitude_limit"]),
        r"$A_k^{(2)}$",
    )
    draw_fs_markers(ax, (0.0, context["amplitude_limit"]))
    save_figure(fig, output_dir / filename, target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_window_normalized_amplitude_spectrum_plot(context, output_dir: Path, probe_data) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    amplitudes = context["window_normalized_amplitudes"]
    ax.plot(
        context["envelope_frequencies_hz"],
        context["window_normalized_envelope_amplitudes"],
        color=WINDOW_GREEN,
        lw=2.4,
        ls="--",
        zorder=2,
    )
    repeated_frequencies, repeated_amplitudes = repeated_spectrum_view(frequencies, amplitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_amplitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(repeated_frequencies, repeated_amplitudes, "o", color=INACTIVE_GREY, ms=7)
    if probe_data["copy_frequencies_hz"]:
        copy_amplitudes = np.full(len(probe_data["copy_frequencies_hz"]), probe_data["window_normalized_amplitude"])
        ax.vlines(probe_data["copy_frequencies_hz"], 0.0, copy_amplitudes, color=ACTIVE_LIGHT_RED, lw=2.6)
        ax.plot(probe_data["copy_frequencies_hz"], copy_amplitudes, "o", color=ACTIVE_LIGHT_RED, ms=8)
    ax.vlines(context["probe_frequency_hz"], 0.0, probe_data["window_normalized_amplitude"], color=ACTIVE_RED, lw=2.8)
    ax.plot([context["probe_frequency_hz"]], [probe_data["window_normalized_amplitude"]], "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        rf"$A_k^{{(2)}}/G_c$, {freq_text(context['probe_frequency_hz'])} Hz",
        (0.0, context["amplitude_limit"]),
        r"$A_k^{(2)}/G_c$",
    )
    draw_fs_markers(ax, (0.0, context["amplitude_limit"]))
    save_figure(fig, output_dir / "16_amplitudenspektrum_fensternormiert.png", target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_window_normalized_amplitude_highlighted_plot(context, output_dir: Path) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    amplitudes = context["window_normalized_amplitudes"]
    repeated_frequencies, repeated_amplitudes = repeated_spectrum_view(frequencies, amplitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_amplitudes, color=ACTIVE_RED, lw=2.6)
    ax.plot(repeated_frequencies, repeated_amplitudes, "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        rf"$A_k^{{(2)}}/G_c$, {freq_text(context['probe_frequency_hz'])} Hz",
        (0.0, context["amplitude_limit"]),
        r"$A_k^{(2)}/G_c$",
    )
    draw_fs_markers(ax, (0.0, context["amplitude_limit"]))
    save_figure(
        fig,
        output_dir / "17_amplitudenspektrum_fensternormiert_ohne_huellkurve.png",
        target_size=REFERENCE_MAG_EXPORT_SIZE,
    )


def export_window_normalized_amplitude_db_plot(context, output_dir: Path) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    levels_db = amplitude_to_db(context["window_normalized_amplitudes"])
    repeated_frequencies, repeated_levels_db = repeated_spectrum_view(frequencies, levels_db)
    ax.vlines(repeated_frequencies, DB_LEVEL_MIN, repeated_levels_db, color=ACTIVE_RED, lw=2.6)
    ax.plot(repeated_frequencies, repeated_levels_db, "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        f"Amplitude level [dB], {freq_text(context['probe_frequency_hz'])} Hz",
        (DB_LEVEL_MIN, DB_LEVEL_MAX),
        "Level [dB]",
    )
    ax.set_yticks(DB_LEVEL_TICKS)
    draw_fs_markers(ax, (DB_LEVEL_MIN, DB_LEVEL_MAX))
    save_figure(fig, output_dir / "18_amplitudenpegel_db.png", target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_one_sided_amplitude_spectrum_plot(context, output_dir: Path, probe_data) -> None:
    fig, ax = create_spectrum_figure()
    ax.plot(
        context["one_sided_envelope_frequencies_hz"],
        context["one_sided_envelope_amplitudes"],
        color=WINDOW_GREEN,
        lw=2.4,
        ls="--",
        zorder=2,
    )
    frequencies = context["one_sided_frequencies_hz"]
    amplitudes = context["one_sided_amplitudes"]
    ax.vlines(frequencies, 0.0, amplitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(frequencies, amplitudes, "o", color=INACTIVE_GREY, ms=7)
    ax.vlines(
        context["probe_frequency_hz"] if context["probe_frequency_hz"] <= NYQUIST_HZ else probe_data["one_sided_frequency_hz"],
        0.0,
        probe_data["one_sided_amplitude"],
        color=ACTIVE_RED,
        lw=2.8,
    )
    ax.plot(
        [probe_data["one_sided_frequency_hz"]],
        [probe_data["one_sided_amplitude"]],
        "o",
        color=ACTIVE_RED,
        ms=8,
    )
    style_one_sided_spectrum_axis(
        ax,
        rf"$A_k^{{(1)}}$, {freq_text(probe_data['one_sided_frequency_hz'])} Hz",
        (0.0, context["one_sided_limit"]),
        r"$A_k^{(1)}$",
    )
    save_figure(fig, output_dir / "19_amplitudenspektrum_einseitig.png", target_size=REFERENCE_MAG_EXPORT_SIZE)


def reference_limits_from_7a() -> dict[str, float]:
    reference_contexts = {case["label"]: prepare_7a_case(case) for case in REFERENCE_7A_CASES}
    apply_7a_global_limits(reference_contexts)
    exemplar = next(iter(reference_contexts.values()))
    return {
        "sum_limit": exemplar["sum_limit"],
        "complex_limit": exemplar["complex_limit"],
        "spectrum_limit": exemplar["spectrum_limit"],
        "amplitude_limit": exemplar["amplitude_limit"],
        "one_sided_limit": exemplar["one_sided_limit"],
    }


REFERENCE_7A_LIMITS = reference_limits_from_7a()


def apply_global_limits(contexts: dict[str, dict]) -> None:
    for context in contexts.values():
        context["sum_limit"] = max(context["sum_limit"], REFERENCE_7A_LIMITS["sum_limit"])
        context["complex_limit"] = max(context["complex_limit"], REFERENCE_7A_LIMITS["complex_limit"])
        context["spectrum_limit"] = max(context["spectrum_limit"], REFERENCE_7A_LIMITS["spectrum_limit"])
        context["amplitude_limit"] = max(context["amplitude_limit"], REFERENCE_7A_LIMITS["amplitude_limit"])
        context["one_sided_limit"] = max(context["one_sided_limit"], REFERENCE_7A_LIMITS["one_sided_limit"])


def export_case(case: dict, context: dict) -> None:
    probe_data = context["probe_data"]
    output_dir = case_dir(case)
    output_dir.mkdir(parents=True, exist_ok=True)
    for png_file in output_dir.glob("*.png"):
        png_file.unlink()

    export_signal_plot(context, output_dir)
    export_windowed_signal_plot(context, output_dir)
    export_basis_plot(
        context,
        output_dir,
        probe_data,
        part="real",
        show_window=True,
        filename="03_signal_mit_cos_basis.png",
    )
    export_basis_plot(
        context,
        output_dir,
        probe_data,
        part="imag",
        show_window=True,
        filename="04_signal_mit_minus_sin_basis.png",
    )
    export_product_plot(context, output_dir, probe_data, part="real")
    export_product_plot(context, output_dir, probe_data, part="imag")
    export_sum_plot(context, output_dir, probe_data, part="real")
    export_sum_plot(context, output_dir, probe_data, part="imag")
    export_phasor_plot(context, output_dir, probe_data)
    export_spectrum_plot(
        context,
        output_dir,
        probe_data,
        show_envelope=False,
        filename="10_dft_betragsspektrum_ohne_huellkurve.png",
    )
    export_spectrum_plot(
        context,
        output_dir,
        probe_data,
        show_envelope=True,
        filename="11_dft_betragsspektrum.png",
    )
    export_phase_plot(context, output_dir, probe_data)
    export_amplitude_spectrum_plot(
        context,
        output_dir,
        probe_data,
        show_envelope=False,
        filename="13_amplitudenspektrum_zweiseitig_ohne_huellkurve.png",
    )
    export_amplitude_spectrum_plot(
        context,
        output_dir,
        probe_data,
        show_envelope=True,
        filename="14_amplitudenspektrum_zweiseitig.png",
    )
    export_negative_frequency_amplitude_plot(
        context,
        output_dir,
        show_envelope=True,
        filename="15_amplitudenspektrum_negative_frequenzen.png",
    )
    export_window_normalized_amplitude_spectrum_plot(context, output_dir, probe_data)
    export_window_normalized_amplitude_highlighted_plot(context, output_dir)
    export_window_normalized_amplitude_db_plot(context, output_dir)
    export_one_sided_amplitude_spectrum_plot(context, output_dir, probe_data)


def main() -> None:
    clear_output_root()
    for case in EXPORT_CASES:
        configure_runtime(case["n"])
        context = prepare_case(case)
        apply_global_limits({case["label"]: context})
        export_case(case, context)
    print(f"PNG storyboard exported to: {GROUP_ROOT}")


if __name__ == "__main__":
    main()
