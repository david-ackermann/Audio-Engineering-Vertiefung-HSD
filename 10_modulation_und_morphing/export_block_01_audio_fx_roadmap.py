from pathlib import Path
import wave

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LECTURE_DIR.parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "01_audio_fx_roadmap"
AUDIO_FILE = PROJECT_DIR / "audio_samples" / "nachhallfrei" / "instrumente" / "Bonobo_Kerala.wav"

DPI = 200
SINGLE_FIGSIZE = (12.0, 4.4)

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
COMPARE_ORANGE = "#d98c2f"
MODULATION_VIOLET = "#7b4ab8"
GRID_GREY = "0.75"
REFERENCE_GREY = "0.80"

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17

DURATION_S = 20.0
MODULATION_FREQUENCY_HZ = 0.25
ENVELOPE_ATTACK_MS = 10.0
ENVELOPE_RELEASE_MS = 180.0
ANALYSIS_FRAME_SIZE = 4096
ANALYSIS_HOP_SIZE = 512
ACTIVE_RMS_THRESHOLD = 0.05
BASS_BAND_HZ = (60.0, 250.0)
COMPRESSOR_STRENGTH = 10.0
COMPRESSOR_MIN_GAIN = 0.12

OUTPUT_FILENAMES = [
    "01_carrier_signal_bonobo_20s.png",
    "02_modulation_signal_low_frequency_sine.png",
    "03_carrier_times_modulation_product.png",
    "04_demodulated_envelope_from_bonobo.png",
    "05_demodulated_bass_envelope_from_bonobo.png",
    "06_demodulated_zero_crossing_rate_from_bonobo.png",
    "07_compressor_output_from_envelope.png",
]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def read_wav_mono(path: Path, duration_s: float) -> tuple[float, np.ndarray]:
    with wave.open(str(path), "rb") as handle:
        sample_rate_hz = float(handle.getframerate())
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        frames_to_read = min(handle.getnframes(), int(round(duration_s * sample_rate_hz)))
        raw = handle.readframes(frames_to_read)

    if sample_width == 1:
        data = (np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128.0) / 128.0
    elif sample_width == 2:
        data = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    elif sample_width == 3:
        bytes_24 = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        signed = (
            bytes_24[:, 0].astype(np.int32)
            | (bytes_24[:, 1].astype(np.int32) << 8)
            | (bytes_24[:, 2].astype(np.int32) << 16)
        )
        signed = np.where(signed & 0x800000, signed - 0x1000000, signed)
        data = signed.astype(np.float64) / float(2**23)
    elif sample_width == 4:
        data = np.frombuffer(raw, dtype="<i4").astype(np.float64) / float(2**31)
    else:
        raise ValueError(f"Unsupported WAV sample width: {sample_width} bytes")

    if channels > 1:
        data = data.reshape(-1, channels).mean(axis=1)

    data -= float(np.mean(data))
    peak = max(float(np.max(np.abs(data))), np.finfo(float).eps)
    return sample_rate_hz, data / peak


def envelope_detector(
    signal: np.ndarray,
    sample_rate_hz: float,
    attack_ms: float = ENVELOPE_ATTACK_MS,
    release_ms: float = ENVELOPE_RELEASE_MS,
) -> np.ndarray:
    rectified = np.abs(signal)
    attack = np.exp(-1.0 / (sample_rate_hz * attack_ms * 1e-3))
    release = np.exp(-1.0 / (sample_rate_hz * release_ms * 1e-3))

    envelope = np.empty_like(rectified)
    state = 0.0
    for sample_index, value in enumerate(rectified):
        coefficient = attack if value > state else release
        state = coefficient * state + (1.0 - coefficient) * value
        envelope[sample_index] = state

    envelope_peak = max(float(np.max(envelope)), np.finfo(float).eps)
    return envelope / envelope_peak


