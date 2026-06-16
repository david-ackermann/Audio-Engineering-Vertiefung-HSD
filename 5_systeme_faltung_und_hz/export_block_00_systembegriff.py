from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "png_storyboards" / "00"

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 26
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_BLUE = "#2b7bbb"
SYSTEM_GREEN = "#66b77a"
GRID_GREY = "0.75"
LOWPASS_IR_DISPLAY_GAIN = 2.0
LOWPASS_IR_LENGTH = 16
DIRAC_LENGTH = 16
NYQUIST_BIN = 8

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*"):
        if image_file.suffix.lower() in {".png", ".gif"}:
            image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def stem_sequence(ax, n: np.ndarray, values: np.ndarray, *, color: str) -> None:
    markerline, stemlines, baseline = ax.stem(n, values)
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor("white")
    markerline.set_markeredgewidth(0.9)
    markerline.set_markersize(8)
    stemlines.set_color(color)
    stemlines.set_linewidth(2.8)
    baseline.set_color(SIGNAL_BLACK)
    baseline.set_linewidth(1.5)


def style_axis(ax, title: str, *, n_max: int = 14) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, n_max + 0.5)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks(np.arange(0, n_max + 1, 2))
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_frequency_bin_axis(
    ax,
    title: str,
    *,
    k_max: int = 15,
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
    yticklabels: list[str] | None = None,
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, k_max + 0.5)
    ax.set_ylim(*ylim)
    tick_step = 1 if k_max <= 8 else 2
    ax.set_xticks(np.arange(0, k_max + 1, tick_step))
    ax.set_yticks(yticks)
    if yticklabels is not None:
        ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Frequency bin k", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=SIGNAL_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def example_signals() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    n = np.arange(15)
    x = np.zeros_like(n, dtype=float)
    x[2] = 0.85
    x[7] = 0.55
    x[11] = 0.38

    delta = np.zeros_like(n, dtype=float)
    delta[0] = 1.0

    h = np.zeros_like(n, dtype=float)
    h[:5] = [0.80, -0.55, 0.32, -0.18, 0.09]

    y = np.convolve(x, h)[: n.size]
    return n, x, delta, h, y


def lowpass_impulse_response() -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(LOWPASS_IR_LENGTH)
    h_lp = np.zeros_like(n, dtype=float)
    alpha = 0.65
    delay = 3
    active = n >= delay
    h_lp[active] = (1.0 - alpha) * alpha ** (n[active] - delay)
    h_lp /= np.sum(h_lp)
    return n, h_lp


