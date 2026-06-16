from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "04_zeitvariante_filter"

DPI = 200
FIGSIZE = (11.5, 4.8)
SPECTROGRAM_FIGSIZE = (11.5, 5.45)
Z_DPI = 150
FIGSIZE_Z_PLANE_2D = (6.2, 5.6)
FIGSIZE_Z_PLANE_3D = (7.6, 5.7)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18
Z_TITLE_SIZE = 22
Z_LABEL_SIZE = 24
Z_TICK_SIZE = 18
SURFACE_TITLE_SIZE = 18
SURFACE_LABEL_SIZE = 18
SURFACE_TICK_SIZE = 14

SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.70"
DARK_GREY = "0.35"
BLACK = "0.10"
LIGHT_GREY = "0.84"
POLE_RED = "#b84a4a"

FS_HZ = 48_000.0
FREQUENCY_MIN_HZ = 20.0
FREQUENCY_MAX_HZ = 20_000.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
WAH_MAGNITUDE_LIMITS_DB = (-15.0, 5.0)
WAH_MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]
PHASER_MAGNITUDE_LIMITS_DB = (-15.0, 5.0)
PHASER_MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]
PHASER_BUILD_MAGNITUDE_LIMITS_DB = (-15.0, 5.0)
PHASER_BUILD_MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]

FRAME_COUNT = 88
FRAME_DURATION_MS = 80

WAH_REFERENCE_HZ = 500.0
WAH_DEPTH_OCT = 1.2
WAH_MIN_HZ = WAH_REFERENCE_HZ * 2.0 ** (-WAH_DEPTH_OCT)
WAH_MAX_HZ = WAH_REFERENCE_HZ * 2.0 ** WAH_DEPTH_OCT
WAH_RATE_HZ = 1.2
WAH_MIX = 0.0
WAH_MIX_HALF = 0.5
WAH_Q_LOW = 5.0
WAH_Q_HIGH = 15.0

PHASER_RANGE_MIN_HZ = 250.0
PHASER_REFERENCE_HZ = 500.0
PHASER_RANGE_MAX_HZ = 1_600.0
PHASER_STATIC_AP_A_HZ = 500.0
PHASER_STATIC_AP_B_HZ = 1_600.0
PHASER_STATIC_AP_Q = 1.0 / np.sqrt(2.0)
PHASER_STAGES = 4
PHASER_NO_FEEDBACK_GAIN = 0.0
PHASER_DEFAULT_FEEDBACK_GAIN = 0.5
PHASER_FEEDBACK_MIN_GAIN = 0.0
PHASER_FEEDBACK_MAX_GAIN = 0.90
PHASER_RATE_HZ = 0.6
PHASER_DRY_GAIN = 0.5
PHASER_DEFAULT_WET_GAIN = 0.5

SPECTROGRAM_DURATION_S = 4.0
SPECTROGRAM_CARRIER_HZ = 500.0
SPECTROGRAM_WINDOW_LENGTH = 4096
SPECTROGRAM_HOP_SIZE = 256
SPECTROGRAM_FREQ_MIN_HZ = 0.0
SPECTROGRAM_FREQ_MAX_HZ = 5_000.0
SPECTROGRAM_DB_FLOOR = -40.0

WAH_OUTPUT_FILES = [
    "01_wah_wah_frequency_start.png",
    "02_wah_wah_frequency_sweep.gif",
    "02b_wah_wah_high_q_frequency_start.png",
    "02c_wah_wah_high_q_frequency_sweep.gif",
    "02d_wah_wah_high_q_mix_start.png",
    "02e_wah_wah_high_q_mix_sweep.gif",
    "02f_wah_wah_high_q_dry_fade_sweep.gif",
    "02g_wah_wah_high_q_dry_fade_z_plane_2d_sweep.gif",
    "03_wah_wah_z_plane_2d.png",
    "04_wah_wah_z_plane_3d.png",
]

PHASER_OUTPUT_FILES = [
    "05_phaser_allpass_A_mag_phase.png",
    "06_phaser_allpass_B_mag_phase.png",
    "07_phaser_allpass_AB_cascade_mag_phase.png",
    "08_phaser_dry_sum_AB_mag_phase.png",
    "09_phaser_no_feedback_start.png",
    "10_phaser_no_feedback_sweep.gif",
    "11_phaser_no_feedback_z_plane_2d.png",
    "12_phaser_no_feedback_z_plane_3d.png",
    "13_phaser_feedback_start.png",
    "14_phaser_feedback_sweep.gif",
    "15_phaser_dry_wet_start.png",
    "16_phaser_dry_wet_sweep.gif",
]

SPECTROGRAM_OUTPUT_FILES = [
    "17_square_wah_wah_spectrogram.png",
    "18_square_phaser_spectrogram.png",
]

Z_LIMIT = 1.35
SURFACE_LIMIT = 1.35
SURFACE_MIN_DB = -25.0
SURFACE_MAX_DB = 25.0
SURFACE_GRID_SIZE = 92

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
class PhaserState:
    allpass_frequency_hz: float

    @property
    def reaper_d(self) -> float:
        return 2.0 * self.allpass_frequency_hz / FS_HZ

    @property
    def coefficient(self) -> float:
        g = np.tan(np.pi * self.allpass_frequency_hz / FS_HZ)
        return (1.0 - g) / (1.0 + g)


PHASER_REFERENCE = PhaserState(PHASER_REFERENCE_HZ)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.glob("*.png"):
        image_file.unlink()
    for gif_file in BLOCK_DIR.glob("*.gif"):
        gif_file.unlink()


def clear_output_files(filenames: list[str]) -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        output_file = BLOCK_DIR / filename
        if output_file.exists():
            output_file.unlink()


def frequency_grid() -> np.ndarray:
    return np.geomspace(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ, 4096)