def compressor_gain_from_envelope(envelope: np.ndarray) -> np.ndarray:
    return COMPRESSOR_MIN_GAIN + (1.0 - COMPRESSOR_MIN_GAIN) / (1.0 + COMPRESSOR_STRENGTH * envelope)


def frame_signal(signal: np.ndarray, frame_size: int, hop_size: int) -> np.ndarray:
    if len(signal) < frame_size:
        padded = np.pad(signal, (0, frame_size - len(signal)))
        return padded[None, :]

    frame_count = 1 + (len(signal) - frame_size) // hop_size
    shape = (frame_count, frame_size)
    strides = (signal.strides[0] * hop_size, signal.strides[0])
    return np.lib.stride_tricks.as_strided(signal, shape=shape, strides=strides).copy()


def moving_average(signal: np.ndarray, length: int) -> np.ndarray:
    if length <= 1:
        return signal
    kernel = np.ones(length) / length
    return np.convolve(signal, kernel, mode="same")


def normalize_control_signal(signal: np.ndarray) -> np.ndarray:
    shifted = signal - float(np.min(signal))
    scale = float(np.percentile(shifted, 98.0))
    if scale <= np.finfo(float).eps:
        scale = max(float(np.max(shifted)), np.finfo(float).eps)
    return np.clip(shifted / scale, 0.0, 1.0)


def band_energy_demodulation_features(signal: np.ndarray, sample_rate_hz: float) -> tuple[np.ndarray, np.ndarray]:
    frames = frame_signal(signal, ANALYSIS_FRAME_SIZE, ANALYSIS_HOP_SIZE)
    window = np.hanning(ANALYSIS_FRAME_SIZE)
    magnitude = np.abs(np.fft.rfft(frames * window[None, :], axis=1))
    frequencies_hz = np.fft.rfftfreq(ANALYSIS_FRAME_SIZE, d=1.0 / sample_rate_hz)
    frame_time_s = (np.arange(len(frames)) * ANALYSIS_HOP_SIZE + 0.5 * ANALYSIS_FRAME_SIZE) / sample_rate_hz
    frame_rms = np.sqrt(np.mean(frames**2, axis=1))
    active_frame = frame_rms > ACTIVE_RMS_THRESHOLD * max(float(np.max(frame_rms)), np.finfo(float).eps)

    bass_bins = (frequencies_hz >= BASS_BAND_HZ[0]) & (frequencies_hz <= BASS_BAND_HZ[1])

    bass_energy = np.sqrt(np.mean(magnitude[:, bass_bins] ** 2, axis=1))
    bass_energy[~active_frame] = 0.0

    bass_envelope = moving_average(normalize_control_signal(bass_energy), 9)
    return frame_time_s, np.clip(bass_envelope, 0.0, 1.0)


def zero_crossing_demodulation_features(signal: np.ndarray, sample_rate_hz: float) -> tuple[np.ndarray, np.ndarray]:
    frames = frame_signal(signal, ANALYSIS_FRAME_SIZE, ANALYSIS_HOP_SIZE)
    frame_time_s = (np.arange(len(frames)) * ANALYSIS_HOP_SIZE + 0.5 * ANALYSIS_FRAME_SIZE) / sample_rate_hz
    frame_rms = np.sqrt(np.mean(frames**2, axis=1))
    active_frame = frame_rms > ACTIVE_RMS_THRESHOLD * max(float(np.max(frame_rms)), np.finfo(float).eps)

    sign_changes = np.diff(np.signbit(frames), axis=1)
    crossings_per_second = np.count_nonzero(sign_changes, axis=1) * sample_rate_hz / ANALYSIS_FRAME_SIZE
    crossings_per_second[~active_frame] = 0.0
    zero_crossing_rate = moving_average(normalize_control_signal(crossings_per_second), 7)
    return frame_time_s, np.clip(zero_crossing_rate, 0.0, 1.0)


