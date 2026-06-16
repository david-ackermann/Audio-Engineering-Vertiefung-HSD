from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "02_fir"
OUTPUT_DIR = BLOCK_DIR

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 26
FRAME_TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
OUTPUT_BLUE = "#2b7bbb"
REFERENCE_GREY = "0.72"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class FirConfig:
    output_subdir: str
    title_name: str
    response_title: str
    zero_at: float
    coefficients: tuple[float, float]
    equation: str
    output_formula: str
    impulse_ylim: tuple[float, float]
    impulse_yticks: list[float]


FILTER_CONFIGS = (
    FirConfig(
        output_subdir="02A_tiefpass",
        title_name="low-pass",
        response_title=r"Two-tap FIR low-pass, zero at $\Omega/\pi=1$",
        zero_at=1.0,
        coefficients=(0.5, 0.5),
        equation=r"$y[n]=0.5\,x[n]+0.5\,x[n-1]$",
        output_formula=r"0.5x[{n}]+0.5x[{prev}]",
        impulse_ylim=(-0.62, 0.62),
        impulse_yticks=[-0.5, 0.0, 0.5],
    ),
    FirConfig(
        output_subdir="02B_hochpass",
        title_name="high-pass",
        response_title=r"Two-tap FIR high-pass, zero at $\Omega/\pi=0$",
        zero_at=0.0,
        coefficients=(0.5, -0.5),
        equation=r"$y[n]=0.5\,x[n]-0.5\,x[n-1]$",
        output_formula=r"0.5x[{n}]-0.5x[{prev}]",
        impulse_ylim=(-0.62, 0.62),
        impulse_yticks=[-0.5, 0.0, 0.5],
    ),
)

NOTCH_OUTPUT_DIR = "02C_notch"
NOTCH_FREQUENCY_NORMALIZED = 0.5
NOTCH_TIME_SUBPLOT = {"left": 0.10, "right": 0.98, "bottom": 0.18, "top": 0.84}
LOWPASS_DESIGN_OUTPUT_DIR = "02D_lowpass_design"
LOWPASS_DESIGN_TAPS = (256, 128, 64, 32, 16, 8)
LOWPASS_DESIGN_LARGE_COEFFICIENT_TAPS = 32768
LOWPASS_DESIGN_EXTRA_DB_TAPS = (4096, 8192, 32768)
LOWPASS_CUTOFF_NORMALIZED = 0.5
LOWPASS_DESIGN_TIME_FIGSIZE = (FIGSIZE[0] * 2.0, FIGSIZE[1])
LOWPASS_DESIGN_TIME_SUBPLOT = {"left": 0.12, "right": 0.98, "bottom": 0.18, "top": 0.84}
LOWPASS_DESIGN_TIME_XLIM = (-136.0, 136.0)
LOWPASS_DESIGN_TIME_XTICKS = [-136, -96, -64, -32, 0, 32, 64, 96, 136]
LOWPASS_DESIGN_MAGNITUDE_YLIM = (-0.08, 1.35)
LOWPASS_DESIGN_MAGNITUDE_YTICKS = [0.0, 0.5, 1.0]
LOWPASS_DESIGN_DB_FLOOR = 1e-4
LOWPASS_DESIGN_DB_YLIM = (-80.0, 6.0)
LOWPASS_DESIGN_DB_YTICKS = [-80, -60, -40, -20, 0]
LOWPASS_DESIGN_GROUP_DELAY_YLIM = (-5.0, 135.0)
LOWPASS_DESIGN_GROUP_DELAY_YTICKS = [0, 32, 64, 96, 128]


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.rglob("*.png"):
        try:
            image_file.unlink()
        except PermissionError:
            print(f"Skipped locked file: {image_file}")


def set_output_dir(path: Path) -> None:
    global OUTPUT_DIR
    OUTPUT_DIR = path
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig, filename: str) -> None:
    output_path = OUTPUT_DIR / filename
    try:
        fig.savefig(output_path, dpi=DPI, facecolor="white", bbox_inches="tight")
    except PermissionError:
        print(f"Skipped locked output file: {output_path}")
    finally:
        plt.close(fig)


def save_figure_fixed_canvas(fig, filename: str) -> None:
    output_path = OUTPUT_DIR / filename
    try:
        fig.savefig(output_path, dpi=DPI, facecolor="white")
    except PermissionError:
        print(f"Skipped locked output file: {output_path}")
    finally:
        plt.close(fig)


def fir_coefficients(config: FirConfig) -> np.ndarray:
    return np.array(config.coefficients, dtype=float)


def notch_coefficients() -> np.ndarray:
    return np.array([1.0, 0.0, 3.0, 0.0, 3.0, 0.0, 1.0], dtype=float) / 8.0


def lowpass_design_coefficients(num_taps: int) -> np.ndarray:
    n = np.arange(num_taps)
    center = 0.5 * (num_taps - 1)
    h = LOWPASS_CUTOFF_NORMALIZED * np.sinc(LOWPASS_CUTOFF_NORMALIZED * (n - center))
    return h / np.sum(h)


def ideal_lowpass_impulse_response(sample_offset: np.ndarray) -> np.ndarray:
    return LOWPASS_CUTOFF_NORMALIZED * np.sinc(LOWPASS_CUTOFF_NORMALIZED * sample_offset)


def fir_filter(x: np.ndarray, b: np.ndarray) -> np.ndarray:
    y = np.zeros_like(x, dtype=float)
    for n in range(x.size):
        for k, coefficient in enumerate(b):
            if n - k >= 0:
                y[n] += coefficient * x[n - k]
    return y


def dense_response(b: np.ndarray, num_points: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, np.pi, num_points)
    n = np.arange(b.size)
    response = np.exp(-1j * np.outer(omega, n)) @ b
    return omega, response


