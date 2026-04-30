from pathlib import Path
import os
import shutil

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "05_dft_analyzerlogik"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
PHASOR_FIGSIZE = (6.8, 6.8)
SPECTRUM_FIGSIZE = (11.0, 4.8)

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17

LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

REFERENCE_TIME_EXPORT_SIZE = (2106, 926)
REFERENCE_PHASOR_EXPORT_SIZE = (1417, 1313)
REFERENCE_MAG_EXPORT_SIZE = (1924, 988)
REFERENCE_PHASE_EXPORT_SIZE = (1974, 988)

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
SIGNAL_ORANGE = "#d97a27"
ACTIVE_RED = "#d7263d"
ACTIVE_LIGHT_RED = "#ef8895"
INACTIVE_GREY = "0.72"

FS_HZ = 16.0
N = 16
DELTA_F_HZ = FS_HZ / N
NYQUIST_HZ = FS_HZ / 2.0
DISPLAY_FREQ_MIN_HZ = -17.0
DISPLAY_FREQ_MAX_HZ = 17.0
PROBE_FREQUENCIES_HZ = (0.0, 2.0, 5.0, 11.0)
SPECTRUM_TICKS_HZ = (-16.0, -12.0, -8.0, -4.0, 0.0, 4.0, 8.0, 12.0, 16.0)
ONE_SIDED_TICKS_HZ = (0.0, 2.0, 4.0, 6.0, 8.0)
SEQUENCE_Y_LIMITS = (-2.2, 2.2)
SEQUENCE_Y_TICKS = np.arange(-2.0, 2.01, 1.0)
PHASOR_TICK_STEP = 2.0

SAMPLE_INDICES = np.arange(N, dtype=float)
DENSE_INDICES = np.linspace(0.0, N - 1, 2400)

# Same mixed signal as in lecture 1, block 2.
COMPONENTS = (
    (2.0, 1.00, np.pi / 4.0),
    (5.0, 0.85, -np.pi / 2.0),
)


def freq_slug(value: float) -> str:
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return text.replace(".", "p")


