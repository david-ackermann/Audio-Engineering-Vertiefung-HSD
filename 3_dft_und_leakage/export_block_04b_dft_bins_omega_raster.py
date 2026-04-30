from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_diskrete_kreisfrequenz"
    / "04B"
    / "04B1_dft_bins_omega_raster"
)
OUTPUT_DIR_N32 = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "04_diskrete_kreisfrequenz"
    / "04B"
    / "04B2_n32_k16_positive_spectrum"
)

DPI = 200
FIGSIZE = (12.0, 4.4)

TITLE_SIZE = 22
LABEL_SIZE = 18
TICK_SIZE = 17
LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

N = 16
OMEGA_STEP = 2.0 * np.pi / N
POSITIVE_K_VALUES = (1, 4, 7)

BIN_GREY = "0.68"
GRID_GREY = "0.75"
SIGNAL_BLUE = "#2b7bbb"
SAMPLE_GREY = "0.54"
WINDOW_GREEN = "#66b77a"
WINDOW_LIGHT_GREEN = "#d7efde"
PERIOD_MARKER_RED = "#f3a2a2"

X_MIN = -2.0 * np.pi
X_MAX = 2.0 * np.pi
X_PADDING = 0.12 * np.pi
BIN_HEIGHT = 0.70
ACTIVE_HEIGHT = BIN_HEIGHT
SAMPLE_BLOCK_X_PADDING_FRACTION = 0.035

PI_TICKS = (
    -2.0 * np.pi,
    -1.5 * np.pi,
    -1.0 * np.pi,
    -0.5 * np.pi,
    0.0,
    0.5 * np.pi,
    1.0 * np.pi,
    1.5 * np.pi,
    2.0 * np.pi,
)
PI_TICK_LABELS = (
    r"$-2\pi$",
    r"$-3\pi/2$",
    r"$-\pi$",
    r"$-\pi/2$",
    r"$0$",
    r"$\pi/2$",
    r"$\pi$",
    r"$3\pi/2$",
    r"$2\pi$",
)


def bin_omegas_for_axis(block_length: int) -> np.ndarray:
    omega_step = 2.0 * np.pi / block_length
    first_bin = int(np.floor((X_MIN - X_PADDING) / omega_step))
    last_bin = int(np.ceil((X_MAX + X_PADDING) / omega_step))
    return np.arange(first_bin, last_bin + 1, dtype=float) * omega_step


def bin_indices_for_axis(block_length: int) -> np.ndarray:
    k_padding = block_length * X_PADDING / (2.0 * np.pi)
    first_bin = int(np.floor(-block_length - k_padding))
    last_bin = int(np.ceil(block_length + k_padding))
    return np.arange(first_bin, last_bin + 1, dtype=float)


def k_tick_values(block_length: int) -> tuple[int, ...]:
    return tuple(int(block_length * factor) for factor in (-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0))


def hz_for_omega(omega: np.ndarray, sample_rate_hz: float) -> np.ndarray:
    return omega / (2.0 * np.pi) * sample_rate_hz


def hz_tick_values(sample_rate_hz: float) -> tuple[float, ...]:
    return tuple(sample_rate_hz * factor for factor in (-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0))


def hz_tick_labels(sample_rate_hz: float) -> tuple[str, ...]:
    return tuple(f"{value:g}" for value in hz_tick_values(sample_rate_hz))