def one_sided_fft_response(b: np.ndarray, *, min_fft_size: int = 65_536, oversampling: int = 16) -> tuple[np.ndarray, np.ndarray]:
    target_size = max(min_fft_size, b.size * oversampling)
    fft_size = 1 << (target_size - 1).bit_length()
    response = np.fft.rfft(b, n=fft_size)
    omega_norm = np.linspace(0.0, 1.0, response.size)
    return omega_norm, response


def dense_phase_response(b: np.ndarray, num_points: int = 4096) -> tuple[np.ndarray, np.ndarray]:
    omega = np.linspace(1e-6, np.pi - 1e-6, num_points)
    n = np.arange(b.size)
    response = np.exp(-1j * np.outer(omega, n)) @ b
    return omega, np.unwrap(np.angle(response))


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


def style_time_axis(
    ax,
    title: str,
    *,
    n_max: int,
    ylabel: str,
    ylim: tuple[float, float] = (-1.2, 1.2),
    yticks: list[float] | None = None,
    title_size: int = TITLE_SIZE,
) -> None:
    if yticks is None:
        yticks = [-1.0, 0.0, 1.0]
    if title:
        ax.set_title(title, fontsize=title_size, pad=10)
    ax.set_xlim(-0.5, n_max + 0.5)
    ax.set_ylim(*ylim)
    ax.set_xticks(np.arange(0, n_max + 1, 1))
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def arrow(ax, xy_a: tuple[float, float], xy_b: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            xy_a,
            xy_b,
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.8,
            color=SIGNAL_BLACK,
        )
    )


def block(ax, xy: tuple[float, float], text: str, *, width: float = 0.95, height: float = 0.58) -> None:
    rect = Rectangle(
        (xy[0] - width / 2, xy[1] - height / 2),
        width,
        height,
        facecolor="white",
        edgecolor=SIGNAL_BLACK,
        linewidth=1.7,
    )
    ax.add_patch(rect)
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=18)


def export_fir_structure(config: FirConfig) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title(f"Two-tap FIR {config.title_name}", fontsize=TITLE_SIZE, pad=14)

    b0, b1 = config.coefficients
    b0_label = f"{b0:.1f}"
    b1_label = f"{b1:.1f}"

    ax.text(0.55, 3.45, r"$x[n]$", fontsize=23, va="center")
    arrow(ax, (1.1, 3.4), (2.0, 3.4))
    block(ax, (3.0, 3.4), "delay")
    arrow(ax, (3.5, 3.4), (4.65, 3.4))
    ax.text(4.82, 3.45, r"$x[n-1]$", fontsize=22, va="center")

    block(ax, (2.0, 1.75), rf"${b0_label}$")
    block(ax, (5.0, 2.75), rf"${b1_label}$")
    ax.plot([2.0, 2.0], [3.4, 2.04], color=SIGNAL_BLACK, lw=1.6)
    ax.plot([5.0, 5.0], [3.4, 3.04], color=SIGNAL_BLACK, lw=1.6)

    ax.add_patch(Circle((7.25, 2.2), radius=0.35, facecolor="white", edgecolor=SIGNAL_BLACK, linewidth=1.8))
    ax.text(7.25, 2.2, r"$\Sigma$", ha="center", va="center", fontsize=23)
    arrow(ax, (2.5, 1.75), (6.88, 2.08))
    arrow(ax, (5.5, 2.75), (6.88, 2.32))
    arrow(ax, (7.60, 2.2), (8.9, 2.2))
    ax.text(9.05, 2.28, r"$y[n]$", fontsize=23, va="center")

    ax.text(5.0, 0.45, config.equation, ha="center", fontsize=25)
    save_figure(fig, "01_two_tap_fir_structure.png")


def export_impulse_response(config: FirConfig) -> None:
    b = fir_coefficients(config)
    n = np.arange(8)
    h = np.zeros_like(n, dtype=float)
    h[: b.size] = b
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    style_time_axis(
        ax,
        rf"Impulse response of the two-tap FIR {config.title_name}, $N=8$",
        n_max=n[-1],
        ylabel="Amplitude",
        ylim=config.impulse_ylim,
        yticks=config.impulse_yticks,
    )
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    save_figure_fixed_canvas(fig, "02_two_tap_fir_impulse_response.png")


def export_dirac_input() -> None:
    n = np.arange(8)
    x = np.zeros_like(n, dtype=float)
    x[0] = 1.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    stem_sequence(ax, n, x, color=SIGNAL_BLACK, marker_size=7.5, line_width=2.4)
    style_time_axis(
        ax,
        r"Dirac impulse as input signal $\delta[n]$",
        n_max=n[-1],
        ylabel=r"$x[n]$",
        ylim=(-0.2, 1.2),
        yticks=[0.0, 0.5, 1.0],
        title_size=FRAME_TITLE_SIZE,
    )
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    save_figure_fixed_canvas(fig, "08_dirac_input_signal.png")


def export_frequency_response(config: FirConfig) -> None:
    b = fir_coefficients(config)
    omega, response = dense_response(b)
    magnitude = np.abs(response)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, magnitude, color=SYSTEM_GREEN, lw=3.0)
    ax.axvline(config.zero_at, color="0.35", lw=2.0, ls="--")
    ax.set_title(config.response_title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.04, 1.08)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    ax.set_yticks([0.0, 0.5, 0.707, 1.0])
    ax.set_yticklabels(["0", "0.5", "0.707", "1"])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, "03_two_tap_fir_frequency_response.png")


