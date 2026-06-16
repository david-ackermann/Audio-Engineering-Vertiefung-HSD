from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from PIL import Image
from scipy.io import wavfile


LECTURE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LECTURE_DIR.parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "02_applications_auto_wah_morphing"
    / "02a_sidechain_auto_wah"
)
AUDIO_FILE = PROJECT_DIR / "audio_samples" / "nachhallfrei" / "sprache" / "Speech_GrimmStoryExcerptGermanFemale.wav"

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18
ATTACK_RELEASE_FIGSIZE = (12.0, 4.4)
ATTACK_RELEASE_TITLE_SIZE = 24
ATTACK_RELEASE_LABEL_SIZE = 19
ATTACK_RELEASE_TICK_SIZE = 16
ATTACK_RELEASE_PLOT_LEFT = 0.125
ATTACK_RELEASE_PLOT_BOTTOM = 0.215
ATTACK_RELEASE_PLOT_RIGHT = 0.965
ATTACK_RELEASE_PLOT_TOP = 0.76

SYSTEM_GREEN = "#66b77a"
MODULATION_VIOLET = "#7b4ab8"
REFERENCE_GREY = "0.70"
ATTACK_RELEASE_REFERENCE_GREY = "0.80"
ATTACK_RELEASE_GRID_GREY = "0.75"
ATTACK_RELEASE_ZERO_GREY = "0.55"
LIGHT_GREY = "0.84"
DARK_GREY = "0.35"

FREQUENCY_MIN_HZ = 20.0
FREQUENCY_MAX_HZ = 20_000.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
MAGNITUDE_LIMITS_DB = (-15.0, 5.0)
MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]

FRAME_COUNT = 88
FRAME_DURATION_MS = 160
START_HOLD_FRAMES = 10
DISPLAY_DURATION_S = 88 * 80 / 1000.0

# Settings from the REAPER screenshot / JSFX.
F_MIN_HZ = 350.0
F_MAX_HZ = 2_500.0
Q = 6.0
ATTACK_MS = 5.0
RELEASE_MS = 100.0
SIDECHAIN_GAIN_DB = 25.5

OUTPUT_FILES = [
    "00_sidechain_signal_speech.png",
    "00_sidechain_signal_speech.gif",
    "01_sidechain_envelope_start.png",
    "02_sidechain_envelope_speech.gif",
    "03_auto_wah_bandpass_start.png",
    "04_auto_wah_bandpass_speech_control.gif",
    "05_attack_release_time_constants.png",
]


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


def read_wav_mono(path: Path) -> tuple[float, np.ndarray]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sample_rate_hz, data = wavfile.read(path)

    signal = data.astype(np.float64)
    if np.issubdtype(data.dtype, np.integer):
        info = np.iinfo(data.dtype)
        signal /= max(abs(info.min), abs(info.max))
    if signal.ndim > 1:
        signal = np.mean(signal, axis=1)
    signal -= float(np.mean(signal))
    return float(sample_rate_hz), signal


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
) -> None:
    if len(signal) > 5000:
        centers, lower, upper = binned_minmax(time, signal)
        ax.fill_between(centers, lower, upper, color=color, alpha=min(0.38, alpha * 0.45), linewidth=0.0, zorder=zorder)
        ax.plot(centers, 0.5 * (lower + upper), color=color, lw=lw, alpha=alpha, zorder=zorder + 0.1)
    else:
        ax.plot(time, signal, color=color, lw=lw, alpha=alpha, zorder=zorder)


def attack_release_envelope(detector_output: np.ndarray, sample_rate_hz: float) -> np.ndarray:
    attack_coefficient = np.exp(-1.0 / (sample_rate_hz * ATTACK_MS * 1e-3))
    release_coefficient = np.exp(-1.0 / (sample_rate_hz * RELEASE_MS * 1e-3))
    envelope = np.empty_like(detector_output)
    state = 0.0
    for index, value in enumerate(detector_output):
        coefficient = attack_coefficient if value > state else release_coefficient
        state = (1.0 - coefficient) * value + coefficient * state
        envelope[index] = state
    return envelope


