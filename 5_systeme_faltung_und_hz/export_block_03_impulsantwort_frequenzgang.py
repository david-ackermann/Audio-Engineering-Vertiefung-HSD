from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from export_block_00_systembegriff import lowpass_impulse_response


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "03_impulsantwort_und_frequenzgang"
OUTPUT_DIR = OUTPUT_ROOT / "3A_zero_padding_tiefpass"

DPI = 200
FIGSIZE = (10.5, 4.2)
FIGSIZE_WIDE = (21.0, 4.2)
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


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*"):
        if image_file.suffix.lower() in {".png", ".gif"}:
            image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight")
    plt.close(fig)


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
    ax.set_xlabel(r"Normalized frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
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
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.04, 2.04)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
    ax.set_xticklabels(["0", "0.5", "1", "1.5", "2"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Normalized frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
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
    ylabel: str,
    ylim: tuple[float, float],
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.04 * np.pi, 2.04 * np.pi)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2.0 * np.pi])
    ax.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.set_yticks(yticks)
    ax.set_xlabel(r"Digital frequency $\Omega$", fontsize=LABEL_SIZE)
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
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
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
        style_frequency_axis(
            ax,
            rf"Sampled magnitude response $|H[k]|$, $N={n_fft}$",
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
    handles.append(plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.3, label=rf"$H[k]$, $N={n_fft}$"))
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


def export_magnitude_response_full_radians(h: np.ndarray, n_fft: int, filename_index: int) -> None:
    _, response_bins = dft_response_full(h, n_fft)
    k_bins = np.arange(response_bins.size)

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.18, top=0.84)
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
    save_figure(fig, f"{filename_index:02d}_magnitude_response_full_radians_n{n_fft}.png")


def export_magnitude_response_full(h: np.ndarray, n_fft: int, filename_index: int) -> None:
    _, response_bins = dft_response_full(h, n_fft)
    k_bins = np.arange(response_bins.size)

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.18, top=0.84)
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


def main() -> None:
    clear_output_dir()
    n, h = lowpass_impulse_response()
    export_impulse_response_frame(n, h, 16, 1)
    export_magnitude_response_full_radians(h, 16, 2)
    export_magnitude_response_full(h, 16, 3)
    export_magnitude_response(h, 16, 4)
    export_magnitude_response(h, 16, 5, with_envelope=True, envelope_axis="k")
    export_magnitude_response(h, 16, 6, with_envelope=True)
    export_impulse_response_frame(n, h, 32, 7)
    export_magnitude_response(h, 32, 8)
    export_magnitude_response(h, 32, 9, with_envelope=True, envelope_axis="k")
    export_magnitude_response(h, 32, 10, with_envelope=True)
    export_impulse_response_frame(n, h, 64, 11)
    export_magnitude_response(h, 64, 12)
    export_magnitude_response(h, 64, 13, with_envelope=True, envelope_axis="k")
    export_magnitude_response(h, 64, 14, with_envelope=True)
    export_magnitude_response_envelope_only(h, 15)
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
