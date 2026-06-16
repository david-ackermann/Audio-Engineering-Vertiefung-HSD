from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import export_block_02_ringmodulation_am_tremolo as base


LECTURE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LECTURE_DIR.parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "03_single_sideband_modulator" / "03a_single_sideband_material"
AUDIO_FILE = PROJECT_DIR / "audio_samples" / "nachhallfrei" / "instrumente" / "Bonobo_Kerala.wav"

DPI = 200
TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (12.0, 4.8)
ZOOM_FIGSIZE = (12.0, 4.4)

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
MODULATION_VIOLET = "#7b4ab8"
REFERENCE_GREY = "0.70"
BACKGROUND_SPECTRUM_GREY = "0.82"

TITLE_SIZE = 24
SPECTRUM_DB_FLOOR = -85.0

DURATION_S = 20.0
EXPECTED_SAMPLE_RATE_HZ = 48_000.0
CARRIER_LOWPASS_HZ = 10_000.0
CARRIER_LOWPASS_TRANSITION_HZ = 1_000.0
MODULATION_FREQUENCY_HZ = 12_000.0


def analytic_signal(signal: np.ndarray) -> np.ndarray:
    spectrum = np.fft.fft(signal)
    response = np.zeros(len(signal))

    if len(signal) % 2 == 0:
        response[0] = 1.0
        response[len(signal) // 2] = 1.0
        response[1 : len(signal) // 2] = 2.0
    else:
        response[0] = 1.0
        response[1 : (len(signal) + 1) // 2] = 2.0

    return np.fft.ifft(spectrum * response)


def normalize(signal: np.ndarray) -> np.ndarray:
    peak = max(float(np.max(np.abs(signal))), np.finfo(float).eps)
    return signal / peak


def save_time_signal(time_s: np.ndarray, signal: np.ndarray, *, title: str, color: str, filename: str) -> Path:
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    base.plot_audio_time(ax, time_s, signal, title=title, color=color)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_original_carrier_spectrum(raw_carrier: np.ndarray, sample_rate_hz: float) -> Path:
    frequencies_khz, raw_magnitude = base.two_sided_spectrum_magnitude(raw_carrier, sample_rate_hz)
    raw_magnitude_db = base.magnitude_to_db(raw_magnitude, float(np.max(raw_magnitude)))

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, raw_magnitude_db, color=SIGNAL_BLACK, lw=1.4)
    ax.set_title("Original carrier spectrum", fontsize=TITLE_SIZE, pad=14)
    base.style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "02_original_carrier_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_carrier_spectrum(raw_carrier: np.ndarray, carrier: np.ndarray, sample_rate_hz: float) -> Path:
    frequencies_khz, raw_magnitude = base.two_sided_spectrum_magnitude(raw_carrier, sample_rate_hz)
    _, carrier_magnitude = base.two_sided_spectrum_magnitude(carrier, sample_rate_hz)
    reference = max(float(np.max(raw_magnitude)), float(np.max(carrier_magnitude)))
    raw_magnitude_db = base.magnitude_to_db(raw_magnitude, reference)
    carrier_magnitude_db = base.magnitude_to_db(carrier_magnitude, reference)

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, raw_magnitude_db, color=BACKGROUND_SPECTRUM_GREY, lw=1.2, zorder=1)
    ax.plot(frequencies_khz, carrier_magnitude_db, color=SIGNAL_BLACK, lw=1.4, zorder=2)
    ax.axvline(-CARRIER_LOWPASS_HZ / 1000.0, color=REFERENCE_GREY, lw=1.4, ls="--")
    ax.axvline(CARRIER_LOWPASS_HZ / 1000.0, color=REFERENCE_GREY, lw=1.4, ls="--")
    ax.set_title("Carrier spectrum", fontsize=TITLE_SIZE, pad=14)
    base.style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "04_band_limited_carrier_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_modulation_time_zoom() -> Path:
    zoom_duration_s = 0.5e-3
    display_time_s = np.linspace(0.0, zoom_duration_s, 1600)
    zoom_time_ms = 1000.0 * display_time_s
    zoom_signal = np.sin(2.0 * np.pi * MODULATION_FREQUENCY_HZ * display_time_s)

    fig, ax = plt.subplots(figsize=ZOOM_FIGSIZE)
    ax.plot(zoom_time_ms, zoom_signal, color=MODULATION_VIOLET, lw=2.6)
    ax.set_title("12 kHz sine", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, zoom_duration_s * 1000.0)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0.0, zoom_duration_s * 1000.0 + 0.001, 0.1))
    base.style_time_axis(ax, xlabel="Time in ms", ylabel="Amplitude")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "05_modulation_signal_12khz_time_zoom.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_modulation_spectrum() -> Path:
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.vlines(
        [-MODULATION_FREQUENCY_HZ / 1000.0, MODULATION_FREQUENCY_HZ / 1000.0],
        SPECTRUM_DB_FLOOR,
        0.0,
        color=MODULATION_VIOLET,
        lw=3.4,
    )
    ax.set_title("Modulator spectrum", fontsize=TITLE_SIZE, pad=14)
    base.style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "06_modulation_signal_12khz_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_output_spectrum(
    output: np.ndarray,
    sample_rate_hz: float,
    *,
    title: str,
    filename: str,
) -> Path:
    frequencies_khz, output_magnitude = base.two_sided_spectrum_magnitude(output, sample_rate_hz)
    output_magnitude_db = base.magnitude_to_db(output_magnitude, float(np.max(output_magnitude)))

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, output_magnitude_db, color=SPECTRUM_BLUE, lw=1.4)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    base.style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated_filenames = [
        "01_original_carrier_time_20s.png",
        "02_original_carrier_spectrum_twosided.png",
        "03_band_limited_carrier_time_20s.png",
        "04_band_limited_carrier_spectrum_twosided.png",
        "05_modulation_signal_12khz_time_zoom.png",
        "06_modulation_signal_12khz_spectrum_twosided.png",
        "07_usb_output_time_20s.png",
        "08_usb_output_spectrum_twosided.png",
        "09_lsb_output_time_20s.png",
        "10_lsb_output_spectrum_twosided.png",
    ]
    for filename in generated_filenames:
        image_file = OUTPUT_DIR / filename
        if image_file.exists():
            image_file.unlink()

    sample_rate_hz, raw_carrier = base.read_wav_mono(AUDIO_FILE, DURATION_S)
    if sample_rate_hz != EXPECTED_SAMPLE_RATE_HZ:
        raise ValueError(f"Expected {EXPECTED_SAMPLE_RATE_HZ:.0f} Hz carrier file, got {sample_rate_hz:.0f} Hz")

    time_s = np.arange(len(raw_carrier)) / sample_rate_hz
    carrier = base.bandlimit_with_fft(
        raw_carrier,
        sample_rate_hz,
        CARRIER_LOWPASS_HZ,
        CARRIER_LOWPASS_TRANSITION_HZ,
    )

    carrier_analytic = analytic_signal(carrier)
    carrier_hilbert = np.imag(carrier_analytic)
    modulator = np.sin(2.0 * np.pi * MODULATION_FREQUENCY_HZ * time_s)
    modulator_quadrature = np.cos(2.0 * np.pi * MODULATION_FREQUENCY_HZ * time_s)

    usb_output = normalize(carrier * modulator + carrier_hilbert * modulator_quadrature)
    lsb_output = normalize(carrier * modulator - carrier_hilbert * modulator_quadrature)

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
        save_time_signal(
            time_s,
            usb_output,
            title="USB output",
            color=SPECTRUM_BLUE,
            filename="07_usb_output_time_20s.png",
        ),
        save_output_spectrum(
            usb_output,
            sample_rate_hz,
            title="USB output spectrum",
            filename="08_usb_output_spectrum_twosided.png",
        ),
        save_time_signal(
            time_s,
            lsb_output,
            title="LSB output",
            color=SPECTRUM_BLUE,
            filename="09_lsb_output_time_20s.png",
        ),
        save_output_spectrum(
            lsb_output,
            sample_rate_hz,
            title="LSB output spectrum",
            filename="10_lsb_output_spectrum_twosided.png",
        ),
    ]

    for path in image_paths:
        print(path)


if __name__ == "__main__":
    main()