def auto_wah_center_hz(envelope: np.ndarray | float) -> np.ndarray | float:
    normalized = np.clip(envelope, 0.0, 1.0)
    f_low = min(F_MIN_HZ, F_MAX_HZ)
    f_high = max(F_MIN_HZ, F_MAX_HZ)
    return f_low * (f_high / f_low) ** normalized


def design_wah_tpt_bandpass(center_hz: float, sample_rate_hz: float) -> BiquadCoefficients:
    g = np.tan(np.pi * center_hz / sample_rate_hz)
    k = 1.0 / Q
    a1_tpt = 1.0 / (1.0 + g * (g + k))
    a2_tpt = g * a1_tpt
    a3_tpt = g * a2_tpt

    # v1 of the TPT-SVF is Q times louder at resonance. Divide by Q so the
    # animation matches the normalized wah plots from lecture 9.
    b0 = a2_tpt / Q
    b1 = 0.0
    b2 = -a2_tpt / Q
    a1 = 2.0 * (a3_tpt - a1_tpt)
    a2 = (1.0 - 2.0 * a1_tpt) * (-1.0 + 2.0 * a3_tpt) + 4.0 * a2_tpt**2
    return BiquadCoefficients(b0, b1, b2, a1, a2)


def frequency_grid() -> np.ndarray:
    return np.geomspace(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ, 4096)


def wah_response(frequency_hz: np.ndarray, center_hz: float, sample_rate_hz: float) -> np.ndarray:
    coefficients = design_wah_tpt_bandpass(center_hz, sample_rate_hz)
    omega = 2.0 * np.pi * frequency_hz / sample_rate_hz
    z1 = np.exp(-1j * omega)
    z2 = np.exp(-2j * omega)
    numerator = coefficients.b0 + coefficients.b1 * z1 + coefficients.b2 * z2
    denominator = 1.0 + coefficients.a1 * z1 + coefficients.a2 * z2
    return numerator / denominator


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-8))


