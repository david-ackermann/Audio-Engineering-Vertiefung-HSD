from pathlib import Path
import wave

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LECTURE_DIR.parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "02_am_modulation" / "02_ringmodulation_am_tremolo"
AUDIO_FILE = PROJECT_DIR / "audio_samples" / "nachhallfrei" / "instrumente" / "Bonobo_Kerala.wav"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (12.0, 4.8)
ZOOM_FIGSIZE = (12.0, 4.4)

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
MODULATION_VIOLET = "#7b4ab8"
GRID_GREY = "0.75"
REFERENCE_GREY = "0.70"
BACKGROUND_SPECTRUM_GREY = "0.82"

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17

DURATION_S = 20.0
EXPECTED_SAMPLE_RATE_HZ = 48_000.0
CARRIER_LOWPASS_HZ = 10_000.0
CARRIER_LOWPASS_TRANSITION_HZ = 1_000.0
RING_MODULATION_FREQUENCY_HZ = 12_000.0
SPECTRUM_FFT_LENGTH = 2**18
SPECTRUM_DB_FLOOR = -85.0

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


def bandlimit_with_fft(
    signal: np.ndarray,
    sample_rate_hz: float,
    cutoff_hz: float,
    transition_hz: float,
) -> np.ndarray:
    spectrum = np.fft.rfft(signal)
    frequencies_hz = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate_hz)

    mask = np.ones_like(frequencies_hz)
    stop_hz = cutoff_hz + transition_hz
    mask[frequencies_hz >= stop_hz] = 0.0
    transition = (frequencies_hz > cutoff_hz) & (frequencies_hz < stop_hz)
    phase = (frequencies_hz[transition] - cutoff_hz) / transition_hz
    mask[transition] = 0.5 * (1.0 + np.cos(np.pi * phase))

    filtered = np.fft.irfft(spectrum * mask, n=len(signal))
    filtered -= float(np.mean(filtered))
    peak = max(float(np.max(np.abs(filtered))), np.finfo(float).eps)
    return filtered / peak


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


def two_sided_spectrum_magnitude(signal: np.ndarray, sample_rate_hz: float) -> tuple[np.ndarray, np.ndarray]:
    if len(signal) >= SPECTRUM_FFT_LENGTH:
        segment = signal[:SPECTRUM_FFT_LENGTH]
    else:
        segment = np.pad(signal, (0, SPECTRUM_FFT_LENGTH - len(signal)))

    window = np.hanning(SPECTRUM_FFT_LENGTH)
    spectrum = np.fft.fftshift(np.fft.fft(segment * window))
    frequencies_hz = np.fft.fftshift(np.fft.fftfreq(SPECTRUM_FFT_LENGTH, d=1.0 / sample_rate_hz))
    magnitude = np.abs(spectrum)
    return frequencies_hz / 1000.0, magnitude


def magnitude_to_db(magnitude: np.ndarray, reference: float) -> np.ndarray:
    magnitude_db = 20.0 * np.log10(magnitude / max(reference, np.finfo(float).eps) + 1e-12)
    return np.maximum(magnitude_db, SPECTRUM_DB_FLOOR)


def two_sided_spectrum_db(signal: np.ndarray, sample_rate_hz: float) -> tuple[np.ndarray, np.ndarray]:
    frequencies_khz, magnitude = two_sided_spectrum_magnitude(signal, sample_rate_hz)
    magnitude_db = magnitude_to_db(magnitude, float(np.max(magnitude)))
    return frequencies_khz, magnitude_db