def format_seconds(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


ALL_BIN_OMEGAS = bin_omegas_for_axis(N)


def clear_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for png_file in output_dir.glob("*.png"):
        png_file.unlink()


def omega_for_k(k: int, block_length: int = N) -> float:
    return 2.0 * np.pi * k / block_length


def unique_positions(values: list[float]) -> list[float]:
    unique = []
    for value in values:
        if X_MIN - 1e-9 <= value <= X_MAX + 1e-9 and not any(np.isclose(value, existing) for existing in unique):
            unique.append(value)
    return unique


def positive_bin_positions() -> list[float]:
    return [omega_for_k(k) for k in POSITIVE_K_VALUES]


def conjugate_negative_positions() -> list[float]:
    return [-omega_for_k(k) for k in POSITIVE_K_VALUES]


def shifted_periodic_positions() -> list[float]:
    positive = positive_bin_positions()
    negative = conjugate_negative_positions()
    return unique_positions(positive + [value + 2.0 * np.pi for value in negative])


def draw_bin_axis(
    ax,
    *,
    title: str,
    active_positions: list[float],
    all_bin_omegas: np.ndarray = ALL_BIN_OMEGAS,
    periodic_positions: list[float] | None = None,
) -> None:
    ax.set_xlim(X_MIN - X_PADDING, X_MAX + X_PADDING)
    ax.set_ylim(0.0, 1.08)
    ax.set_yticks([])
    ax.set_xticks(PI_TICKS)
    ax.set_xticklabels(PI_TICK_LABELS)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel(r"Discrete angular frequency $\Omega$ [rad/sample]", fontsize=LABEL_SIZE)
    ax.set_ylabel("DFT bins", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)

    ax.axvline(-2.0 * np.pi, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)
    ax.axvline(0.0, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)
    ax.axvline(2.0 * np.pi, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)

    ax.vlines(all_bin_omegas, 0.0, BIN_HEIGHT, color=BIN_GREY, lw=2.2, zorder=1, clip_on=False)
    ax.scatter(
        all_bin_omegas,
        np.full_like(all_bin_omegas, BIN_HEIGHT),
        s=52,
        color=BIN_GREY,
        edgecolor="white",
        linewidth=0.9,
        zorder=2,
        clip_on=False,
    )

    active_positions = unique_positions(active_positions)
    if active_positions:
        ax.vlines(active_positions, 0.0, ACTIVE_HEIGHT, color=SIGNAL_BLUE, lw=3.4, zorder=3)
        ax.scatter(
            active_positions,
            np.full(len(active_positions), ACTIVE_HEIGHT),
            s=98,
            color=SIGNAL_BLUE,
            edgecolor="white",
            linewidth=1.1,
            zorder=4,
        )

    periodic_positions = unique_positions(periodic_positions or [])
    if periodic_positions:
        ax.vlines(
            periodic_positions,
            0.0,
            ACTIVE_HEIGHT,
            color=SIGNAL_BLUE,
            lw=3.0,
            linestyles="--",
            zorder=5,
        )
        ax.scatter(
            periodic_positions,
            np.full(len(periodic_positions), ACTIVE_HEIGHT),
            s=98,
            facecolor="white",
            edgecolor=SIGNAL_BLUE,
            linewidth=2.2,
            zorder=6,
        )


def draw_hz_bin_axis(
    ax,
    *,
    title: str,
    block_length: int,
    sample_rate_hz: float,
) -> None:
    all_bin_hz = hz_for_omega(bin_omegas_for_axis(block_length), sample_rate_hz)
    f_min = -sample_rate_hz
    f_max = sample_rate_hz
    f_padding = sample_rate_hz * X_PADDING / (2.0 * np.pi)

    ax.set_xlim(f_min - f_padding, f_max + f_padding)
    ax.set_ylim(0.0, 1.08)
    ax.set_yticks([])
    ax.set_xticks(hz_tick_values(sample_rate_hz))
    ax.set_xticklabels(hz_tick_labels(sample_rate_hz))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("DFT bins", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)

    ax.axvline(-sample_rate_hz, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)
    ax.axvline(0.0, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)
    ax.axvline(sample_rate_hz, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)

    ax.vlines(all_bin_hz, 0.0, BIN_HEIGHT, color=BIN_GREY, lw=2.2, zorder=1, clip_on=False)
    ax.scatter(
        all_bin_hz,
        np.full_like(all_bin_hz, BIN_HEIGHT),
        s=52,
        color=BIN_GREY,
        edgecolor="white",
        linewidth=0.9,
        zorder=2,
        clip_on=False,
    )


def draw_k_bin_axis(
    ax,
    *,
    title: str,
    block_length: int,
) -> None:
    all_bin_indices = bin_indices_for_axis(block_length)
    k_padding = block_length * X_PADDING / (2.0 * np.pi)

    ax.set_xlim(-block_length - k_padding, block_length + k_padding)
    ax.set_ylim(0.0, 1.08)
    ax.set_yticks([])
    ax.set_xticks(k_tick_values(block_length))
    ax.set_xticklabels([str(value) for value in k_tick_values(block_length)])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel(r"Bin index $k$", fontsize=LABEL_SIZE)
    ax.set_ylabel("DFT bins", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)

    ax.axvline(-block_length, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)
    ax.axvline(0.0, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)
    ax.axvline(block_length, color=PERIOD_MARKER_RED, lw=2.2, alpha=0.82, zorder=0)

    ax.vlines(all_bin_indices, 0.0, BIN_HEIGHT, color=BIN_GREY, lw=2.2, zorder=1, clip_on=False)
    ax.scatter(
        all_bin_indices,
        np.full_like(all_bin_indices, BIN_HEIGHT),
        s=52,
        color=BIN_GREY,
        edgecolor="white",
        linewidth=0.9,
        zorder=2,
        clip_on=False,
    )


def n_tick_values(block_length: int) -> tuple[int, ...]:
    if block_length <= 16:
        return tuple(range(0, block_length + 1, 4))
    return tuple(range(0, block_length + 1, 8))


def draw_sample_block_axis(
    ax,
    *,
    title: str,
    block_length: int,
) -> None:
    sample_indices = np.arange(block_length)
    sample_values = np.ones(block_length)
    y_arrow = -0.18

    ax.axvspan(0.0, float(block_length), color=WINDOW_LIGHT_GREEN, alpha=0.72, zorder=0)
    ax.axhline(0.0, color=GRID_GREY, lw=1.0, zorder=1)
    ax.axvline(0.0, color=WINDOW_GREEN, lw=2.2, ls="--", zorder=2)
    ax.axvline(float(block_length), color=WINDOW_GREEN, lw=2.2, ls="--", zorder=2)

    ax.vlines(sample_indices, 0.0, sample_values, color=SAMPLE_GREY, lw=2.7, zorder=3)
    ax.scatter(
        sample_indices,
        sample_values,
        s=74,
        color=SAMPLE_GREY,
        edgecolor="white",
        linewidth=1.1,
        zorder=4,
    )

    x_padding = SAMPLE_BLOCK_X_PADDING_FRACTION * block_length
    ax.set_xlim(-x_padding, block_length + x_padding)
    ax.set_ylim(-0.28, 1.18)
    ax.set_xticks(n_tick_values(block_length))
    ax.set_yticks([0.0, 1.0])
    ax.set_yticklabels(["0", "1"])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel(r"Sample index $n$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Window $w_N[n]$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)

    ax.annotate(
        "",
        xy=(0.0, y_arrow),
        xytext=(float(block_length), y_arrow),
        arrowprops=dict(arrowstyle="<->", lw=1.8, color=PERIOD_MARKER_RED),
        zorder=20,
    )
    ax.text(
        0.5 * block_length,
        y_arrow + 0.045,
        rf"$N = {block_length}$ samples",
        color=PERIOD_MARKER_RED,
        fontsize=15,
        ha="center",
        va="bottom",
        zorder=21,
    )


def time_tick_values(observation_time: float) -> np.ndarray:
    if observation_time <= 0.55:
        step = 0.1
    elif observation_time <= 1.1:
        step = 0.2
    else:
        step = 0.5
    return np.arange(0.0, observation_time + 1e-9, step)


def draw_sample_block_time_axis(
    ax,
    *,
    title: str,
    block_length: int,
    sample_rate_hz: float,
    reference_sample_rate_hz: float = 16.0,
) -> None:
    sample_indices = np.arange(block_length)
    sample_times = sample_indices / sample_rate_hz
    sample_values = np.ones(block_length)
    observation_time = block_length / sample_rate_hz
    reference_observation_time = block_length / reference_sample_rate_hz
    x_padding = SAMPLE_BLOCK_X_PADDING_FRACTION * reference_observation_time
    y_arrow = -0.18

    ax.axvspan(0.0, observation_time, color=WINDOW_LIGHT_GREEN, alpha=0.72, zorder=0)
    ax.axhline(0.0, color=GRID_GREY, lw=1.0, zorder=1)
    ax.axvline(0.0, color=WINDOW_GREEN, lw=2.2, ls="--", zorder=2)
    ax.axvline(observation_time, color=WINDOW_GREEN, lw=2.2, ls="--", zorder=2)

    ax.vlines(sample_times, 0.0, sample_values, color=SAMPLE_GREY, lw=2.7, zorder=3)
    ax.scatter(
        sample_times,
        sample_values,
        s=74,
        color=SAMPLE_GREY,
        edgecolor="white",
        linewidth=1.1,
        zorder=4,
    )

    ax.set_xlim(-x_padding, reference_observation_time + x_padding)
    ax.set_ylim(-0.28, 1.18)
    ax.set_xticks(time_tick_values(reference_observation_time))
    ax.set_yticks([0.0, 1.0])
    ax.set_yticklabels(["0", "1"])
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=8)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Window $w_N[n]$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)

    ax.annotate(
        "",
        xy=(0.0, y_arrow),
        xytext=(observation_time, y_arrow),
        arrowprops=dict(arrowstyle="<->", lw=1.8, color=PERIOD_MARKER_RED),
        zorder=20,
    )
    ax.text(
        0.5 * observation_time,
        y_arrow + 0.045,
        rf"$T_{{obs}} = {format_seconds(observation_time)}\,\mathrm{{s}}$",
        color=PERIOD_MARKER_RED,
        fontsize=15,
        ha="center",
        va="bottom",
        zorder=21,
    )