def create_signal_figure(title: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.985, bottom=0.18, top=0.84)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlabel("Time in s", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.set_ylim(-1.05, 1.05)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def create_frequency_figure(title: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax.set_yticks(MAGNITUDE_TICKS_DB)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|H(f)|$ in dB", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def add_text_box(ax: plt.Axes, text: str, color: str, y_position: float) -> None:
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


def prepare_sidechain_data() -> dict[str, np.ndarray | float]:
    sample_rate_hz, speech = read_wav_mono(AUDIO_FILE)
    sample_count = min(len(speech), int(round(DISPLAY_DURATION_S * sample_rate_hz)))
    speech = speech[:sample_count]
    time = np.arange(sample_count, dtype=np.float64) / sample_rate_hz

    display_peak = max(float(np.max(np.abs(speech))), np.finfo(float).eps)
    display_speech = speech / display_peak

    sidechain_gain = 10.0 ** (SIDECHAIN_GAIN_DB / 20.0)
    detector = np.clip(np.abs(speech) * sidechain_gain, 0.0, 1.0)
    envelope = attack_release_envelope(detector, sample_rate_hz)
    center_hz = auto_wah_center_hz(envelope)

    frame_times = np.linspace(0.0, time[-1], FRAME_COUNT)
    frame_indices = np.clip(np.round(frame_times * sample_rate_hz).astype(int), 0, sample_count - 1)
    return {
        "sample_rate_hz": sample_rate_hz,
        "time": time,
        "speech": display_speech,
        "envelope": envelope,
        "center_hz": center_hz,
        "frame_indices": frame_indices,
        "frame_times": frame_times,
    }


def render_envelope_frame(data: dict[str, np.ndarray | float], frame_index: int) -> plt.Figure:
    time = data["time"]
    speech = data["speech"]
    envelope = data["envelope"]
    frame_indices = data["frame_indices"]
    current_sample = int(frame_indices[frame_index])
    current_time = float(time[current_sample])
    current_env = float(envelope[current_sample])

    fig, ax = create_signal_figure("Sidechain envelope from speech")
    ax.set_xlim(float(time[0]), float(time[-1]))
    plot_signal(ax, time, speech, color=REFERENCE_GREY, lw=1.5, alpha=0.72, zorder=1)
    ax.plot(time[: current_sample + 1], envelope[: current_sample + 1], color=MODULATION_VIOLET, lw=3.0, alpha=0.98, zorder=3)
    ax.plot(time[current_sample:], envelope[current_sample:], color=MODULATION_VIOLET, lw=2.0, alpha=0.28, zorder=2)
    ax.axvline(current_time, color=DARK_GREY, lw=1.8, alpha=0.82, zorder=4)
    ax.plot(current_time, current_env, marker="o", ms=8, color=MODULATION_VIOLET, zorder=5)
    ax.legend(
        handles=[
            Line2D([0], [0], color=REFERENCE_GREY, lw=3.0, alpha=0.72),
            Line2D([0], [0], color=MODULATION_VIOLET, lw=3.0, alpha=0.98),
        ],
        labels=["Speech input", "Envelope"],
        loc="lower left",
        frameon=True,
        framealpha=0.92,
        fontsize=15,
        borderpad=0.35,
        handlelength=2.4,
    )
    ax.text(
        0.98,
        0.17,
        rf"$e[n]={current_env:.2f}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=15,
        color=MODULATION_VIOLET,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        zorder=20,
    )
    ax.text(
        0.98,
        0.05,
        rf"$\tau_a={ATTACK_MS:.0f}\,\mathrm{{ms}},\ \tau_r={RELEASE_MS:.0f}\,\mathrm{{ms}}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=15,
        color=DARK_GREY,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        zorder=20,
    )
    return fig


def render_sidechain_signal(data: dict[str, np.ndarray | float]) -> plt.Figure:
    time = data["time"]
    speech = data["speech"]

    fig, ax = create_signal_figure("Sidechain signal")
    ax.set_xlim(float(time[0]), float(time[-1]))
    plot_signal(ax, time, speech, color=MODULATION_VIOLET, lw=1.8, alpha=1.0, zorder=2)
    ax.legend(
        handles=[Line2D([0], [0], color=MODULATION_VIOLET, lw=3.0, alpha=1.0)],
        labels=[r"$s[n]$"],
        loc="lower left",
        frameon=True,
        framealpha=0.92,
        fontsize=15,
        borderpad=0.35,
        handlelength=2.4,
    )
    return fig


def render_sidechain_signal_frame(data: dict[str, np.ndarray | float], frame_index: int) -> plt.Figure:
    time = data["time"]
    speech = data["speech"]
    frame_indices = data["frame_indices"]
    current_sample = int(frame_indices[frame_index])
    current_time = float(time[current_sample])
    current_value = float(speech[current_sample])

    fig, ax = create_signal_figure("Sidechain signal")
    ax.set_xlim(float(time[0]), float(time[-1]))
    plot_signal(ax, time, speech, color=MODULATION_VIOLET, lw=1.4, alpha=0.28, zorder=1)
    plot_signal(ax, time[: current_sample + 1], speech[: current_sample + 1], color=MODULATION_VIOLET, lw=1.8, alpha=1.0, zorder=2)
    ax.axvline(current_time, color=DARK_GREY, lw=1.8, alpha=0.82, zorder=4)
    ax.plot(current_time, current_value, marker="o", ms=7, color=MODULATION_VIOLET, zorder=5)
    ax.legend(
        handles=[Line2D([0], [0], color=MODULATION_VIOLET, lw=3.0, alpha=1.0)],
        labels=[r"$s[n]$"],
        loc="lower left",
        frameon=True,
        framealpha=0.92,
        fontsize=15,
        borderpad=0.35,
        handlelength=2.4,
    )
    return fig


def rectangular_attack_release_response(
    time_ms: np.ndarray,
    *,
    pulse_on_ms: float,
    pulse_off_ms: float,
    attack_ms: float,
    release_ms: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    attack_mask = (time_ms >= pulse_on_ms) & (time_ms <= pulse_off_ms)
    release_mask = time_ms > pulse_off_ms

    response = np.zeros_like(time_ms)
    attack_time_ms = time_ms[attack_mask] - pulse_on_ms
    response[attack_mask] = 1.0 - np.exp(-attack_time_ms / attack_ms)

    value_at_release = 1.0 - np.exp(-(pulse_off_ms - pulse_on_ms) / attack_ms)
    release_time_ms = time_ms[release_mask] - pulse_off_ms
    response[release_mask] = value_at_release * np.exp(-release_time_ms / release_ms)
    return response, attack_mask, release_mask


def render_attack_release_time_constants() -> plt.Figure:
    time_ms = np.linspace(-100.0, 1000.0, 3300)
    pulse_on_ms = 0.0
    pulse_off_ms = 400.0
    rectangular = ((time_ms >= pulse_on_ms) & (time_ms <= pulse_off_ms)).astype(float)
    response, attack_mask, release_mask = rectangular_attack_release_response(
        time_ms,
        pulse_on_ms=pulse_on_ms,
        pulse_off_ms=pulse_off_ms,
        attack_ms=ATTACK_MS,
        release_ms=RELEASE_MS,
    )

    fig, ax = plt.subplots(figsize=ATTACK_RELEASE_FIGSIZE, dpi=DPI, facecolor="white")
    ax.fill_between(time_ms, 0.0, rectangular, color=ATTACK_RELEASE_REFERENCE_GREY, alpha=0.34, linewidth=0.0, zorder=1)
    ax.step(time_ms, rectangular, where="post", color=ATTACK_RELEASE_REFERENCE_GREY, lw=2.0, alpha=0.95, zorder=2)
    ax.plot(time_ms[attack_mask], response[attack_mask], color=MODULATION_VIOLET, lw=2.9, alpha=0.98, zorder=3)
    ax.plot(
        time_ms[release_mask],
        response[release_mask],
        color=MODULATION_VIOLET,
        lw=2.9,
        ls="--",
        alpha=0.98,
        zorder=3,
    )

    fig.suptitle("Attack and release time constants", fontsize=ATTACK_RELEASE_TITLE_SIZE, y=0.965)
    ax.set_xlim(-100.0, 1000.0)
    ax.set_xticks([-100.0, 0.0, 200.0, 400.0, 600.0, 800.0, 1000.0])
    ax.set_ylim(-0.08, 1.14)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel("Time (ms)", fontsize=ATTACK_RELEASE_LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=ATTACK_RELEASE_LABEL_SIZE)
    ax.grid(True, color=ATTACK_RELEASE_GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=ATTACK_RELEASE_ZERO_GREY, lw=0.9)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", labelsize=ATTACK_RELEASE_TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    ax.text(
        0.64,
        0.72,
        r"$y_A(t)=1-e^{-t/\tau_A}$" + "\n" + r"$y_R(t)=y_A(T)e^{-(t-T)/\tau_R}$",
        transform=ax.transAxes,
        fontsize=16,
        color=MODULATION_VIOLET,
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
        zorder=10,
    )

    fig.legend(
        handles=[
            Line2D([0], [0], color=MODULATION_VIOLET, lw=2.9),
            Line2D([0], [0], color=MODULATION_VIOLET, lw=2.9, ls="--"),
        ],
        labels=[rf"$\tau_A={ATTACK_MS:.0f}\,\mathrm{{ms}}$", rf"$\tau_R={RELEASE_MS:.0f}\,\mathrm{{ms}}$"],
        loc="upper center",
        bbox_to_anchor=(0.55, 0.845),
        ncol=2,
        frameon=False,
        fontsize=12,
        handlelength=2.2,
        columnspacing=1.25,
    )

    fig.subplots_adjust(
        left=ATTACK_RELEASE_PLOT_LEFT,
        right=ATTACK_RELEASE_PLOT_RIGHT,
        bottom=ATTACK_RELEASE_PLOT_BOTTOM,
        top=ATTACK_RELEASE_PLOT_TOP,
    )
    return fig


def render_bandpass_frame(data: dict[str, np.ndarray | float], frame_index: int) -> plt.Figure:
    sample_rate_hz = float(data["sample_rate_hz"])
    frame_indices = data["frame_indices"]
    envelope = data["envelope"]
    current_sample = int(frame_indices[frame_index])
    current_env = float(envelope[current_sample])
    active_center_hz = float(auto_wah_center_hz(current_env))

    frequency_hz = frequency_grid()
    reference = wah_response(frequency_hz, F_MIN_HZ, sample_rate_hz)
    active = wah_response(frequency_hz, active_center_hz, sample_rate_hz)

    fig, ax = create_frequency_figure("Auto-Wah bandpass controlled by speech")
    ax.plot(frequency_hz, magnitude_db(reference), color=REFERENCE_GREY, lw=2.5, alpha=0.78, zorder=1)
    ax.plot(frequency_hz, magnitude_db(active), color=SYSTEM_GREEN, lw=3.2, zorder=3)
    ax.axvline(active_center_hz, color=SYSTEM_GREEN, lw=1.8, alpha=0.68, ls=":", zorder=2)
    add_text_box(ax, rf"$f_c={active_center_hz:.0f}\,\mathrm{{Hz}},\ Q={Q:.1f}$", SYSTEM_GREEN, 0.96)
    add_text_box(
        ax,
        rf"$f_\mathrm{{min}}={F_MIN_HZ:.0f}\,\mathrm{{Hz}},\ f_\mathrm{{max}}={F_MAX_HZ:.0f}\,\mathrm{{Hz}}$",
        DARK_GREY,
        0.84,
    )
    return fig


def figure_to_pil_image(fig: plt.Figure, marker_index: int) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=fig.dpi, facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    image = Image.open(buffer).convert("RGB")
    image.load()
    marker_value = 255 - (marker_index % 32)
    image.putpixel((0, 0), (255, 255, marker_value))
    return image


def save_still(render_function, data: dict[str, np.ndarray | float], filename: str) -> None:
    fig = render_function(data, 0)
    fig.savefig(OUTPUT_DIR / filename, dpi=fig.dpi, facecolor="white")
    plt.close(fig)


def save_animation(render_function, data: dict[str, np.ndarray | float], filename: str) -> None:
    frames: list[Image.Image] = []
    for hold_index in range(START_HOLD_FRAMES):
        fig = render_function(data, 0)
        frames.append(figure_to_pil_image(fig, hold_index))
    for frame_index in range(FRAME_COUNT):
        fig = render_function(data, frame_index)
        frames.append(figure_to_pil_image(fig, START_HOLD_FRAMES + frame_index))

    frames[0].save(
        OUTPUT_DIR / filename,
        save_all=True,
        append_images=frames[1:],
        duration=[FRAME_DURATION_MS] * len(frames),
        loop=0,
        optimize=False,
        disposal=2,
    )


def render_auto_wah_assets(clear_existing: bool = True) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if clear_existing:
        for filename in OUTPUT_FILES:
            path = OUTPUT_DIR / filename
            if path.exists():
                path.unlink()

    data = prepare_sidechain_data()
    fig = render_sidechain_signal(data)
    fig.savefig(OUTPUT_DIR / "00_sidechain_signal_speech.png", dpi=fig.dpi, facecolor="white")
    plt.close(fig)
    save_animation(render_sidechain_signal_frame, data, "00_sidechain_signal_speech.gif")
    fig = render_attack_release_time_constants()
    fig.savefig(OUTPUT_DIR / "05_attack_release_time_constants.png", dpi=fig.dpi, facecolor="white")
    plt.close(fig)
    save_still(render_envelope_frame, data, "01_sidechain_envelope_start.png")
    save_animation(render_envelope_frame, data, "02_sidechain_envelope_speech.gif")
    save_still(render_bandpass_frame, data, "03_auto_wah_bandpass_start.png")
    save_animation(render_bandpass_frame, data, "04_auto_wah_bandpass_speech_control.gif")


if __name__ == "__main__":
    render_auto_wah_assets()
    print(f"Rendered Auto-Wah animation assets to {OUTPUT_DIR}")