def freq_text(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def build_signal(sample_positions: np.ndarray) -> np.ndarray:
    signal_values = np.zeros_like(sample_positions, dtype=float)
    for frequency_hz, amplitude, phase_rad in COMPONENTS:
        signal_values += amplitude * np.cos(2.0 * np.pi * frequency_hz * sample_positions / FS_HZ + phase_rad)
    return signal_values


SIGNAL_VALUES = build_signal(SAMPLE_INDICES)
SIGNAL_DENSE = build_signal(DENSE_INDICES)


def probe_dir(probe_frequency_hz: float) -> Path:
    return OUTPUT_ROOT / f"05A_probe_{freq_slug(probe_frequency_hz)}_hz"


def handle_remove_readonly(function, path, _excinfo) -> None:
    os.chmod(path, 0o666)
    function(path)


def clear_output_root() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for child in OUTPUT_ROOT.glob("05A_probe_*"):
        if child.is_dir():
            shutil.rmtree(child, onerror=handle_remove_readonly)
        elif child.exists():
            child.unlink()


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
    ax.set_xticks(np.arange(0, N, 2))
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

    if not repeated_frequencies:
        return np.array([]), np.array([])

    return np.concatenate(repeated_frequencies), np.concatenate(repeated_values)


def draw_fs_markers(ax, y_limits) -> None:
    for fs_marker_hz, label in ((-FS_HZ, r"$-f_s$"), (FS_HZ, r"$f_s$")):
        if not (DISPLAY_FREQ_MIN_HZ <= fs_marker_hz <= DISPLAY_FREQ_MAX_HZ):
            continue
        ax.axvline(fs_marker_hz, color="0.45", lw=1.4, ls="--", zorder=0)
        ax.text(
            fs_marker_hz,
            y_limits[1] * 0.96,
            label,
            ha="center",
            va="top",
            fontsize=TICK_SIZE,
            color="0.35",
        )


def draw_signal_block(ax) -> None:
    ax.plot(DENSE_INDICES, SIGNAL_DENSE, color=SIGNAL_LIGHT_BLUE, lw=1.5, zorder=1)
    ax.vlines(SAMPLE_INDICES, 0.0, SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.0, zorder=2)
    ax.scatter(SAMPLE_INDICES, SIGNAL_VALUES, s=65, color=SIGNAL_BLACK, edgecolor="white", linewidth=1.0, zorder=3)


def draw_basis(ax, dense_values, sample_values, color) -> None:
    ax.plot(DENSE_INDICES, dense_values, color=color, lw=2.1, ls="--", zorder=1)
    ax.vlines(SAMPLE_INDICES, 0.0, sample_values, color=color, lw=1.9, alpha=0.95, zorder=3)
    ax.scatter(SAMPLE_INDICES, sample_values, s=42, color=color, edgecolor="white", linewidth=0.8, zorder=4)


def draw_product(ax, product_values, color) -> None:
    ax.vlines(SAMPLE_INDICES, 0.0, product_values, color=color, lw=2.2, zorder=3)
    ax.scatter(SAMPLE_INDICES, product_values, s=55, color=color, edgecolor="white", linewidth=0.9, zorder=4)


def dft_scale() -> float:
    return 1.0


def phasor_ticks(limit: float) -> np.ndarray:
    tick_extent = np.ceil(limit / PHASOR_TICK_STEP) * PHASOR_TICK_STEP
    return np.arange(-tick_extent, tick_extent + 0.001, PHASOR_TICK_STEP)


def sum_ticks(limit: float) -> np.ndarray:
    tick_step = 2.0 if limit > 4.0 else 1.0
    tick_extent = np.ceil(limit / tick_step) * tick_step
    return np.arange(-tick_extent, tick_extent + 0.001, tick_step)


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


def prepare_context():
    fft_values = np.fft.fft(SIGNAL_VALUES)
    spectrum_coefficients = np.fft.fftshift(fft_values)
    spectrum_frequencies_hz = np.fft.fftshift(np.fft.fftfreq(N, d=1.0 / FS_HZ))
    spectrum_magnitudes = np.abs(spectrum_coefficients)
    amplitude_magnitudes = spectrum_magnitudes / N
    one_sided_frequencies_hz = np.fft.rfftfreq(N, d=1.0 / FS_HZ)
    one_sided_amplitudes = np.abs(fft_values[: N // 2 + 1]) / N
    if N > 2:
        one_sided_amplitudes[1:-1] *= 2.0
    spectrum_phases_deg = np.degrees(np.angle(spectrum_coefficients))

    probe_results = {}
    max_product = 0.0
    max_sum = 0.0
    max_complex = np.max(spectrum_magnitudes)

    for probe_frequency_hz in PROBE_FREQUENCIES_HZ:
        bin_index = int(round(probe_frequency_hz / DELTA_F_HZ))
        basis_real_samples = np.cos(2.0 * np.pi * bin_index * SAMPLE_INDICES / N)
        basis_imag_samples = -np.sin(2.0 * np.pi * bin_index * SAMPLE_INDICES / N)
        basis_real_dense = np.cos(2.0 * np.pi * bin_index * DENSE_INDICES / N)
        basis_imag_dense = -np.sin(2.0 * np.pi * bin_index * DENSE_INDICES / N)

        real_product = SIGNAL_VALUES * basis_real_samples
        imag_product = SIGNAL_VALUES * basis_imag_samples
        scale = dft_scale()
        real_sum = scale * np.sum(real_product)
        imag_sum = scale * np.sum(imag_product)
        coefficient = real_sum + 1j * imag_sum

        probe_results[probe_frequency_hz] = {
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
            "one_sided_frequency_hz": one_sided_bin_frequency(probe_frequency_hz),
            "one_sided_amplitude": (
                abs(coefficient) / N
                if probe_frequency_hz in (0.0, NYQUIST_HZ)
                else 2.0 * abs(coefficient) / N
            ),
            "phase_deg": np.degrees(np.angle(coefficient)),
            "copy_frequencies_hz": visible_periodic_copy_frequencies(probe_frequency_hz),
        }

        max_product = max(max_product, np.max(np.abs(real_product)), np.max(np.abs(imag_product)))
        max_sum = max(max_sum, abs(real_sum), abs(imag_sum))
        max_complex = max(max_complex, abs(real_sum), abs(imag_sum), abs(coefficient))

    signal_limit = 1.15 * max(1.0, np.max(np.abs(SIGNAL_DENSE)))
    product_limit = 1.15 * max(0.4, max_product)
    sum_limit = 1.15 * max(product_limit, max_sum)
    spectrum_limit = 1.15 * max(1.0, np.max(spectrum_magnitudes))
    amplitude_limit = 1.15 * max(0.08, np.max(amplitude_magnitudes))
    one_sided_limit = 1.15 * max(0.08, np.max(one_sided_amplitudes))
    phase_threshold = 0.02 * np.max(spectrum_magnitudes)

    return {
        "signal_limit": signal_limit,
        "product_limit": product_limit,
        "sum_limit": sum_limit,
        "complex_limit": 1.15 * max(0.2, max_complex),
        "spectrum_frequencies_hz": spectrum_frequencies_hz,
        "spectrum_coefficients": spectrum_coefficients,
        "spectrum_magnitudes": spectrum_magnitudes,
        "amplitude_magnitudes": amplitude_magnitudes,
        "one_sided_frequencies_hz": one_sided_frequencies_hz,
        "one_sided_amplitudes": one_sided_amplitudes,
        "spectrum_phases_deg": spectrum_phases_deg,
        "spectrum_limit": spectrum_limit,
        "amplitude_limit": amplitude_limit,
        "one_sided_limit": one_sided_limit,
        "phase_threshold": phase_threshold,
        "probe_results": probe_results,
    }


def export_signal_plot(context, output_dir: Path, probe_frequency_hz: float) -> None:
    fig, ax = create_time_figure()
    draw_signal_block(ax)
    style_sequence_axis(
        ax,
        rf"$x[n]$, {freq_text(probe_frequency_hz)} Hz",
        SEQUENCE_Y_LIMITS,
    )
    save_figure(fig, output_dir / "01_signalblock_x_n.png", target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_basis_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data, part: str) -> None:
    if part == "real":
        basis_dense = probe_data["basis_real_dense"]
        basis_samples = probe_data["basis_real_samples"]
        color = SIGNAL_BLUE
        title = rf"$x[n]$ and $\cos$, {freq_text(probe_frequency_hz)} Hz"
        filename = "02_signal_mit_cos_basis.png"
        box_text = rf"$k = {probe_data['bin_index']}$" + "\n" + rf"$f_k = {freq_text(probe_frequency_hz)}\,\mathrm{{Hz}}$"
    else:
        basis_dense = probe_data["basis_imag_dense"]
        basis_samples = probe_data["basis_imag_samples"]
        color = SIGNAL_ORANGE
        title = rf"$x[n]$ and $-\sin$, {freq_text(probe_frequency_hz)} Hz"
        filename = "03_signal_mit_minus_sin_basis.png"
        box_text = rf"$k = {probe_data['bin_index']}$" + "\n" + rf"$\Delta f = {freq_text(DELTA_F_HZ)}\,\mathrm{{Hz}}$"

    fig, ax = create_time_figure()
    draw_signal_block(ax)
    draw_basis(ax, basis_dense, basis_samples, color)
    style_sequence_axis(ax, title, SEQUENCE_Y_LIMITS)
    save_figure(fig, output_dir / filename, target_size=REFERENCE_TIME_EXPORT_SIZE)


def export_product_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data, part: str) -> None:
    if part == "real":
        product_values = probe_data["real_product"]
        color = SIGNAL_BLUE
        title = rf"$x[n]\cos$, {freq_text(probe_frequency_hz)} Hz"
        filename = "04_produkt_cos.png"
        ylabel = "Product"
    else:
        product_values = probe_data["imag_product"]
        color = SIGNAL_ORANGE
        title = rf"$x[n](-\sin)$, {freq_text(probe_frequency_hz)} Hz"
        filename = "05_produkt_minus_sin.png"
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


def export_sum_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data, part: str) -> None:
    if part == "real":
        product_values = probe_data["real_product"]
        sum_value = probe_data["real_sum"]
        color = SIGNAL_BLUE
        title = rf"$\Re\{{X[k]\}}$, {freq_text(probe_frequency_hz)} Hz"
        filename = "06_summe_cos.png"
        box_text = rf"$\Re\{{X[k]\}} = {sum_value:+.3f}$"
    else:
        product_values = probe_data["imag_product"]
        sum_value = probe_data["imag_sum"]
        color = SIGNAL_ORANGE
        title = rf"$\Im\{{X[k]\}}$, {freq_text(probe_frequency_hz)} Hz"
        filename = "07_summe_minus_sin.png"
        box_text = rf"$\Im\{{X[k]\}} = {sum_value:+.3f}$"

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


def export_phasor_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data) -> None:
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
    ax.set_xlim(-context["complex_limit"], context["complex_limit"])
    ax.set_ylim(-context["complex_limit"], context["complex_limit"])
    tick_values = phasor_ticks(context["complex_limit"])
    ax.set_xticks(tick_values)
    ax.set_yticks(tick_values)
    ax.grid(alpha=0.22)
    ax.set_xlabel(r"Re$\{X[k]\}$", fontsize=phasor_label_size, color=SIGNAL_BLUE)
    ax.set_ylabel(r"Im$\{X[k]\}$", fontsize=phasor_label_size, color=SIGNAL_ORANGE)
    ax.set_title(
        rf"$X[k]$, {freq_text(probe_frequency_hz)} Hz",
        pad=10,
        fontsize=phasor_title_size,
    )
    ax.tick_params(axis="x", labelsize=phasor_tick_size, colors=SIGNAL_BLUE)
    ax.tick_params(axis="y", labelsize=phasor_tick_size, colors=SIGNAL_ORANGE)
    save_figure(fig, output_dir / "08_komplexer_bin_wert.png", target_size=REFERENCE_PHASOR_EXPORT_SIZE)