def peak_bands(time_s: np.ndarray, signal: np.ndarray, target_columns: int = 3500) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if len(signal) <= target_columns:
        return time_s, signal, signal

    bin_size = max(1, int(np.ceil(len(signal) / target_columns)))
    usable = (len(signal) // bin_size) * bin_size
    y = signal[:usable].reshape(-1, bin_size)
    t = time_s[:usable].reshape(-1, bin_size)
    return t.mean(axis=1), y.min(axis=1), y.max(axis=1)


def decimate_for_line(time_s: np.ndarray, signal: np.ndarray, target_points: int = 5000) -> tuple[np.ndarray, np.ndarray]:
    stride = max(1, int(np.ceil(len(signal) / target_points)))
    return time_s[::stride], signal[::stride]


def style_axis(ax: plt.Axes, *, xlabel: str = "Time in s", ylabel: str = "Amplitude") -> None:
    ax.set_xlabel(xlabel, fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color="0.55", lw=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_carrier(ax: plt.Axes, time_s: np.ndarray, carrier: np.ndarray, *, title: str) -> None:
    band_time, lower, upper = peak_bands(time_s, carrier)
    ax.fill_between(band_time, lower, upper, color=SIGNAL_BLACK, linewidth=0.0)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Amplitude")


def plot_modulation(ax: plt.Axes, time_s: np.ndarray, modulation: np.ndarray, *, title: str) -> None:
    ax.plot(time_s, modulation, color=MODULATION_VIOLET, lw=2.6)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Modulation amplitude")


def plot_product(ax: plt.Axes, time_s: np.ndarray, modulation: np.ndarray, product: np.ndarray, *, title: str) -> None:
    product_time, product_lower, product_upper = peak_bands(time_s, product)
    ax.fill_between(product_time, product_lower, product_upper, color=SPECTRUM_BLUE, linewidth=0.0, alpha=0.95)
    modulation_time, modulation_line = decimate_for_line(time_s, modulation)
    ax.plot(modulation_time, modulation_line, color="0.55", lw=2.5, alpha=0.85)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Amplitude")


def plot_envelope(ax: plt.Axes, time_s: np.ndarray, carrier: np.ndarray, envelope: np.ndarray, *, title: str) -> None:
    band_time, lower, upper = peak_bands(time_s, carrier)
    envelope_time, envelope_line = decimate_for_line(time_s, envelope)

    ax.fill_between(band_time, lower, upper, color=REFERENCE_GREY, linewidth=0.0, alpha=0.85)
    ax.plot(envelope_time, envelope_line, color=MODULATION_VIOLET, lw=2.8)
    ax.plot(envelope_time, -envelope_line, color=MODULATION_VIOLET, lw=1.2, alpha=0.45)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Amplitude / envelope")


def plot_compressed_output(
    ax: plt.Axes,
    time_s: np.ndarray,
    carrier: np.ndarray,
    compressed: np.ndarray,
    *,
    title: str,
) -> None:
    carrier_time, carrier_lower, carrier_upper = peak_bands(time_s, carrier)
    output_time, output_lower, output_upper = peak_bands(time_s, compressed)

    ax.fill_between(carrier_time, carrier_lower, carrier_upper, color=REFERENCE_GREY, linewidth=0.0, alpha=0.75)
    ax.fill_between(output_time, output_lower, output_upper, color=SPECTRUM_BLUE, linewidth=0.0, alpha=0.95)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Amplitude")


def plot_bass_envelope(
    ax: plt.Axes,
    time_s: np.ndarray,
    carrier: np.ndarray,
    feature_time_s: np.ndarray,
    bass_envelope: np.ndarray,
    *,
    title: str,
) -> None:
    band_time, lower, upper = peak_bands(time_s, carrier)
    ax.fill_between(band_time, lower, upper, color=REFERENCE_GREY, linewidth=0.0, alpha=0.85)
    ax.plot(feature_time_s, bass_envelope, color=MODULATION_VIOLET, lw=2.8)
    ax.plot(feature_time_s, -bass_envelope, color=MODULATION_VIOLET, lw=1.2, alpha=0.45)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Amplitude / bass envelope")


def plot_zero_crossing_rate(
    ax: plt.Axes,
    feature_time_s: np.ndarray,
    zero_crossing_rate: np.ndarray,
    *,
    title: str,
) -> None:
    ax.plot(feature_time_s, zero_crossing_rate, color=MODULATION_VIOLET, lw=2.6)
    ax.fill_between(feature_time_s, 0.0, zero_crossing_rate, color=MODULATION_VIOLET, alpha=0.20, linewidth=0.0)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_axis(ax, ylabel="Zero-crossing rate")


def save_single_carrier(time_s: np.ndarray, carrier: np.ndarray) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_carrier(ax, time_s, carrier, title="Carrier signal")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "01_carrier_signal_bonobo_20s.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_single_modulation(time_s: np.ndarray, modulation: np.ndarray) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_modulation(ax, time_s, modulation, title="Modulation signal: low-frequency sine (0.25 Hz)")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "02_modulation_signal_low_frequency_sine.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_single_product(time_s: np.ndarray, modulation: np.ndarray, product: np.ndarray) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_product(ax, time_s, modulation, product, title="Modulated output signal: carrier x modulation signal")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "03_carrier_times_modulation_product.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_single_envelope(time_s: np.ndarray, carrier: np.ndarray, envelope: np.ndarray) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_envelope(ax, time_s, carrier, envelope, title="Demodulation: envelope extracted from the carrier")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "04_demodulated_envelope_from_bonobo.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_single_compressed_output(time_s: np.ndarray, carrier: np.ndarray, compressed: np.ndarray) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_compressed_output(ax, time_s, carrier, compressed, title="Compressor output: envelope as modulator")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "07_compressor_output_from_envelope.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_single_bass_envelope(
    time_s: np.ndarray,
    carrier: np.ndarray,
    feature_time_s: np.ndarray,
    bass_envelope: np.ndarray,
) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_bass_envelope(
        ax,
        time_s,
        carrier,
        feature_time_s,
        bass_envelope,
        title="Demodulation signal: bass envelope (60-250 Hz)",
    )
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "05_demodulated_bass_envelope_from_bonobo.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_single_zero_crossing_rate(feature_time_s: np.ndarray, zero_crossing_rate: np.ndarray) -> Path:
    fig, ax = plt.subplots(figsize=SINGLE_FIGSIZE)
    plot_zero_crossing_rate(
        ax,
        feature_time_s,
        zero_crossing_rate,
        title="Demodulation signal: zero-crossing rate",
    )
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "06_demodulated_zero_crossing_rate_from_bonobo.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename in OUTPUT_FILENAMES:
        path = OUTPUT_DIR / filename
        if path.exists():
            path.unlink()

    sample_rate_hz, carrier = read_wav_mono(AUDIO_FILE, DURATION_S)
    time_s = np.arange(len(carrier)) / sample_rate_hz
    modulation = np.sin(2.0 * np.pi * MODULATION_FREQUENCY_HZ * time_s)
    product = carrier * modulation
    envelope = envelope_detector(carrier, sample_rate_hz)
    compressor_gain = compressor_gain_from_envelope(envelope)
    compressed = carrier * compressor_gain
    band_feature_time_s, bass_envelope = band_energy_demodulation_features(carrier, sample_rate_hz)
    zero_crossing_time_s, zero_crossing_rate = zero_crossing_demodulation_features(carrier, sample_rate_hz)

    paths = [
        save_single_carrier(time_s, carrier),
        save_single_modulation(time_s, modulation),
        save_single_product(time_s, modulation, product),
        save_single_envelope(time_s, carrier, envelope),
        save_single_bass_envelope(time_s, carrier, band_feature_time_s, bass_envelope),
        save_single_zero_crossing_rate(zero_crossing_time_s, zero_crossing_rate),
        save_single_compressed_output(time_s, carrier, compressed),
    ]

    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