def z_surface_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    real_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, SURFACE_GRID_SIZE)
    imag_axis = np.linspace(-SURFACE_LIMIT, SURFACE_LIMIT, SURFACE_GRID_SIZE)
    real_grid, imag_grid = np.meshgrid(real_axis, imag_axis)
    return real_grid, imag_grid, real_grid + 1j * imag_grid


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def normalize_peak(response: np.ndarray) -> np.ndarray:
    peak = np.max(np.abs(response))
    if peak <= np.finfo(float).eps:
        return response
    return response / peak


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


def build_bandlimited_square() -> np.ndarray:
    time_s = np.arange(int(round(SPECTROGRAM_DURATION_S * FS_HZ))) / FS_HZ
    phase = 2.0 * np.pi * np.cumsum(np.full_like(time_s, SPECTROGRAM_CARRIER_HZ)) / FS_HZ
    harmonic_count = int(np.floor((0.48 * FS_HZ) / SPECTROGRAM_CARRIER_HZ))

    signal = np.zeros_like(time_s)
    for harmonic in range(1, harmonic_count + 1, 2):
        signal += np.sin(harmonic * phase) / harmonic
    signal *= 4.0 / np.pi
    signal /= max(float(np.max(np.abs(signal))), np.finfo(float).eps)
    return fade_edges(signal)


def phase_wrapped(response: np.ndarray) -> np.ndarray:
    return np.angle(response)


def magnitude_db_clipped(response: np.ndarray) -> np.ndarray:
    return np.clip(20.0 * np.log10(np.maximum(np.abs(response), 1e-9)), SURFACE_MIN_DB, SURFACE_MAX_DB)


def reaper_gain(db_value: float) -> float:
    return 2.0 ** (db_value / 6.0)


def cyclic_modulation(frame_index: int, frame_count: int = FRAME_COUNT) -> float:
    phase = (frame_index % frame_count) / frame_count
    if phase < 0.25:
        return phase / 0.25
    if phase < 0.50:
        return 1.0 - (phase - 0.25) / 0.25
    if phase < 0.75:
        return -(phase - 0.50) / 0.25
    return -1.0 + (phase - 0.75) / 0.25


def dry_fade_control(frame_index: int, frame_count: int = FRAME_COUNT) -> tuple[float, float]:
    fade = frame_index / max(frame_count - 1, 1)
    return cyclic_modulation(frame_index, frame_count), WAH_MIX_HALF * fade


def frequency_from_reference(reference_hz: float, min_hz: float, max_hz: float, modulation: float) -> float:
    log_reference = np.log(reference_hz)
    if modulation >= 0.0:
        return float(np.exp(log_reference + modulation * (np.log(max_hz) - log_reference)))
    return float(np.exp(log_reference + modulation * (log_reference - np.log(min_hz))))


def wet_gain_from_reference(frame_index: int, frame_count: int = FRAME_COUNT) -> float:
    return PHASER_DEFAULT_WET_GAIN * (0.5 + 0.5 * np.cos(2.0 * np.pi * frame_index / frame_count))


def feedback_gain_from_modulation(frame_index: int, frame_count: int = FRAME_COUNT) -> float:
    phase = (frame_index % frame_count) / frame_count
    if phase < 0.5:
        return PHASER_FEEDBACK_MAX_GAIN * phase / 0.5
    return PHASER_FEEDBACK_MAX_GAIN * (1.0 - (phase - 0.5) / 0.5)


def feedback_output_compensation(feedback_gain: float) -> float:
    return max(0.0, 1.0 - abs(feedback_gain))


def effective_wet_gain(wet_gain: float, feedback_gain: float) -> float:
    return wet_gain * feedback_output_compensation(feedback_gain)


def wah_center_from_modulation(modulation: float) -> float:
    return frequency_from_reference(WAH_REFERENCE_HZ, WAH_MIN_HZ, WAH_MAX_HZ, modulation)


def phaser_frequency_from_modulation(modulation: float) -> float:
    return frequency_from_reference(PHASER_REFERENCE_HZ, PHASER_RANGE_MIN_HZ, PHASER_RANGE_MAX_HZ, modulation)


def design_wah_tpt_bandpass(center_hz: float, q: float, normalize_peak: bool = True) -> BiquadCoefficients:
    g = np.tan(np.pi * center_hz / FS_HZ)
    k = 1.0 / q
    a1_tpt = 1.0 / (1.0 + g * (g + k))
    a2_tpt = g * a1_tpt
    a3_tpt = g * a2_tpt
    b0 = a2_tpt
    b1 = 0.0
    b2 = -a2_tpt
    if normalize_peak:
        b0 /= q
        b2 /= q
    a1 = 2.0 * (a3_tpt - a1_tpt)
    a2 = (1.0 - 2.0 * a1_tpt) * (-1.0 + 2.0 * a3_tpt) + 4.0 * a2_tpt**2
    return BiquadCoefficients(b0, b1, b2, a1, a2)