def style_time_axis(ax: plt.Axes, *, xlabel: str = "Time in s", ylabel: str = "Amplitude") -> None:
    ax.set_xlabel(xlabel, fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color="0.55", lw=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def style_spectrum_axis(ax: plt.Axes) -> None:
    ax.set_xlabel("Frequency (kHz)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude (dB)", fontsize=LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.set_xlim(-24.0, 24.0)
    ax.set_ylim(SPECTRUM_DB_FLOOR, 3.0)
    ax.set_xticks(np.arange(-24.0, 24.1, 6.0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_audio_time(ax: plt.Axes, time_s: np.ndarray, signal: np.ndarray, *, title: str, color: str) -> None:
    band_time, lower, upper = peak_bands(time_s, signal)
    ax.fill_between(band_time, lower, upper, color=color, linewidth=0.0)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.1, 5.0))
    style_time_axis(ax)


def save_time_signal(time_s: np.ndarray, signal: np.ndarray, *, title: str, color: str, filename: str) -> Path:
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    plot_audio_time(ax, time_s, signal, title=title, color=color)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_original_carrier_spectrum(raw_carrier: np.ndarray, sample_rate_hz: float) -> Path:
    frequencies_khz, raw_magnitude = two_sided_spectrum_magnitude(raw_carrier, sample_rate_hz)
    raw_magnitude_db = magnitude_to_db(raw_magnitude, float(np.max(raw_magnitude)))

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, raw_magnitude_db, color=SIGNAL_BLACK, lw=1.4)
    ax.set_title("Original carrier spectrum", fontsize=TITLE_SIZE, pad=14)
    style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "02_original_carrier_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_carrier_spectrum(raw_carrier: np.ndarray, carrier: np.ndarray, sample_rate_hz: float) -> Path:
    frequencies_khz, raw_magnitude = two_sided_spectrum_magnitude(raw_carrier, sample_rate_hz)
    _, carrier_magnitude = two_sided_spectrum_magnitude(carrier, sample_rate_hz)
    reference = max(float(np.max(raw_magnitude)), float(np.max(carrier_magnitude)))
    raw_magnitude_db = magnitude_to_db(raw_magnitude, reference)
    carrier_magnitude_db = magnitude_to_db(carrier_magnitude, reference)

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, raw_magnitude_db, color=BACKGROUND_SPECTRUM_GREY, lw=1.2, zorder=1)
    ax.plot(frequencies_khz, carrier_magnitude_db, color=SIGNAL_BLACK, lw=1.4, zorder=2)
    ax.axvline(-CARRIER_LOWPASS_HZ / 1000.0, color=REFERENCE_GREY, lw=1.4, ls="--")
    ax.axvline(CARRIER_LOWPASS_HZ / 1000.0, color=REFERENCE_GREY, lw=1.4, ls="--")
    ax.set_title("Carrier spectrum", fontsize=TITLE_SIZE, pad=14)
    style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "04_band_limited_carrier_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_modulation_time_zoom() -> Path:
    zoom_duration_s = 0.5e-3
    display_time_s = np.linspace(0.0, zoom_duration_s, 1600)
    zoom_time_ms = 1000.0 * display_time_s
    zoom_signal = np.sin(2.0 * np.pi * RING_MODULATION_FREQUENCY_HZ * display_time_s)

    fig, ax = plt.subplots(figsize=ZOOM_FIGSIZE)
    ax.plot(zoom_time_ms, zoom_signal, color=MODULATION_VIOLET, lw=2.6)
    ax.set_title("12 kHz sine", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, zoom_duration_s * 1000.0)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, zoom_duration_s * 1000.0 + 0.001, 0.1))
    style_time_axis(ax, xlabel="Time in ms", ylabel="Amplitude")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "05_modulation_signal_12khz_time_zoom.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_modulation_spectrum() -> Path:
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.vlines(
        [-RING_MODULATION_FREQUENCY_HZ / 1000.0, RING_MODULATION_FREQUENCY_HZ / 1000.0],
        SPECTRUM_DB_FLOOR,
        0.0,
        color=MODULATION_VIOLET,
        lw=3.4,
    )
    ax.set_title("Modulator spectrum", fontsize=TITLE_SIZE, pad=14)
    style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "06_modulation_signal_12khz_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_output_time(time_s: np.ndarray, output: np.ndarray) -> Path:
    return save_time_signal(
        time_s,
        output,
        title="Ring-modulated output",
        color=SPECTRUM_BLUE,
        filename="07_ring_modulated_output_time_20s.png",
    )


def save_output_spectrum(output: np.ndarray, sample_rate_hz: float) -> Path:
    frequencies_khz, output_magnitude = two_sided_spectrum_magnitude(output, sample_rate_hz)
    output_magnitude_db = magnitude_to_db(output_magnitude, float(np.max(output_magnitude)))

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, output_magnitude_db, color=SPECTRUM_BLUE, lw=1.4)
    ax.set_title("Output spectrum", fontsize=TITLE_SIZE, pad=14)
    style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "08_ring_modulated_output_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()

    sample_rate_hz, raw_carrier = read_wav_mono(AUDIO_FILE, DURATION_S)
    if sample_rate_hz != EXPECTED_SAMPLE_RATE_HZ:
        raise ValueError(f"Expected {EXPECTED_SAMPLE_RATE_HZ:.0f} Hz carrier file, got {sample_rate_hz:.0f} Hz")

    time_s = np.arange(len(raw_carrier)) / sample_rate_hz
    carrier = bandlimit_with_fft(
        raw_carrier,
        sample_rate_hz,
        CARRIER_LOWPASS_HZ,
        CARRIER_LOWPASS_TRANSITION_HZ,
    )
    modulation = np.sin(2.0 * np.pi * RING_MODULATION_FREQUENCY_HZ * time_s)
    output = carrier * modulation
    output /= max(float(np.max(np.abs(output))), np.finfo(float).eps)

    image_paths = [
        save_time_signal(
            time_s,
            raw_carrier,
            title="Original carrier",
            color=SIGNAL_BLACK,
            filename="01_original_carrier_time_20s.png",
        ),
        save_original_carrier_spectrum(raw_carrier, sample_rate_hz),
        save_time_signal(
            time_s,
            carrier,
            title="Band-limited carrier",
            color=SIGNAL_BLACK,
            filename="03_band_limited_carrier_time_20s.png",
        ),
        save_carrier_spectrum(raw_carrier, carrier, sample_rate_hz),
        save_modulation_time_zoom(),
        save_modulation_spectrum(),
        save_output_time(time_s, output),
        save_output_spectrum(output, sample_rate_hz),
    ]

    for path in image_paths:
        print(path)


if __name__ == "__main__":
    main()
