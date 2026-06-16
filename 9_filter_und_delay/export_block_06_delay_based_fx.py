from pathlib import Path
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "06_delay_based_fx"

DPI = 200
FIGSIZE = (11.5, 4.8)
SPECTROGRAM_FIGSIZE = (11.5, 5.45)

SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.70"
DARK_GREY = "0.35"
SIGNAL_BLACK = "0.08"
MODULATION_VIOLET = "#7b4ab8"

FS_HZ = 48_000.0
DURATION_S = 4.0
CARRIER_HZ = 500.0

SIMPLE_CHORUS_DRY_GAIN = 0.50
SIMPLE_CHORUS_G1 = 0.35
SIMPLE_CHORUS_G2 = 0.35
SIMPLE_CHORUS_M1_CENTER_MS = 12.0
SIMPLE_CHORUS_M1_DEPTH_MS = 2.0
SIMPLE_CHORUS_M2_CENTER_MS = 20.0
SIMPLE_CHORUS_M2_DEPTH_MS = 3.0
SIMPLE_CHORUS_NOISE_CUTOFF_HZ = 1.0
SIMPLE_CHORUS_M1_SEED = 202611
SIMPLE_CHORUS_M2_SEED = 202613

FIR_COMB_BL = 1.0
FIR_COMB_FF = 1.0
FIR_COMB_FB = 0.0
FIR_COMB_DELAY_MS = 1.0
FIR_COMB_DEPTH_MS = 0.0

IIR_COMB_BL = 0.0
IIR_COMB_FF = 0.7
IIR_COMB_FB = 0.9
IIR_COMB_DELAY_MS = 5.0
IIR_COMB_DEPTH_MS = 0.0

VIBRATO_BL = 0.0
VIBRATO_FF = 1.0
VIBRATO_FB = 0.0
VIBRATO_DELAY_MS = 0.0
VIBRATO_DEPTH_MS = 3.0
VIBRATO_MOD_HZ = 5.0

CHORUS_BL = 0.7
CHORUS_FF = 0.7
CHORUS_FB = -0.7
CHORUS_DELAY_MS = 20.0
CHORUS_DEPTH_MS = 6.0
CHORUS_NOISE_CUTOFF_HZ = 1.0
NOISE_CONTROL_RATE_HZ = 20.0

FLANGER_BL = 0.7
FLANGER_FF = 0.7
FLANGER_FB = 0.7
FLANGER_DELAY_MS = 0.0
FLANGER_DEPTH_MS = 2.0
FLANGER_MOD_HZ = 1.0
FREQUENCY_RESPONSE_FRAMES = 88
FREQUENCY_RESPONSE_FRAME_DURATION_MS = 80

DOUBLING_BL = 0.7
DOUBLING_FF = 0.7
DOUBLING_FB = 0.0
DOUBLING_DELAY_MS = 100.0
DOUBLING_DEPTH_MS = 100.0
DOUBLING_NOISE_CUTOFF_HZ = 1.0

MODULATION_DISPLAY_HZ = 1.0
LOWPASS_NOISE_DISPLAY_DEPTH = 0.40

WINDOW_LENGTH = 4096
HOP_SIZE = 256
VISIBLE_FREQ_MIN_HZ = 0.0
VISIBLE_FREQ_MAX_HZ = 5_000.0
DB_FLOOR = -40.0

TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18
FREQUENCY_MIN_HZ = 20.0
FREQUENCY_MAX_HZ = 20_000.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
DELAY_MAGNITUDE_LIMITS_DB = (-15.0, 5.0)
DELAY_MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]
INPUT_SPECTRUM_LIMITS_DB = (DB_FLOOR, 5.0)
INPUT_SPECTRUM_TICKS_DB = [-40.0, -30.0, -20.0, -10.0, 0.0]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.glob("*.png"):
        image_file.unlink()
    for image_file in BLOCK_DIR.glob("*.gif"):
        image_file.unlink()


def one_sided_amplitude_scaled_coefficients(coefficients: np.ndarray, window_length: int) -> np.ndarray:
    scaled = coefficients.copy()
    if window_length % 2 == 0:
        scaled[1:-1] *= 2.0
    else:
        scaled[1:] *= 2.0
    return scaled


