from pathlib import Path
import wave

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LECTURE_DIR.parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "01_demodulators_envelope_followers"
    / "01a_detector_types"
)
AVERAGER_OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "01_demodulators_envelope_followers"
    / "01b_averager_smoothing"
)
CONTROL_OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "01_demodulators_envelope_followers"
    / "01c_envelope_follower_control"
)
ATTACK_RELEASE_BUILD_OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "01_demodulators_envelope_followers"
    / "01d_attack_release_build"
)
AUDIO_FILE = PROJECT_DIR / "audio_samples" / "nachhallfrei" / "instrumente" / "Bonobo_Kerala.wav"

DPI = 200
FIGSIZE = (12.0, 4.4)
PLOT_LEFT = 0.125
PLOT_RIGHT = 0.985
PLOT_BOTTOM = 0.215
PLOT_TOP = 0.845

SIGNAL_BLACK = "0.10"
MODULATION_VIOLET = "#7b4ab8"
VIOLET_SCALE_COLORS = ["#cdb8ee", "#a77bd8", "#7b4ab8", "#4a267d"]
REFERENCE_GREY = "0.80"
GRID_GREY = "0.75"
ZERO_GREY = "0.55"

TITLE_SIZE = 24
LABEL_SIZE = 19
TICK_SIZE = 16

SINE_SAMPLE_RATE_HZ = 2_000.0
SINE_DURATION_S = 0.08
SINE_FREQUENCY_HZ = 50.0
AUDIO_DURATION_S = 2.0
AUDIO_ZOOM_START_S = 0.75
AUDIO_ZOOM_END_S = 0.80
AVERAGER_TAU_MS = 5.0
BLOCK_5B_START_S = 15.5
BLOCK_5B_END_S = 18.5
LONG_RELEASE_TAU_MS = 100.0
COMPRESSOR_ATTACK_MS = 5.0
COMPRESSOR_RELEASE_MS = 100.0
RMS_METER_ATTACK_MS = 300.0
RMS_METER_RELEASE_MS = 1000.0
ANALYTIC_ATTACK_TIMES_MS = [5.0, 20.0, 50.0, 100.0]
ANALYTIC_RELEASE_TIMES_MS = [5.0, 20.0, 100.0, 300.0]
ATTACK_RELEASE_BUILD_TIMES_MS = [5.0, 20.0, 100.0]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def decode_wav_mono(raw: bytes, channels: int, sample_width: int) -> np.ndarray:
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
    return data / peak


def read_wav_mono(path: Path, duration_s: float) -> tuple[float, np.ndarray]:
    with wave.open(str(path), "rb") as handle:
        sample_rate_hz = float(handle.getframerate())
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        frames_to_read = min(handle.getnframes(), int(round(duration_s * sample_rate_hz)))
        raw = handle.readframes(frames_to_read)

    return sample_rate_hz, decode_wav_mono(raw, channels, sample_width)


def read_wav_mono_segment(path: Path, start_s: float, end_s: float) -> tuple[float, np.ndarray]:
    with wave.open(str(path), "rb") as handle:
        sample_rate_hz = float(handle.getframerate())
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        start_frame = int(round(start_s * sample_rate_hz))
        end_frame = min(handle.getnframes(), int(round(end_s * sample_rate_hz)))
        if start_frame >= end_frame:
            raise ValueError(f"Invalid WAV segment: {start_s:.3f}-{end_s:.3f} s")
        handle.setpos(start_frame)
        raw = handle.readframes(end_frame - start_frame)

    return sample_rate_hz, decode_wav_mono(raw, channels, sample_width)


