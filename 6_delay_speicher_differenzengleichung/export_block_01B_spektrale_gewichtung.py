from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards" / "01_impulsantwort_und_frequenzgang"
OUTPUT_DIR = OUTPUT_ROOT / "1B_spektrale_gewichtung"

DPI = 200
FIGSIZE = (10.5, 4.2)
TITLE_SIZE = 26
LABEL_SIZE = 24
TICK_SIZE = 18
LEGEND_SIZE = 14

INPUT_BLACK = "0.10"
OUTPUT_BLUE = "#2b7bbb"
SYSTEM_GREEN = "#66b77a"
GRID_GREY = "0.72"

TIME_YLIM = (-1.20, 1.20)
TIME_YTICKS = [-1.0, 0.0, 1.0]
SYSTEM_TIME_YLIM = (-0.03, 0.42)
SYSTEM_TIME_YTICKS = [0.0, 0.2, 0.4]
SYSTEM_SPECTRUM_YMAX = 1.10

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
    baseline.set_color(INPUT_BLACK)
    baseline.set_linewidth(1.4)


def style_time_axis(
    ax,
    title: str,
    *,
    n_fft: int,
    ymin: float,
    ymax: float,
    yticks: list[float],
) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, n_fft - 0.5)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(0, n_fft + 1, 4 if n_fft <= 32 else 8))
    ax.set_yticks(yticks)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=INPUT_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_spectrum_axis(
    ax,
    title: str,
    *,
    n_fft: int,
    ymax: float,
    ylabel: str = "Magnitude",
    show_xlabel: bool = True,
) -> None:
    k_max = n_fft // 2
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, k_max + 0.5)
    ax.set_ylim(-0.04 * ymax, ymax)
    ax.set_xticks(dft_bin_ticks(k_max))
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    if show_xlabel:
        ax.set_xlabel(r"DFT bin $k$", fontsize=LABEL_SIZE)
    else:
        ax.tick_params(labelbottom=False)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=INPUT_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def periodic_square_sequence(n_fft: int, period_samples: int = 16) -> np.ndarray:
    n = np.arange(n_fft)
    half_period = period_samples // 2
    x = np.where((n % period_samples) < half_period, 1.0, -1.0)
    return x


def one_sided_bins(n_fft: int) -> np.ndarray:
    return np.arange(n_fft // 2 + 1)


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


def spectral_filtering(x: np.ndarray, h: np.ndarray, n_fft: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x_bins = np.fft.rfft(x, n=n_fft)
    h_bins = np.fft.rfft(h, n=n_fft)
    y_bins = h_bins * x_bins
    y = np.fft.irfft(y_bins, n=n_fft)
    return x_bins, h_bins, y_bins, y


def export_time_sequence(
    values: np.ndarray,
    *,
    title: str,
    color: str,
    filename: str,
    ymin: float,
    ymax: float,
    yticks: list[float],
    reference_values: np.ndarray | None = None,
    reference_label: str | None = None,
    value_label: str | None = None,
) -> None:
    n = np.arange(values.size)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    if reference_values is not None:
        stem_sequence(ax, n, reference_values, color=GRID_GREY, alpha=0.55, marker_size=6.2, line_width=1.8)
    stem_sequence(ax, n, values, color=color)
    style_time_axis(ax, title, n_fft=values.size, ymin=ymin, ymax=ymax, yticks=yticks)
    if reference_values is not None:
        ax.legend(
            handles=[
                plt.Line2D([0], [0], color=GRID_GREY, marker="o", lw=1.8, label=reference_label or r"$x[n]$"),
                plt.Line2D([0], [0], color=color, marker="o", lw=2.8, label=value_label or r"$y[n]$"),
            ],
            loc="upper right",
            fontsize=LEGEND_SIZE,
            frameon=True,
            framealpha=0.95,
        )
    save_figure(fig, filename)


def export_impulse_response_frame(h: np.ndarray, *, n_fft: int, filename: str) -> None:
    h_frame = np.zeros(n_fft)
    h_frame[: h.size] = h
    export_time_sequence(
        h_frame,
        title=rf"System impulse response $h[n]$, $N={n_fft}$",
        color=SYSTEM_GREEN,
        filename=filename,
        ymin=SYSTEM_TIME_YLIM[0],
        ymax=SYSTEM_TIME_YLIM[1],
        yticks=SYSTEM_TIME_YTICKS,
        value_label=rf"$h[n]$, $N={n_fft}$",
    )


def export_impulse_response_system_length(h: np.ndarray, *, filename: str) -> None:
    n = np.arange(h.size)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    stem_sequence(ax, n, h, color=SYSTEM_GREEN)
    ax.set_title(r"Low-pass impulse response $h[n]$, $M=15$", fontsize=TITLE_SIZE, pad=14)
    ax.set_xlim(-0.5, h.size - 0.5)
    ax.set_ylim(SYSTEM_TIME_YLIM[0], SYSTEM_TIME_YLIM[1])
    ax.set_xticks(np.arange(0, h.size, 2))
    ax.set_yticks(SYSTEM_TIME_YTICKS)
    ax.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=INPUT_BLACK, lw=1.2)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=SYSTEM_GREEN, marker="o", lw=2.8, label=r"$h[n]$, $M=15$"),
        ],
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, filename)