def export_sample_block_reference(output_dir: Path, *, block_length: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    draw_sample_block_axis(
        ax,
        title=rf"Observation block for $x[n]$ ($N={block_length}$)",
        block_length=block_length,
    )
    fig.savefig(output_dir / f"00_n{block_length}_sample_block_xn.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_sample_block_time_references(output_dir: Path, *, block_length: int) -> None:
    for sample_rate_hz in (16, 32):
        fig, ax = plt.subplots(figsize=FIGSIZE)
        fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
        draw_sample_block_time_axis(
            ax,
            title=rf"Observation block for $x[n]$ ($N={block_length}$, $f_s={sample_rate_hz}\,\mathrm{{Hz}}$)",
            block_length=block_length,
            sample_rate_hz=sample_rate_hz,
        )
        fig.savefig(
            output_dir / f"00_n{block_length}_sample_block_fs{sample_rate_hz}hz.png",
            dpi=DPI,
            facecolor="white",
        )
        plt.close(fig)


def export_grey_k_reference(output_dir: Path, *, block_length: int) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    draw_k_bin_axis(
        ax,
        title=rf"DFT bin grid ($N={block_length}$)",
        block_length=block_length,
    )
    fig.savefig(output_dir / f"00_n{block_length}_dft_bin_grid_k.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def export_grey_hz_references(output_dir: Path, *, block_length: int) -> None:
    for sample_rate_hz in (16, 32):
        fig, ax = plt.subplots(figsize=FIGSIZE)
        fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
        draw_hz_bin_axis(
            ax,
            title=rf"DFT bin grid ($N={block_length}$, $f_s={sample_rate_hz}\,\mathrm{{Hz}}$)",
            block_length=block_length,
            sample_rate_hz=sample_rate_hz,
        )
        fig.savefig(
            output_dir / f"00_n{block_length}_dft_bin_grid_fs{sample_rate_hz}hz.png",
            dpi=DPI,
            facecolor="white",
        )
        plt.close(fig)


def export_series() -> None:
    title = rf"DFT bin grid ($N={N}$)"
    stages = (
        (
            [],
            [],
            "01_dft_bin_grid.png",
        ),
        (
            [omega_for_k(1)],
            [],
            "02_k01_bin.png",
        ),
        (
            [omega_for_k(1), omega_for_k(4)],
            [],
            "03_k04_bin.png",
        ),
        (
            [omega_for_k(1), omega_for_k(4), omega_for_k(7)],
            [],
            "04_k07_bin.png",
        ),
        (
            [omega_for_k(1), omega_for_k(4), omega_for_k(7), omega_for_k(-7)],
            [],
            "05_kminus7_bin.png",
        ),
        (
            [omega_for_k(1), omega_for_k(4), omega_for_k(7), omega_for_k(-7)],
            [omega_for_k(9)],
            "06_k09_periodic_bin.png",
        ),
        (
            [omega_for_k(1), omega_for_k(4), omega_for_k(7), omega_for_k(-7), omega_for_k(0)],
            [omega_for_k(9), omega_for_k(16)],
            "07_k16_periodic_dc_bin.png",
        ),
    )

    export_grey_hz_references(OUTPUT_DIR, block_length=N)
    export_grey_k_reference(OUTPUT_DIR, block_length=N)
    export_sample_block_reference(OUTPUT_DIR, block_length=N)
    export_sample_block_time_references(OUTPUT_DIR, block_length=N)

    for active_positions, periodic_positions, filename in stages:
        fig, ax = plt.subplots(figsize=FIGSIZE)
        fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
        draw_bin_axis(
            ax,
            title=title,
            active_positions=active_positions,
            periodic_positions=periodic_positions,
        )
        fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
        plt.close(fig)


def export_n32_k16_spectrum() -> None:
    block_length = 32
    active_k_values = (1, 4, 7, 9, 16)
    all_bin_omegas = bin_omegas_for_axis(block_length)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    draw_bin_axis(
        ax,
        title=rf"DFT bin grid ($N={block_length}$)",
        active_positions=[],
        all_bin_omegas=all_bin_omegas,
    )
    fig.savefig(OUTPUT_DIR_N32 / "00_n32_dft_bin_grid.png", dpi=DPI, facecolor="white")
    plt.close(fig)

    export_grey_hz_references(OUTPUT_DIR_N32, block_length=block_length)
    export_grey_k_reference(OUTPUT_DIR_N32, block_length=block_length)
    export_sample_block_reference(OUTPUT_DIR_N32, block_length=block_length)
    export_sample_block_time_references(OUTPUT_DIR_N32, block_length=block_length)

    active_positions = [omega_for_k(k, block_length) for k in active_k_values]
    active_positions.append(-np.pi)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    draw_bin_axis(
        ax,
        title=rf"DFT bin grid ($N={block_length}$)",
        active_positions=active_positions,
        all_bin_omegas=all_bin_omegas,
    )
    fig.savefig(OUTPUT_DIR_N32 / "01_n32_k16_positive_bins_to_pi.png", dpi=DPI, facecolor="white")
    plt.close(fig)


def main() -> None:
    clear_output_dir(OUTPUT_DIR)
    clear_output_dir(OUTPUT_DIR_N32)
    export_series()
    export_n32_k16_spectrum()
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")
    print(f"PNG storyboard exported to: {OUTPUT_DIR_N32}")


if __name__ == "__main__":
    main()