def export_spectrum_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    magnitudes = context["spectrum_magnitudes"]
    repeated_frequencies, repeated_magnitudes = repeated_spectrum_view(frequencies, magnitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_magnitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(repeated_frequencies, repeated_magnitudes, "o", color=INACTIVE_GREY, ms=7)
    if probe_data["copy_frequencies_hz"]:
        copy_magnitudes = np.full(len(probe_data["copy_frequencies_hz"]), probe_data["magnitude"])
        ax.vlines(probe_data["copy_frequencies_hz"], 0.0, copy_magnitudes, color=ACTIVE_LIGHT_RED, lw=2.6)
        ax.plot(probe_data["copy_frequencies_hz"], copy_magnitudes, "o", color=ACTIVE_LIGHT_RED, ms=8)
    ax.vlines(probe_frequency_hz, 0.0, probe_data["magnitude"], color=ACTIVE_RED, lw=2.8)
    ax.plot([probe_frequency_hz], [probe_data["magnitude"]], "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        rf"$|X[k]|$, {freq_text(probe_frequency_hz)} Hz",
        (0.0, context["spectrum_limit"]),
        r"$|X[k]|$",
    )
    draw_fs_markers(ax, (0.0, context["spectrum_limit"]))
    save_figure(fig, output_dir / "09_dft_betragsspektrum.png", target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_phase_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data) -> None:
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
        ax.vlines(probe_frequency_hz, 0.0, probe_data["phase_deg"], color=ACTIVE_RED, lw=2.8)
        ax.plot([probe_frequency_hz], [probe_data["phase_deg"]], "o", color=ACTIVE_RED, ms=8)
    else:
        ax.plot([probe_frequency_hz], [0.0], "o", color=ACTIVE_RED, ms=8)

    style_spectrum_axis(
        ax,
        f"Phase, {freq_text(probe_frequency_hz)} Hz",
        (-190.0, 190.0),
        "Phase [deg]",
    )
    draw_fs_markers(ax, (-190.0, 190.0))

    save_figure(fig, output_dir / "10_dft_phasenspektrum.png", target_size=REFERENCE_PHASE_EXPORT_SIZE)


def export_amplitude_spectrum_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["spectrum_frequencies_hz"]
    amplitudes = context["amplitude_magnitudes"]
    repeated_frequencies, repeated_amplitudes = repeated_spectrum_view(frequencies, amplitudes)
    ax.vlines(repeated_frequencies, 0.0, repeated_amplitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(repeated_frequencies, repeated_amplitudes, "o", color=INACTIVE_GREY, ms=7)
    if probe_data["copy_frequencies_hz"]:
        copy_amplitudes = np.full(len(probe_data["copy_frequencies_hz"]), probe_data["amplitude_magnitude"])
        ax.vlines(probe_data["copy_frequencies_hz"], 0.0, copy_amplitudes, color=ACTIVE_LIGHT_RED, lw=2.6)
        ax.plot(probe_data["copy_frequencies_hz"], copy_amplitudes, "o", color=ACTIVE_LIGHT_RED, ms=8)
    ax.vlines(probe_frequency_hz, 0.0, probe_data["amplitude_magnitude"], color=ACTIVE_RED, lw=2.8)
    ax.plot([probe_frequency_hz], [probe_data["amplitude_magnitude"]], "o", color=ACTIVE_RED, ms=8)
    style_spectrum_axis(
        ax,
        rf"$A_k^{{(2)}}$, {freq_text(probe_frequency_hz)} Hz",
        (0.0, context["amplitude_limit"]),
        r"$A_k^{(2)}$",
    )
    draw_fs_markers(ax, (0.0, context["amplitude_limit"]))
    save_figure(fig, output_dir / "11_amplitudenspektrum_zweiseitig.png", target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_one_sided_amplitude_spectrum_plot(context, output_dir: Path, probe_frequency_hz: float, probe_data) -> None:
    fig, ax = create_spectrum_figure()
    frequencies = context["one_sided_frequencies_hz"]
    amplitudes = context["one_sided_amplitudes"]
    ax.vlines(frequencies, 0.0, amplitudes, color=INACTIVE_GREY, lw=2.4)
    ax.plot(frequencies, amplitudes, "o", color=INACTIVE_GREY, ms=7)
    highlight_frequency_hz = probe_data["one_sided_frequency_hz"]
    highlight_amplitude = probe_data["one_sided_amplitude"]
    ax.vlines(highlight_frequency_hz, 0.0, highlight_amplitude, color=ACTIVE_RED, lw=2.8)
    ax.plot([highlight_frequency_hz], [highlight_amplitude], "o", color=ACTIVE_RED, ms=8)
    style_one_sided_spectrum_axis(
        ax,
        rf"$A_k^{{(1)}}$, {freq_text(probe_data['one_sided_frequency_hz'])} Hz",
        (0.0, context["one_sided_limit"]),
        r"$A_k^{(1)}$",
    )
    save_figure(fig, output_dir / "12_amplitudenspektrum_einseitig.png", target_size=REFERENCE_MAG_EXPORT_SIZE)


def export_probe_series(context, probe_frequency_hz: float) -> None:
    probe_data = context["probe_results"][probe_frequency_hz]
    output_dir = probe_dir(probe_frequency_hz)
    output_dir.mkdir(parents=True, exist_ok=True)

    export_signal_plot(context, output_dir, probe_frequency_hz)
    export_basis_plot(context, output_dir, probe_frequency_hz, probe_data, part="real")
    export_basis_plot(context, output_dir, probe_frequency_hz, probe_data, part="imag")
    export_product_plot(context, output_dir, probe_frequency_hz, probe_data, part="real")
    export_product_plot(context, output_dir, probe_frequency_hz, probe_data, part="imag")
    export_sum_plot(context, output_dir, probe_frequency_hz, probe_data, part="real")
    export_sum_plot(context, output_dir, probe_frequency_hz, probe_data, part="imag")
    export_phasor_plot(context, output_dir, probe_frequency_hz, probe_data)
    export_spectrum_plot(context, output_dir, probe_frequency_hz, probe_data)
    export_phase_plot(context, output_dir, probe_frequency_hz, probe_data)
    export_amplitude_spectrum_plot(context, output_dir, probe_frequency_hz, probe_data)
    export_one_sided_amplitude_spectrum_plot(context, output_dir, probe_frequency_hz, probe_data)


def main() -> None:
    clear_output_root()
    context = prepare_context()
    for probe_frequency_hz in PROBE_FREQUENCIES_HZ:
        export_probe_series(context, probe_frequency_hz)
    print(f"PNG storyboard exported to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