def fade_edges(signal: np.ndarray) -> np.ndarray:
    fade_length = int(round(0.02 * FS_HZ))
    fade = np.sin(0.5 * np.pi * np.linspace(0.0, 1.0, fade_length)) ** 2
    result = signal.copy()
    result[:fade_length] *= fade
    result[-fade_length:] *= fade[::-1]
    return result


def build_bandlimited_sawtooth(*, apply_fade: bool = True) -> np.ndarray:
    time_s = np.arange(int(round(DURATION_S * FS_HZ))) / FS_HZ
    instantaneous_frequency_hz = np.full_like(time_s, CARRIER_HZ)
    phase = 2.0 * np.pi * np.cumsum(instantaneous_frequency_hz) / FS_HZ
    harmonic_count = int(np.floor((0.48 * FS_HZ) / CARRIER_HZ))

    signal = np.zeros_like(time_s)
    for harmonic in range(1, harmonic_count + 1):
        signal += ((-1.0) ** (harmonic + 1)) * np.sin(harmonic * phase) / harmonic
    signal *= 2.0 / np.pi
    signal /= max(float(np.max(np.abs(signal))), np.finfo(float).eps)
    if apply_fade:
        return fade_edges(signal)
    return signal


def variable_delay(signal: np.ndarray, delay_samples: np.ndarray) -> np.ndarray:
    sample_indices = np.arange(len(signal), dtype=float)
    read_positions = sample_indices - delay_samples
    return np.interp(read_positions, sample_indices, signal, left=0.0, right=0.0)


def sine_modulation(sample_count: int, modulation_frequency_hz: float) -> np.ndarray:
    time_s = np.arange(sample_count) / FS_HZ
    return 0.5 * (1.0 + np.sin(2.0 * np.pi * modulation_frequency_hz * time_s))


def lowpass_noise_modulation(sample_count: int, cutoff_hz: float, seed: int = 202609) -> np.ndarray:
    rng = np.random.default_rng(seed)
    noise_period = max(1, int(np.floor(FS_HZ / NOISE_CONTROL_RATE_HZ)))
    noise_alpha = 1.0 - np.exp(-2.0 * np.pi * cutoff_hz / FS_HZ)
    noise_state = 0.0
    noise_target = 0.0
    noise_count = 0
    modulation = np.zeros(sample_count)

    for sample_index in range(sample_count):
        if noise_count <= 0:
            noise_target = rng.uniform(-1.0, 1.0)
            noise_count = noise_period
        noise_count -= 1
        noise_state += noise_alpha * (noise_target - noise_state)
        modulation[sample_index] = 0.5 + 0.5 * np.clip(noise_state, -1.0, 1.0)

    return np.clip(modulation, 0.0, 1.0)


def read_fractional_history(history: np.ndarray, read_position: float, newest_index: int) -> float:
    if read_position < 0.0:
        return 0.0
    left_index = int(np.floor(read_position))
    fraction = read_position - left_index
    right_index = left_index + 1

    if left_index > newest_index:
        return 0.0
    left_value = history[left_index]
    if right_index > newest_index:
        right_value = left_value
    else:
        right_value = history[right_index]
    return float((1.0 - fraction) * left_value + fraction * right_value)


def apply_dafx_variable_delay(
    signal: np.ndarray,
    *,
    base_delay_ms: float,
    depth_ms: float,
    bl: float,
    ff: float,
    fb: float,
    modulation: np.ndarray,
) -> np.ndarray:
    base_delay_samples = base_delay_ms * 1e-3 * FS_HZ
    depth_samples = depth_ms * 1e-3 * FS_HZ
    delay_samples = base_delay_samples + depth_samples * modulation
    delay_samples = np.maximum(delay_samples, 0.0)

    feedback_delay_samples = max(base_delay_samples + 0.5 * depth_samples, 1.0)
    delay_line_input = np.zeros_like(signal)
    delayed_signal = np.zeros_like(signal)
    for sample_index, input_sample in enumerate(signal):
        feedback_sample = read_fractional_history(
            delay_line_input,
            sample_index - feedback_delay_samples,
            sample_index - 1,
        )
        delay_line_input[sample_index] = input_sample + fb * feedback_sample
        delayed_signal[sample_index] = read_fractional_history(
            delay_line_input,
            sample_index - delay_samples[sample_index],
            sample_index,
        )

    output = bl * signal + ff * delayed_signal
    output /= max(float(np.max(np.abs(output))), np.finfo(float).eps)
    return fade_edges(output)