def lowpass_frequency_response(h_lp: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_fft = 16
    k = np.arange(n_fft // 2 + 1)
    omega = 2.0 * np.pi * k / n_fft
    response = np.fft.rfft(h_lp, n=n_fft)
    magnitude = np.abs(response)
    return k, omega, magnitude


def lowpass_group_delay(h_lp: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    k, omega, _ = lowpass_frequency_response(h_lp)
    n = np.arange(h_lp.size)
    response = np.exp(-1j * np.outer(omega, n)) @ h_lp
    phase = np.unwrap(np.angle(response))
    group_delay = -np.gradient(phase, omega)
    return k, group_delay


def export_input_sequence(n: np.ndarray, x: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.82)
    stem_sequence(ax, n, x, color=SIGNAL_BLACK)
    style_axis(ax, r"Input sequence $x[n]$")
    save_figure(fig, "01_eingangsfolge_x.png")


def export_output_sequence(n: np.ndarray, y: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.82)
    stem_sequence(ax, n, y, color=SYSTEM_BLUE)
    style_axis(ax, r"Output sequence $y[n]$")
    save_figure(fig, "02_ausgangsfolge_y.png")


def export_discrete_impulse(n: np.ndarray, delta: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.82)
    stem_sequence(ax, n, delta, color=SYSTEM_GREEN)
    style_axis(ax, r"Discrete impulse $\delta[n]$, $N=16$", n_max=DIRAC_LENGTH - 1)
    save_figure(fig, "03_diskreter_impuls_delta.png")


def export_impulse_response(n: np.ndarray, h: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.82)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    style_axis(ax, r"Impulse response $h[n]$")
    save_figure(fig, "04_impulsantwort_h.png")


def export_dirac_magnitude_spectrum() -> None:
    k = np.arange(NYQUIST_BIN + 1)
    magnitude = np.ones_like(k, dtype=float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.82)
    stem_sequence(ax, k, magnitude, color=SYSTEM_GREEN)
    ax.axvline(NYQUIST_BIN, color=GRID_GREY, lw=1.8, ls="--")
    style_frequency_bin_axis(
        ax,
        r"Magnitude spectrum $|\Delta_N[k]|$, $N=16$",
        k_max=NYQUIST_BIN,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    save_figure(fig, "05_dirac_betragsspektrum.png")


def export_dirac_phase() -> None:
    k = np.arange(NYQUIST_BIN + 1)
    phase = np.zeros_like(k, dtype=float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.82)
    stem_sequence(ax, k, phase, color=SYSTEM_GREEN)
    ax.axvline(NYQUIST_BIN, color=GRID_GREY, lw=1.8, ls="--")
    style_frequency_bin_axis(
        ax,
        r"Phase $\angle\Delta_N[k]$, $N=16$",
        k_max=NYQUIST_BIN,
        ylabel="Phase",
        ylim=(-np.pi, np.pi),
        yticks=[-np.pi, 0.0, np.pi],
        yticklabels=[r"$-\pi$", "0", r"$\pi$"],
    )
    save_figure(fig, "06_dirac_phase.png")


def export_dirac_group_delay() -> None:
    k = np.arange(NYQUIST_BIN + 1)
    group_delay = np.zeros_like(k, dtype=float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.82)
    stem_sequence(ax, k, group_delay, color=SYSTEM_GREEN)
    ax.axvline(NYQUIST_BIN, color=GRID_GREY, lw=1.8, ls="--")
    style_frequency_bin_axis(
        ax,
        r"Group delay of $\delta[n]$, $N=16$",
        k_max=NYQUIST_BIN,
        ylabel="Samples",
        ylim=(-1.05, 1.05),
        yticks=[-1.0, 0.0, 1.0],
    )
    save_figure(fig, "07_dirac_gruppenlaufzeit.png")


def export_lowpass_impulse_response(n: np.ndarray, h_lp: np.ndarray) -> None:
    h_lp_display = LOWPASS_IR_DISPLAY_GAIN * h_lp

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.82)
    stem_sequence(ax, n, h_lp_display, color=SYSTEM_GREEN)
    style_axis(ax, r"Low-pass impulse response $h[n]$, $N=16$", n_max=LOWPASS_IR_LENGTH - 1)
    save_figure(fig, "08_tiefpass_impulsantwort_h.png")


def export_lowpass_magnitude_response(h_lp: np.ndarray) -> None:
    k, _, magnitude = lowpass_frequency_response(h_lp)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.82)
    stem_sequence(ax, k, magnitude, color=SYSTEM_GREEN)
    ax.axvline(8, color=GRID_GREY, lw=1.8, ls="--")
    style_frequency_bin_axis(
        ax,
        r"Low-pass magnitude response $|H_N[k]|$, $N=16$",
        k_max=8,
        ylabel="Magnitude",
        ylim=(-0.05, 1.10),
        yticks=[0.0, 0.5, 1.0],
    )
    save_figure(fig, "09_tiefpass_betragsfrequenzgang.png")


def export_lowpass_group_delay(h_lp: np.ndarray) -> None:
    k, group_delay = lowpass_group_delay(h_lp)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.82)
    stem_sequence(ax, k, group_delay, color=SYSTEM_GREEN)
    ax.axvline(8, color=GRID_GREY, lw=1.8, ls="--")
    style_frequency_bin_axis(
        ax,
        r"Group delay of low-pass, $N=16$",
        k_max=8,
        ylabel="Samples",
        ylim=(-0.2, 6.2),
        yticks=[0.0, 2.5, 5.0],
    )
    save_figure(fig, "10_tiefpass_gruppenlaufzeit.png")


def main() -> None:
    clear_output_dir()
    n, x, delta, h, y = example_signals()
    n_dirac = np.arange(DIRAC_LENGTH)
    delta_dirac = np.zeros_like(n_dirac, dtype=float)
    delta_dirac[0] = 1.0
    n_lp, h_lp = lowpass_impulse_response()
    export_input_sequence(n, x)
    export_output_sequence(n, y)
    export_discrete_impulse(n_dirac, delta_dirac)
    export_impulse_response(n, h)
    export_dirac_magnitude_spectrum()
    export_dirac_phase()
    export_dirac_group_delay()
    export_lowpass_impulse_response(n_lp, h_lp)
    export_lowpass_magnitude_response(h_lp)
    export_lowpass_group_delay(h_lp)


if __name__ == "__main__":
    main()
