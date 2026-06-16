from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "03_single_sideband_modulator" / "03a_single_sideband_material"

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18

FS_HZ = 48_000.0
FREQUENCY_MIN_HZ = 20.0
FREQUENCY_MAX_HZ = 20_000.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
MAGNITUDE_LIMITS_DB = (-15.0, 5.0)
MAGNITUDE_TICKS_DB = [-15.0, -10.0, -5.0, 0.0, 5.0]
TIME_LIMITS = (-1.0, 1.0)

FFT_LENGTH = 16_384
FILTER_LENGTH = 129
LONG_FILTER_LENGTHS = [512, 1024]
ALLPASS_IMPULSE_LENGTH = 192
ALLPASS_COEF_0 = np.array(
    [
        0.036681502163648,
        0.274631759379454,
        0.561098969787919,
        0.769741833862266,
        0.892260818003879,
        0.962094548378084,
    ]
)
ALLPASS_COEF_1 = np.array(
    [
        0.136547624631958,
        0.423138617436567,
        0.677540049974162,
        0.839889624849638,
        0.931541959963184,
        0.987816370732897,
    ]
)

LEFT_GREEN = "#1f7a3f"
RIGHT_GREEN = "#66b77a"
REFERENCE_GREY = "0.72"
BLACK = "0.10"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def phase_wrapped(response: np.ndarray) -> np.ndarray:
    return np.angle(response)


def ideal_hilbert_fir(length: int) -> tuple[np.ndarray, int]:
    if length % 2 == 0:
        raise ValueError("Hilbert FIR length must be odd.")

    delay = (length - 1) // 2
    n = np.arange(length)
    k = n - delay
    impulse_response = np.zeros(length)

    odd = (k % 2) != 0
    impulse_response[odd] = 2.0 / (np.pi * k[odd])
    impulse_response *= np.hamming(length)
    return impulse_response, delay


def designed_hilbert_fir(length: int) -> tuple[np.ndarray, float]:
    transition_low_hz = 80.0
    transition_high_hz = 23_000.0
    impulse_response = -signal.firwin2(
        length,
        [0.0, 20.0, transition_low_hz, FREQUENCY_MAX_HZ, transition_high_hz, FS_HZ / 2.0],
        [0.0, 0.0, 1.0, 1.0, 0.3, 0.0],
        fs=FS_HZ,
        antisymmetric=True,
        window="hamming",
    )
    delay = 0.5 * (length - 1)
    return impulse_response, delay


def compensation_delay_fir(length: int, delay: int) -> np.ndarray:
    impulse_response = np.zeros(length)
    impulse_response[delay] = 1.0
    return impulse_response


def acausal_ideal_hilbert_impulse(length: int) -> tuple[np.ndarray, np.ndarray]:
    if length % 2 == 0:
        raise ValueError("Acausal Hilbert impulse length must be odd.")

    half_width = (length - 1) // 2
    sample_axis = np.arange(-half_width, half_width + 1)
    impulse_response = np.zeros(length)
    odd = (sample_axis % 2) != 0
    impulse_response[odd] = 2.0 / (np.pi * sample_axis[odd])
    return sample_axis, impulse_response


