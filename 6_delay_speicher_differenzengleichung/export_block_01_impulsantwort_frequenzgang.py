from pathlib import Path
import wave

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "01_impulsantwort_und_frequenzgang"
OUTPUT_DIR = OUTPUT_ROOT / "1A_zero_padding_tiefpass"
AUDIO_DIR = OUTPUT_DIR / "audio_systemantworten_48khz"

DPI = 200
SAMPLE_RATE_HZ = 48_000
FIGSIZE = (10.5, 4.2)
FIGSIZE_WIDE = (21.0, 4.2)
ONE_SIDED_AXIS_LEFT = 0.12
ONE_SIDED_AXIS_RIGHT = 0.98
FULL_AXIS_LEFT = 0.06
FULL_AXIS_RIGHT = 0.99
TITLE_SIZE = 26
LABEL_SIZE = 24
TICK_SIZE = 18
LEGEND_SIZE = 14

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.72"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def lowpass_impulse_response() -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(15)
    h_lp = np.zeros_like(n, dtype=float)
    alpha = 0.65
    delay = 3
    active = n >= delay
    h_lp[active] = (1.0 - alpha) * alpha ** (n[active] - delay)
    h_lp /= np.sum(h_lp)
    return n, h_lp


def truncate_impulse_response(h: np.ndarray, *, last_sample: int) -> np.ndarray:
    h_truncated = h.copy()
    h_truncated[last_sample + 1 :] = 0.0
    return h_truncated


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*"):
        if image_file.suffix.lower() in {".png", ".gif"}:
            image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def save_figure_fixed_canvas(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def write_impulse_response_wav(
    h: np.ndarray,
    filename: str,
    *,
    sample_rate_hz: int = SAMPLE_RATE_HZ,
    duration_seconds: float = 1.0,
) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    num_samples = max(int(round(sample_rate_hz * duration_seconds)), h.size)
    audio = np.zeros(num_samples, dtype=float)
    audio[: h.size] = h
    pcm = np.round(np.clip(audio, -1.0, 1.0) * 32767.0).astype("<i2")

    with wave.open(str(AUDIO_DIR / filename), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate_hz)
        wav_file.writeframes(pcm.tobytes())


def export_impulse_response_wavs(
    h_original: np.ndarray,
    h_truncated_6: np.ndarray,
    h_truncated_4: np.ndarray,
) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    for wav_file in AUDIO_DIR.glob("*.wav"):
        wav_file.unlink()

    write_impulse_response_wav(h_original, "system_response_original_m15_48khz.wav")
    write_impulse_response_wav(h_truncated_6, "system_response_cut_n6_m15_48khz.wav")
    write_impulse_response_wav(h_truncated_4, "system_response_cut_n4_m15_48khz.wav")


def figure_prefix(filename_index: int | str) -> str:
    if isinstance(filename_index, int):
        return f"{filename_index:02d}"
    return filename_index


def full_response_figsize(n_fft: int, *, match_one_sided_spacing: bool = False) -> tuple[float, float]:
    if not match_one_sided_spacing:
        return FIGSIZE_WIDE

    one_sided_axis_fraction = ONE_SIDED_AXIS_RIGHT - ONE_SIDED_AXIS_LEFT
    full_axis_fraction = FULL_AXIS_RIGHT - FULL_AXIS_LEFT
    one_sided_bin_units = n_fft // 2 + 1
    full_bin_units = n_fft
    width = FIGSIZE[0] * one_sided_axis_fraction * full_bin_units / (one_sided_bin_units * full_axis_fraction)
    return width, FIGSIZE[1]


def full_transition_title(n_fft: int) -> str:
    return rf"Sampled magnitude response $|H(e^{{j\Omega_k}})|$, $N={n_fft}$"


def full_transition_legend_label(n_fft: int) -> str:
    return rf"$H(e^{{j\Omega_k}})$, $N={n_fft}$"


def match_canvas_to_reference(reference_filename: str, target_filenames: list[str]) -> None:
    reference_image = Image.open(OUTPUT_DIR / reference_filename).convert("RGB")
    reference_width, reference_height = reference_image.size
    reference_axis_y = strongest_horizontal_axis_row(reference_image)
    reference_axis_x = strongest_vertical_axis_col(reference_image)

    for filename in target_filenames:
        image_path = OUTPUT_DIR / filename
        image = Image.open(image_path).convert("RGB")
        canvas = Image.new("RGB", (reference_width, reference_height), "white")
        target_axis_y = strongest_horizontal_axis_row(image)
        target_axis_x = strongest_vertical_axis_col(image)
        paste_y = reference_axis_y - target_axis_y
        paste_x = reference_axis_x - target_axis_x

        source_left = max(0, -paste_x)
        source_top = max(0, -paste_y)
        target_left = max(0, paste_x)
        target_top = max(0, paste_y)
        copy_width = min(image.width - source_left, reference_width - target_left)
        copy_height = min(image.height - source_top, reference_height - target_top)

        crop_box = (source_left, source_top, source_left + copy_width, source_top + copy_height)
        canvas.paste(image.crop(crop_box), (target_left, target_top))
        canvas.save(image_path)


def strongest_horizontal_axis_row(image: Image.Image) -> int:
    width, height = image.size
    row_scores = []
    for y in range(height):
        score = 0
        for x in range(width):
            red, green, blue = image.getpixel((x, y))
            if red < 45 and green < 45 and blue < 45:
                score += 1
        row_scores.append(score)
    return max(range(height), key=lambda y: row_scores[y])


def strongest_vertical_axis_col(image: Image.Image) -> int:
    width, height = image.size
    col_scores = []
    for x in range(width):
        score = 0
        for y in range(height):
            red, green, blue = image.getpixel((x, y))
            if red < 45 and green < 45 and blue < 45:
                score += 1
        col_scores.append(score)
    return max(range(width), key=lambda x: col_scores[x])


def stem_sequence(
    ax,
    n: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    alpha: float = 1.0,
    marker_size: float = 8.0,
    line_width: float = 2.8,
) -> None:
    markerline, stemlines, baseline = ax.stem(n, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.9)
    markerline.set_markersize(marker_size)
    markerline.set_alpha(alpha)
    stemlines.set_color(color)
    stemlines.set_linewidth(line_width)
    stemlines.set_alpha(alpha)
    baseline.set_color(SIGNAL_BLACK)
    baseline.set_linewidth(1.4)


def style_time_axis(ax, title: str, *, n_max: int) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, n_max + 0.5)
    ax.set_ylim(-0.03, 0.42)
    step = 2 if n_max <= 18 else 8
    ax.set_xticks(np.arange(0, n_max + 1, step))
    ax.set_yticks([0.0, 0.2, 0.4])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_axis(
    ax,
    title: str,
    *,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_ratio_axis(
    ax,
    title: str,
    *,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.01, 0.51)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.0, 0.125, 0.25, 0.375, 0.5])
    ax.set_xticklabels(["0", "0.125", "0.25", "0.375", "0.5"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Normalized frequency $f/f_s$ (1 = $f_s$)", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_discrete_frequency_axis(
    ax,
    title: str,
    *,
    n_fft: int,
    sample_rate_hz: float,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    k_max = n_fft // 2
    nyquist_khz = sample_rate_hz / 2000.0
    frequency_ticks = [tick * sample_rate_hz / n_fft / 1000.0 for tick in dft_bin_ticks(k_max)]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5 * sample_rate_hz / n_fft / 1000.0, nyquist_khz + 0.5 * sample_rate_hz / n_fft / 1000.0)
    ax.set_ylim(*ylim)
    ax.set_xticks(frequency_ticks)
    ax.set_xticklabels([f"{tick:g}" for tick in frequency_ticks])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Discrete frequency $f_k$ [kHz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_khz_axis(
    ax,
    title: str,
    *,
    sample_rate_hz: float,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    nyquist_khz = sample_rate_hz / 2000.0
    tick_step = nyquist_khz / 4.0

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.02 * nyquist_khz, 1.02 * nyquist_khz)
    ax.set_ylim(*ylim)
    ticks = [tick_step * tick for tick in range(5)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{tick:g}" for tick in ticks])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Frequency $f$ [kHz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_log_axis(
    ax,
    title: str,
    *,
    sample_rate_hz: float,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    nyquist_hz = sample_rate_hz / 2.0
    ticks_hz = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    tick_labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(20.0, nyquist_hz)
    ax.set_ylim(*ylim)
    ax.set_xticks(ticks_hz)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Frequency $f$ [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25, which="both")
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_loglog_axis(
    ax,
    title: str,
    *,
    sample_rate_hz: float,
    ylabel: str,
) -> None:
    nyquist_hz = sample_rate_hz / 2.0
    ticks_hz = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    tick_labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(20.0, nyquist_hz)
    ax.set_ylim(0.1, 1.1)
    ax.set_xticks(ticks_hz)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([0.1, 0.2, 0.5, 1.0])
    ax.set_yticklabels(["0.1", "0.2", "0.5", "1"])
    ax.set_xlabel(r"Frequency $f$ [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25, which="both")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_db_axis(
    ax,
    title: str,
    *,
    sample_rate_hz: float,
    ylabel: str | None = "Magnitude [dB]",
) -> None:
    nyquist_hz = sample_rate_hz / 2.0
    ticks_hz = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    tick_labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(20.0, nyquist_hz)
    ax.set_ylim(-15.0, 1.0)
    ax.set_xticks(ticks_hz)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([-15, -12, -9, -6, -3, 0])
    ax.set_yticklabels(["-15", "-12", "-9", "-6", "-3", "0"])
    ax.set_xlabel(r"Frequency $f$ [Hz]", fontsize=LABEL_SIZE)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25, which="both")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_normalized_dft_axis(
    ax,
    title: str,
    *,
    n_fft: int,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    k_max = n_fft // 2
    normalized_ticks = [tick / k_max for tick in dft_bin_ticks(k_max)]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5 / k_max, 1.0 + 0.5 / k_max)
    ax.set_ylim(*ylim)
    ax.set_xticks(normalized_ticks)
    ax.set_xticklabels([f"{tick:g}" for tick in normalized_ticks])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def dft_bin_ticks(k_max: int) -> list[int]:
    if k_max <= 8:
        step = 2
    elif k_max <= 16:
        step = 4
    else:
        step = 8

    ticks = list(range(0, k_max + 1, step))
    if ticks[-1] != k_max:
        ticks.append(k_max)
    return ticks


def style_dft_bin_axis(
    ax,
    title: str,
    *,
    k_max: int,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, k_max + 0.5)
    ax.set_ylim(*ylim)
    ax.set_xticks(dft_bin_ticks(k_max))
    ax.set_yticks(yticks)
    ax.set_xlabel(r"DFT bin $k$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_full_frequency_axis(
    ax,
    title: str,
    *,
    n_fft: int,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    bin_width = 2.0 / n_fft
    tick_indices = np.arange(0, n_fft, n_fft // 4)
    tick_values = 2.0 * tick_indices / n_fft

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5 * bin_width, 2.0 - 0.5 * bin_width)
    ax.set_ylim(*ylim)
    ax.set_xticks(tick_values)
    ax.set_xticklabels(["0", "0.5", "1", "1.5"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Normalized frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_full_discrete_frequency_axis(
    ax,
    title: str,
    *,
    n_fft: int,
    sample_rate_hz: float,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    bin_width_khz = sample_rate_hz / n_fft / 1000.0
    tick_indices = np.arange(0, n_fft, n_fft // 4)
    tick_values = tick_indices * bin_width_khz

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5 * bin_width_khz, sample_rate_hz / 1000.0 - 0.5 * bin_width_khz)
    ax.set_ylim(*ylim)
    ax.set_xticks(tick_values)
    ax.set_xticklabels([f"{tick:g}" for tick in tick_values])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Discrete frequency $f_k$ [kHz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_full_frequency_axis_radians(
    ax,
    title: str,
    *,
    n_fft: int,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    bin_width = 2.0 * np.pi / n_fft
    tick_indices = np.arange(0, n_fft, n_fft // 4)
    tick_values = 2.0 * np.pi * tick_indices / n_fft

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5 * bin_width, 2.0 * np.pi - 0.5 * bin_width)
    ax.set_ylim(*ylim)
    ax.set_xticks(tick_values)
    ax.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Angular frequency $\Omega$ [rad/sample]", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def dense_response(h: np.ndarray, num_points: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, np.pi, num_points)
    n = np.arange(h.size)
    response = np.exp(-1j * np.outer(omega, n)) @ h
    return omega, response


def dense_response_full(h: np.ndarray, num_points: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, 2.0 * np.pi, num_points)
    n = np.arange(h.size)
    response = np.exp(-1j * np.outer(omega, n)) @ h
    return omega, response


def cutoff_frequency_hz(h: np.ndarray, sample_rate_hz: float, *, target_db: float = -3.0) -> float:
    omega_dense, response_dense = dense_response(h, num_points=65536)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response_dense), 1e-12))
    below_target = np.flatnonzero(magnitude_db <= target_db)
    if below_target.size == 0:
        return float("nan")

    right_index = int(below_target[0])
    if right_index == 0:
        return float(frequency_hz[0])

    left_index = right_index - 1
    return float(
        np.interp(
            target_db,
            [magnitude_db[left_index], magnitude_db[right_index]],
            [frequency_hz[left_index], frequency_hz[right_index]],
        )
    )


def dft_response(h: np.ndarray, n_fft: int) -> tuple[np.ndarray, np.ndarray]:
    k = np.arange(n_fft // 2 + 1)
    omega = 2.0 * np.pi * k / n_fft
    response = np.fft.rfft(h, n=n_fft)
    return omega, response


def dft_response_full(h: np.ndarray, n_fft: int) -> tuple[np.ndarray, np.ndarray]:
    k = np.arange(n_fft)
    omega = 2.0 * np.pi * k / n_fft
    response = np.fft.fft(h, n=n_fft)
    return omega, response


def export_impulse_response_frame(n: np.ndarray, h: np.ndarray, n_fft: int, filename_index: int) -> None:
    padded = np.zeros(n_fft, dtype=float)
    padded[: h.size] = h
    n_padded = np.arange(n_fft)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    stem_sequence(ax, n_padded, padded, color=REFERENCE_GREY, alpha=0.50, marker_size=5.5, line_width=1.6)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    style_time_axis(ax, rf"Low-pass impulse response $h[n]$, $N={n_fft}$", n_max=n_fft - 1)
    save_figure(fig, f"{filename_index:02d}_impulse_response_n{n_fft}.png")


def export_truncated_impulse_response(
    h_truncated: np.ndarray,
    *,
    last_sample: int,
    filename_index: int,
) -> None:
    n = np.arange(h_truncated.size)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    stem_sequence(ax, n, h_truncated, color=SYSTEM_GREEN)
    ax.axvline(last_sample + 0.5, color="0.35", lw=2.2, ls="--")
    style_time_axis(
        ax,
        rf"Truncated low-pass impulse response $h_{{{last_sample}}}[n]$, $M=15$",
        n_max=h_truncated.size - 1,
    )
    ax.legend(
        handles=[
            plt.Line2D(
                [0],
                [0],
                color=SYSTEM_GREEN,
                marker="o",
                lw=2.8,
                label=rf"$h_{{{last_sample}}}[n]$, cut after $n={last_sample}$",
            ),
            plt.Line2D([0], [0], color="0.35", lw=2.2, ls="--", label="cut"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure_fixed_canvas(fig, f"{filename_index:02d}_truncated_impulse_response_m15_cut_n{last_sample}.png")


def export_magnitude_response(
    h: np.ndarray,
    n_fft: int,
    filename_index: int,
    *,
    with_envelope: bool = False,
    envelope_axis: str = "omega",
) -> None:
    omega_bins, response_bins = dft_response(h, n_fft)
    k_bins = np.arange(response_bins.size)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=ONE_SIDED_AXIS_LEFT, right=ONE_SIDED_AXIS_RIGHT, bottom=0.18, top=0.84)
    if with_envelope and envelope_axis == "k":
        omega_dense, response_dense = dense_response(h)
        k_dense = omega_dense * n_fft / (2.0 * np.pi)
        ax.plot(k_dense, np.abs(response_dense), color=SYSTEM_GREEN, alpha=0.45, lw=2.5)
        stem_sequence(ax, k_bins, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
        style_dft_bin_axis(
            ax,
            rf"Sampled magnitude response $|H[k]|$, $N={n_fft}$",
            k_max=n_fft // 2,
            ylabel="Magnitude",
            ylim=(-0.05, 1.10),
            yticks=[0.0, 0.5, 1.0],
        )
    elif with_envelope:
        omega_dense, response_dense = dense_response(h)
        ax.plot(omega_dense / np.pi, np.abs(response_dense), color=SYSTEM_GREEN, alpha=0.45, lw=2.5)
        stem_sequence(ax, omega_bins / np.pi, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
        style_normalized_dft_axis(
            ax,
            rf"Sampled magnitude response $|H(e^{{j\Omega_k}})|$, $N={n_fft}$",
            n_fft=n_fft,
            ylabel="Magnitude",
            ylim=(-0.05, 1.10),
            yticks=[0.0, 0.5, 1.0],
        )
    else:
        stem_sequence(ax, k_bins, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
        style_dft_bin_axis(
            ax,
            rf"Sampled magnitude response $|H[k]|$, $N={n_fft}$",
            k_max=n_fft // 2,
            ylabel="Magnitude",
            ylim=(-0.05, 1.10),
            yticks=[0.0, 0.5, 1.0],
        )
    handles = []
    if with_envelope:
        handles.append(plt.Line2D([0], [0], color=SYSTEM_GREEN, alpha=0.45, lw=2.5, label=r"$|H(e^{j\Omega})|$"))
    sampled_label = rf"$H(e^{{j\Omega_k}})$, $N={n_fft}$" if with_envelope and envelope_axis == "omega" else rf"$H[k]$, $N={n_fft}$"
    handles.append(plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.3, label=sampled_label))
    ax.legend(
        handles=handles,
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    suffix = ""
    if with_envelope and envelope_axis == "k":
        suffix = "_with_envelope_k"
    elif with_envelope:
        suffix = "_with_envelope"
    save_figure(fig, f"{filename_index:02d}_magnitude_response_n{n_fft}{suffix}.png")


def export_magnitude_response_normalized_axis(h: np.ndarray, n_fft: int, filename_index: int | str) -> None:
    omega_bins, response_bins = dft_response(h, n_fft)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=ONE_SIDED_AXIS_LEFT, right=ONE_SIDED_AXIS_RIGHT, bottom=0.18, top=0.84)
    stem_sequence(ax, omega_bins / np.pi, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_normalized_dft_axis(
        ax,
        rf"Sampled magnitude response $|H(e^{{j\Omega_k}})|$, $N={n_fft}$",
        n_fft=n_fft,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.3, label=rf"$H(e^{{j\Omega_k}})$, $N={n_fft}$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{figure_prefix(filename_index)}_magnitude_response_normalized_n{n_fft}.png")


def export_magnitude_response_discrete_frequency_axis_with_envelope(
    h: np.ndarray,
    n_fft: int,
    filename_index: int | str,
    *,
    sample_rate_hz: float = SAMPLE_RATE_HZ,
) -> None:
    omega_bins, response_bins = dft_response(h, n_fft)
    omega_dense, response_dense = dense_response(h)
    frequency_bins_khz = omega_bins / (2.0 * np.pi) * sample_rate_hz / 1000.0
    frequency_dense_khz = omega_dense / (2.0 * np.pi) * sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=ONE_SIDED_AXIS_LEFT, right=ONE_SIDED_AXIS_RIGHT, bottom=0.18, top=0.84)
    ax.plot(frequency_dense_khz, np.abs(response_dense), color=SYSTEM_GREEN, alpha=0.45, lw=2.5)
    stem_sequence(ax, frequency_bins_khz, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_discrete_frequency_axis(
        ax,
        rf"Sampled magnitude response over $f_k$, $N={n_fft}$",
        n_fft=n_fft,
        sample_rate_hz=sample_rate_hz,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, alpha=0.45, lw=2.5, label=r"$|H(e^{j2\pi f/f_s})|$"),
            plt.Line2D(
                [0],
                [0],
                color=SYSTEM_GREEN,
                marker="o",
                lw=2.3,
                label=rf"$|H(e^{{j2\pi f_k/f_s}})|$, $N={n_fft}$",
            ),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{figure_prefix(filename_index)}_magnitude_response_frequency_bins_n{n_fft}_with_envelope.png")


def export_magnitude_response_full_radians(
    h: np.ndarray,
    n_fft: int,
    filename_index: int | str,
    *,
    match_one_sided_spacing: bool = False,
) -> None:
    _, response_bins = dft_response_full(h, n_fft)
    k_bins = np.arange(response_bins.size)

    fig, ax = plt.subplots(figsize=full_response_figsize(n_fft, match_one_sided_spacing=match_one_sided_spacing))
    fig.subplots_adjust(left=FULL_AXIS_LEFT, right=FULL_AXIS_RIGHT, bottom=0.18, top=0.84)
    stem_sequence(ax, k_bins, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_dft_bin_axis(
        ax,
        rf"Sampled magnitude response $|H[k]|$, $N={n_fft}$",
        k_max=n_fft - 1,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.axvline(n_fft / 2, color="0.35", lw=1.8, ls="--")
    ax.legend(
        handles=[
            plt.Line2D(
                [0],
                [0],
                color=SYSTEM_GREEN,
                marker="o",
                lw=2.3,
                label=rf"$H[k]$, $N={n_fft}$",
            ),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{figure_prefix(filename_index)}_magnitude_response_full_radians_n{n_fft}.png")


def export_magnitude_response_full_omega_axis(
    h: np.ndarray,
    n_fft: int,
    filename_index: int | str,
    *,
    match_one_sided_spacing: bool = False,
) -> None:
    omega_bins, response_bins = dft_response_full(h, n_fft)

    fig, ax = plt.subplots(figsize=full_response_figsize(n_fft, match_one_sided_spacing=match_one_sided_spacing))
    fig.subplots_adjust(left=FULL_AXIS_LEFT, right=FULL_AXIS_RIGHT, bottom=0.18, top=0.84)
    stem_sequence(ax, omega_bins, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_full_frequency_axis_radians(
        ax,
        full_transition_title(n_fft),
        n_fft=n_fft,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.axvline(np.pi, color="0.35", lw=1.8, ls="--")
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.3, label=full_transition_legend_label(n_fft)),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{figure_prefix(filename_index)}_magnitude_response_full_omega_n{n_fft}.png")


def export_magnitude_response_full_normalized_axis(
    h: np.ndarray,
    n_fft: int,
    filename_index: int | str,
    *,
    match_one_sided_spacing: bool = False,
) -> None:
    omega_bins, response_bins = dft_response_full(h, n_fft)
    omega_norm = omega_bins / np.pi

    fig, ax = plt.subplots(figsize=full_response_figsize(n_fft, match_one_sided_spacing=match_one_sided_spacing))
    fig.subplots_adjust(left=FULL_AXIS_LEFT, right=FULL_AXIS_RIGHT, bottom=0.18, top=0.84)
    stem_sequence(ax, omega_norm, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_full_frequency_axis(
        ax,
        full_transition_title(n_fft),
        n_fft=n_fft,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.axvline(1.0, color="0.35", lw=1.8, ls="--")
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.3, label=full_transition_legend_label(n_fft)),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{figure_prefix(filename_index)}_magnitude_response_full_normalized_n{n_fft}.png")


def export_magnitude_response_full_discrete_frequency_axis(
    h: np.ndarray,
    n_fft: int,
    filename_index: int | str,
    *,
    match_one_sided_spacing: bool = False,
    sample_rate_hz: float = SAMPLE_RATE_HZ,
) -> None:
    _, response_bins = dft_response_full(h, n_fft)
    k_bins = np.arange(response_bins.size)
    frequency_bins_khz = k_bins * sample_rate_hz / n_fft / 1000.0

    fig, ax = plt.subplots(figsize=full_response_figsize(n_fft, match_one_sided_spacing=match_one_sided_spacing))
    fig.subplots_adjust(left=FULL_AXIS_LEFT, right=FULL_AXIS_RIGHT, bottom=0.18, top=0.84)
    stem_sequence(ax, frequency_bins_khz, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_full_discrete_frequency_axis(
        ax,
        rf"Sampled magnitude response over $f_k$, $N={n_fft}$",
        n_fft=n_fft,
        sample_rate_hz=sample_rate_hz,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.axvline(sample_rate_hz / 2000.0, color="0.35", lw=1.8, ls="--")
    ax.legend(
        handles=[
            plt.Line2D(
                [0],
                [0],
                color=SYSTEM_GREEN,
                marker="o",
                lw=2.3,
                label=rf"$H(e^{{j2\pi f_k/f_s}})$, $N={n_fft}$",
            ),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{figure_prefix(filename_index)}_magnitude_response_full_frequency_n{n_fft}.png")


def export_magnitude_response_full(h: np.ndarray, n_fft: int, filename_index: int) -> None:
    _, response_bins = dft_response_full(h, n_fft)
    k_bins = np.arange(response_bins.size)

    fig, ax = plt.subplots(figsize=full_response_figsize(n_fft))
    fig.subplots_adjust(left=FULL_AXIS_LEFT, right=FULL_AXIS_RIGHT, bottom=0.18, top=0.84)
    stem_sequence(ax, k_bins, np.abs(response_bins), color=SYSTEM_GREEN, marker_size=7.5, line_width=2.3)
    style_dft_bin_axis(
        ax,
        rf"Sampled magnitude response $|H[k]|$, $N={n_fft}$",
        k_max=n_fft - 1,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.axvline(n_fft / 2, color="0.35", lw=1.8, ls="--")
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.3, label=rf"$H[k]$, $N={n_fft}$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_full_n{n_fft}.png")


def export_magnitude_response_envelope_only(h: np.ndarray, filename_index: int) -> None:
    omega_dense, response_dense = dense_response(h)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega_dense / np.pi, np.abs(response_dense), color=SYSTEM_GREEN, lw=3.0)
    style_frequency_axis(
        ax,
        r"System magnitude response $|H(e^{j\Omega})|$",
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$|H(e^{j\Omega})|$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_only.png")


def export_magnitude_response_envelope_frequency_ratio(h: np.ndarray, filename_index: int) -> None:
    omega_dense, response_dense = dense_response(h)
    normalized_frequency = omega_dense / (2.0 * np.pi)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(normalized_frequency, np.abs(response_dense), color=SYSTEM_GREEN, lw=3.0)
    style_frequency_ratio_axis(
        ax,
        r"System magnitude response, $f/f_s$",
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$|H(e^{j\Omega})|$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_frequency_ratio.png")


def export_magnitude_response_envelope_frequency_khz(
    h: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_dense = dense_response(h)
    frequency_khz = omega_dense / (2.0 * np.pi) * sample_rate_hz / 1000.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_khz, np.abs(response_dense), color=SYSTEM_GREEN, lw=3.0)
    style_frequency_khz_axis(
        ax,
        rf"System magnitude response, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$|H(e^{j\Omega})|$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_frequency_48khz.png")


def export_magnitude_response_envelope_frequency_log(
    h: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_dense = dense_response(h)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    audio_band = frequency_hz >= 20.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], np.abs(response_dense)[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_log_axis(
        ax,
        rf"System magnitude response, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$|H(e^{j\Omega})|$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_frequency_48khz_log.png")


def export_magnitude_response_envelope_frequency_loglog(
    h: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_dense = dense_response(h)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    magnitude = np.abs(response_dense)
    audio_band = frequency_hz >= 20.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], magnitude[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_loglog_axis(
        ax,
        rf"System magnitude response, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
        ylabel="Magnitude",
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$|H(e^{j\Omega})|$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_frequency_48khz_loglog.png")


def export_magnitude_response_envelope_frequency_db(
    h: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_dense = dense_response(h)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    magnitude = np.maximum(np.abs(response_dense), 1e-12)
    magnitude_db = 20.0 * np.log10(magnitude)
    audio_band = frequency_hz >= 20.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], magnitude_db[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_db_axis(
        ax,
        rf"System magnitude response, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$20\log_{10}|H(e^{j\Omega})|$"),
        ],
        loc="lower left",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_frequency_48khz_db.png")


def export_magnitude_response_envelope_frequency_db_cutoff(
    h: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_dense = dense_response(h)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    magnitude = np.maximum(np.abs(response_dense), 1e-12)
    magnitude_db = 20.0 * np.log10(magnitude)
    audio_band = frequency_hz >= 20.0
    cutoff_hz = cutoff_frequency_hz(h, sample_rate_hz)
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], magnitude_db[audio_band], color=SYSTEM_GREEN, lw=3.0)
    if np.isfinite(cutoff_hz):
        ax.axvline(cutoff_hz, color="0.35", lw=2.2, ls="--")
    style_frequency_db_axis(
        ax,
        rf"System magnitude response, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$20\log_{10}|H(e^{j\Omega})|$"),
            plt.Line2D([0], [0], color="0.35", lw=2.2, ls="--", label=r"$f_c$ (-3 dB)"),
        ],
        loc="lower left",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_magnitude_response_envelope_frequency_48khz_db_cutoff.png")


def export_truncated_frequency_response_db(
    h_original: np.ndarray,
    h_truncated: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_original = dense_response(h_original)
    _, response_truncated = dense_response(h_truncated)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    audio_band = frequency_hz >= 20.0
    original_db = 20.0 * np.log10(np.maximum(np.abs(response_original), 1e-12))
    truncated_db = 20.0 * np.log10(np.maximum(np.abs(response_truncated), 1e-12))
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], original_db[audio_band], color=REFERENCE_GREY, lw=2.8)
    ax.plot(frequency_hz[audio_band], truncated_db[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_db_axis(
        ax,
        rf"Effect of truncating $h[n]$, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=REFERENCE_GREY, lw=2.8, label=r"$20\log_{10}|H(e^{j\Omega})|$"),
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$20\log_{10}|H_6(e^{j\Omega})|$"),
        ],
        loc="lower left",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, f"{filename_index:02d}_truncated_frequency_response_48khz_db.png")


def export_truncated_frequency_response_comparison_db(
    h_original: np.ndarray,
    h_truncated_6: np.ndarray,
    h_truncated_4: np.ndarray,
    filename_index: int,
    *,
    sample_rate_hz: float,
) -> None:
    omega_dense, response_original = dense_response(h_original)
    _, response_truncated_6 = dense_response(h_truncated_6)
    _, response_truncated_4 = dense_response(h_truncated_4)
    frequency_hz = omega_dense / (2.0 * np.pi) * sample_rate_hz
    audio_band = frequency_hz >= 20.0
    original_db = 20.0 * np.log10(np.maximum(np.abs(response_original), 1e-12))
    truncated_6_db = 20.0 * np.log10(np.maximum(np.abs(response_truncated_6), 1e-12))
    truncated_4_db = 20.0 * np.log10(np.maximum(np.abs(response_truncated_4), 1e-12))
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], original_db[audio_band], color=REFERENCE_GREY, lw=2.8)
    ax.plot(frequency_hz[audio_band], truncated_6_db[audio_band], color="0.45", lw=2.8, ls="--")
    ax.plot(frequency_hz[audio_band], truncated_4_db[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_db_axis(
        ax,
        rf"Effect of truncating $h[n]$, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
    )
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=REFERENCE_GREY, lw=2.8, label=r"$20\log_{10}|H(e^{j\Omega})|$"),
            plt.Line2D([0], [0], color="0.45", lw=2.8, ls="--", label=r"$20\log_{10}|H_6(e^{j\Omega})|$"),
            plt.Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$20\log_{10}|H_4(e^{j\Omega})|$"),
        ],
        loc="lower left",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure_fixed_canvas(fig, f"{filename_index:02d}_truncated_frequency_response_n4_vs_n6_48khz_db.png")


def main() -> None:
    clear_output_dir()
    n, h = lowpass_impulse_response()
    h_truncated_6 = truncate_impulse_response(h, last_sample=6)
    h_truncated_4 = truncate_impulse_response(h, last_sample=4)
    export_impulse_response_wavs(h, h_truncated_6, h_truncated_4)
    export_impulse_response_frame(n, h, 16, 1)
    export_magnitude_response_full_radians(h, 16, 2)
    export_magnitude_response_full(h, 16, 3)
    export_magnitude_response(h, 16, 4)
    export_magnitude_response(h, 16, 5, with_envelope=True, envelope_axis="k")
    export_magnitude_response(h, 16, 6, with_envelope=True)
    export_magnitude_response_normalized_axis(h, 16, "06a")
    export_impulse_response_frame(n, h, 32, 7)
    export_magnitude_response_full_radians(h, 32, "08a", match_one_sided_spacing=True)
    export_magnitude_response_full_omega_axis(h, 32, "08b", match_one_sided_spacing=True)
    export_magnitude_response_full_normalized_axis(h, 32, "08c", match_one_sided_spacing=True)
    export_magnitude_response_full_discrete_frequency_axis(h, 32, "08d", match_one_sided_spacing=True)
    export_magnitude_response(h, 32, 8)
    export_magnitude_response(h, 32, 9, with_envelope=True, envelope_axis="k")
    export_magnitude_response(h, 32, 10, with_envelope=True)
    export_magnitude_response_normalized_axis(h, 32, "10a")
    export_magnitude_response_discrete_frequency_axis_with_envelope(h, 32, "10b")
    export_impulse_response_frame(n, h, 64, 11)
    export_magnitude_response(h, 64, 12)
    export_magnitude_response(h, 64, 13, with_envelope=True, envelope_axis="k")
    export_magnitude_response(h, 64, 14, with_envelope=True)
    export_magnitude_response_normalized_axis(h, 64, "14a")
    export_magnitude_response_envelope_only(h, 15)
    export_magnitude_response_envelope_frequency_ratio(h, 16)
    export_magnitude_response_envelope_frequency_khz(h, 17, sample_rate_hz=48_000.0)
    export_magnitude_response_envelope_frequency_log(h, 18, sample_rate_hz=48_000.0)
    export_magnitude_response_envelope_frequency_loglog(h, 19, sample_rate_hz=48_000.0)
    export_magnitude_response_envelope_frequency_db(h, 20, sample_rate_hz=48_000.0)
    export_magnitude_response_envelope_frequency_db_cutoff(h, 21, sample_rate_hz=48_000.0)
    export_truncated_impulse_response(h_truncated_6, last_sample=6, filename_index=22)
    export_truncated_frequency_response_db(h, h_truncated_6, 23, sample_rate_hz=48_000.0)
    export_truncated_impulse_response(h_truncated_4, last_sample=4, filename_index=24)
    export_truncated_frequency_response_comparison_db(
        h,
        h_truncated_6,
        h_truncated_4,
        25,
        sample_rate_hz=48_000.0,
    )
    match_canvas_to_reference(
        "15_magnitude_response_envelope_only.png",
        [
            "16_magnitude_response_envelope_frequency_ratio.png",
            "17_magnitude_response_envelope_frequency_48khz.png",
            "18_magnitude_response_envelope_frequency_48khz_log.png",
            "19_magnitude_response_envelope_frequency_48khz_loglog.png",
            "20_magnitude_response_envelope_frequency_48khz_db.png",
            "21_magnitude_response_envelope_frequency_48khz_db_cutoff.png",
        ],
    )
    match_canvas_to_reference(
        "20_magnitude_response_envelope_frequency_48khz_db.png",
        [
            "23_truncated_frequency_response_48khz_db.png",
        ],
    )
    match_canvas_to_reference(
        "08a_magnitude_response_full_radians_n32.png",
        [
            "08b_magnitude_response_full_omega_n32.png",
            "08c_magnitude_response_full_normalized_n32.png",
            "08d_magnitude_response_full_frequency_n32.png",
        ],
    )
    match_canvas_to_reference(
        "04_magnitude_response_n16.png",
        [
            "06_magnitude_response_n16_with_envelope.png",
            "06a_magnitude_response_normalized_n16.png",
        ],
    )
    match_canvas_to_reference(
        "08_magnitude_response_n32.png",
        [
            "10_magnitude_response_n32_with_envelope.png",
            "10a_magnitude_response_normalized_n32.png",
            "10b_magnitude_response_frequency_bins_n32_with_envelope.png",
        ],
    )
    match_canvas_to_reference(
        "12_magnitude_response_n64.png",
        [
            "14_magnitude_response_n64_with_envelope.png",
            "14a_magnitude_response_normalized_n64.png",
        ],
    )
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