def normalize_biquad(b0: float, b1: float, b2: float, a0: float, a1: float, a2: float) -> BiquadCoefficients:
    return BiquadCoefficients(b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def design_second_order_allpass(center_hz: float, q: float = PHASER_STATIC_AP_Q) -> BiquadCoefficients:
    omega0 = 2.0 * np.pi * center_hz / FS_HZ
    alpha = np.sin(omega0) / (2.0 * q)
    cos_omega0 = np.cos(omega0)
    b0 = 1.0 - alpha
    b1 = -2.0 * cos_omega0
    b2 = 1.0 + alpha
    a0 = 1.0 + alpha
    a1 = -2.0 * cos_omega0
    a2 = 1.0 - alpha
    return normalize_biquad(b0, b1, b2, a0, a1, a2)


def wah_response(frequency_hz: np.ndarray, center_hz: float, q: float = WAH_Q_LOW) -> np.ndarray:
    coefficients = design_wah_tpt_bandpass(center_hz, q)
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    z1 = np.exp(-1j * omega)
    z2 = np.exp(-2j * omega)
    numerator = coefficients.b0 + coefficients.b1 * z1 + coefficients.b2 * z2
    denominator = 1.0 + coefficients.a1 * z1 + coefficients.a2 * z2
    return numerator / denominator


def wah_mixed_response(frequency_hz: np.ndarray, center_hz: float, q: float, mix: float) -> np.ndarray:
    wet = wah_response(frequency_hz, center_hz, q)
    return (1.0 - mix) * wet + mix


def biquad_response(frequency_hz: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    z1 = np.exp(-1j * omega)
    z2 = np.exp(-2j * omega)
    numerator = coefficients.b0 + coefficients.b1 * z1 + coefficients.b2 * z2
    denominator = 1.0 + coefficients.a1 * z1 + coefficients.a2 * z2
    return numerator / denominator


def biquad_response_at_z(z_values: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    numerator = coefficients.b0 * z_values**2 + coefficients.b1 * z_values + coefficients.b2
    denominator = z_values**2 + coefficients.a1 * z_values + coefficients.a2
    return numerator / denominator


def static_allpass_a_response(frequency_hz: np.ndarray) -> np.ndarray:
    return biquad_response(frequency_hz, design_second_order_allpass(PHASER_STATIC_AP_A_HZ))


def static_allpass_b_response(frequency_hz: np.ndarray) -> np.ndarray:
    return biquad_response(frequency_hz, design_second_order_allpass(PHASER_STATIC_AP_B_HZ))


def static_allpass_cascade_response(frequency_hz: np.ndarray) -> np.ndarray:
    return static_allpass_a_response(frequency_hz) * static_allpass_b_response(frequency_hz)


def static_phaser_sum_response(frequency_hz: np.ndarray) -> np.ndarray:
    return PHASER_DRY_GAIN + PHASER_DEFAULT_WET_GAIN * static_allpass_cascade_response(frequency_hz)


def static_phaser_sum_response_at_z(z_values: np.ndarray) -> np.ndarray:
    coefficients_a = design_second_order_allpass(PHASER_STATIC_AP_A_HZ)
    coefficients_b = design_second_order_allpass(PHASER_STATIC_AP_B_HZ)
    return PHASER_DRY_GAIN + PHASER_DEFAULT_WET_GAIN * biquad_response_at_z(z_values, coefficients_a) * biquad_response_at_z(z_values, coefficients_b)


def wah_response_at_z(z_values: np.ndarray, center_hz: float, q: float = WAH_Q_LOW) -> np.ndarray:
    coefficients = design_wah_tpt_bandpass(center_hz, q)
    numerator = coefficients.b0 * z_values**2 + coefficients.b1 * z_values + coefficients.b2
    denominator = z_values**2 + coefficients.a1 * z_values + coefficients.a2
    return numerator / denominator


def wah_roots(center_hz: float, q: float = WAH_Q_LOW) -> tuple[np.ndarray, np.ndarray]:
    coefficients = design_wah_tpt_bandpass(center_hz, q)
    zeros = np.roots([coefficients.b0, coefficients.b1, coefficients.b2])
    poles = np.roots([1.0, coefficients.a1, coefficients.a2])
    return zeros, poles


def wah_mixed_roots(center_hz: float, q: float, mix: float) -> tuple[np.ndarray, np.ndarray]:
    coefficients = design_wah_tpt_bandpass(center_hz, q)
    wet_numerator = np.array([coefficients.b0, coefficients.b1, coefficients.b2])
    denominator = np.array([1.0, coefficients.a1, coefficients.a2])
    numerator = (1.0 - mix) * wet_numerator + mix * denominator
    zeros = np.roots(numerator)
    poles = np.roots(denominator)
    return zeros, poles


def allpass_stage_response_from_q(q_values: np.ndarray, coefficient: float) -> np.ndarray:
    return (coefficient - q_values) / (1.0 - coefficient * q_values)


def allpass_cascade_response(frequency_hz: np.ndarray, coefficient: float) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    q_values = np.exp(-1j * omega)
    return allpass_stage_response_from_q(q_values, coefficient) ** PHASER_STAGES


def phaser_response(
    frequency_hz: np.ndarray,
    coefficient: float,
    wet_gain: float = PHASER_DEFAULT_WET_GAIN,
    feedback_gain: float | None = None,
) -> np.ndarray:
    allpass_cascade = allpass_cascade_response(frequency_hz, coefficient)
    feedback = PHASER_DEFAULT_FEEDBACK_GAIN if feedback_gain is None else feedback_gain
    wet_path = feedback_output_compensation(feedback) * allpass_cascade / (1.0 - feedback * allpass_cascade)
    return PHASER_DRY_GAIN + wet_gain * wet_path


def phaser_response_at_z(
    z_values: np.ndarray,
    coefficient: float,
    wet_gain: float = PHASER_DEFAULT_WET_GAIN,
    feedback_gain: float | None = None,
) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        stage = (coefficient * z_values - 1.0) / (z_values - coefficient)
        cascade = stage**PHASER_STAGES
        feedback = PHASER_DEFAULT_FEEDBACK_GAIN if feedback_gain is None else feedback_gain
        wet_path = feedback_output_compensation(feedback) * cascade / (1.0 - feedback * cascade)
        return PHASER_DRY_GAIN + wet_gain * wet_path


def poly_power_ascending(coefficients: np.ndarray, power: int) -> np.ndarray:
    result = np.array([1.0])
    for _ in range(power):
        result = np.convolve(result, coefficients)
    return result


def roots_in_z_from_q_polynomial(coefficients_ascending_q: np.ndarray) -> np.ndarray:
    roots_q = np.roots(coefficients_ascending_q[::-1])
    finite_roots_q = roots_q[np.abs(roots_q) > 1e-10]
    return 1.0 / finite_roots_q


def biquad_polynomials_ascending_q(coefficients: BiquadCoefficients) -> tuple[np.ndarray, np.ndarray]:
    numerator = np.array([coefficients.b0, coefficients.b1, coefficients.b2])
    denominator = np.array([1.0, coefficients.a1, coefficients.a2])
    return numerator, denominator


def static_phaser_sum_roots() -> tuple[np.ndarray, np.ndarray]:
    coefficients_a = design_second_order_allpass(PHASER_STATIC_AP_A_HZ)
    coefficients_b = design_second_order_allpass(PHASER_STATIC_AP_B_HZ)
    numerator_a, denominator_a = biquad_polynomials_ascending_q(coefficients_a)
    numerator_b, denominator_b = biquad_polynomials_ascending_q(coefficients_b)
    numerator_cascade = np.convolve(numerator_a, numerator_b)
    denominator_cascade = np.convolve(denominator_a, denominator_b)
    numerator_sum = PHASER_DRY_GAIN * denominator_cascade + PHASER_DEFAULT_WET_GAIN * numerator_cascade
    zeros = roots_in_z_from_q_polynomial(numerator_sum)
    poles = roots_in_z_from_q_polynomial(denominator_cascade)
    return zeros, poles


def phaser_roots(
    coefficient: float,
    wet_gain: float = PHASER_DEFAULT_WET_GAIN,
    feedback_gain: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    numerator_stage = np.array([coefficient, -1.0])
    denominator_stage = np.array([1.0, -coefficient])
    numerator_cascade = poly_power_ascending(numerator_stage, PHASER_STAGES)
    denominator_cascade = poly_power_ascending(denominator_stage, PHASER_STAGES)
    feedback = PHASER_DEFAULT_FEEDBACK_GAIN if feedback_gain is None else feedback_gain
    denominator = denominator_cascade - feedback * numerator_cascade
    compensated_wet_gain = wet_gain * feedback_output_compensation(feedback)
    numerator = PHASER_DRY_GAIN * denominator_cascade + (compensated_wet_gain - PHASER_DRY_GAIN * feedback) * numerator_cascade
    zeros = roots_in_z_from_q_polynomial(numerator)
    poles = roots_in_z_from_q_polynomial(denominator)
    return zeros, poles


def normalize_audio_for_spectrogram(signal: np.ndarray) -> np.ndarray:
    normalized = signal / max(float(np.max(np.abs(signal))), np.finfo(float).eps)
    return fade_edges(normalized)


def process_wah_wah_signal(signal: np.ndarray) -> np.ndarray:
    ic1 = 0.0
    ic2 = 0.0
    output = np.zeros_like(signal)

    for sample_index, input_sample in enumerate(signal):
        time_s = sample_index / FS_HZ
        lfo = np.sin(2.0 * np.pi * WAH_RATE_HZ * time_s)
        center_hz = WAH_REFERENCE_HZ * 2.0 ** (WAH_DEPTH_OCT * lfo)
        center_hz = min(max(center_hz, 20.0), min(18_000.0, 0.45 * FS_HZ))

        g = np.tan(np.pi * center_hz / FS_HZ)
        k = 1.0 / WAH_Q_LOW
        a1 = 1.0 / (1.0 + g * (g + k))
        a2 = g * a1
        a3 = g * a2

        v3 = input_sample - ic2
        v1 = a1 * ic1 + a2 * v3
        v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2

        bandpass = v1 / WAH_Q_LOW
        output[sample_index] = (1.0 - WAH_MIX) * bandpass + WAH_MIX * input_sample

    return normalize_audio_for_spectrogram(output)


def process_phaser_signal(signal: np.ndarray) -> np.ndarray:
    allpass_x = np.zeros(PHASER_STAGES)
    allpass_y = np.zeros(PHASER_STAGES)
    feedback_memory = 0.0
    output = np.zeros_like(signal)
    wet_gain = effective_wet_gain(PHASER_DEFAULT_WET_GAIN, PHASER_DEFAULT_FEEDBACK_GAIN)

    for sample_index, input_sample in enumerate(signal):
        time_s = sample_index / FS_HZ
        lfo = np.sin(2.0 * np.pi * PHASER_RATE_HZ * time_s)
        allpass_frequency_hz = phaser_frequency_from_modulation(lfo)
        coefficient = PhaserState(allpass_frequency_hz).coefficient

        stage_input = input_sample + PHASER_DEFAULT_FEEDBACK_GAIN * feedback_memory
        for stage_index in range(PHASER_STAGES):
            stage_output = coefficient * (allpass_y[stage_index] + stage_input) - allpass_x[stage_index]
            allpass_x[stage_index] = stage_input
            allpass_y[stage_index] = stage_output
            stage_input = stage_output

        allpass_output = stage_input
        feedback_memory = allpass_output
        output[sample_index] = PHASER_DRY_GAIN * input_sample + wet_gain * allpass_output

    return normalize_audio_for_spectrogram(output)


def compute_spectrogram_magnitude_db(signal: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    window = np.hanning(SPECTROGRAM_WINDOW_LENGTH)
    coherent_gain = np.mean(window)
    frame_starts = np.arange(0, len(signal) - SPECTROGRAM_WINDOW_LENGTH + 1, SPECTROGRAM_HOP_SIZE)
    frame_centers_s = (frame_starts + 0.5 * SPECTROGRAM_WINDOW_LENGTH) / FS_HZ
    frequency_hz = np.fft.rfftfreq(SPECTROGRAM_WINDOW_LENGTH, d=1.0 / FS_HZ)

    magnitudes = []
    for frame_start in frame_starts:
        block = signal[frame_start : frame_start + SPECTROGRAM_WINDOW_LENGTH]
        spectrum = np.fft.rfft(block * window) / (SPECTROGRAM_WINDOW_LENGTH * coherent_gain)
        spectrum = one_sided_amplitude_scaled_coefficients(spectrum, SPECTROGRAM_WINDOW_LENGTH)
        magnitudes.append(np.abs(spectrum))

    magnitude = np.vstack(magnitudes)
    magnitude /= max(float(np.max(magnitude)), np.finfo(float).eps)
    magnitude_db = 20.0 * np.log10(np.maximum(magnitude, 10.0 ** (SPECTROGRAM_DB_FLOOR / 20.0)))
    return frame_centers_s, frequency_hz, magnitude_db


def export_filter_spectrogram(signal: np.ndarray, filename: str, title: str, annotation: str) -> None:
    frame_centers_s, frequency_hz, magnitude_db = compute_spectrogram_magnitude_db(signal)
    frequency_mask = (frequency_hz >= SPECTROGRAM_FREQ_MIN_HZ) & (frequency_hz <= SPECTROGRAM_FREQ_MAX_HZ)
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
        vmin=SPECTROGRAM_DB_FLOOR,
        vmax=0.0,
    )

    fig.suptitle(title, fontsize=TITLE_SIZE, y=0.965)
    fig.text(
        0.50,
        0.875,
        annotation,
        ha="center",
        va="top",
        multialignment="center",
        fontsize=14,
        color=DARK_GREY,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "0.82", "alpha": 0.95},
    )
    ax.set_xlabel("Time in s", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_xlim(0.0, SPECTROGRAM_DURATION_S)
    ax.set_ylim(SPECTROGRAM_FREQ_MIN_HZ, SPECTROGRAM_FREQ_MAX_HZ)
    ax.set_xticks(np.arange(0.0, SPECTROGRAM_DURATION_S + 0.01, 0.5))
    ax.set_yticks(np.arange(0.0, SPECTROGRAM_FREQ_MAX_HZ + 1.0, 1_000.0))
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    colorbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.02)
    colorbar.set_label(r"$|X[m,k]|$ in dB", fontsize=16)
    colorbar.set_ticks(np.arange(SPECTROGRAM_DB_FLOOR, 1.0, 10.0))
    colorbar.ax.tick_params(labelsize=14)

    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)


def style_frequency_axis(ax, title: str, magnitude_limits: tuple[float, float], magnitude_ticks: list[float]) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_ylim(*magnitude_limits)
    ax.set_yticks(magnitude_ticks)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|H(f)|$ in dB", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_text_box(ax, text: str, color: str, y_position: float) -> None:
    ax.text(
        0.02,
        y_position,
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
        color=color,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        zorder=20,
    )


def create_frequency_figure(title: str, magnitude_limits: tuple[float, float], magnitude_ticks: list[float]):
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    style_frequency_axis(ax, title, magnitude_limits, magnitude_ticks)
    return fig, ax


def create_mag_phase_figure(title: str):
    fig, ax_magnitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax_phase = ax_magnitude.twinx()

    style_frequency_axis(
        ax_magnitude,
        title,
        PHASER_BUILD_MAGNITUDE_LIMITS_DB,
        PHASER_BUILD_MAGNITUDE_TICKS_DB,
    )
    ax_phase.set_ylim(-np.pi, np.pi)
    ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi])
    ax_phase.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax_phase.set_ylabel("Phase in rad", fontsize=LABEL_SIZE)
    ax_phase.tick_params(labelsize=TICK_SIZE)
    ax_phase.spines["top"].set_visible(False)
    for phase_value in (-0.5 * np.pi, 0.5 * np.pi):
        ax_phase.axhline(
            phase_value,
            color=REFERENCE_GREY,
            lw=1.25,
            ls=":",
            alpha=0.55,
            zorder=0,
        )
    return fig, ax_magnitude, ax_phase