def frequency_response(
    impulse_response: np.ndarray,
    *,
    phase_advance_samples: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    frequencies_hz = np.fft.rfftfreq(FFT_LENGTH, d=1.0 / FS_HZ)
    response = np.fft.rfft(impulse_response, n=FFT_LENGTH)
    if phase_advance_samples != 0.0:
        omega = 2.0 * np.pi * frequencies_hz / FS_HZ
        response = response * np.exp(1j * omega * phase_advance_samples)
    mask = (frequencies_hz >= FREQUENCY_MIN_HZ) & (frequencies_hz <= FREQUENCY_MAX_HZ)
    return frequencies_hz[mask], response[mask]


def allpass2_chain(input_signal: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    output = np.asarray(input_signal, dtype=float).copy()
    for coefficient in coefficients:
        section_output = np.zeros_like(output)
        x1 = x2 = y1 = y2 = 0.0
        for index, sample in enumerate(output):
            section_sample = coefficient * y2 + x2 - coefficient * sample
            section_output[index] = section_sample
            x2 = x1
            x1 = sample
            y2 = y1
            y1 = section_sample
        output = section_output
    return output


def allpass_hilbert_impulse_pair(length: int = ALLPASS_IMPULSE_LENGTH) -> tuple[np.ndarray, np.ndarray]:
    impulse = np.zeros(length)
    impulse[0] = 1.0
    in_phase = allpass2_chain(impulse, ALLPASS_COEF_0)
    quadrature_raw = allpass2_chain(impulse, ALLPASS_COEF_1)
    quadrature = np.concatenate(([0.0], quadrature_raw[:-1]))
    return in_phase, quadrature


def allpass_hilbert_frequency_response() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    frequencies_hz = np.fft.rfftfreq(FFT_LENGTH, d=1.0 / FS_HZ)
    omega = 2.0 * np.pi * frequencies_hz / FS_HZ
    z_minus_1 = np.exp(-1j * omega)
    z_minus_2 = np.exp(-2j * omega)

    response_0 = np.ones_like(omega, dtype=complex)
    for coefficient in ALLPASS_COEF_0:
        response_0 *= (z_minus_2 - coefficient) / (1.0 - coefficient * z_minus_2)

    response_90 = z_minus_1.copy()
    for coefficient in ALLPASS_COEF_1:
        response_90 *= (z_minus_2 - coefficient) / (1.0 - coefficient * z_minus_2)

    relative_response = response_90 / response_0
    mask = (frequencies_hz >= FREQUENCY_MIN_HZ) & (frequencies_hz <= FREQUENCY_MAX_HZ)
    return frequencies_hz[mask], response_0[mask], response_90[mask], relative_response[mask]


def style_time_axis(ax: plt.Axes, *, title: str, y_limits: tuple[float, float]) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0, FILTER_LENGTH - 1)
    ax.set_ylim(*y_limits)
    ax.set_xticks([0, 32, 64, 96, 128])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(BLACK)


def style_noncausal_time_axis(
    ax: plt.Axes,
    *,
    title: str,
    y_limits: tuple[float, float],
    length: int,
) -> None:
    half_width = int(np.ceil(0.5 * (length - 1)))
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-half_width, half_width)
    ax.set_ylim(*y_limits)
    tick_step = max(32, int(2 ** np.floor(np.log2(max(half_width / 2.0, 1.0)))))
    ticks = [-half_width, -tick_step, 0, tick_step, half_width]
    ax.set_xticks(ticks)
    ax.set_xlabel("Sample index relative to center", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(BLACK)


def style_frequency_axis(ax_magnitude: plt.Axes, ax_phase: plt.Axes, *, title: str) -> None:
    ax_magnitude.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax_magnitude.set_xscale("log")
    ax_magnitude.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax_magnitude.set_xticks(FREQUENCY_TICKS_HZ)
    ax_magnitude.set_xticklabels(FREQUENCY_TICKLABELS)
    ax_magnitude.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax_magnitude.set_yticks(MAGNITUDE_TICKS_DB)
    ax_magnitude.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax_magnitude.set_ylabel(r"$|H(f)|$ in dB", fontsize=LABEL_SIZE)
    ax_magnitude.grid(alpha=0.30, which="major")
    ax_magnitude.grid(alpha=0.18, which="minor", ls=":")
    ax_magnitude.set_axisbelow(True)
    ax_magnitude.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax_magnitude.spines[spine].set_visible(False)
    for spine in ax_magnitude.spines.values():
        spine.set_color(BLACK)

    ax_phase.set_ylim(-np.pi, np.pi)
    ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi])
    ax_phase.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax_phase.set_ylabel("Phase in rad", fontsize=LABEL_SIZE, labelpad=8)
    ax_phase.tick_params(labelsize=TICK_SIZE)
    ax_phase.spines["top"].set_visible(False)
    ax_phase.spines["left"].set_visible(False)
    ax_phase.spines["right"].set_color(BLACK)
    for phase_value in (-0.5 * np.pi, 0.5 * np.pi):
        ax_phase.axhline(
            phase_value,
            color=REFERENCE_GREY,
            lw=1.25,
            ls=":",
            alpha=0.55,
            zorder=0,
        )