def export_frequency_response_normalized_db(config: FirConfig) -> None:
    b = fir_coefficients(config)
    omega, response = dense_response(b)
    magnitude = np.maximum(np.abs(response), 1e-3)
    magnitude_db = 20.0 * np.log10(magnitude)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, magnitude_db, color=SYSTEM_GREEN, lw=3.0)
    ax.axvline(config.zero_at, color="0.35", lw=2.0, ls="--")
    ax.set_title(rf"Two-tap FIR {config.title_name} magnitude", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-24.0, 0.0)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    ax.set_yticks([-24, -18, -12, -6, 0])
    ax.set_yticklabels(["-24", "-18", "-12", "-6", "0"])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, "04_two_tap_fir_frequency_response_db.png")


def export_phase_response_normalized(config: FirConfig) -> None:
    b = fir_coefficients(config)
    omega, phase = dense_phase_response(b)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, phase, color=SYSTEM_GREEN, lw=3.0)
    ax.set_title(rf"Two-tap FIR {config.title_name} phase", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-np.pi / 2.0 - 0.15, np.pi / 2.0 + 0.15)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    ax.set_yticks([-np.pi / 2.0, -np.pi / 4.0, 0.0, np.pi / 4.0, np.pi / 2.0])
    ax.set_yticklabels([r"$-\pi/2$", r"$-\pi/4$", "0", r"$\pi/4$", r"$\pi/2$"])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Phase [rad]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, "05_two_tap_fir_phase_response_normalized.png")


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


def style_frequency_db_axis(ax, title: str, *, sample_rate_hz: float) -> None:
    nyquist_hz = sample_rate_hz / 2.0
    ticks_hz = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    tick_labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(20.0, nyquist_hz)
    ax.set_ylim(-24.0, 0.0)
    ax.set_xticks(ticks_hz)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([-24, -18, -12, -6, 0])
    ax.set_yticklabels(["-24", "-18", "-12", "-6", "0"])
    ax.set_xlabel(r"Frequency $f$ [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25, which="both")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_frequency_response_log(config: FirConfig, *, sample_rate_hz: float = 48_000.0) -> None:
    b = fir_coefficients(config)
    omega, response = dense_response(b, num_points=4096)
    frequency_hz = omega / (2.0 * np.pi) * sample_rate_hz
    audio_band = frequency_hz >= 20.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], np.abs(response)[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_log_axis(
        ax,
        rf"Two-tap FIR {config.title_name}, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    save_figure_fixed_canvas(fig, "06_two_tap_fir_frequency_response_48khz_log.png")


def export_frequency_response_db(config: FirConfig, *, sample_rate_hz: float = 48_000.0) -> None:
    b = fir_coefficients(config)
    omega, response = dense_response(b, num_points=4096)
    frequency_hz = omega / (2.0 * np.pi) * sample_rate_hz
    magnitude = np.maximum(np.abs(response), 1e-3)
    magnitude_db = 20.0 * np.log10(magnitude)
    audio_band = frequency_hz >= 20.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], magnitude_db[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_frequency_db_axis(
        ax,
        rf"Two-tap FIR {config.title_name}, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
    )
    save_figure_fixed_canvas(fig, "07_two_tap_fir_frequency_response_48khz_db.png")


def style_phase_frequency_axis(
    ax,
    title: str,
    *,
    sample_rate_hz: float,
    log_frequency: bool,
) -> None:
    nyquist_hz = sample_rate_hz / 2.0
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    if log_frequency:
        ticks_hz = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        tick_labels = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
        ax.set_xscale("log")
        ax.set_xlim(20.0, nyquist_hz)
        ax.set_xticks(ticks_hz)
        ax.set_xticklabels(tick_labels)
        grid_mode = "both"
    else:
        ax.set_xlim(0.0, nyquist_hz)
        ax.set_xticks([0, 4000, 8000, 12000, 16000, 20000, 24000])
        ax.set_xticklabels(["0", "4k", "8k", "12k", "16k", "20k", "24k"])
        grid_mode = "major"
    ax.set_ylim(-np.pi / 2.0 - 0.15, np.pi / 2.0 + 0.15)
    ax.set_yticks([-np.pi / 2.0, -np.pi / 4.0, 0.0, np.pi / 4.0, np.pi / 2.0])
    ax.set_yticklabels([r"$-\pi/2$", r"$-\pi/4$", "0", r"$\pi/4$", r"$\pi/2$"])
    ax.set_xlabel(r"Frequency $f$ [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Phase [rad]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25, which=grid_mode)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_phase_response_linear(config: FirConfig, *, sample_rate_hz: float = 48_000.0) -> None:
    b = fir_coefficients(config)
    omega, phase = dense_phase_response(b)
    frequency_hz = omega / (2.0 * np.pi) * sample_rate_hz
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz, phase, color=SYSTEM_GREEN, lw=3.0)
    style_phase_frequency_axis(
        ax,
        rf"Two-tap FIR {config.title_name} phase, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
        log_frequency=False,
    )
    save_figure_fixed_canvas(fig, "09_two_tap_fir_phase_response_48khz_linear.png")


def export_phase_response_log(config: FirConfig, *, sample_rate_hz: float = 48_000.0) -> None:
    b = fir_coefficients(config)
    omega, phase = dense_phase_response(b)
    frequency_hz = omega / (2.0 * np.pi) * sample_rate_hz
    audio_band = frequency_hz >= 20.0
    sample_rate_khz = sample_rate_hz / 1000.0

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(frequency_hz[audio_band], phase[audio_band], color=SYSTEM_GREEN, lw=3.0)
    style_phase_frequency_axis(
        ax,
        rf"Two-tap FIR {config.title_name} phase, $f_s={sample_rate_khz:g}$ kHz",
        sample_rate_hz=sample_rate_hz,
        log_frequency=True,
    )
    save_figure_fixed_canvas(fig, "10_two_tap_fir_phase_response_48khz_log.png")


def export_notch_empty_impulse_response() -> None:
    n = np.arange(8)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**NOTCH_TIME_SUBPLOT)
    style_time_axis(
        ax,
        "Impulse response",
        n_max=n[-1],
        ylabel="Value",
        ylim=(-0.05, 0.42),
        yticks=[0.0, 0.125, 0.25, 0.375],
    )
    ax.set_yticklabels(["0", "1/8", "1/4", "3/8"])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    save_figure_fixed_canvas(fig, "01_fir_notch_impulse_response_empty.png")


def export_notch_impulse_response() -> None:
    b = notch_coefficients()
    n = np.arange(8)
    h = np.zeros_like(n, dtype=float)
    h[: b.size] = b

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**NOTCH_TIME_SUBPLOT)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    style_time_axis(
        ax,
        r"Narrowband FIR notch impulse response, $N=8$",
        n_max=n[-1],
        ylabel="Value",
        ylim=(-0.05, 0.42),
        yticks=[0.0, 0.125, 0.25, 0.375],
    )
    ax.set_yticklabels(["0", "1/8", "1/4", "3/8"])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    save_figure_fixed_canvas(fig, "02_fir_notch_impulse_response.png")