def render_wah_frequency_frame(
    modulation: float,
    q: float = WAH_Q_LOW,
    mix: float = WAH_MIX,
    reference_q: float | None = None,
    normalize_to_unity: bool = False,
    highlight_mix: bool = False,
):
    frequency_hz = frequency_grid()
    active_center_hz = wah_center_from_modulation(modulation)
    plotted_reference_q = q if reference_q is None else reference_q
    reference = wah_mixed_response(frequency_hz, WAH_REFERENCE_HZ, plotted_reference_q, mix)
    active = wah_mixed_response(frequency_hz, active_center_hz, q, mix)
    if normalize_to_unity:
        reference = normalize_peak(reference)
        active = normalize_peak(active)

    fig, ax = create_frequency_figure("Time-varying wah-wah", WAH_MAGNITUDE_LIMITS_DB, WAH_MAGNITUDE_TICKS_DB)
    ax.plot(frequency_hz, magnitude_db(reference), color=REFERENCE_GREY, lw=2.5, alpha=0.78, zorder=1)
    ax.plot(frequency_hz, magnitude_db(active), color=SYSTEM_GREEN, lw=3.2, zorder=3)
    active_label = rf"$f_c={active_center_hz:.0f}\,\mathrm{{Hz}},\ Q={q:.1f}$"
    context_label = rf"$f_\mathrm{{center}}={WAH_REFERENCE_HZ:.0f}\,\mathrm{{Hz}},\ \mathrm{{depth}}={WAH_DEPTH_OCT:.1f}\,\mathrm{{oct}},\ \mathrm{{rate}}={WAH_RATE_HZ:.1f}\,\mathrm{{Hz}}$"
    if highlight_mix:
        active_label = rf"$f_c={active_center_hz:.0f}\,\mathrm{{Hz}},\ Q={q:.1f},\ \mathrm{{mix}}={mix:.1f}$"
    else:
        context_label = context_label[:-1] + rf",\ \mathrm{{mix}}={mix:.1f}$"
    add_text_box(ax, active_label, SYSTEM_GREEN, 0.96)
    add_text_box(
        ax,
        context_label,
        DARK_GREY,
        0.84,
    )
    return fig