def build_effect_signal(effect: str) -> np.ndarray:
    dry_signal = build_bandlimited_sawtooth()
    if effect == "static":
        return dry_signal
    if effect == "simple_chorus":
        modulation_1 = 2.0 * lowpass_noise_modulation(
            len(dry_signal),
            SIMPLE_CHORUS_NOISE_CUTOFF_HZ,
            seed=SIMPLE_CHORUS_M1_SEED,
        ) - 1.0
        modulation_2 = 2.0 * lowpass_noise_modulation(
            len(dry_signal),
            SIMPLE_CHORUS_NOISE_CUTOFF_HZ,
            seed=SIMPLE_CHORUS_M2_SEED,
        ) - 1.0
        delay_1_samples = (
            SIMPLE_CHORUS_M1_CENTER_MS + SIMPLE_CHORUS_M1_DEPTH_MS * modulation_1
        ) * 1e-3 * FS_HZ
        delay_2_samples = (
            SIMPLE_CHORUS_M2_CENTER_MS + SIMPLE_CHORUS_M2_DEPTH_MS * modulation_2
        ) * 1e-3 * FS_HZ
        delayed_1 = variable_delay(dry_signal, delay_1_samples)
        delayed_2 = variable_delay(dry_signal, delay_2_samples)
        output = SIMPLE_CHORUS_DRY_GAIN * dry_signal + SIMPLE_CHORUS_G1 * delayed_1 + SIMPLE_CHORUS_G2 * delayed_2
        output /= max(float(np.max(np.abs(output))), np.finfo(float).eps)
        return fade_edges(output)
    if effect == "fir_comb":
        return apply_dafx_variable_delay(
            dry_signal,
            base_delay_ms=FIR_COMB_DELAY_MS,
            depth_ms=FIR_COMB_DEPTH_MS,
            bl=FIR_COMB_BL,
            ff=FIR_COMB_FF,
            fb=FIR_COMB_FB,
            modulation=np.zeros(len(dry_signal)),
        )
    if effect == "iir_comb":
        return apply_dafx_variable_delay(
            dry_signal,
            base_delay_ms=IIR_COMB_DELAY_MS,
            depth_ms=IIR_COMB_DEPTH_MS,
            bl=IIR_COMB_BL,
            ff=IIR_COMB_FF,
            fb=IIR_COMB_FB,
            modulation=np.zeros(len(dry_signal)),
        )
    if effect == "vibrato":
        return apply_dafx_variable_delay(
            dry_signal,
            base_delay_ms=VIBRATO_DELAY_MS,
            depth_ms=VIBRATO_DEPTH_MS,
            bl=VIBRATO_BL,
            ff=VIBRATO_FF,
            fb=VIBRATO_FB,
            modulation=sine_modulation(len(dry_signal), VIBRATO_MOD_HZ),
        )
    if effect == "chorus":
        chorus_modulation = lowpass_noise_modulation(len(dry_signal), CHORUS_NOISE_CUTOFF_HZ)
        return apply_dafx_variable_delay(
            dry_signal,
            base_delay_ms=CHORUS_DELAY_MS,
            depth_ms=CHORUS_DEPTH_MS,
            bl=CHORUS_BL,
            ff=CHORUS_FF,
            fb=CHORUS_FB,
            modulation=chorus_modulation,
        )
    if effect == "flanger":
        return apply_dafx_variable_delay(
            dry_signal,
            base_delay_ms=FLANGER_DELAY_MS,
            depth_ms=FLANGER_DEPTH_MS,
            bl=FLANGER_BL,
            ff=FLANGER_FF,
            fb=FLANGER_FB,
            modulation=sine_modulation(len(dry_signal), FLANGER_MOD_HZ),
        )
    if effect == "doubling":
        doubling_modulation = lowpass_noise_modulation(len(dry_signal), DOUBLING_NOISE_CUTOFF_HZ)
        return apply_dafx_variable_delay(
            dry_signal,
            base_delay_ms=DOUBLING_DELAY_MS,
            depth_ms=DOUBLING_DEPTH_MS,
            bl=DOUBLING_BL,
            ff=DOUBLING_FF,
            fb=DOUBLING_FB,
            modulation=doubling_modulation,
        )
    raise ValueError(f"Unknown effect: {effect}")