def export_notch_coefficient_view() -> None:
    b = notch_coefficients()
    n = np.arange(8)
    h = np.zeros_like(n, dtype=float)
    h[: b.size] = b

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**NOTCH_TIME_SUBPLOT)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    style_time_axis(
        ax,
        r"Narrowband FIR notch coefficients, $N=8$",
        n_max=n[-1],
        ylabel="Value",
        ylim=(-0.05, 0.42),
        yticks=[0.0, 0.125, 0.25, 0.375],
    )
    ax.set_yticklabels(["0", "1/8", "1/4", "3/8"])
    ax.set_xticklabels([rf"$b_{index}$" for index in n])
    ax.set_xlabel(r"FIR coefficient $b_k$", fontsize=LABEL_SIZE)
    save_figure_fixed_canvas(fig, "03_fir_notch_coefficient_view.png")


def export_notch_frequency_response() -> None:
    b = notch_coefficients()
    omega, response = dense_response(b, num_points=8192)
    magnitude = np.abs(response)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, magnitude, color=SYSTEM_GREEN, lw=3.0)
    ax.axvline(NOTCH_FREQUENCY_NORMALIZED, color="0.35", lw=2.0, ls="--")
    ax.set_title(r"Narrowband FIR notch magnitude", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.04, 1.08)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, "04_fir_notch_magnitude_response.png")


def export_notch_frequency_response_db() -> None:
    b = notch_coefficients()
    omega, response = dense_response(b, num_points=8192)
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response), 1e-4))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega / np.pi, magnitude_db, color=SYSTEM_GREEN, lw=3.0)
    ax.axvline(NOTCH_FREQUENCY_NORMALIZED, color="0.35", lw=2.0, ls="--")
    ax.set_title(r"Narrowband FIR notch magnitude [dB]", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-80.0, 6.0)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([-80, -60, -40, -20, 0])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, "05_fir_notch_magnitude_response_db.png")


def export_notch_filter() -> None:
    set_output_dir(BLOCK_DIR / NOTCH_OUTPUT_DIR)
    export_notch_empty_impulse_response()
    export_notch_impulse_response()
    export_notch_coefficient_view()
    export_notch_frequency_response()
    export_notch_frequency_response_db()