def render_wah_dry_fade_frame(control: tuple[float, float]):
    modulation, mix = control
    return render_wah_frequency_frame(
        modulation,
        WAH_Q_HIGH,
        mix,
        normalize_to_unity=True,
        highlight_mix=True,
    )


def render_phaser_frequency_frame(modulation: float):
    frequency_hz = frequency_grid()
    active_frequency_hz = phaser_frequency_from_modulation(modulation)
    active_state = PhaserState(active_frequency_hz)
    reference = phaser_response(frequency_hz, PHASER_REFERENCE.coefficient, feedback_gain=PHASER_NO_FEEDBACK_GAIN)
    active = phaser_response(frequency_hz, active_state.coefficient, feedback_gain=PHASER_NO_FEEDBACK_GAIN)

    fig, ax = create_frequency_figure("Time-varying four-stage phaser", PHASER_MAGNITUDE_LIMITS_DB, PHASER_MAGNITUDE_TICKS_DB)
    ax.plot(frequency_hz, magnitude_db(reference), color=REFERENCE_GREY, lw=2.5, alpha=0.78, zorder=1)
    ax.plot(frequency_hz, magnitude_db(active), color=SYSTEM_GREEN, lw=3.2, zorder=3)
    add_text_box(ax, rf"$f_\mathrm{{AP}}={active_frequency_hz:.0f}\,\mathrm{{Hz}}$", SYSTEM_GREEN, 0.96)
    add_text_box(
        ax,
        rf"$e={PHASER_DEFAULT_WET_GAIN:.2f},\ f_b=0.000$",
        DARK_GREY,
        0.84,
    )
    return fig