def compute_stft_magnitude_db(signal: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    window = np.hanning(WINDOW_LENGTH)
    coherent_gain = np.mean(window)
    frame_starts = np.arange(0, len(signal) - WINDOW_LENGTH + 1, HOP_SIZE)
    frame_centers_s = (frame_starts + 0.5 * WINDOW_LENGTH) / FS_HZ
    frequency_hz = np.fft.rfftfreq(WINDOW_LENGTH, d=1.0 / FS_HZ)

    magnitudes = []
    for frame_start in frame_starts:
        block = signal[frame_start : frame_start + WINDOW_LENGTH]
        spectrum = np.fft.rfft(block * window) / (WINDOW_LENGTH * coherent_gain)
        spectrum = one_sided_amplitude_scaled_coefficients(spectrum, WINDOW_LENGTH)
        magnitudes.append(np.abs(spectrum))

    magnitude = np.vstack(magnitudes)
    magnitude /= max(float(np.max(magnitude)), np.finfo(float).eps)
    magnitude_db = 20.0 * np.log10(np.maximum(magnitude, 10.0 ** (DB_FLOOR / 20.0)))
    return frame_centers_s, frequency_hz, magnitude_db


def annotation_for_effect(effect: str) -> str:
    if effect == "static":
        return (
            rf"$f_0={CARRIER_HZ:.0f}\,\mathrm{{Hz}}$" "\n"
            rf"$\mathrm{{unprocessed\ input}}$"
        )
    if effect == "simple_chorus":
        return (
            rf"$l={SIMPLE_CHORUS_DRY_GAIN:.2f},\ g_1={SIMPLE_CHORUS_G1:.2f},\ g_2={SIMPLE_CHORUS_G2:.2f}$" "\n"
            rf"$M_1={SIMPLE_CHORUS_M1_CENTER_MS:.0f}\pm{SIMPLE_CHORUS_M1_DEPTH_MS:.0f}\,\mathrm{{ms}},\ "
            rf"M_2={SIMPLE_CHORUS_M2_CENTER_MS:.0f}\pm{SIMPLE_CHORUS_M2_DEPTH_MS:.0f}\,\mathrm{{ms}},\ "
            rf"MOD=\mathrm{{lowpass\,noise}}$"
        )
    if effect == "fir_comb":
        return (
            rf"$BL={FIR_COMB_BL:.1f},\ FF={FIR_COMB_FF:.1f},\ FB={FIR_COMB_FB:.1f}$" "\n"
            rf"$DELAY={FIR_COMB_DELAY_MS:.0f}\,\mathrm{{ms}},\ DEPTH={FIR_COMB_DEPTH_MS:.0f}\,\mathrm{{ms}},\ MOD=\mathrm{{none}}$"
        )
    if effect == "iir_comb":
        return (
            rf"$BL={IIR_COMB_BL:.1f},\ FF={IIR_COMB_FF:.1f},\ FB={IIR_COMB_FB:.1f}$" "\n"
            rf"$DELAY={IIR_COMB_DELAY_MS:.0f}\,\mathrm{{ms}},\ DEPTH={IIR_COMB_DEPTH_MS:.0f}\,\mathrm{{ms}},\ MOD=\mathrm{{none}}$"
        )
    if effect == "vibrato":
        return (
            rf"$BL={VIBRATO_BL:.1f},\ FF={VIBRATO_FF:.1f},\ FB={VIBRATO_FB:.1f}$" "\n"
            rf"$DELAY={VIBRATO_DELAY_MS:.0f}\,\mathrm{{ms}},\ DEPTH=0\ldots{VIBRATO_DEPTH_MS:.0f}\,\mathrm{{ms}},\ MOD={VIBRATO_MOD_HZ:.1f}\,\mathrm{{Hz}}\ \mathrm{{sine}}$"
        )
    if effect == "chorus":
        return (
            rf"$BL={CHORUS_BL:.1f},\ FF={CHORUS_FF:.1f},\ FB={CHORUS_FB:.1f}$" "\n"
            rf"$DELAY={CHORUS_DELAY_MS:.0f}\,\mathrm{{ms}},\ DEPTH={CHORUS_DEPTH_MS:.0f}\,\mathrm{{ms}},\ MOD=\mathrm{{lowpass\,noise}}$"
        )
    if effect == "flanger":
        return (
            rf"$BL={FLANGER_BL:.1f},\ FF={FLANGER_FF:.1f},\ FB={FLANGER_FB:.1f}$" "\n"
            rf"$DELAY={FLANGER_DELAY_MS:.0f}\,\mathrm{{ms}},\ DEPTH=0\ldots{FLANGER_DEPTH_MS:.0f}\,\mathrm{{ms}},\ MOD={FLANGER_MOD_HZ:.1f}\,\mathrm{{Hz}}\ \mathrm{{sine}}$"
        )
    if effect == "doubling":
        return (
            rf"$BL={DOUBLING_BL:.1f},\ FF={DOUBLING_FF:.1f},\ FB={DOUBLING_FB:.1f}$" "\n"
            rf"$DELAY={DOUBLING_DELAY_MS:.0f}\,\mathrm{{ms}},\ DEPTH={DOUBLING_DEPTH_MS:.0f}\,\mathrm{{ms}},\ MOD=\mathrm{{lowpass\,noise}}$"
        )
    raise ValueError(f"Unknown effect: {effect}")


def export_spectrogram(*, effect: str, filename: str, title: str) -> None:
    signal = build_effect_signal(effect)
    frame_centers_s, frequency_hz, magnitude_db = compute_stft_magnitude_db(signal)

    frequency_mask = (frequency_hz >= VISIBLE_FREQ_MIN_HZ) & (frequency_hz <= VISIBLE_FREQ_MAX_HZ)
    visible_frequency_hz = frequency_hz[frequency_mask]
    visible_db = magnitude_db[:, frequency_mask].T

    fig, ax = plt.subplots(figsize=SPECTROGRAM_FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.10, right=0.88, bottom=0.13, top=0.79)

    image = ax.imshow(
        visible_db,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="bilinear",
        extent=(
            float(frame_centers_s[0]),
            float(frame_centers_s[-1]),
            float(visible_frequency_hz[0]),
            float(visible_frequency_hz[-1]),
        ),
        vmin=DB_FLOOR,
        vmax=0.0,
    )

    fig.suptitle(title, fontsize=TITLE_SIZE, y=0.965)
    fig.text(
        0.50,
        0.875,
        annotation_for_effect(effect),
        ha="center",
        va="top",
        multialignment="center",
        fontsize=14,
        color=DARK_GREY,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "0.82", "alpha": 0.95},
    )
    ax.set_xlabel("Time in s", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(VISIBLE_FREQ_MIN_HZ, VISIBLE_FREQ_MAX_HZ)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 1.0, 1_000.0))
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    colorbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.02)
    colorbar.set_label(r"$|X[m,k]|$ in dB", fontsize=16)
    colorbar.set_ticks(np.arange(DB_FLOOR, 1.0, 10.0))
    colorbar.ax.tick_params(labelsize=14)

    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)