def save_impulse_response(
    impulse_response: np.ndarray,
    *,
    title: str,
    y_limits: tuple[float, float],
    filename: str,
) -> Path:
    sample_axis = np.arange(len(impulse_response))
    delay = (len(impulse_response) - 1) // 2

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax.axhline(0.0, color=REFERENCE_GREY, lw=1.15, zorder=0)
    ax.axvline(delay, color=REFERENCE_GREY, lw=1.25, ls=":", alpha=0.85, zorder=1)
    ax.vlines(sample_axis, 0.0, impulse_response, color=LEFT_GREEN, lw=1.35, zorder=2)
    ax.scatter(sample_axis, impulse_response, color=LEFT_GREEN, s=18, zorder=3)
    style_time_axis(ax, title=title, y_limits=y_limits)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_noncausal_impulse_response(
    impulse_response: np.ndarray,
    *,
    title: str,
    y_limits: tuple[float, float],
    filename: str,
    center_samples: float | None = None,
) -> Path:
    center = 0.5 * (len(impulse_response) - 1) if center_samples is None else center_samples
    sample_axis = np.arange(len(impulse_response)) - center
    marker_size = 18 if len(impulse_response) <= 256 else 7
    stem_width = 1.35 if len(impulse_response) <= 256 else 0.55

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax.axhline(0.0, color=REFERENCE_GREY, lw=1.15, zorder=0)
    ax.axvline(0.0, color=REFERENCE_GREY, lw=1.25, ls=":", alpha=0.85, zorder=1)
    ax.vlines(sample_axis, 0.0, impulse_response, color=LEFT_GREEN, lw=stem_width, zorder=2)
    ax.scatter(sample_axis, impulse_response, color=LEFT_GREEN, s=marker_size, zorder=3)
    style_noncausal_time_axis(ax, title=title, y_limits=y_limits, length=len(impulse_response))
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_magnitude_phase(
    impulse_response: np.ndarray,
    *,
    title: str,
    filename: str,
    phase_advance_samples: float = 0.0,
) -> Path:
    frequencies_hz, response = frequency_response(
        impulse_response,
        phase_advance_samples=phase_advance_samples,
    )

    fig, ax_magnitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax_phase = ax_magnitude.twinx()
    style_frequency_axis(ax_magnitude, ax_phase, title=title)

    magnitude_line = ax_magnitude.plot(
        frequencies_hz,
        magnitude_db(response),
        color=LEFT_GREEN,
        lw=3.0,
        label="Magnitude",
        zorder=3,
    )[0]
    phase_line = ax_phase.plot(
        frequencies_hz,
        phase_wrapped(response),
        color=RIGHT_GREEN,
        lw=2.5,
        ls="--",
        label="Phase",
        zorder=4,
    )[0]
    legend = ax_magnitude.legend(
        [magnitude_line, phase_line],
        [magnitude_line.get_label(), phase_line.get_label()],
        loc="lower right",
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)

    fig.subplots_adjust(left=0.12, right=0.89, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_allpass_hilbert_impulse_response(filename: str) -> Path:
    in_phase, quadrature = allpass_hilbert_impulse_pair()
    sample_axis = np.arange(len(in_phase))

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax.axhline(0.0, color=REFERENCE_GREY, lw=1.15, zorder=0)
    ax.vlines(sample_axis, 0.0, in_phase, color=LEFT_GREEN, lw=1.2, alpha=0.90, zorder=2)
    ax.scatter(sample_axis, in_phase, color=LEFT_GREEN, s=15, zorder=4, label=r"$x_0[n]$")
    ax.vlines(sample_axis, 0.0, quadrature, color=RIGHT_GREEN, lw=1.2, alpha=0.65, zorder=1)
    ax.scatter(sample_axis, quadrature, color=RIGHT_GREEN, s=15, zorder=3, label=r"$x_{90}[n]$")
    ax.set_title("Biquad allpass Hilbert pair impulse response", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0, ALLPASS_IMPULSE_LENGTH - 1)
    ax.set_ylim(*TIME_LIMITS)
    ax.set_xticks([0, 48, 96, 144, 191])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(BLACK)
    legend = ax.legend(loc="upper right", fontsize=13, frameon=True)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_allpass_single_impulse_response(
    impulse_response: np.ndarray,
    *,
    title: str,
    filename: str,
    color: str,
) -> Path:
    sample_axis = np.arange(len(impulse_response))

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax.axhline(0.0, color=REFERENCE_GREY, lw=1.15, zorder=0)
    ax.vlines(sample_axis, 0.0, impulse_response, color=color, lw=1.2, alpha=0.90, zorder=2)
    ax.scatter(sample_axis, impulse_response, color=color, s=15, zorder=3)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0, ALLPASS_IMPULSE_LENGTH - 1)
    ax.set_ylim(*TIME_LIMITS)
    ax.set_xticks([0, 48, 96, 144, 191])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(BLACK)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_allpass_hilbert_magnitude_phase(filename: str) -> Path:
    frequencies_hz, response_0, response_90, relative_response = allpass_hilbert_frequency_response()

    fig, ax_magnitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax_phase = ax_magnitude.twinx()
    ax_magnitude.set_title("Biquad allpass Hilbert pair magnitude and relative phase", fontsize=TITLE_SIZE, pad=14)
    ax_magnitude.set_xscale("log")
    ax_magnitude.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax_magnitude.set_xticks(FREQUENCY_TICKS_HZ)
    ax_magnitude.set_xticklabels(FREQUENCY_TICKLABELS)
    ax_magnitude.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax_magnitude.set_yticks(MAGNITUDE_TICKS_DB)
    ax_magnitude.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax_magnitude.set_ylabel("Magnitude in dB", fontsize=LABEL_SIZE)
    ax_magnitude.grid(alpha=0.30, which="major")
    ax_magnitude.grid(alpha=0.18, which="minor", ls=":")
    ax_magnitude.set_axisbelow(True)
    ax_magnitude.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax_magnitude.spines[spine].set_visible(False)
    for spine in ax_magnitude.spines.values():
        spine.set_color(BLACK)

    ax_phase.set_ylim(-np.pi, np.pi)
    ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi])
    ax_phase.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax_phase.set_ylabel("Relative phase in rad", fontsize=LABEL_SIZE, labelpad=8)
    ax_phase.tick_params(labelsize=TICK_SIZE)
    ax_phase.spines["top"].set_visible(False)
    ax_phase.spines["left"].set_visible(False)
    ax_phase.spines["right"].set_color(BLACK)
    for phase_value in (-0.5 * np.pi, 0.5 * np.pi):
        ax_phase.axhline(
            phase_value,
            color=REFERENCE_GREY,
            lw=1.25,
            ls=":",
            alpha=0.55,
            zorder=0,
        )

    magnitude_0 = ax_magnitude.plot(
        frequencies_hz,
        magnitude_db(response_0),
        color=LEFT_GREEN,
        lw=3.0,
        label=r"$|A_0|$",
        zorder=3,
    )[0]
    magnitude_90 = ax_magnitude.plot(
        frequencies_hz,
        magnitude_db(response_90),
        color=RIGHT_GREEN,
        lw=2.4,
        label=r"$|z^{-1}A_1|$",
        zorder=4,
    )[0]
    phase_line = ax_phase.plot(
        frequencies_hz,
        phase_wrapped(relative_response),
        color=BLACK,
        lw=2.2,
        ls="--",
        label="Relative phase",
        zorder=5,
    )[0]
    legend = ax_magnitude.legend(
        [magnitude_0, magnitude_90, phase_line],
        [magnitude_0.get_label(), magnitude_90.get_label(), phase_line.get_label()],
        loc="lower right",
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    fig.subplots_adjust(left=0.12, right=0.89, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_allpass_single_magnitude_phase(
    response: np.ndarray,
    *,
    frequencies_hz: np.ndarray,
    title: str,
    filename: str,
    color: str,
) -> Path:
    fig, ax_magnitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax_phase = ax_magnitude.twinx()
    ax_magnitude.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax_magnitude.set_xscale("log")
    ax_magnitude.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax_magnitude.set_xticks(FREQUENCY_TICKS_HZ)
    ax_magnitude.set_xticklabels(FREQUENCY_TICKLABELS)
    ax_magnitude.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax_magnitude.set_yticks(MAGNITUDE_TICKS_DB)
    ax_magnitude.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax_magnitude.set_ylabel("Magnitude in dB", fontsize=LABEL_SIZE)
    ax_magnitude.grid(alpha=0.30, which="major")
    ax_magnitude.grid(alpha=0.18, which="minor", ls=":")
    ax_magnitude.set_axisbelow(True)
    ax_magnitude.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax_magnitude.spines[spine].set_visible(False)
    for spine in ax_magnitude.spines.values():
        spine.set_color(BLACK)

    ax_phase.set_ylim(-np.pi, np.pi)
    ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi])
    ax_phase.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax_phase.set_ylabel("Phase in rad", fontsize=LABEL_SIZE, labelpad=8)
    ax_phase.tick_params(labelsize=TICK_SIZE)
    ax_phase.spines["top"].set_visible(False)
    ax_phase.spines["left"].set_visible(False)
    ax_phase.spines["right"].set_color(BLACK)

    magnitude_line = ax_magnitude.plot(
        frequencies_hz,
        magnitude_db(response),
        color=color,
        lw=3.0,
        label="Magnitude",
        zorder=3,
    )[0]
    phase_line = ax_phase.plot(
        frequencies_hz,
        phase_wrapped(response),
        color=BLACK,
        lw=2.4,
        ls="--",
        label="Phase",
        zorder=4,
    )[0]
    legend = ax_magnitude.legend(
        [magnitude_line, phase_line],
        [magnitude_line.get_label(), phase_line.get_label()],
        loc="lower right",
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    fig.subplots_adjust(left=0.12, right=0.89, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_acausal_ideal_hilbert_impulse_response(filename: str) -> Path:
    sample_axis, impulse_response = acausal_ideal_hilbert_impulse(FILTER_LENGTH)

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax.axhline(0.0, color=REFERENCE_GREY, lw=1.15, zorder=0)
    ax.axvline(0.0, color=REFERENCE_GREY, lw=1.25, ls=":", alpha=0.85, zorder=1)
    ax.vlines(sample_axis, 0.0, impulse_response, color=LEFT_GREEN, lw=1.35, zorder=2)
    ax.scatter(sample_axis, impulse_response, color=LEFT_GREEN, s=18, zorder=3)
    ax.set_title("Acausal ideal Hilbert filter impulse response", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(sample_axis[0], sample_axis[-1])
    ax.set_ylim(*TIME_LIMITS)
    ax.set_xticks([sample_axis[0], -32, 0, 32, sample_axis[-1]])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(BLACK)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_acausal_ideal_hilbert_magnitude_phase(filename: str) -> Path:
    frequencies_hz = np.geomspace(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ, 2048)
    magnitude = np.zeros_like(frequencies_hz)
    phase = -0.5 * np.pi * np.ones_like(frequencies_hz)

    fig, ax_magnitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax_phase = ax_magnitude.twinx()
    style_frequency_axis(ax_magnitude, ax_phase, title="Acausal ideal Hilbert filter magnitude and phase")

    magnitude_line = ax_magnitude.plot(
        frequencies_hz,
        magnitude,
        color=LEFT_GREEN,
        lw=3.0,
        label="Magnitude",
        zorder=3,
    )[0]
    phase_line = ax_phase.plot(
        frequencies_hz,
        phase,
        color=RIGHT_GREEN,
        lw=2.8,
        ls="--",
        label="Phase",
        zorder=4,
    )[0]
    legend = ax_magnitude.legend(
        [magnitude_line, phase_line],
        [magnitude_line.get_label(), phase_line.get_label()],
        loc="lower right",
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    fig.subplots_adjust(left=0.12, right=0.89, bottom=0.18, top=0.84)

    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    hilbert_response, delay = ideal_hilbert_fir(FILTER_LENGTH)
    compensation_response = compensation_delay_fir(FILTER_LENGTH, delay)

    image_paths = [
        save_impulse_response(
            hilbert_response,
            title="Hilbert filter impulse response",
            y_limits=TIME_LIMITS,
            filename="11_hilbert_filter_impulse_response.png",
        ),
        save_magnitude_phase(
            hilbert_response,
            title="Hilbert filter magnitude and phase",
            filename="12_hilbert_filter_magnitude_phase.png",
        ),
        save_impulse_response(
            compensation_response,
            title="Compensation filter impulse response",
            y_limits=TIME_LIMITS,
            filename="13_compensation_filter_impulse_response.png",
        ),
        save_magnitude_phase(
            compensation_response,
            title="Compensation filter magnitude and phase",
            filename="14_compensation_filter_magnitude_phase.png",
        ),
        save_noncausal_impulse_response(
            hilbert_response,
            title="Non-causal Hilbert filter impulse response",
            y_limits=TIME_LIMITS,
            filename="15_noncausal_hilbert_filter_impulse_response.png",
        ),
        save_magnitude_phase(
            hilbert_response,
            title="Non-causal Hilbert filter magnitude and phase",
            filename="16_noncausal_hilbert_filter_magnitude_phase.png",
            phase_advance_samples=delay,
        ),
    ]

    for length in LONG_FILTER_LENGTHS:
        long_hilbert_response, long_delay = designed_hilbert_fir(length)
        image_paths.extend(
            [
                save_noncausal_impulse_response(
                    long_hilbert_response,
                    title=f"Non-causal Hilbert filter impulse response ({length} taps)",
                    y_limits=TIME_LIMITS,
                    filename=f"{17 if length == 512 else 19}_noncausal_hilbert_filter_{length}_taps_impulse_response.png",
                    center_samples=long_delay,
                ),
                save_magnitude_phase(
                    long_hilbert_response,
                    title=f"Non-causal Hilbert filter magnitude and phase ({length} taps)",
                    filename=f"{18 if length == 512 else 20}_noncausal_hilbert_filter_{length}_taps_magnitude_phase.png",
                    phase_advance_samples=long_delay,
                ),
            ]
        )

    iir_correction_impulse, iir_hilbert_impulse = allpass_hilbert_impulse_pair()
    frequencies_hz, iir_correction_response, iir_hilbert_response, _relative_response = (
        allpass_hilbert_frequency_response()
    )
    image_paths.extend(
        [
            save_allpass_single_impulse_response(
                iir_correction_impulse,
                title="IIR correction filter impulse response",
                filename="25_iir_correction_filter_impulse_response.png",
                color=LEFT_GREEN,
            ),
            save_allpass_single_magnitude_phase(
                iir_correction_response,
                frequencies_hz=frequencies_hz,
                title="IIR correction filter magnitude and phase",
                filename="26_iir_correction_filter_magnitude_phase.png",
                color=LEFT_GREEN,
            ),
            save_allpass_single_impulse_response(
                iir_hilbert_impulse,
                title="IIR Hilbert filter impulse response",
                filename="27_iir_hilbert_filter_impulse_response.png",
                color=LEFT_GREEN,
            ),
            save_allpass_single_magnitude_phase(
                iir_hilbert_response,
                frequencies_hz=frequencies_hz,
                title="IIR Hilbert filter magnitude and phase",
                filename="28_iir_hilbert_filter_magnitude_phase.png",
                color=LEFT_GREEN,
            ),
            save_acausal_ideal_hilbert_impulse_response(
                "29_acausal_ideal_hilbert_filter_impulse_response.png"
            ),
            save_acausal_ideal_hilbert_magnitude_phase(
                "30_acausal_ideal_hilbert_filter_magnitude_phase.png"
            ),
        ]
    )

    for path in image_paths:
        print(path)


if __name__ == "__main__":
    main()