def phaser_reference_stage_responses() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    frequency_hz = frequency_grid()
    allpass_a = static_allpass_a_response(frequency_hz)
    allpass_b = static_allpass_b_response(frequency_hz)
    cascade = allpass_a * allpass_b
    dry_sum = PHASER_DRY_GAIN + PHASER_DEFAULT_WET_GAIN * cascade
    return allpass_a, allpass_b, cascade, dry_sum


def render_phaser_build_up_frame(response_index: int):
    frequency_hz = frequency_grid()
    responses = phaser_reference_stage_responses()
    titles = [
        "All-pass A filter response",
        "All-pass B filter response",
        "All-pass cascade response",
        "Dry signal plus all-pass cascade",
    ]
    legend_labels = [
        (r"Magnitude $A(z)$", r"Phase $A(z)$"),
        (r"Magnitude $B(z)$", r"Phase $B(z)$"),
        (r"Magnitude $A(z)B(z)$", r"Phase $A(z)B(z)$"),
        (r"Magnitude $H(z)$", r"Phase $H(z)$"),
    ]
    response = responses[response_index]

    fig, ax_magnitude, ax_phase = create_mag_phase_figure(titles[response_index])
    magnitude_line = ax_magnitude.plot(
        frequency_hz,
        magnitude_db(response),
        color=SYSTEM_GREEN,
        lw=3.0,
        zorder=3,
    )[0]
    phase_line = ax_phase.plot(
        frequency_hz,
        phase_wrapped(response),
        color=SYSTEM_GREEN,
        lw=3.0,
        ls="--",
        zorder=3,
    )[0]
    legend = ax_magnitude.legend(
        [magnitude_line, phase_line],
        legend_labels[response_index],
        loc="lower right",
        ncol=1,
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    return fig


def render_phaser_mix_frame(wet_gain: float):
    frequency_hz = frequency_grid()
    reference = phaser_response(
        frequency_hz,
        PHASER_REFERENCE.coefficient,
        PHASER_DEFAULT_WET_GAIN,
        PHASER_NO_FEEDBACK_GAIN,
    )
    active = phaser_response(
        frequency_hz,
        PHASER_REFERENCE.coefficient,
        wet_gain,
        PHASER_NO_FEEDBACK_GAIN,
    )

    fig, ax = create_frequency_figure("Phaser dry/wet mix", PHASER_MAGNITUDE_LIMITS_DB, PHASER_MAGNITUDE_TICKS_DB)
    ax.plot(frequency_hz, magnitude_db(reference), color=REFERENCE_GREY, lw=2.5, alpha=0.78, zorder=1)
    ax.plot(frequency_hz, magnitude_db(active), color=SYSTEM_GREEN, lw=3.2, zorder=3)
    add_text_box(ax, rf"$e={wet_gain:.2f}$", SYSTEM_GREEN, 0.96)
    add_text_box(
        ax,
        rf"$f_b=0.000,\ f_\mathrm{{AP}}={PHASER_REFERENCE_HZ:.0f}\,\mathrm{{Hz}}$",
        DARK_GREY,
        0.84,
    )
    return fig


def render_phaser_feedback_frame(feedback_gain: float):
    frequency_hz = frequency_grid()
    reference = phaser_response(
        frequency_hz,
        PHASER_REFERENCE.coefficient,
        PHASER_DEFAULT_WET_GAIN,
        PHASER_NO_FEEDBACK_GAIN,
    )
    active = phaser_response(
        frequency_hz,
        PHASER_REFERENCE.coefficient,
        PHASER_DEFAULT_WET_GAIN,
        feedback_gain,
    )

    fig, ax = create_frequency_figure("Phaser feedback", PHASER_MAGNITUDE_LIMITS_DB, PHASER_MAGNITUDE_TICKS_DB)
    ax.plot(frequency_hz, magnitude_db(reference), color=REFERENCE_GREY, lw=2.5, alpha=0.78, zorder=1)
    ax.plot(frequency_hz, magnitude_db(active), color=SYSTEM_GREEN, lw=3.2, zorder=3)
    add_text_box(
        ax,
        rf"$f_b={feedback_gain:.3f},\ e_\mathrm{{eff}}={effective_wet_gain(PHASER_DEFAULT_WET_GAIN, feedback_gain):.2f}$",
        SYSTEM_GREEN,
        0.96,
    )
    add_text_box(
        ax,
        rf"$e={PHASER_DEFAULT_WET_GAIN:.2f},\ f_\mathrm{{AP}}={PHASER_REFERENCE_HZ:.0f}\,\mathrm{{Hz}}$",
        DARK_GREY,
        0.84,
    )
    return fig


def setup_z_plane_2d(ax) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    ax.set_title("z-Plane", fontsize=Z_TITLE_SIZE, pad=10)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-Z_LIMIT, Z_LIMIT)
    ax.set_ylim(-Z_LIMIT, Z_LIMIT)
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel(r"Re$\{z\}$", fontsize=Z_LABEL_SIZE)
    ax.set_ylabel(r"Im$\{z\}$", fontsize=Z_LABEL_SIZE)
    ax.grid(alpha=0.20)
    ax.tick_params(labelsize=Z_TICK_SIZE)
    ax.axhline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax.axvline(0.0, color=BLACK, lw=1.1, zorder=0)
    ax.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_pole_zero_count_annotation(ax, zero_count: int, pole_count: int) -> None:
    ax.text(
        0.04,
        0.96,
        f"Zeros: {zero_count}\nPoles: {pole_count}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=15,
        color=DARK_GREY,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        zorder=20,
    )