def hilbert_transform_fft(signal: np.ndarray) -> np.ndarray:
    spectrum = np.fft.fft(signal)
    weights = np.zeros(len(signal))
    weights[0] = 1.0
    if len(signal) % 2 == 0:
        weights[1 : len(signal) // 2] = 2.0
        weights[len(signal) // 2] = 1.0
    else:
        weights[1 : (len(signal) + 1) // 2] = 2.0
    analytic = np.fft.ifft(spectrum * weights)
    return np.imag(analytic)


def binned_minmax(time: np.ndarray, signal: np.ndarray, target_bins: int = 1600) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if len(signal) <= target_bins:
        return time, signal, signal

    edges = np.linspace(0, len(signal), target_bins + 1, dtype=int)
    centers = np.empty(target_bins)
    lower = np.empty(target_bins)
    upper = np.empty(target_bins)
    for index in range(target_bins):
        start = edges[index]
        stop = max(edges[index + 1], start + 1)
        segment = signal[start:stop]
        centers[index] = 0.5 * (time[start] + time[stop - 1])
        lower[index] = float(np.min(segment))
        upper[index] = float(np.max(segment))
    return centers, lower, upper


def plot_signal(
    ax: plt.Axes,
    time: np.ndarray,
    signal: np.ndarray,
    *,
    color: str,
    lw: float,
    alpha: float,
    zorder: int,
    centerline: bool = True,
) -> None:
    if len(signal) > 5000:
        centers, lower, upper = binned_minmax(time, signal)
        fill_alpha = min(0.38, alpha * 0.45)
        ax.fill_between(centers, lower, upper, color=color, alpha=fill_alpha, linewidth=0.0, zorder=zorder)
        if centerline:
            center = 0.5 * (lower + upper)
            ax.plot(centers, center, color=color, lw=lw, alpha=alpha, zorder=zorder + 0.1)
    else:
        ax.plot(time, signal, color=color, lw=lw, alpha=alpha, zorder=zorder)


def one_pole_averager(detector_output: np.ndarray, sample_rate_hz: float, tau_ms: float) -> np.ndarray:
    coefficient = np.exp(-1.0 / (sample_rate_hz * tau_ms * 1e-3))
    averaged = np.empty_like(detector_output)
    state = 0.0
    for index, value in enumerate(detector_output):
        state = (1.0 - coefficient) * value + coefficient * state
        averaged[index] = state
    return averaged


def attack_release_averager(
    detector_output: np.ndarray,
    sample_rate_hz: float,
    attack_ms: float,
    release_ms: float,
) -> np.ndarray:
    attack_coefficient = np.exp(-1.0 / (sample_rate_hz * attack_ms * 1e-3))
    release_coefficient = np.exp(-1.0 / (sample_rate_hz * release_ms * 1e-3))
    averaged = np.empty_like(detector_output)
    state = 0.0
    for index, value in enumerate(detector_output):
        coefficient = attack_coefficient if state < value else release_coefficient
        state = (1.0 - coefficient) * value + coefficient * state
        averaged[index] = state
    return averaged


def scale_averager_output(detector_name: str, averaged_signal: np.ndarray) -> np.ndarray:
    nonnegative = np.maximum(averaged_signal, 0.0)
    if detector_name == "half_wave":
        return np.pi * nonnegative
    if detector_name == "full_wave":
        return 0.5 * np.pi * nonnegative
    if detector_name == "squarer":
        return np.sqrt(2.0 * nonnegative)
    if detector_name == "instantaneous":
        return np.sqrt(nonnegative)
    raise ValueError(f"Unknown detector name: {detector_name}")


def setup_time_axis(
    ax: plt.Axes,
    *,
    show_xlabel: bool,
    x_limit: tuple[float, float],
    x_label: str,
) -> None:
    ax.set_xlim(*x_limit)
    ax.set_ylim(-1.2, 1.2)
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=ZERO_GREY, lw=0.9)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    if show_xlabel:
        ax.set_xlabel(x_label, fontsize=LABEL_SIZE)
    else:
        ax.set_xticklabels([])


def save_input_plot(
    time: np.ndarray,
    input_signal: np.ndarray,
    *,
    title: str,
    x_label: str,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, input_signal, color=SIGNAL_BLACK, lw=2.6, alpha=1.0, zorder=2)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    setup_time_axis(ax, show_xlabel=True, x_limit=x_limit, x_label=x_label)
    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_averager_input_plot(
    time: np.ndarray,
    input_signal: np.ndarray,
    *,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, input_signal, color=SIGNAL_BLACK, lw=2.5, alpha=1.0, zorder=2)
    ax.set_title("Input audio signal", fontsize=TITLE_SIZE, pad=14)
    setup_time_axis(
        ax,
        show_xlabel=True,
        x_limit=x_limit,
        x_label="Time (s)",
    )
    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = AVERAGER_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_averager_detector_plot(
    time: np.ndarray,
    input_signal: np.ndarray,
    detector_signal: np.ndarray,
    *,
    title: str,
    formula: str,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, input_signal, color=REFERENCE_GREY, lw=1.7, alpha=0.66, zorder=1, centerline=False)
    plot_signal(ax, time, detector_signal, color=MODULATION_VIOLET, lw=2.4, alpha=0.95, zorder=2)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.text(
        0.015,
        0.78,
        formula,
        transform=ax.transAxes,
        fontsize=16,
        color=MODULATION_VIOLET,
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
    )
    setup_time_axis(
        ax,
        show_xlabel=True,
        x_limit=x_limit,
        x_label="Time (s)",
    )
    ax.set_ylim(-0.1, 1.4)
    ax.set_yticks([0.0, 0.5, 1.0])
    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = AVERAGER_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_detector_output_plot(
    time: np.ndarray,
    input_signal: np.ndarray,
    output_signal: np.ndarray,
    *,
    title: str,
    formula: str,
    x_label: str,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, input_signal, color=REFERENCE_GREY, lw=2.2, alpha=0.78, zorder=1)
    plot_signal(ax, time, output_signal, color=MODULATION_VIOLET, lw=2.8, alpha=0.92, zorder=2)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.text(
        0.015,
        0.08,
        formula,
        transform=ax.transAxes,
        fontsize=17,
        color=MODULATION_VIOLET,
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
    )
    setup_time_axis(ax, show_xlabel=True, x_limit=x_limit, x_label=x_label)

    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_scaled_averager_plot(
    time: np.ndarray,
    detector_signal: np.ndarray,
    scaled_signal: np.ndarray,
    *,
    title: str,
    tau_ms: float,
    scaler_formula: str,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, detector_signal, color=REFERENCE_GREY, lw=1.7, alpha=0.72, zorder=1, centerline=False)
    plot_signal(ax, time, scaled_signal, color=VIOLET_SCALE_COLORS[0], lw=2.8, alpha=0.98, zorder=2)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.text(
        0.015,
        0.72,
        scaler_formula + "\n" + rf"$\tau={tau_ms:.0f}\,\mathrm{{ms}}$",
        transform=ax.transAxes,
        fontsize=16,
        color=VIOLET_SCALE_COLORS[0],
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
    )
    setup_time_axis(
        ax,
        show_xlabel=True,
        x_limit=x_limit,
        x_label="Time (s)",
    )
    ax.set_ylim(-0.1, 1.4)
    ax.set_yticks([0.0, 0.5, 1.0])

    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = AVERAGER_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_scaled_comparison_plot(
    time: np.ndarray,
    scaled_signals: dict[str, np.ndarray],
    *,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    cases = [
        ("Half-wave", scaled_signals["half_wave"], VIOLET_SCALE_COLORS[0]),
        ("Full-wave", scaled_signals["full_wave"], VIOLET_SCALE_COLORS[1]),
        ("Squarer", scaled_signals["squarer"], VIOLET_SCALE_COLORS[2]),
        ("Instantaneous", scaled_signals["instantaneous"], VIOLET_SCALE_COLORS[3]),
    ]
    for label, signal, color in cases:
        plot_signal(ax, time, signal, color=color, lw=2.7, alpha=0.98, zorder=2)

    ax.set_title("Envelope follower outputs", fontsize=TITLE_SIZE, pad=14)
    setup_time_axis(
        ax,
        show_xlabel=True,
        x_limit=x_limit,
        x_label="Time (s)",
    )
    ax.set_ylim(-0.1, 1.4)
    ax.set_yticks([0.0, 0.5, 1.0])
    legend = ax.legend(
        [Line2D([0], [0], color=color, lw=3.4, alpha=0.98) for _label, _signal, color in cases],
        [case[0] for case in cases],
        loc="upper left",
        frameon=True,
        fontsize=15,
        borderpad=0.45,
        labelspacing=0.35,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.88)

    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = AVERAGER_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_tau_series_plot(
    time: np.ndarray,
    detector_label: str,
    detector_signal: np.ndarray,
    *,
    visible_scaled_by_tau: list[tuple[float, np.ndarray]],
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, detector_signal, color=REFERENCE_GREY, lw=1.7, alpha=0.72, zorder=1, centerline=False)
    legend_handles = [Line2D([0], [0], color=REFERENCE_GREY, lw=3.4, alpha=0.62)]
    labels = [f"{detector_label} detector"]
    for index, (tau_ms, scaled_signal) in enumerate(visible_scaled_by_tau):
        color = VIOLET_SCALE_COLORS[index]
        plot_signal(
            ax,
            time,
            scaled_signal,
            color=color,
            lw=2.7 + 0.15 * index,
            alpha=0.98,
            zorder=2 + index,
        )
        legend_handles.append(Line2D([0], [0], color=color, lw=3.4, alpha=0.98))
        labels.append(f"tau = {tau_ms:.0f} ms")
    if len(visible_scaled_by_tau) == 1:
        title = f"{detector_label}: time constant"
    else:
        title = f"{detector_label}: time constant build-up"

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    setup_time_axis(ax, show_xlabel=True, x_limit=x_limit, x_label="Time (s)")
    ax.set_ylim(-0.1, 1.4)
    ax.set_yticks([0.0, 0.5, 1.0])
    legend = ax.legend(
        legend_handles,
        labels,
        loc="upper left",
        frameon=True,
        fontsize=14,
        borderpad=0.45,
        labelspacing=0.35,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.88)

    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = AVERAGER_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_attack_release_application_plot(
    time: np.ndarray,
    detector_label: str,
    input_signal: np.ndarray,
    attack_release_signal: np.ndarray,
    *,
    title: str,
    attack_ms: float,
    release_ms: float,
    x_limit: tuple[float, float],
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_signal(ax, time, input_signal, color=REFERENCE_GREY, lw=1.7, alpha=0.72, zorder=1, centerline=False)
    plot_signal(ax, time, attack_release_signal, color=VIOLET_SCALE_COLORS[3], lw=3.0, alpha=1.0, zorder=2)

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    setup_time_axis(ax, show_xlabel=True, x_limit=x_limit, x_label="Time (s)")
    ax.set_ylim(-0.1, 1.4)
    ax.set_yticks([0.0, 0.5, 1.0])
    legend = ax.legend(
        [
            Line2D([0], [0], color=REFERENCE_GREY, lw=3.4, alpha=0.62),
            Line2D([0], [0], color=VIOLET_SCALE_COLORS[3], lw=3.4, alpha=1.0),
        ],
        [
            "Audio input",
            f"attack = {attack_ms:.0f} ms, release = {release_ms:.0f} ms",
        ],
        loc="upper left",
        frameon=True,
        fontsize=14,
        borderpad=0.45,
        labelspacing=0.35,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.88)

    fig.subplots_adjust(left=PLOT_LEFT, right=PLOT_RIGHT, bottom=PLOT_BOTTOM, top=PLOT_TOP)
    path = CONTROL_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_analytic_attack_release_plot(filename: str) -> Path:
    time_ms = np.linspace(-100.0, 1000.0, 3300)
    pulse_on_ms = 0.0
    pulse_off_ms = 300.0
    rectangular = ((time_ms >= pulse_on_ms) & (time_ms <= pulse_off_ms)).astype(float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.fill_between(time_ms, 0.0, rectangular, color=REFERENCE_GREY, alpha=0.34, linewidth=0.0, zorder=1)
    ax.step(time_ms, rectangular, where="post", color=REFERENCE_GREY, lw=2.0, alpha=0.95, zorder=2)

    attack_mask = (time_ms >= pulse_on_ms) & (time_ms <= pulse_off_ms)
    release_mask = time_ms >= pulse_off_ms
    attack_time_ms = time_ms[attack_mask] - pulse_on_ms
    release_time_ms = time_ms[release_mask] - pulse_off_ms

    for tau_ms, color in zip(ANALYTIC_ATTACK_TIMES_MS, VIOLET_SCALE_COLORS):
        attack = 1.0 - np.exp(-attack_time_ms / tau_ms)
        ax.plot(
            time_ms[attack_mask],
            attack,
            color=color,
            lw=2.8,
            alpha=0.98,
            label=rf"attack $\tau_a={tau_ms:.0f}$ ms",
            zorder=3,
        )

    for tau_ms, attack_tau_ms, color in zip(ANALYTIC_RELEASE_TIMES_MS, ANALYTIC_ATTACK_TIMES_MS, VIOLET_SCALE_COLORS):
        value_at_release = 1.0 - np.exp(-(pulse_off_ms - pulse_on_ms) / attack_tau_ms)
        release = value_at_release * np.exp(-release_time_ms / tau_ms)
        ax.plot(
            time_ms[release_mask],
            release,
            color=color,
            lw=2.8,
            ls="--",
            alpha=0.98,
            label=rf"release $\tau_r={tau_ms:.0f}$ ms",
            zorder=3,
        )

    fig.suptitle("Attack and release time constants", fontsize=TITLE_SIZE, y=0.965)
    ax.set_xlim(-100.0, 1000.0)
    ax.set_xticks([-100.0, 0.0, 200.0, 400.0, 600.0, 800.0, 1000.0])
    ax.set_ylim(-0.08, 1.14)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=ZERO_GREY, lw=0.9)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.set_xlabel("Time (ms)", fontsize=LABEL_SIZE)
    ax.text(
        0.66,
        0.72,
        r"$y_a(t)=1-e^{-t/\tau_a}$" + "\n" + r"$y_r(t)=y_a(T)e^{-(t-T)/\tau_r}$",
        transform=ax.transAxes,
        fontsize=16,
        color=VIOLET_SCALE_COLORS[3],
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
    )

    attack_handles = [
        Line2D([0], [0], color=color, lw=2.8, alpha=0.98)
        for color in VIOLET_SCALE_COLORS
    ]
    release_handles = [
        Line2D([0], [0], color=color, lw=2.8, ls="--", alpha=0.98)
        for color in VIOLET_SCALE_COLORS
    ]
    attack_labels = [rf"$\tau_a={tau_ms:.0f}$ ms" for tau_ms in ANALYTIC_ATTACK_TIMES_MS]
    release_labels = [rf"$\tau_r={tau_ms:.0f}$ ms" for tau_ms in ANALYTIC_RELEASE_TIMES_MS]
    fig.text(0.17, 0.855, "Attack", fontsize=13, fontweight="bold", ha="left", va="center")
    fig.text(0.17, 0.795, "Release", fontsize=13, fontweight="bold", ha="left", va="center")
    fig.legend(
        attack_handles,
        attack_labels,
        loc="upper center",
        bbox_to_anchor=(0.56, 0.885),
        ncol=4,
        frameon=False,
        fontsize=12,
        handlelength=2.2,
        columnspacing=1.25,
    )
    fig.legend(
        release_handles,
        release_labels,
        loc="upper center",
        bbox_to_anchor=(0.56, 0.825),
        ncol=4,
        frameon=False,
        fontsize=12,
        handlelength=2.2,
        columnspacing=1.25,
    )

    fig.subplots_adjust(left=PLOT_LEFT, right=0.965, bottom=PLOT_BOTTOM, top=0.71)
    path = AVERAGER_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def rectangular_attack_release_response(
    time_ms: np.ndarray,
    *,
    pulse_on_ms: float,
    pulse_off_ms: float,
    tau_ms: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    attack_mask = (time_ms >= pulse_on_ms) & (time_ms <= pulse_off_ms)
    release_mask = time_ms > pulse_off_ms

    response = np.zeros_like(time_ms)
    attack_time_ms = time_ms[attack_mask] - pulse_on_ms
    response[attack_mask] = 1.0 - np.exp(-attack_time_ms / tau_ms)

    value_at_release = 1.0 - np.exp(-(pulse_off_ms - pulse_on_ms) / tau_ms)
    release_time_ms = time_ms[release_mask] - pulse_off_ms
    response[release_mask] = value_at_release * np.exp(-release_time_ms / tau_ms)
    return response, attack_mask, release_mask


def save_attack_release_build_plot(
    visible_taus_ms: list[float],
    *,
    filename: str,
) -> Path:
    time_ms = np.linspace(-100.0, 1000.0, 3300)
    pulse_on_ms = 0.0
    pulse_off_ms = 400.0
    rectangular = ((time_ms >= pulse_on_ms) & (time_ms <= pulse_off_ms)).astype(float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.fill_between(time_ms, 0.0, rectangular, color=REFERENCE_GREY, alpha=0.34, linewidth=0.0, zorder=1)
    ax.step(time_ms, rectangular, where="post", color=REFERENCE_GREY, lw=2.0, alpha=0.95, zorder=2)

    handles = []
    labels = []
    for tau_ms, color in zip(visible_taus_ms, VIOLET_SCALE_COLORS[: len(visible_taus_ms)]):
        response, attack_mask, release_mask = rectangular_attack_release_response(
            time_ms,
            pulse_on_ms=pulse_on_ms,
            pulse_off_ms=pulse_off_ms,
            tau_ms=tau_ms,
        )
        ax.plot(time_ms[attack_mask], response[attack_mask], color=color, lw=2.9, alpha=0.98, zorder=3)
        ax.plot(time_ms[release_mask], response[release_mask], color=color, lw=2.9, ls="--", alpha=0.98, zorder=3)
        handles.append(Line2D([0], [0], color=color, lw=2.9, alpha=0.98))
        labels.append(rf"$\tau={tau_ms:.0f}$ ms")

    fig.suptitle("Attack and release time constants", fontsize=TITLE_SIZE, y=0.965)
    ax.set_xlim(-100.0, 1000.0)
    ax.set_xticks([-100.0, 0.0, 200.0, 400.0, 600.0, 800.0, 1000.0])
    ax.set_ylim(-0.08, 1.14)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=ZERO_GREY, lw=0.9)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.set_xlabel("Time (ms)", fontsize=LABEL_SIZE)
    ax.text(
        0.64,
        0.72,
        r"$y_a(t)=1-e^{-t/\tau}$" + "\n" + r"$y_r(t)=y_a(T)e^{-(t-T)/\tau}$",
        transform=ax.transAxes,
        fontsize=16,
        color=VIOLET_SCALE_COLORS[3],
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
        zorder=10,
    )

    if handles:
        fig.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.55, 0.845),
            ncol=len(handles),
            frameon=False,
            fontsize=12,
            handlelength=2.2,
            columnspacing=1.25,
        )

    fig.subplots_adjust(left=PLOT_LEFT, right=0.965, bottom=PLOT_BOTTOM, top=0.76)
    path = ATTACK_RELEASE_BUILD_OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()
    AVERAGER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in AVERAGER_OUTPUT_DIR.glob("*.png"):
        image_file.unlink()
    CONTROL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in CONTROL_OUTPUT_DIR.glob("*.png"):
        image_file.unlink()
    ATTACK_RELEASE_BUILD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in ATTACK_RELEASE_BUILD_OUTPUT_DIR.glob("*.png"):
        image_file.unlink()

    time_s = np.arange(int(round(SINE_DURATION_S * SINE_SAMPLE_RATE_HZ))) / SINE_SAMPLE_RATE_HZ
    time_ms = 1000.0 * time_s
    x = np.sin(2.0 * np.pi * SINE_FREQUENCY_HZ * time_s)
    x_hilbert = -np.cos(2.0 * np.pi * SINE_FREQUENCY_HZ * time_s)

    detector_cases = [
        (
            "Half-wave rectifier",
            r"$d_h[n]=\max(0,x[n])$",
            np.maximum(0.0, x),
            "02_half_wave_rectifier_sine.png",
        ),
        (
            "Full-wave rectifier",
            r"$d_f[n]=|x[n]|$",
            np.abs(x),
            "03_full_wave_rectifier_sine.png",
        ),
        (
            "Squarer",
            r"$d_r[n]=x^2[n]$",
            x**2,
            "04_squarer_sine.png",
        ),
        (
            "Hilbert transform",
            r"$\hat{x}[n]=\mathcal{H}\{x[n]\}$",
            x_hilbert,
            "05_hilbert_transform_sine.png",
        ),
        (
            "Hilbert transform squared",
            r"$\hat{x}^2[n]$",
            x_hilbert**2,
            "06_hilbert_transform_squared_sine.png",
        ),
        (
            "Instantaneous envelope",
            r"$d_i^2[n]=x^2[n]+\hat{x}^2[n]$",
            x**2 + x_hilbert**2,
            "07_instantaneous_envelope_sine.png",
        ),
    ]

    paths = [
        save_input_plot(
            time_ms,
            x,
            title="Input sine",
            x_label="Time (ms)",
            x_limit=(0.0, SINE_DURATION_S * 1000.0),
            filename="01_input_sine.png",
        )
    ]
    paths.extend(
        save_detector_output_plot(
            time_ms,
            x,
            output,
            title=title,
            formula=formula,
            x_label="Time (ms)",
            x_limit=(0.0, SINE_DURATION_S * 1000.0),
            filename=filename,
        )
        for title, formula, output, filename in detector_cases
    )

    audio_sample_rate_hz, audio = read_wav_mono(AUDIO_FILE, AUDIO_DURATION_S)
    audio_time_s = np.arange(len(audio)) / audio_sample_rate_hz
    audio_hilbert = hilbert_transform_fft(audio)
    audio_detector_outputs = {
        "half_wave": np.maximum(0.0, audio),
        "full_wave": np.abs(audio),
        "squarer": audio**2,
        "instantaneous": audio**2 + audio_hilbert**2,
    }
    audio_detector_cases = [
        (
            "Audio half-wave rectifier",
            r"$d_h[n]=\max(0,x[n])$",
            audio_detector_outputs["half_wave"],
            "09_half_wave_rectifier_audio_2s.png",
        ),
        (
            "Audio full-wave rectifier",
            r"$d_f[n]=|x[n]|$",
            audio_detector_outputs["full_wave"],
            "10_full_wave_rectifier_audio_2s.png",
        ),
        (
            "Audio squarer",
            r"$d_r[n]=x^2[n]$",
            audio_detector_outputs["squarer"],
            "11_squarer_audio_2s.png",
        ),
        (
            "Audio instantaneous envelope",
            r"$d_i^2[n]=x^2[n]+\hat{x}^2[n]$",
            audio_detector_outputs["instantaneous"],
            "12_instantaneous_envelope_audio_2s.png",
        ),
    ]

    paths.append(
        save_input_plot(
            audio_time_s,
            audio,
            title="Audio input, first 2 s",
            x_label="Time (s)",
            x_limit=(0.0, AUDIO_DURATION_S),
            filename="08_input_audio_2s.png",
        )
    )
    paths.extend(
        save_detector_output_plot(
            audio_time_s,
            audio,
            output,
            title=title,
            formula=formula,
            x_label="Time (s)",
            x_limit=(0.0, AUDIO_DURATION_S),
            filename=filename,
        )
        for title, formula, output, filename in audio_detector_cases
    )

    zoom_mask = (audio_time_s >= AUDIO_ZOOM_START_S) & (audio_time_s <= AUDIO_ZOOM_END_S)
    zoom_time_s = audio_time_s[zoom_mask]
    zoom_audio = audio[zoom_mask]
    paths.append(
        save_input_plot(
            zoom_time_s,
            zoom_audio,
            title="Audio input, 0.75-0.80 s",
            x_label="Time (s)",
            x_limit=(AUDIO_ZOOM_START_S, AUDIO_ZOOM_END_S),
            filename="13_input_audio_zoom_075_080s.png",
        )
    )
    zoom_detector_cases = [
        (
            "Audio half-wave rectifier, zoom",
            r"$d_h[n]=\max(0,x[n])$",
            audio_detector_outputs["half_wave"][zoom_mask],
            "14_half_wave_rectifier_audio_zoom_075_080s.png",
        ),
        (
            "Audio full-wave rectifier, zoom",
            r"$d_f[n]=|x[n]|$",
            audio_detector_outputs["full_wave"][zoom_mask],
            "15_full_wave_rectifier_audio_zoom_075_080s.png",
        ),
        (
            "Audio squarer, zoom",
            r"$d_r[n]=x^2[n]$",
            audio_detector_outputs["squarer"][zoom_mask],
            "16_squarer_audio_zoom_075_080s.png",
        ),
        (
            "Audio instantaneous envelope, zoom",
            r"$d_i^2[n]=x^2[n]+\hat{x}^2[n]$",
            audio_detector_outputs["instantaneous"][zoom_mask],
            "19_instantaneous_envelope_audio_zoom_075_080s.png",
        ),
    ]
    paths.append(
        save_detector_output_plot(
            zoom_time_s,
            zoom_audio,
            audio_hilbert[zoom_mask],
            title="Audio Hilbert transform, zoom",
            formula=r"$\hat{x}[n]=\mathcal{H}\{x[n]\}$",
            x_label="Time (s)",
            x_limit=(AUDIO_ZOOM_START_S, AUDIO_ZOOM_END_S),
            filename="17_hilbert_transform_audio_zoom_075_080s.png",
        )
    )
    paths.append(
        save_detector_output_plot(
            zoom_time_s,
            zoom_audio,
            (audio_hilbert**2)[zoom_mask],
            title="Audio Hilbert transform squared, zoom",
            formula=r"$\hat{x}^2[n]$",
            x_label="Time (s)",
            x_limit=(AUDIO_ZOOM_START_S, AUDIO_ZOOM_END_S),
            filename="18_hilbert_transform_squared_audio_zoom_075_080s.png",
        )
    )
    paths.extend(
        save_detector_output_plot(
            zoom_time_s,
            zoom_audio,
            output,
            title=title,
            formula=formula,
            x_label="Time (s)",
            x_limit=(AUDIO_ZOOM_START_S, AUDIO_ZOOM_END_S),
            filename=filename,
        )
        for title, formula, output, filename in zoom_detector_cases
    )

    block5b_sample_rate_hz, block5b_audio = read_wav_mono_segment(AUDIO_FILE, BLOCK_5B_START_S, BLOCK_5B_END_S)
    block5b_time_s = BLOCK_5B_START_S + np.arange(len(block5b_audio)) / block5b_sample_rate_hz
    block5b_x_limit = (BLOCK_5B_START_S, BLOCK_5B_END_S)
    paths.append(
        save_averager_input_plot(
            block5b_time_s,
            block5b_audio,
            x_limit=block5b_x_limit,
            filename="00_input_audio_155_185s.png",
        )
    )
    block5b_hilbert = hilbert_transform_fft(block5b_audio)
    block5b_detector_outputs = {
        "half_wave": np.maximum(0.0, block5b_audio),
        "full_wave": np.abs(block5b_audio),
        "squarer": block5b_audio**2,
        "instantaneous": block5b_audio**2 + block5b_hilbert**2,
    }
    block5b_detector_cases = [
        (
            "Half-wave detector output",
            block5b_detector_outputs["half_wave"],
            r"$d_h[n]=\max(0,x[n])$",
            "00a_detector_half_wave_audio_155_185s.png",
        ),
        (
            "Full-wave detector output",
            block5b_detector_outputs["full_wave"],
            r"$d_f[n]=|x[n]|$",
            "00b_detector_full_wave_audio_155_185s.png",
        ),
        (
            "Squarer detector output",
            block5b_detector_outputs["squarer"],
            r"$d_r[n]=x^2[n]$",
            "00c_detector_squarer_audio_155_185s.png",
        ),
        (
            "Instantaneous envelope detector output",
            block5b_detector_outputs["instantaneous"],
            r"$d_i^2[n]=x^2[n]+\hat{x}^2[n]$",
            "00d_detector_instantaneous_audio_155_185s.png",
        ),
    ]
    paths.extend(
        save_averager_detector_plot(
            block5b_time_s,
            block5b_audio,
            detector,
            title=title,
            formula=formula,
            x_limit=block5b_x_limit,
            filename=filename,
        )
        for title, detector, formula, filename in block5b_detector_cases
    )
    tau_values_ms = [AVERAGER_TAU_MS, 20.0, LONG_RELEASE_TAU_MS]
    scaled_outputs_by_tau = {
        tau_ms: {
            name: scale_averager_output(
                name,
                one_pole_averager(detector, block5b_sample_rate_hz, tau_ms),
            )
            for name, detector in block5b_detector_outputs.items()
        }
        for tau_ms in tau_values_ms
    }
    scaled_outputs = scaled_outputs_by_tau[AVERAGER_TAU_MS]
    build_series_cases = [
        ([], "01_rectangular_input_only.png"),
        ([ATTACK_RELEASE_BUILD_TIMES_MS[0]], "02_tau_5ms.png"),
        (ATTACK_RELEASE_BUILD_TIMES_MS[:2], "03_tau_5_20ms.png"),
        (ATTACK_RELEASE_BUILD_TIMES_MS[:3], "04_tau_5_20_100ms.png"),
    ]
    paths.extend(
        save_attack_release_build_plot(visible_taus, filename=filename)
        for visible_taus, filename in build_series_cases
    )
    averager_cases = [
        (
            "Envelope follower after half-wave detector",
            "half_wave",
            block5b_detector_outputs["half_wave"],
            scaled_outputs["half_wave"],
            r"$z_h[n]=\pi\,y[n]$",
            "01_scaled_mean_half_wave_audio_155_185s.png",
        ),
        (
            "Envelope follower after full-wave detector",
            "full_wave",
            block5b_detector_outputs["full_wave"],
            scaled_outputs["full_wave"],
            r"$z_f[n]=\frac{\pi}{2}\,y[n]$",
            "02_scaled_mean_full_wave_audio_155_185s.png",
        ),
        (
            "Envelope follower after squarer",
            "squarer",
            block5b_detector_outputs["squarer"],
            scaled_outputs["squarer"],
            r"$z_r[n]=\sqrt{2\,y[n]}$",
            "03_scaled_mean_squarer_audio_155_185s.png",
        ),
        (
            "Envelope follower after instantaneous envelope",
            "instantaneous",
            block5b_detector_outputs["instantaneous"],
            scaled_outputs["instantaneous"],
            r"$z_i[n]=\sqrt{y[n]}$",
            "04_scaled_mean_instantaneous_audio_155_185s.png",
        ),
    ]
    paths.extend(
        save_scaled_averager_plot(
            block5b_time_s,
            detector,
            scaled,
            title=title,
            tau_ms=AVERAGER_TAU_MS,
            scaler_formula=scaler_formula,
            x_limit=block5b_x_limit,
            filename=filename,
        )
        for title, _name, detector, scaled, scaler_formula, filename in averager_cases
    )
    paths.append(
        save_scaled_comparison_plot(
            block5b_time_s,
            scaled_outputs,
            x_limit=block5b_x_limit,
            filename="05_scaled_outputs_comparison_audio_155_185s.png",
        )
    )
    tau_series_cases = [
        (
            "Half-wave",
            "half_wave",
            [
                "06_tau_5_half_wave_audio_155_185s.png",
                "07_tau_5_20_half_wave_audio_155_185s.png",
                "08_tau_5_20_100_half_wave_audio_155_185s.png",
            ],
        ),
        (
            "Full-wave",
            "full_wave",
            [
                "09_tau_5_full_wave_audio_155_185s.png",
                "10_tau_5_20_full_wave_audio_155_185s.png",
                "11_tau_5_20_100_full_wave_audio_155_185s.png",
            ],
        ),
        (
            "Squarer",
            "squarer",
            [
                "12_tau_5_squarer_audio_155_185s.png",
                "13_tau_5_20_squarer_audio_155_185s.png",
                "14_tau_5_20_100_squarer_audio_155_185s.png",
            ],
        ),
        (
            "Instantaneous",
            "instantaneous",
            [
                "15_tau_5_instantaneous_audio_155_185s.png",
                "16_tau_5_20_instantaneous_audio_155_185s.png",
                "17_tau_5_20_100_instantaneous_audio_155_185s.png",
            ],
        ),
    ]
    for detector_label, name, filenames in tau_series_cases:
        for visible_taus_ms, filename in zip(
            [tau_values_ms[:1], tau_values_ms[:2], tau_values_ms[:3]],
            filenames,
        ):
            paths.append(
                save_tau_series_plot(
                    block5b_time_s,
                    detector_label,
                    block5b_detector_outputs[name],
                    visible_scaled_by_tau=[
                        (tau_ms, scaled_outputs_by_tau[tau_ms][name])
                        for tau_ms in visible_taus_ms
                    ],
                    x_limit=block5b_x_limit,
                    filename=filename,
                )
            )

    compressor_detector = block5b_detector_outputs["full_wave"]
    compressor_attack_release = attack_release_averager(
        compressor_detector,
        block5b_sample_rate_hz,
        COMPRESSOR_ATTACK_MS,
        COMPRESSOR_RELEASE_MS,
    )
    compressor_attack_release = scale_averager_output("full_wave", compressor_attack_release)
    rms_detector = block5b_detector_outputs["squarer"]
    rms_attack_release = scale_averager_output(
        "squarer",
        attack_release_averager(
            rms_detector,
            block5b_sample_rate_hz,
            RMS_METER_ATTACK_MS,
            RMS_METER_RELEASE_MS,
        ),
    )
    paths.append(
        save_attack_release_application_plot(
            block5b_time_s,
            "Full-wave detector",
            block5b_audio,
            compressor_attack_release,
            title="Compressor envelope follower",
            attack_ms=COMPRESSOR_ATTACK_MS,
            release_ms=COMPRESSOR_RELEASE_MS,
            x_limit=block5b_x_limit,
            filename="01_compressor_attack_release_envelope_audio_155_185s.png",
        )
    )
    paths.append(
        save_attack_release_application_plot(
            block5b_time_s,
            "Squarer detector",
            block5b_audio,
            rms_attack_release,
            title="RMS meter envelope",
            attack_ms=RMS_METER_ATTACK_MS,
            release_ms=RMS_METER_RELEASE_MS,
            x_limit=block5b_x_limit,
            filename="02_rms_meter_attack_release_audio_155_185s.png",
        )
    )

    for path in paths:
        print(path.relative_to(LECTURE_DIR))


if __name__ == "__main__":
    main()