def export_input_time_domain() -> None:
    signal = build_bandlimited_sawtooth(apply_fade=False)
    visible_duration_s = 0.012
    visible_count = int(round(visible_duration_s * FS_HZ))
    time_ms = 1_000.0 * np.arange(visible_count) / FS_HZ

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)

    ax.plot(time_ms, signal[:visible_count], color=SIGNAL_BLACK, lw=3.0)
    ax.set_title("Sawtooth input signal", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlabel("Time in ms", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.set_xlim(0.0, visible_duration_s * 1_000.0)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xticks(np.arange(0.0, visible_duration_s * 1_000.0 + 0.01, 2.0))
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.grid(alpha=0.30, which="major")
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.savefig(BLOCK_DIR / "00a_sawtooth_input_time.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_input_spectrum() -> None:
    signal = build_bandlimited_sawtooth(apply_fade=False)
    spectrum = np.fft.rfft(signal) / len(signal)
    spectrum = one_sided_amplitude_scaled_coefficients(spectrum, len(signal))

    harmonic_frequency_hz = np.arange(CARRIER_HZ, FREQUENCY_MAX_HZ + 0.1, CARRIER_HZ)
    harmonic_indices = np.round(harmonic_frequency_hz * len(signal) / FS_HZ).astype(int)
    harmonic_magnitude = np.abs(spectrum[harmonic_indices])
    harmonic_magnitude /= max(float(np.max(harmonic_magnitude)), np.finfo(float).eps)
    harmonic_magnitude_db = 20.0 * np.log10(np.maximum(harmonic_magnitude, 10.0 ** (DB_FLOOR / 20.0)))

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    ax.vlines(harmonic_frequency_hz, INPUT_SPECTRUM_LIMITS_DB[0], harmonic_magnitude_db, color=SIGNAL_BLACK, lw=2.2)
    ax.scatter(harmonic_frequency_hz, harmonic_magnitude_db, color=SIGNAL_BLACK, s=22, zorder=3)
    ax.set_title("Sawtooth input spectrum", fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_ylim(*INPUT_SPECTRUM_LIMITS_DB)
    ax.set_yticks(INPUT_SPECTRUM_TICKS_DB)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|X(f)|$ in dB", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.savefig(BLOCK_DIR / "00b_sawtooth_input_spectrum.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def create_modulation_figure(title: str):
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlabel("Time in s", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$MOD[n]$", fontsize=LABEL_SIZE)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.grid(alpha=0.30, which="major")
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def export_modulation_source_series() -> None:
    sample_count = int(round(DURATION_S * FS_HZ))
    time_s = np.arange(sample_count) / FS_HZ
    sine = sine_modulation(sample_count, MODULATION_DISPLAY_HZ)
    lowpass_noise = lowpass_noise_modulation(sample_count, CHORUS_NOISE_CUTOFF_HZ, seed=202617)
    noise_centered = lowpass_noise - 0.5
    noise_centered /= max(float(np.max(np.abs(noise_centered))), np.finfo(float).eps)
    lowpass_noise_display = 0.5 + LOWPASS_NOISE_DISPLAY_DEPTH * noise_centered

    fig, ax = create_modulation_figure("Sine modulation signal")
    ax.plot(time_s, sine, color=MODULATION_VIOLET, lw=3.0, label="sine")
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="none", framealpha=0.92, fontsize=16)
    fig.savefig(BLOCK_DIR / "03a_modulation_sine.png", dpi=DPI, facecolor="white")
    plt.close(fig)

    fig, ax = create_modulation_figure("Sine and lowpass-noise modulation")
    ax.plot(time_s, sine, color=MODULATION_VIOLET, lw=3.0, label="sine")
    ax.plot(
        time_s,
        lowpass_noise_display,
        color=MODULATION_VIOLET,
        lw=3.0,
        ls="--",
        label="lowpass noise",
    )
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="none", framealpha=0.92, fontsize=16)
    fig.savefig(BLOCK_DIR / "03b_modulation_sine_lowpass_noise.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def audio_frequency_grid() -> np.ndarray:
    return np.geomspace(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ, 4096)


DELAY_FREQUENCY_EFFECTS = {
    "flanger": {
        "title": "Flanger magnitude response",
        "start_filename": "06_flanger_magnitude_response_start.png",
        "gif_filename": "07_flanger_magnitude_response_sweep.gif",
        "bl": FLANGER_BL,
        "ff": FLANGER_FF,
        "fb": FLANGER_FB,
        "fb_sign": 1.0,
        "delay_ms": FLANGER_DELAY_MS,
        "depth_ms": FLANGER_DEPTH_MS,
        "mod": "sine",
        "mod_label": rf"{FLANGER_MOD_HZ:.1f}\,\mathrm{{Hz}}\ \mathrm{{sine}}",
        "seed": 0,
    },
    "chorus": {
        "title": "Chorus magnitude response",
        "start_filename": "10_chorus_magnitude_response_start.png",
        "gif_filename": "11_chorus_magnitude_response_sweep.gif",
        "bl": CHORUS_BL,
        "ff": CHORUS_FF,
        "fb": CHORUS_FB,
        "fb_sign": 1.0,
        "delay_ms": CHORUS_DELAY_MS,
        "depth_ms": CHORUS_DEPTH_MS,
        "mod": "lowpass_noise",
        "mod_label": r"\mathrm{lowpass\,noise}",
        "seed": 17,
    },
    "doubling": {
        "title": "Doubler magnitude response",
        "start_filename": "12_doubler_magnitude_response_start.png",
        "gif_filename": "13_doubler_magnitude_response_sweep.gif",
        "bl": DOUBLING_BL,
        "ff": DOUBLING_FF,
        "fb": DOUBLING_FB,
        "fb_sign": 1.0,
        "delay_ms": DOUBLING_DELAY_MS,
        "depth_ms": DOUBLING_DEPTH_MS,
        "mod": "lowpass_noise",
        "mod_label": r"\mathrm{lowpass\,noise}",
        "seed": 29,
    },
}


def frame_phase(frame_index: int) -> float:
    return 2.0 * np.pi * frame_index / FREQUENCY_RESPONSE_FRAMES


def periodic_lowpass_noise_frame_modulation(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    phase = 2.0 * np.pi * np.arange(FREQUENCY_RESPONSE_FRAMES) / FREQUENCY_RESPONSE_FRAMES
    control = np.zeros(FREQUENCY_RESPONSE_FRAMES)
    for harmonic in range(1, 6):
        amplitude = rng.uniform(0.2, 1.0) / harmonic
        offset = rng.uniform(0.0, 2.0 * np.pi)
        control += amplitude * np.sin(harmonic * phase + offset)
    control -= control[0]
    control /= max(float(np.max(np.abs(control))), np.finfo(float).eps)
    return np.clip(0.5 + 0.5 * control, 0.0, 1.0)


def delay_modulation_value(effect_key: str, frame_index: int) -> float:
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    if effect["mod"] == "sine":
        return 0.5 + 0.5 * np.sin(frame_phase(frame_index))
    if effect["mod"] == "lowpass_noise":
        return float(periodic_lowpass_noise_frame_modulation(effect["seed"])[frame_index])
    raise ValueError(f"Unknown modulation type: {effect['mod']}")


def delay_ms_for_effect(effect_key: str, modulation: float) -> float:
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    return float(effect["delay_ms"] + effect["depth_ms"] * modulation)


def feedback_delay_ms_for_effect(effect_key: str) -> float:
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    center_delay_ms = effect["delay_ms"] + 0.5 * effect["depth_ms"]
    return max(float(center_delay_ms), 1000.0 / FS_HZ)


def delay_frequency_response(effect_key: str, frequency_hz: np.ndarray, delay_ms: float) -> np.ndarray:
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    delay_factor = np.exp(-1j * 2.0 * np.pi * frequency_hz * delay_ms * 1e-3)
    feedback_delay_factor = np.exp(-1j * 2.0 * np.pi * frequency_hz * feedback_delay_ms_for_effect(effect_key) * 1e-3)
    denominator = 1.0 - effect["fb_sign"] * effect["fb"] * feedback_delay_factor
    return effect["bl"] + effect["ff"] * delay_factor / denominator


def normalize_response(response: np.ndarray) -> np.ndarray:
    return response / max(float(np.max(np.abs(response))), np.finfo(float).eps)


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def create_delay_frequency_figure(title: str):
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_ylim(*DELAY_MAGNITUDE_LIMITS_DB)
    ax.set_yticks(DELAY_MAGNITUDE_TICKS_DB)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|H(f)|$ in dB", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def add_text_box(ax, text: str, color: str, y_position: float) -> None:
    ax.text(
        0.02,
        y_position,
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=14,
        color=color,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        zorder=20,
    )


def render_delay_frequency_frame(effect_key: str, frame_index: int):
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    frequency_hz = audio_frequency_grid()
    reference_delay_ms = delay_ms_for_effect(effect_key, 0.5)
    active_delay_ms = delay_ms_for_effect(effect_key, delay_modulation_value(effect_key, frame_index))
    reference_response = normalize_response(delay_frequency_response(effect_key, frequency_hz, reference_delay_ms))
    active_response = normalize_response(delay_frequency_response(effect_key, frequency_hz, active_delay_ms))

    fig, ax = create_delay_frequency_figure(effect["title"])
    ax.plot(frequency_hz, magnitude_db(reference_response), color=REFERENCE_GREY, lw=2.5, alpha=0.78, zorder=1)
    ax.plot(frequency_hz, magnitude_db(active_response), color=SYSTEM_GREEN, lw=3.2, zorder=3)
    add_text_box(ax, rf"$D={active_delay_ms:.2f}\,\mathrm{{ms}}$", SYSTEM_GREEN, 0.94)
    if effect_key == "flanger":
        parameter_text = rf"$BL/FF/FB={effect['bl']:.1f}/{effect['ff']:.1f}/{effect['fb']:.1f},\ MOD={effect['mod_label']}$"
    else:
        parameter_text = rf"$D={effect['delay_ms']:.0f}\ldots{effect['delay_ms'] + effect['depth_ms']:.0f}\,\mathrm{{ms}},\ BL/FF/FB={effect['bl']:.1f}/{effect['ff']:.1f}/{effect['fb']:.1f},\ MOD={effect['mod_label']}$"
    add_text_box(
        ax,
        parameter_text,
        DARK_GREY,
        0.84,
    )
    return fig


def figure_to_pil_image(fig, frame_index: int) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=fig.dpi, facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    image = Image.open(buffer).convert("RGB")
    image.load()
    marker_value = 255 - (frame_index % 32)
    image.putpixel((0, 0), (255, 255, marker_value))
    return image


def save_delay_frequency_still(effect_key: str) -> None:
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    fig = render_delay_frequency_frame(effect_key, 0)
    fig.savefig(BLOCK_DIR / effect["start_filename"], dpi=DPI, facecolor="white")
    plt.close(fig)


def save_delay_frequency_animation(effect_key: str) -> None:
    effect = DELAY_FREQUENCY_EFFECTS[effect_key]
    frames = []
    for frame_index in range(FREQUENCY_RESPONSE_FRAMES):
        fig = render_delay_frequency_frame(effect_key, frame_index)
        frames.append(figure_to_pil_image(fig, frame_index))

    frames[0].save(
        BLOCK_DIR / effect["gif_filename"],
        save_all=True,
        append_images=frames[1:],
        duration=[FREQUENCY_RESPONSE_FRAME_DURATION_MS] * len(frames),
        loop=0,
        optimize=False,
        disposal=2,
    )


def save_delay_frequency_response_assets(effect_key: str) -> None:
    save_delay_frequency_still(effect_key)
    save_delay_frequency_animation(effect_key)


def main() -> None:
    clear_output_dir()
    export_input_time_domain()
    export_input_spectrum()
    export_spectrogram(
        effect="static",
        filename="01_sawtooth_spectrogram_static.png",
        title="Sawtooth spectrogram",
    )
    export_spectrogram(
        effect="simple_chorus",
        filename="02_simple_two_voice_chorus_spectrogram.png",
        title="Sawtooth simple chorus spectrogram",
    )
    export_modulation_source_series()
    export_spectrogram(
        effect="vibrato",
        filename="04_sawtooth_vibrato_spectrogram.png",
        title="Sawtooth vibrato spectrogram",
    )
    export_spectrogram(
        effect="flanger",
        filename="05_sawtooth_flanger_spectrogram.png",
        title="Sawtooth flanger spectrogram",
    )
    save_delay_frequency_response_assets("flanger")
    export_spectrogram(
        effect="chorus",
        filename="08_sawtooth_chorus_spectrogram.png",
        title="Sawtooth chorus spectrogram",
    )
    export_spectrogram(
        effect="doubling",
        filename="09_sawtooth_doubler_spectrogram.png",
        title="Sawtooth doubler spectrogram",
    )
    save_delay_frequency_response_assets("chorus")
    save_delay_frequency_response_assets("doubling")


if __name__ == "__main__":
    main()