def plot_poles_zeros_2d(ax, zeros: np.ndarray, poles: np.ndarray) -> None:
    ax.scatter(
        zeros.real,
        zeros.imag,
        s=10.5**2,
        marker="o",
        facecolors="white",
        edgecolors=SYSTEM_GREEN,
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


def render_z_plane_2d_frame(zeros: np.ndarray, poles: np.ndarray):
    fig, ax = plt.subplots(figsize=FIGSIZE_Z_PLANE_2D, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.16, right=0.96, bottom=0.15, top=0.86)
    setup_z_plane_2d(ax)
    add_pole_zero_count_annotation(ax, len(zeros), len(poles))
    plot_poles_zeros_2d(ax, zeros, poles)
    return fig


def render_wah_z_plane_2d_frame(modulation: float, q: float = WAH_Q_LOW):
    return render_z_plane_2d_frame(*wah_roots(wah_center_from_modulation(modulation), q))


def render_wah_high_q_z_plane_2d_frame(modulation: float):
    return render_z_plane_2d_frame(*wah_roots(wah_center_from_modulation(modulation), WAH_Q_HIGH))


def render_phaser_z_plane_2d_frame(modulation: float):
    return render_z_plane_2d_frame(*static_phaser_sum_roots())


def setup_surface_axis(ax_surface) -> None:
    ax_surface.set_title("z-Plane", fontsize=SURFACE_TITLE_SIZE, y=1.005, pad=0)
    ax_surface.set_xlabel(r"Re$\{z\}$", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_ylabel(r"Im$\{z\}$", fontsize=SURFACE_LABEL_SIZE, labelpad=8)
    ax_surface.set_zlabel(r"$|H(z)|$ in dB", fontsize=SURFACE_LABEL_SIZE, labelpad=-2)
    ax_surface.set_xlim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax_surface.set_ylim(-SURFACE_LIMIT, SURFACE_LIMIT)
    ax_surface.set_zlim(SURFACE_MIN_DB, SURFACE_MAX_DB)
    ax_surface.set_xticks([-1.0, 0.0, 1.0])
    ax_surface.set_yticks([-1.0, 0.0, 1.0])
    ax_surface.set_zticks([-25.0, 0.0, 25.0])
    ax_surface.tick_params(labelsize=SURFACE_TICK_SIZE)
    ax_surface.view_init(elev=25, azim=-58)
    for axis in (ax_surface.xaxis, ax_surface.yaxis, ax_surface.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
        axis._axinfo["grid"]["color"] = (0.82, 0.82, 0.82, 0.75)
    try:
        ax_surface.set_box_aspect((1.9, 1.9, 1.25), zoom=1.08)
    except (TypeError, AttributeError):
        ax_surface.set_box_aspect((1.9, 1.9, 1.25))


def plot_poles_zeros_3d(ax, zeros: np.ndarray, poles: np.ndarray) -> None:
    ax.scatter(
        zeros.real,
        zeros.imag,
        np.full(zeros.shape, SURFACE_MIN_DB),
        s=82,
        marker="o",
        facecolors="white",
        edgecolors=SYSTEM_GREEN,
        linewidth=2.2,
        depthshade=False,
        zorder=8,
    )
    ax.scatter(
        poles.real,
        poles.imag,
        np.full(poles.shape, SURFACE_MIN_DB),
        s=86,
        marker="x",
        color=POLE_RED,
        linewidth=2.3,
        depthshade=False,
        zorder=8,
    )


def render_z_plane_3d_frame(response_function, zeros: np.ndarray, poles: np.ndarray):
    theta = np.linspace(0.0, 2.0 * np.pi, 540)
    unit_circle = np.exp(1j * theta)
    unit_response = magnitude_db_clipped(response_function(unit_circle))
    real_grid, imag_grid, z_grid = z_surface_grid()
    response_db = magnitude_db_clipped(response_function(z_grid))
    response_db[~np.isfinite(response_db)] = np.nan
    for pole in poles:
        response_db[np.abs(z_grid - pole) < 0.035] = np.nan

    fig = plt.figure(figsize=FIGSIZE_Z_PLANE_3D, dpi=Z_DPI, facecolor="white")
    ax = fig.add_subplot(1, 1, 1, projection="3d", computed_zorder=False)
    fig.subplots_adjust(left=0.02, right=0.86, bottom=0.04, top=0.82)
    ax.plot(
        unit_circle.real,
        unit_circle.imag,
        np.full_like(theta, SURFACE_MIN_DB),
        color=LIGHT_GREY,
        lw=2.1,
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
    ax.plot(
        unit_circle.real,
        unit_circle.imag,
        unit_response,
        color=SYSTEM_GREEN,
        lw=3.0,
        alpha=0.96,
        zorder=5,
    )
    plot_poles_zeros_3d(ax, zeros, poles)
    setup_surface_axis(ax)
    return fig


def render_wah_z_plane_3d_frame(modulation: float, q: float = WAH_Q_LOW):
    center_hz = wah_center_from_modulation(modulation)
    zeros, poles = wah_roots(center_hz, q)
    return render_z_plane_3d_frame(lambda z: wah_response_at_z(z, center_hz, q), zeros, poles)


def render_phaser_z_plane_3d_frame(modulation: float):
    zeros, poles = static_phaser_sum_roots()
    return render_z_plane_3d_frame(
        static_phaser_sum_response_at_z,
        zeros,
        poles,
    )


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


def save_still(render_function, filename: str, control_value: float = 0.0) -> None:
    fig = render_function(control_value)
    fig.savefig(BLOCK_DIR / filename, dpi=fig.dpi, facecolor="white")
    plt.close(fig)


def save_tight_still(render_function, filename: str, control_value: float = 0.0) -> None:
    fig = render_function(control_value)
    fig.savefig(BLOCK_DIR / filename, dpi=fig.dpi, facecolor="white", bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def save_animation(render_function, filename: str, control_function) -> None:
    frames = []
    for frame_index in range(FRAME_COUNT):
        fig = render_function(control_function(frame_index))
        frames.append(figure_to_pil_image(fig, frame_index))

    frames[0].save(
        BLOCK_DIR / filename,
        save_all=True,
        append_images=frames[1:],
        duration=[FRAME_DURATION_MS] * len(frames),
        loop=0,
        optimize=False,
        disposal=2,
    )


def render_wah_assets(clear_existing: bool = True) -> None:
    if clear_existing:
        clear_output_files(WAH_OUTPUT_FILES)
    save_still(lambda modulation: render_wah_frequency_frame(modulation, WAH_Q_LOW), "01_wah_wah_frequency_start.png")
    save_animation(lambda modulation: render_wah_frequency_frame(modulation, WAH_Q_LOW), "02_wah_wah_frequency_sweep.gif", cyclic_modulation)
    save_still(
        lambda modulation: render_wah_frequency_frame(modulation, WAH_Q_HIGH, reference_q=WAH_Q_LOW),
        "02b_wah_wah_high_q_frequency_start.png",
    )
    save_animation(lambda modulation: render_wah_frequency_frame(modulation, WAH_Q_HIGH), "02c_wah_wah_high_q_frequency_sweep.gif", cyclic_modulation)
    save_still(lambda modulation: render_wah_frequency_frame(modulation, WAH_Q_HIGH, WAH_MIX_HALF), "02d_wah_wah_high_q_mix_start.png")
    save_animation(lambda modulation: render_wah_frequency_frame(modulation, WAH_Q_HIGH, WAH_MIX_HALF), "02e_wah_wah_high_q_mix_sweep.gif", cyclic_modulation)
    save_animation(render_wah_dry_fade_frame, "02f_wah_wah_high_q_dry_fade_sweep.gif", dry_fade_control)
    save_animation(
        render_wah_high_q_z_plane_2d_frame,
        "02g_wah_wah_high_q_dry_fade_z_plane_2d_sweep.gif",
        cyclic_modulation,
    )
    save_still(lambda modulation: render_wah_z_plane_2d_frame(modulation, WAH_Q_LOW), "03_wah_wah_z_plane_2d.png")
    save_still(lambda modulation: render_wah_z_plane_3d_frame(modulation, WAH_Q_LOW), "04_wah_wah_z_plane_3d.png")


def render_phaser_assets(clear_existing: bool = True) -> None:
    if clear_existing:
        clear_output_files(PHASER_OUTPUT_FILES)
    save_tight_still(lambda _: render_phaser_build_up_frame(0), "05_phaser_allpass_A_mag_phase.png")
    save_tight_still(lambda _: render_phaser_build_up_frame(1), "06_phaser_allpass_B_mag_phase.png")
    save_tight_still(lambda _: render_phaser_build_up_frame(2), "07_phaser_allpass_AB_cascade_mag_phase.png")
    save_tight_still(lambda _: render_phaser_build_up_frame(3), "08_phaser_dry_sum_AB_mag_phase.png")

    save_still(render_phaser_frequency_frame, "09_phaser_no_feedback_start.png")
    save_animation(render_phaser_frequency_frame, "10_phaser_no_feedback_sweep.gif", cyclic_modulation)
    save_still(render_phaser_z_plane_2d_frame, "11_phaser_no_feedback_z_plane_2d.png")
    save_still(render_phaser_z_plane_3d_frame, "12_phaser_no_feedback_z_plane_3d.png")

    save_still(lambda _: render_phaser_feedback_frame(PHASER_NO_FEEDBACK_GAIN), "13_phaser_feedback_start.png")
    save_animation(render_phaser_feedback_frame, "14_phaser_feedback_sweep.gif", feedback_gain_from_modulation)
    save_still(lambda _: render_phaser_mix_frame(PHASER_DEFAULT_WET_GAIN), "15_phaser_dry_wet_start.png")
    save_animation(render_phaser_mix_frame, "16_phaser_dry_wet_sweep.gif", wet_gain_from_reference)


def render_spectrogram_assets(clear_existing: bool = True) -> None:
    if clear_existing:
        clear_output_files(SPECTROGRAM_OUTPUT_FILES)

    input_signal = build_bandlimited_square()
    export_filter_spectrogram(
        process_wah_wah_signal(input_signal),
        "17_square_wah_wah_spectrogram.png",
        "Square wave wah-wah spectrogram",
        rf"$f_0={SPECTROGRAM_CARRIER_HZ:.0f}\,\mathrm{{Hz}},\ f_c={WAH_REFERENCE_HZ:.0f}\,\mathrm{{Hz}},\ Q={WAH_Q_LOW:.1f},\ \mathrm{{depth}}={WAH_DEPTH_OCT:.1f}\,\mathrm{{oct}},\ \mathrm{{rate}}={WAH_RATE_HZ:.1f}\,\mathrm{{Hz}}$",
    )
    export_filter_spectrogram(
        process_phaser_signal(input_signal),
        "18_square_phaser_spectrogram.png",
        "Square wave phaser spectrogram",
        rf"$f_0={SPECTROGRAM_CARRIER_HZ:.0f}\,\mathrm{{Hz}},\ f_\mathrm{{AP}}={PHASER_REFERENCE_HZ:.0f}\,\mathrm{{Hz}},\ e={PHASER_DEFAULT_WET_GAIN:.2f},\ f_b={PHASER_DEFAULT_FEEDBACK_GAIN:.2f}$",
    )


def main() -> None:
    clear_output_dir()
    render_wah_assets(clear_existing=False)
    render_phaser_assets(clear_existing=False)
    render_spectrogram_assets(clear_existing=False)


if __name__ == "__main__":
    main()