def export_ideal_lowpass_frequency_response(figure_number: int) -> None:
    omega_norm = np.array([0.0, LOWPASS_CUTOFF_NORMALIZED, LOWPASS_CUTOFF_NORMALIZED, 1.0])
    magnitude = np.array([1.0, 1.0, 0.0, 0.0])

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(omega_norm, magnitude, color=SYSTEM_GREEN, lw=3.2)
    ax.axvline(LOWPASS_CUTOFF_NORMALIZED, color="0.35", lw=1.8, ls=":")
    ax.set_title(r"Ideal low-pass magnitude", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(*LOWPASS_DESIGN_MAGNITUDE_YLIM)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks(LOWPASS_DESIGN_MAGNITUDE_YTICKS)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_ideal_lowpass_magnitude.png")


def export_ideal_lowpass_sinc_response(figure_number: int) -> None:
    n_dense = np.linspace(*LOWPASS_DESIGN_TIME_XLIM, 7000)
    n_samples = np.arange(-136, 137)

    fig, ax = plt.subplots(figsize=LOWPASS_DESIGN_TIME_FIGSIZE)
    fig.subplots_adjust(**LOWPASS_DESIGN_TIME_SUBPLOT)
    ax.plot(n_dense, ideal_lowpass_impulse_response(n_dense), color=REFERENCE_GREY, lw=2.8, zorder=1)
    sample_marker, sample_stems, baseline = ax.stem(n_samples, ideal_lowpass_impulse_response(n_samples))
    sample_marker.set_markerfacecolor(SYSTEM_GREEN)
    sample_marker.set_markeredgecolor("white")
    sample_marker.set_markeredgewidth(0.7)
    sample_marker.set_markersize(5.2)
    sample_marker.set_alpha(0.92)
    sample_stems.set_color(SYSTEM_GREEN)
    sample_stems.set_linewidth(1.1)
    sample_stems.set_alpha(0.72)
    baseline.set_color(SIGNAL_BLACK)
    baseline.set_linewidth(1.2)
    ax.set_title("Ideal discrete-time impulse response", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlim(*LOWPASS_DESIGN_TIME_XLIM)
    ax.set_ylim(-0.58, 0.58)
    ax.set_xticks(LOWPASS_DESIGN_TIME_XTICKS)
    ax.set_yticks([-0.5, -0.25, 0.0, 0.25, 0.5])
    ax.set_xlabel(r"Discrete-time index $n$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$h_\mathrm{ideal}[n]$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_ideal_lowpass_sinc_response.png")


def coefficient_tick_indices(num_taps: int) -> np.ndarray:
    if num_taps <= 8:
        indices = np.array([0])
    elif num_taps <= 16:
        indices = np.array([0, num_taps // 2])
    elif num_taps <= 32:
        indices = np.arange(0, num_taps, 8)
    elif num_taps <= 64:
        indices = np.arange(0, num_taps, 16)
    elif num_taps <= 128:
        indices = np.arange(0, num_taps, 16)
    else:
        indices = np.arange(0, num_taps, 32)
    return np.unique(np.append(indices, num_taps - 1))


def coefficient_tick_positions(num_taps: int) -> tuple[np.ndarray, list[str]]:
    indices = coefficient_tick_indices(num_taps)
    positions = indices - 0.5 * (num_taps - 1)
    labels = [rf"$b_{{{index}}}$" for index in indices]
    return positions, labels


def style_lowpass_design_time_axis(ax, *, num_taps: int, title: str) -> None:
    tick_positions, tick_labels = coefficient_tick_positions(num_taps)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlim(*LOWPASS_DESIGN_TIME_XLIM)
    ax.set_ylim(-0.58, 0.58)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([-0.5, -0.25, 0.0, 0.25, 0.5])
    ax.set_xlabel(r"FIR coefficients", fontsize=LABEL_SIZE)
    ax.set_ylabel("Value", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def visible_large_coefficient_indices(num_taps: int) -> tuple[int, int]:
    center = 0.5 * (num_taps - 1)
    left_index = int(np.ceil(center + LOWPASS_DESIGN_TIME_XLIM[0]))
    right_index = int(np.floor(center + LOWPASS_DESIGN_TIME_XLIM[1]))
    return left_index, right_index


def style_lowpass_design_large_time_axis(ax, *, num_taps: int, title: str) -> None:
    center = 0.5 * (num_taps - 1)
    left_index, right_index = visible_large_coefficient_indices(num_taps)
    tick_indices = np.array([left_index, num_taps // 2, right_index])
    tick_positions = tick_indices - center
    tick_labels = [rf"$b_{{{index}}}$" for index in tick_indices]

    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlim(*LOWPASS_DESIGN_TIME_XLIM)
    ax.set_ylim(-0.58, 0.58)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([-0.5, -0.25, 0.0, 0.25, 0.5])
    ax.set_xlabel(r"FIR coefficients", fontsize=LABEL_SIZE)
    ax.set_ylabel("Value", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_lowpass_design_impulse_response(num_taps: int, figure_number: int) -> None:
    h = lowpass_design_coefficients(num_taps)
    n = np.arange(num_taps, dtype=float) - 0.5 * (num_taps - 1)
    left_edge = -0.5 * num_taps
    right_edge = 0.5 * num_taps

    fig, ax = plt.subplots(figsize=LOWPASS_DESIGN_TIME_FIGSIZE)
    fig.subplots_adjust(**LOWPASS_DESIGN_TIME_SUBPLOT)
    ax.axvline(left_edge, color="0.35", lw=2.0, ls="--", zorder=1)
    ax.axvline(right_edge, color="0.35", lw=2.0, ls="--", zorder=1)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN, marker_size=7.2, line_width=2.5)
    style_lowpass_design_time_axis(
        ax,
        num_taps=num_taps,
        title=rf"Low-pass FIR coefficients, {num_taps} taps",
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_coefficients_{num_taps:02d}_taps.png")


def export_lowpass_design_impulse_response_with_rectangular_window(num_taps: int, figure_number: int) -> None:
    h = lowpass_design_coefficients(num_taps)
    n = np.arange(num_taps, dtype=float) - 0.5 * (num_taps - 1)
    left_edge = -0.5 * num_taps
    right_edge = 0.5 * num_taps
    window_height = 0.5

    fig, ax = plt.subplots(figsize=LOWPASS_DESIGN_TIME_FIGSIZE)
    fig.subplots_adjust(**LOWPASS_DESIGN_TIME_SUBPLOT)
    ax.fill_between(
        [left_edge, right_edge],
        [0.0, 0.0],
        [window_height, window_height],
        color=SYSTEM_GREEN,
        alpha=0.14,
        step="post",
        zorder=0,
    )
    ax.plot(
        [left_edge, left_edge, right_edge, right_edge],
        [0.0, window_height, window_height, 0.0],
        color=SYSTEM_GREEN,
        lw=2.8,
        ls="--",
        zorder=2,
    )
    ax.axvline(left_edge, color="0.35", lw=2.0, ls="--", zorder=1)
    ax.axvline(right_edge, color="0.35", lw=2.0, ls="--", zorder=1)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN, marker_size=7.2, line_width=2.5)
    style_lowpass_design_time_axis(
        ax,
        num_taps=num_taps,
        title=rf"Low-pass FIR coefficients with rectangular window, {num_taps} taps",
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_coefficients_{num_taps:02d}_taps_rectangular_window.png")


def export_lowpass_design_large_impulse_response(num_taps: int, figure_number: int) -> None:
    h = lowpass_design_coefficients(num_taps)
    center = 0.5 * (num_taps - 1)
    left_index, right_index = visible_large_coefficient_indices(num_taps)
    visible_indices = np.arange(left_index, right_index + 1)
    n_visible = visible_indices - center
    h_visible = h[visible_indices]
    left_hidden_range = rf"$b_0 \ldots b_{{{left_index - 1}}}$"
    right_hidden_range = rf"$b_{{{right_index + 1}}} \ldots b_{{{num_taps - 1}}}$"

    fig, ax = plt.subplots(figsize=LOWPASS_DESIGN_TIME_FIGSIZE)
    fig.subplots_adjust(**LOWPASS_DESIGN_TIME_SUBPLOT)
    stem_sequence(ax, n_visible, h_visible, color=SYSTEM_GREEN, marker_size=7.2, line_width=2.5)
    style_lowpass_design_large_time_axis(
        ax,
        num_taps=num_taps,
        title=rf"Low-pass FIR coefficients, {num_taps} taps",
    )
    ax.annotate(
        "",
        xy=(-134.0, -0.34),
        xytext=(-111.0, -0.34),
        arrowprops={"arrowstyle": "->", "color": "0.35", "lw": 2.0},
        zorder=5,
    )
    ax.annotate(
        "",
        xy=(134.0, -0.34),
        xytext=(111.0, -0.34),
        arrowprops={"arrowstyle": "->", "color": "0.35", "lw": 2.0},
        zorder=5,
    )
    ax.text(-110.0, -0.42, left_hidden_range, color="0.35", fontsize=15, ha="left", va="center")
    ax.text(110.0, -0.42, right_hidden_range, color="0.35", fontsize=15, ha="right", va="center")
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_coefficients_{num_taps}_taps_center_view.png")


def export_lowpass_design_group_delay(num_taps: int, figure_number: int, previous_taps: tuple[int, ...]) -> None:
    group_delay = 0.5 * (num_taps - 1)
    x = np.array([0.0, 1.0])

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    for previous_num_taps in previous_taps:
        previous_group_delay = 0.5 * (previous_num_taps - 1)
        ax.plot(
            x,
            [previous_group_delay, previous_group_delay],
            color=lowpass_history_gray(previous_num_taps),
            lw=2.7,
            alpha=0.88,
            zorder=2,
        )

    ax.plot(x, [group_delay, group_delay], color=SYSTEM_GREEN, lw=3.2, zorder=4)
    ax.set_title(rf"Low-pass FIR group delay, {num_taps} taps", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(*LOWPASS_DESIGN_GROUP_DELAY_YLIM)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks(LOWPASS_DESIGN_GROUP_DELAY_YTICKS)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Group delay [samples]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_group_delay_{num_taps:02d}_taps.png")


def style_lowpass_design_frequency_axis(ax, *, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(*LOWPASS_DESIGN_MAGNITUDE_YLIM)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks(LOWPASS_DESIGN_MAGNITUDE_YTICKS)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axvline(LOWPASS_CUTOFF_NORMALIZED, color="0.35", lw=1.8, ls=":")
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_lowpass_design_db_axis(ax, *, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(*LOWPASS_DESIGN_DB_YLIM)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks(LOWPASS_DESIGN_DB_YTICKS)
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axvline(LOWPASS_CUTOFF_NORMALIZED, color="0.35", lw=1.8, ls=":")
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def plot_lowpass_design_response(
    ax,
    *,
    num_taps: int,
    color: str,
    line_style: str = "-",
    line_width: float = 3.0,
    alpha: float = 1.0,
    zorder: int = 3,
) -> None:
    omega, response = dense_response(lowpass_design_coefficients(num_taps), num_points=8192)
    ax.plot(
        omega / np.pi,
        np.abs(response),
        color=color,
        lw=line_width,
        ls=line_style,
        alpha=alpha,
        zorder=zorder,
        label=f"{num_taps} taps",
    )


def plot_lowpass_design_response_db(
    ax,
    *,
    num_taps: int,
    color: str,
    line_style: str = "-",
    line_width: float = 3.0,
    alpha: float = 1.0,
    zorder: int = 3,
) -> None:
    omega, response = dense_response(lowpass_design_coefficients(num_taps), num_points=8192)
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response), LOWPASS_DESIGN_DB_FLOOR))
    ax.plot(
        omega / np.pi,
        magnitude_db,
        color=color,
        lw=line_width,
        ls=line_style,
        alpha=alpha,
        zorder=zorder,
        label=f"{num_taps} taps",
    )


def plot_lowpass_design_response_db_fft(
    ax,
    *,
    num_taps: int,
    color: str,
    line_style: str = "-",
    line_width: float = 3.0,
    alpha: float = 1.0,
    zorder: int = 3,
) -> None:
    omega_norm, response = one_sided_fft_response(lowpass_design_coefficients(num_taps))
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response), LOWPASS_DESIGN_DB_FLOOR))
    ax.plot(
        omega_norm,
        magnitude_db,
        color=color,
        lw=line_width,
        ls=line_style,
        alpha=alpha,
        zorder=zorder,
        label=f"{num_taps} taps",
    )


def lowpass_history_gray(num_taps: int) -> str:
    gray_levels = {
        256: "0.30",
        128: "0.42",
        64: "0.55",
        32: "0.68",
        16: "0.80",
        8: "0.88",
    }
    return gray_levels[num_taps]


def export_lowpass_design_frequency_response(figure_number: int, active_taps: int, previous_taps: tuple[int, ...]) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    for num_taps in previous_taps:
        plot_lowpass_design_response(
            ax,
            num_taps=num_taps,
            color=lowpass_history_gray(num_taps),
            line_style="-",
            line_width=2.7,
            alpha=0.88,
            zorder=2,
        )
    plot_lowpass_design_response(ax, num_taps=active_taps, color=SYSTEM_GREEN, line_width=3.2, zorder=4)
    style_lowpass_design_frequency_axis(
        ax,
        title=rf"Low-pass FIR magnitude, $\Omega_c/\pi=0.5$",
    )
    ax.legend(loc="upper right", fontsize=15, frameon=True)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_magnitude_{active_taps:02d}_taps.png")


def export_lowpass_design_frequency_response_db(figure_number: int, active_taps: int, previous_taps: tuple[int, ...]) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    for num_taps in previous_taps:
        plot_lowpass_design_response_db(
            ax,
            num_taps=num_taps,
            color=lowpass_history_gray(num_taps),
            line_style="-",
            line_width=2.7,
            alpha=0.88,
            zorder=2,
        )
    plot_lowpass_design_response_db(ax, num_taps=active_taps, color=SYSTEM_GREEN, line_width=3.2, zorder=4)
    style_lowpass_design_db_axis(
        ax,
        title=rf"Low-pass FIR magnitude [dB], $\Omega_c/\pi=0.5$",
    )
    ax.legend(loc="upper right", fontsize=15, frameon=True)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_magnitude_db_{active_taps:02d}_taps.png")


def export_lowpass_design_extra_frequency_response_db(figure_number: int, num_taps: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    plot_lowpass_design_response_db_fft(
        ax,
        num_taps=num_taps,
        color=SYSTEM_GREEN,
        line_width=3.2,
        zorder=4,
    )
    style_lowpass_design_db_axis(
        ax,
        title=rf"Low-pass FIR magnitude [dB], $\Omega_c/\pi=0.5$",
    )
    ax.legend(loc="upper right", fontsize=15, frameon=True)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_lowpass_magnitude_db_{num_taps}_taps.png")


def export_lowpass_design_filter() -> None:
    set_output_dir(BLOCK_DIR / LOWPASS_DESIGN_OUTPUT_DIR)
    figure_number = 1
    export_ideal_lowpass_frequency_response(figure_number)
    figure_number += 1
    export_ideal_lowpass_sinc_response(figure_number)
    figure_number += 1

    for tap_index, num_taps in enumerate(LOWPASS_DESIGN_TAPS):
        previous_taps = LOWPASS_DESIGN_TAPS[:tap_index]
        export_lowpass_design_impulse_response(num_taps, figure_number)
        figure_number += 1
        if num_taps == LOWPASS_DESIGN_TAPS[0]:
            export_lowpass_design_impulse_response_with_rectangular_window(num_taps, figure_number)
            figure_number += 1
            export_lowpass_design_large_impulse_response(LOWPASS_DESIGN_LARGE_COEFFICIENT_TAPS, figure_number)
            figure_number += 1
        export_lowpass_design_group_delay(num_taps, figure_number, previous_taps)
        figure_number += 1

    for tap_index, active_taps in enumerate(LOWPASS_DESIGN_TAPS):
        previous_taps = LOWPASS_DESIGN_TAPS[:tap_index]
        export_lowpass_design_frequency_response(figure_number, active_taps, previous_taps)
        figure_number += 1

    for tap_index, active_taps in enumerate(LOWPASS_DESIGN_TAPS):
        previous_taps = LOWPASS_DESIGN_TAPS[:tap_index]
        export_lowpass_design_frequency_response_db(figure_number, active_taps, previous_taps)
        figure_number += 1

    for num_taps in LOWPASS_DESIGN_EXTRA_DB_TAPS:
        export_lowpass_design_extra_frequency_response_db(figure_number, num_taps)
        figure_number += 1


def input_sequences(num_samples: int = 8) -> dict[str, tuple[str, np.ndarray]]:
    n = np.arange(num_samples)
    return {
        "dc": ("DC input", np.ones(num_samples)),
        "nyquist": (r"Nyquist input, $\Omega/\pi=1$", (-1.0) ** n),
        "half_nyquist": (r"Half-Nyquist input, $\Omega/\pi=0.5$", np.cos(0.5 * np.pi * n)),
    }


def continuous_input(sequence_key: str, t: np.ndarray) -> np.ndarray:
    if sequence_key == "dc":
        return np.ones_like(t)
    if sequence_key == "nyquist":
        return np.cos(np.pi * t)
    if sequence_key == "half_nyquist":
        return np.cos(0.5 * np.pi * t)
    raise ValueError(f"Unknown sequence key: {sequence_key}")


def continuous_output(config: FirConfig, sequence_key: str, t: np.ndarray) -> np.ndarray:
    b0, b1 = config.coefficients
    current = continuous_input(sequence_key, t)
    delayed = continuous_input(sequence_key, t - 1.0)
    return b0 * current + b1 * delayed


def plot_partial_stems(
    ax,
    indices: np.ndarray,
    values: np.ndarray,
    *,
    color: str,
    marker_size: float = 7.0,
    alpha: float = 1.0,
    line_width: float = 2.2,
    line_style: str = "-",
) -> None:
    if indices.size == 0:
        return
    ax.vlines(indices, 0.0, values, color=color, lw=line_width, alpha=alpha, linestyles=line_style)
    ax.scatter(indices, values, s=marker_size**2, color=color, edgecolor="white", linewidth=0.9, zorder=3, alpha=alpha)


def setup_sequence_axis(ax, *, title: str, ylabel: str, n_max: int) -> None:
    style_time_axis(ax, title, n_max=n_max, ylabel=ylabel, title_size=FRAME_TITLE_SIZE)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)


def export_full_input(
    *,
    sequence_key: str,
    sequence_title: str,
    x: np.ndarray,
    figure_number: int,
) -> None:
    n_all = np.arange(x.size)
    t_dense = np.linspace(0.0, x.size - 1, 600)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    ax.plot(t_dense, continuous_input(sequence_key, t_dense), color=REFERENCE_GREY, lw=2.6, zorder=1)
    plot_partial_stems(ax, n_all, x, color=SIGNAL_BLACK, marker_size=7.5, line_width=2.4)
    setup_sequence_axis(ax, title=f"{sequence_title}: full input signal", ylabel=r"$x[n]$", n_max=x.size - 1)
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_input_full.png")


def export_input_sample_frame(
    *,
    sequence_key: str,
    sequence_title: str,
    x: np.ndarray,
    frame_index: int,
    figure_number: int,
) -> None:
    n_all = np.arange(x.size)
    previous_index = frame_index - 1
    current_value = x[frame_index]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    t_dense = np.linspace(0.0, x.size - 1, 600)
    ax.plot(t_dense, continuous_input(sequence_key, t_dense), color=REFERENCE_GREY, lw=2.2, zorder=1)
    plot_partial_stems(
        ax,
        n_all,
        x,
        color=SIGNAL_BLACK,
        marker_size=5.8,
        alpha=0.35,
        line_width=1.25,
    )
    if previous_index >= 0:
        plot_partial_stems(
            ax,
            np.array([previous_index]),
            np.array([x[previous_index]]),
            color=SIGNAL_BLACK,
            marker_size=7.8,
            alpha=0.78,
            line_width=2.1,
            line_style="--",
        )
    plot_partial_stems(
        ax,
        np.array([frame_index]),
        np.array([current_value]),
        color=SIGNAL_BLACK,
        marker_size=10.0,
        line_width=2.8,
    )
    ax.axvline(frame_index, color="0.35", lw=1.6, ls="--")
    setup_sequence_axis(
        ax,
        title=f"{sequence_title}: input sample n={frame_index}",
        ylabel=r"$x[n]$",
        n_max=x.size - 1,
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_input_sample_{frame_index:02d}.png")


def export_empty_output(
    *,
    sequence_key: str,
    y: np.ndarray,
    figure_number: int,
) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    setup_sequence_axis(
        ax,
        title="",
        ylabel=r"$y[n]$",
        n_max=y.size - 1,
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_output_empty.png")


def export_output_sample_frame(
    *,
    config: FirConfig,
    sequence_key: str,
    y: np.ndarray,
    frame_index: int,
    figure_number: int,
) -> None:
    n_all = np.arange(y.size)
    computed = n_all <= frame_index
    previous_index = frame_index - 1
    current_output = y[frame_index]
    formula = config.output_formula.format(n=frame_index, prev=previous_index)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    plot_partial_stems(
        ax,
        n_all[computed],
        y[computed],
        color=OUTPUT_BLUE,
        marker_size=7.0,
        line_width=2.3,
    )
    plot_partial_stems(
        ax,
        np.array([frame_index]),
        np.array([current_output]),
        color=OUTPUT_BLUE,
        marker_size=10.0,
        line_width=3.0,
    )
    ax.axvline(frame_index, color="0.35", lw=1.6, ls="--")
    setup_sequence_axis(
        ax,
        title=rf"$y[{frame_index}]={formula}={current_output:+.2f}$",
        ylabel=r"$y[n]$",
        n_max=y.size - 1,
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_output_sample_{frame_index:02d}.png")


def export_output_with_envelope(
    *,
    config: FirConfig,
    sequence_key: str,
    sequence_title: str,
    y: np.ndarray,
    figure_number: int,
) -> None:
    n_all = np.arange(y.size)
    t_transient = np.linspace(0.0, 1.0, 160)
    t_dense = np.linspace(1.0, y.size - 1, 600)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.19, top=0.82)
    ax.plot(
        t_transient,
        continuous_output(config, sequence_key, t_transient),
        color=REFERENCE_GREY,
        lw=2.6,
        ls="--",
        zorder=1,
    )
    ax.plot(t_dense, continuous_output(config, sequence_key, t_dense), color=REFERENCE_GREY, lw=2.6, zorder=1)
    plot_partial_stems(
        ax,
        n_all,
        y,
        color=OUTPUT_BLUE,
        marker_size=7.5,
        line_width=2.4,
    )
    setup_sequence_axis(
        ax,
        title="Output with continuous counterpart",
        ylabel=r"$y[n]$",
        n_max=y.size - 1,
    )
    save_figure_fixed_canvas(fig, f"{figure_number:02d}_{sequence_key}_output_envelope.png")


def export_sequence_frames(config: FirConfig) -> None:
    b = fir_coefficients(config)
    figure_number = 11
    for sequence_key, (sequence_title, x) in input_sequences().items():
        y = fir_filter(x, b)
        export_full_input(
            sequence_key=sequence_key,
            sequence_title=sequence_title,
            x=x,
            figure_number=figure_number,
        )
        figure_number += 1
        export_empty_output(
            sequence_key=sequence_key,
            y=y,
            figure_number=figure_number,
        )
        figure_number += 1
        for frame_index in range(x.size):
            export_input_sample_frame(
                sequence_key=sequence_key,
                sequence_title=sequence_title,
                x=x,
                frame_index=frame_index,
                figure_number=figure_number,
            )
            figure_number += 1
            export_output_sample_frame(
                config=config,
                sequence_key=sequence_key,
                y=y,
                frame_index=frame_index,
                figure_number=figure_number,
            )
            figure_number += 1
        export_output_with_envelope(
            config=config,
            sequence_key=sequence_key,
            sequence_title=sequence_title,
            y=y,
            figure_number=figure_number,
        )
        figure_number += 1


def export_filter(config: FirConfig) -> None:
    set_output_dir(BLOCK_DIR / config.output_subdir)
    export_fir_structure(config)
    export_impulse_response(config)
    export_frequency_response(config)
    export_frequency_response_normalized_db(config)
    export_phase_response_normalized(config)
    export_frequency_response_log(config, sample_rate_hz=48_000.0)
    export_frequency_response_db(config, sample_rate_hz=48_000.0)
    export_dirac_input()
    export_phase_response_linear(config, sample_rate_hz=48_000.0)
    export_phase_response_log(config, sample_rate_hz=48_000.0)
    export_sequence_frames(config)


def main() -> None:
    clear_output_dir()
    for config in FILTER_CONFIGS:
        export_filter(config)
    export_notch_filter()
    export_lowpass_design_filter()
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