def export_spectrum(
    bins: np.ndarray,
    *,
    n_fft: int,
    title: str,
    legend_label: str,
    color: str,
    filename: str,
    reference_bins: np.ndarray | None = None,
    reference_label: str | None = None,
    ymax_override: float | None = None,
    normalize_by_n: bool = False,
) -> None:
    omega_norm = one_sided_bins(n_fft)
    scale = n_fft if normalize_by_n else 1.0
    magnitude = np.abs(bins) / scale
    if ymax_override is not None:
        ymax = ymax_override
    elif reference_bins is None:
        ymax = max(float(np.max(magnitude)) * 1.18, 1.0)
    else:
        ymax = max(float(np.max(magnitude)) * 1.18, float(np.max(np.abs(reference_bins) / scale)) * 1.18, 1.0)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    if reference_bins is not None:
        stem_sequence(ax, omega_norm, np.abs(reference_bins) / scale, color=GRID_GREY, alpha=0.55, marker_size=6.2, line_width=1.8)
    stem_sequence(ax, omega_norm, magnitude, color=color, marker_size=7.5, line_width=2.3)
    style_spectrum_axis(ax, title, n_fft=n_fft, ymax=ymax)
    handles = []
    if reference_bins is not None:
        handles.append(plt.Line2D([0], [0], color=GRID_GREY, marker="o", lw=1.8, label=reference_label or r"$X[k]$"))
    handles.append(plt.Line2D([0], [0], color=color, marker="o", lw=2.3, label=legend_label))
    ax.legend(
        handles=handles,
        loc="upper right",
        fontsize=LEGEND_SIZE,
        frameon=True,
        framealpha=0.95,
    )
    save_figure(fig, filename)


def export_filtering_series(
    *,
    figure_index: int,
    n_fft: int,
    x: np.ndarray,
    h: np.ndarray,
    x_bins: np.ndarray,
    h_bins: np.ndarray,
    y_bins: np.ndarray,
    y: np.ndarray,
    signal_spectrum_ymax: float,
) -> int:
    export_time_sequence(
        x,
        title=rf"Periodic square wave $x[n]$, $N={n_fft}$",
        color=INPUT_BLACK,
        filename=f"{figure_index:02d}_input_sequence_n{n_fft}.png",
        ymin=TIME_YLIM[0],
        ymax=TIME_YLIM[1],
        yticks=TIME_YTICKS,
    )
    figure_index += 1

    export_spectrum(
        x_bins,
        n_fft=n_fft,
        title=rf"Input spectrum $|X[k]|/N$, $N={n_fft}$",
        legend_label=rf"$|X[k]|/N$, $N={n_fft}$",
        color=INPUT_BLACK,
        filename=f"{figure_index:02d}_input_spectrum_n{n_fft}.png",
        ymax_override=signal_spectrum_ymax,
        normalize_by_n=True,
    )
    figure_index += 1

    export_impulse_response_frame(
        h,
        n_fft=n_fft,
        filename=f"{figure_index:02d}_system_impulse_response_n{n_fft}.png",
    )
    figure_index += 1

    export_spectrum(
        h_bins,
        n_fft=n_fft,
        title=rf"System response bins $|H[k]|$, $N={n_fft}$",
        legend_label=rf"$H[k]$, $N={n_fft}$",
        color=SYSTEM_GREEN,
        filename=f"{figure_index:02d}_system_response_bins_n{n_fft}.png",
        ymax_override=SYSTEM_SPECTRUM_YMAX,
    )
    figure_index += 1

    export_spectrum(
        y_bins,
        n_fft=n_fft,
        title=rf"Output spectrum $|Y[k]|/N=|H[k]X[k]|/N$, $N={n_fft}$",
        legend_label=rf"$|Y[k]|/N$, $N={n_fft}$",
        color=OUTPUT_BLUE,
        filename=f"{figure_index:02d}_output_spectrum_product_n{n_fft}.png",
        reference_bins=x_bins,
        reference_label=rf"$|X[k]|/N$, $N={n_fft}$",
        ymax_override=signal_spectrum_ymax,
        normalize_by_n=True,
    )
    figure_index += 1

    export_time_sequence(
        y,
        title=rf"Output sequence $y[n]$, $N={n_fft}$",
        color=OUTPUT_BLUE,
        filename=f"{figure_index:02d}_output_sequence_n{n_fft}.png",
        ymin=TIME_YLIM[0],
        ymax=TIME_YLIM[1],
        yticks=TIME_YTICKS,
        reference_values=x,
        reference_label=rf"$x[n]$, $N={n_fft}$",
        value_label=rf"$y[n]$, $N={n_fft}$",
    )
    return figure_index + 1


def main() -> None:
    clear_output_dir()
    _, h = lowpass_impulse_response()
    export_impulse_response_system_length(h, filename="00_system_impulse_response_m15.png")

    cases = []
    for n_fft in (16, 32, 64):
        x = periodic_square_sequence(n_fft)
        x_bins, h_bins, y_bins, y = spectral_filtering(x, h, n_fft)
        cases.append(
            {
                "n_fft": n_fft,
                "x": x,
                "x_bins": x_bins,
                "h_bins": h_bins,
                "y_bins": y_bins,
                "y": y,
            }
        )

    signal_spectrum_ymax = max(
        max(
            float(np.max(np.abs(case["x_bins"])) / case["n_fft"]),
            float(np.max(np.abs(case["y_bins"])) / case["n_fft"]),
        )
        for case in cases
    ) * 1.15

    figure_index = 1
    for case in cases:
        figure_index = export_filtering_series(
            figure_index=figure_index,
            n_fft=case["n_fft"],
            x=case["x"],
            h=h,
            x_bins=case["x_bins"],
            h_bins=case["h_bins"],
            y_bins=case["y_bins"],
            y=case["y"],
            signal_spectrum_ymax=signal_spectrum_ymax,
        )

    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
