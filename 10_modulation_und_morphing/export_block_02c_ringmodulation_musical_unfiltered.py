from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import export_block_02b_ringmodulation_audible_low_band as base


LECTURE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LECTURE_DIR.parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "02_am_modulation" / "02c_ringmodulation_musical_unfiltered"
AUDIO_OUTPUT_DIR = LECTURE_DIR / "audio_exports" / "02_am_modulation" / "02c_ringmodulation_musical_unfiltered"
AUDIO_FILE = PROJECT_DIR / "audio_samples" / "nachhallfrei" / "instrumente" / "Bonobo_Kerala.wav"

DURATION_S = 20.0
EXPECTED_SAMPLE_RATE_HZ = 48_000.0
RING_MODULATION_FREQUENCY_HZ = 110.0
WET_MIX = 0.35

TIME_FIGSIZE = (12.0, 4.4)
SPECTRUM_FIGSIZE = (12.0, 4.8)
ZOOM_FIGSIZE = (12.0, 4.4)
DPI = 200

SIGNAL_BLACK = "0.10"
SPECTRUM_BLUE = "#2b7bbb"
MODULATION_VIOLET = "#7b4ab8"
TITLE_SIZE = 24
SPECTRUM_DB_FLOOR = -85.0


def save_time_signal(time_s: np.ndarray, signal: np.ndarray, *, title: str, color: str, filename: str) -> Path:
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    base.plot_audio_time(ax, time_s, signal, title=title, color=color)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_spectrum(signal: np.ndarray, sample_rate_hz: float, *, title: str, color: str, filename: str) -> Path:
    frequencies_khz, magnitude = base.two_sided_spectrum_magnitude(signal, sample_rate_hz)
    magnitude_db = base.magnitude_to_db(magnitude, float(np.max(magnitude)))

    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(frequencies_khz, magnitude_db, color=color, lw=1.4)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    base.style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_modulation_time_zoom() -> Path:
    zoom_duration_s = 3.0 / RING_MODULATION_FREQUENCY_HZ
    display_time_s = np.linspace(0.0, zoom_duration_s, 2400)
    zoom_time_ms = 1000.0 * display_time_s
    zoom_signal = np.sin(2.0 * np.pi * RING_MODULATION_FREQUENCY_HZ * display_time_s)

    fig, ax = plt.subplots(figsize=ZOOM_FIGSIZE)
    ax.plot(zoom_time_ms, zoom_signal, color=MODULATION_VIOLET, lw=2.6)
    ax.set_title("110 Hz sine", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, zoom_duration_s * 1000.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xticks(np.arange(0.0, zoom_duration_s * 1000.0 + 0.1, 10.0))
    base.style_time_axis(ax, xlabel="Time in ms", ylabel="Amplitude")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "03_modulation_signal_110hz_time_zoom.png"
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
    base.style_spectrum_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    path = OUTPUT_DIR / "04_modulation_signal_110hz_spectrum_twosided.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()
    for audio_file in AUDIO_OUTPUT_DIR.glob("*.wav"):
        audio_file.unlink()

    sample_rate_hz, carrier = base.read_wav_mono(AUDIO_FILE, DURATION_S)
    if sample_rate_hz != EXPECTED_SAMPLE_RATE_HZ:
        raise ValueError(f"Expected {EXPECTED_SAMPLE_RATE_HZ:.0f} Hz carrier file, got {sample_rate_hz:.0f} Hz")

    time_s = np.arange(len(carrier)) / sample_rate_hz
    modulator = np.sin(2.0 * np.pi * RING_MODULATION_FREQUENCY_HZ * time_s)
    ringmod_wet = carrier * modulator
    ringmod_wet /= max(float(np.max(np.abs(ringmod_wet))), np.finfo(float).eps)

    mixed_output = (1.0 - WET_MIX) * carrier + WET_MIX * ringmod_wet
    mixed_output /= max(float(np.max(np.abs(mixed_output))), np.finfo(float).eps)

    image_paths = [
        save_time_signal(
            time_s,
            carrier,
            title="Original carrier",
            color=SIGNAL_BLACK,
            filename="01_original_carrier_time_20s.png",
        ),
        save_spectrum(
            carrier,
            sample_rate_hz,
            title="Original carrier spectrum",
            color=SIGNAL_BLACK,
            filename="02_original_carrier_spectrum_twosided.png",
        ),
        save_modulation_time_zoom(),
        save_modulation_spectrum(),
        save_time_signal(
            time_s,
            ringmod_wet,
            title="Ring-modulated output",
            color=SPECTRUM_BLUE,
            filename="05_ring_modulated_output_time_20s.png",
        ),
        save_spectrum(
            ringmod_wet,
            sample_rate_hz,
            title="Output spectrum",
            color=SPECTRUM_BLUE,
            filename="06_ring_modulated_output_spectrum_twosided.png",
        ),
        save_time_signal(
            time_s,
            mixed_output,
            title="Wet/dry output",
            color=SPECTRUM_BLUE,
            filename="07_wetdry_output_time_20s.png",
        ),
        save_spectrum(
            mixed_output,
            sample_rate_hz,
            title="Wet/dry spectrum",
            color=SPECTRUM_BLUE,
            filename="08_wetdry_output_spectrum_twosided.png",
        ),
    ]

    audio_paths = [
        base.write_wav_mono(AUDIO_OUTPUT_DIR / "01_original_carrier_20s_48k.wav", sample_rate_hz, carrier),
        base.write_wav_mono(AUDIO_OUTPUT_DIR / "02_modulation_signal_110hz_20s_48k.wav", sample_rate_hz, modulator),
        base.write_wav_mono(AUDIO_OUTPUT_DIR / "03_ring_modulated_full_wet_110hz_20s_48k.wav", sample_rate_hz, ringmod_wet),
        base.write_wav_mono(AUDIO_OUTPUT_DIR / "04_ring_modulated_wetdry_35pct_110hz_20s_48k.wav", sample_rate_hz, mixed_output),
    ]

    for path in image_paths + audio_paths:
        print(path)


if __name__ == "__main__":
    main()
