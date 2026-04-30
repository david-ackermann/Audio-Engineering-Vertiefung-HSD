from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "03_istft_und_overlap_add"
    / "03A_istft_rueckweg_pro_frame"
)

DPI = 200
TIME_FIGSIZE = (12.0, 4.6)
PAIR_FIGSIZE = (12.0, 7.8)

TITLE_SIZE = 22
LABEL_SIZE = 20
TICK_SIZE = 17

LEFT_MARGIN = 0.10
RIGHT_MARGIN = 0.98
BOTTOM_MARGIN = 0.18
TOP_MARGIN = 0.86

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
SIGNAL_LIGHT_BLUE = "#bddcf3"
WINDOW_GREEN = "#66b77a"
ORIGINAL_SIGNAL_GREY = "0.86"
OLD_BLOCK_GREY = "0.78"
GRID_GREY = "0.78"
INACTIVE_GREY = "0.84"
FIXED_DISPLAY_LIMIT = 2.5
ERROR_DISPLAY_LIMIT = 1e-14
EDGE_WARNING_RED = "#f6d7d7"
EDGE_SHADE_SHRINK_S = 0.05

FS_HZ = 24.0
DURATION_S = 6.0
TOTAL_SAMPLES = int(FS_HZ * DURATION_S)

WINDOW_LENGTH = 48
HOP_SIZE = 24
SELECTED_FRAME_INDEX = 0
FRAME_SPECTRUM_SEQUENCE = (0, 1, 2)
VISIBLE_FREQ_MAX_HZ = 12.0

FRAME_STARTS = np.arange(0, TOTAL_SAMPLES - WINDOW_LENGTH + 1, HOP_SIZE)
FRAME_TIMES_S = FRAME_STARTS / FS_HZ
WINDOW_DURATION_S = WINDOW_LENGTH / FS_HZ
FRAME_STOPS_S = FRAME_TIMES_S + WINDOW_DURATION_S

TIME_VALUES = np.arange(TOTAL_SAMPLES) / FS_HZ
DENSE_TIME_VALUES = np.linspace(0.0, (TOTAL_SAMPLES - 1) / FS_HZ, 4000)
LOCAL_TIME_VALUES = np.arange(WINDOW_LENGTH) / FS_HZ
WINDOW_VALUES = np.hanning(WINDOW_LENGTH)
WINDOW_SAMPLE_POSITIONS_S = np.arange(WINDOW_LENGTH) / FS_HZ
COHERENT_GAIN = np.mean(WINDOW_VALUES)

FREQ_VALUES_HZ = np.fft.rfftfreq(WINDOW_LENGTH, d=1.0 / FS_HZ)
VISIBLE_FREQ_MASK = FREQ_VALUES_HZ <= VISIBLE_FREQ_MAX_HZ
VISIBLE_FREQ_VALUES_HZ = FREQ_VALUES_HZ[VISIBLE_FREQ_MASK]

TRANSITION_WIDTH_S = 0.18
LOW_FREQUENCY_HZ = 2.35
HIGH_FREQUENCY_HZ = 5.40


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def smooth_step(time_values_s: np.ndarray, center_s: float, width_s: float) -> np.ndarray:
    normalized = (time_values_s - (center_s - 0.5 * width_s)) / width_s
    clipped = np.clip(normalized, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


def build_signal(time_values_s: np.ndarray) -> np.ndarray:
    low_component = 0.95 * np.cos(2.0 * np.pi * LOW_FREQUENCY_HZ * time_values_s + 0.18 * np.pi)
    high_component = 0.90 * np.cos(2.0 * np.pi * HIGH_FREQUENCY_HZ * time_values_s - 0.22 * np.pi)
    mixed_component = 0.58 * low_component + 0.78 * high_component

    switch_12 = smooth_step(time_values_s, DURATION_S / 3.0, TRANSITION_WIDTH_S)
    switch_23 = smooth_step(time_values_s, 2.0 * DURATION_S / 3.0, TRANSITION_WIDTH_S)

    first_region = (1.0 - switch_12) * low_component
    second_region = switch_12 * (1.0 - switch_23) * high_component
    third_region = switch_23 * mixed_component

    fade_in = smooth_step(time_values_s, 0.10, 0.20)
    fade_out = 1.0 - smooth_step(time_values_s, DURATION_S - 0.10, 0.20)

    return (first_region + second_region + third_region) * fade_in * fade_out


SIGNAL_VALUES = build_signal(TIME_VALUES)
DENSE_SIGNAL_VALUES = build_signal(DENSE_TIME_VALUES)
SIGNAL_LIMIT = 1.15 * max(1.0, np.max(np.abs(DENSE_SIGNAL_VALUES)))

FRAME_SEGMENTS = np.vstack([SIGNAL_VALUES[start : start + WINDOW_LENGTH] for start in FRAME_STARTS])
ANALYSIS_BLOCKS = FRAME_SEGMENTS * WINDOW_VALUES
FULL_FRAME_COEFFICIENTS = np.fft.fft(ANALYSIS_BLOCKS, axis=1)
LOCAL_RECONSTRUCTED_BLOCKS = np.real(np.fft.ifft(FULL_FRAME_COEFFICIENTS, axis=1))
SYNTHESIZED_BLOCKS = LOCAL_RECONSTRUCTED_BLOCKS * WINDOW_VALUES


def one_sided_amplitude_scaled_coefficients(coefficients: np.ndarray, n_samples: int) -> np.ndarray:
    scaled_coefficients = coefficients.copy()
    if n_samples % 2 == 0:
        scaled_coefficients[..., 1:-1] *= 2.0
    else:
        scaled_coefficients[..., 1:] *= 2.0
    return scaled_coefficients


DISPLAY_COEFFICIENTS = one_sided_amplitude_scaled_coefficients(
    np.fft.rfft(ANALYSIS_BLOCKS, axis=1) / (WINDOW_LENGTH * COHERENT_GAIN),
    WINDOW_LENGTH,
)
DISPLAY_MAGNITUDES = np.abs(DISPLAY_COEFFICIENTS[:, VISIBLE_FREQ_MASK])


def embed_block(block_values: np.ndarray, frame_index: int) -> np.ndarray:
    full_values = np.zeros(TOTAL_SAMPLES)
    start = FRAME_STARTS[frame_index]
    full_values[start : start + WINDOW_LENGTH] = block_values
    return full_values


SHIFTED_SYNTH_BLOCKS = np.vstack(
    [embed_block(SYNTHESIZED_BLOCKS[frame_index], frame_index) for frame_index in range(len(FRAME_STARTS))]
)

RAW_OVERLAP_ADD = np.sum(SHIFTED_SYNTH_BLOCKS, axis=0)
WINDOW_OVERLAP = np.sum(
    np.vstack([embed_block(WINDOW_VALUES**2, frame_index) for frame_index in range(len(FRAME_STARTS))]),
    axis=0,
)
SHIFTED_WINDOW_OVERLAP_COMPONENTS = np.vstack(
    [embed_block(WINDOW_VALUES**2, frame_index) for frame_index in range(len(FRAME_STARTS))]
)

RECONSTRUCTED_SIGNAL = np.zeros_like(SIGNAL_VALUES)
valid_mask = WINDOW_OVERLAP > 1e-12
INVERSE_WINDOW_OVERLAP = np.full_like(WINDOW_OVERLAP, np.nan)
INVERSE_WINDOW_OVERLAP[valid_mask] = 1.0 / WINDOW_OVERLAP[valid_mask]
RECONSTRUCTED_SIGNAL[valid_mask] = RAW_OVERLAP_ADD[valid_mask] / WINDOW_OVERLAP[valid_mask]
RECONSTRUCTION_ERROR = RECONSTRUCTED_SIGNAL - SIGNAL_VALUES
display_mask = WINDOW_OVERLAP > 0.10
DISPLAY_RECONSTRUCTED_SIGNAL = RECONSTRUCTED_SIGNAL.copy()
DISPLAY_RECONSTRUCTED_SIGNAL[~display_mask] = np.nan
DISPLAY_RECONSTRUCTION_ERROR = RECONSTRUCTION_ERROR.copy()
DISPLAY_RECONSTRUCTION_ERROR[~display_mask] = np.nan
DISPLAY_INVERSE_WINDOW_OVERLAP = INVERSE_WINDOW_OVERLAP.copy()
DISPLAY_INVERSE_WINDOW_OVERLAP[~display_mask] = np.nan
VALID_DISPLAY_INDICES = np.flatnonzero(display_mask)
VALID_DISPLAY_START_S = TIME_VALUES[VALID_DISPLAY_INDICES[0]]
VALID_DISPLAY_STOP_S = TIME_VALUES[VALID_DISPLAY_INDICES[-1]]


def shifted_window_dense(frame_index: int) -> np.ndarray:
    frame_start_s = FRAME_TIMES_S[frame_index]
    frame_stop_s = frame_start_s + WINDOW_DURATION_S
    window_dense = np.zeros_like(DENSE_TIME_VALUES)
    inside_mask = (DENSE_TIME_VALUES >= frame_start_s) & (DENSE_TIME_VALUES <= frame_stop_s)
    local_time_s = DENSE_TIME_VALUES[inside_mask] - frame_start_s
    window_dense[inside_mask] = np.interp(local_time_s, WINDOW_SAMPLE_POSITIONS_S, WINDOW_VALUES)
    return window_dense


def create_time_figure():
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    return fig, ax


def create_pair_figure():
    fig, axes = plt.subplots(2, 1, figsize=PAIR_FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.10, top=0.92, hspace=0.52)
    return fig, axes


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def style_signal_axis(ax, title: str, y_label: str = "Amplitude") -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(TIME_VALUES[0], TIME_VALUES[-1])
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_fixed_signal_axis(ax, title: str, y_label: str = "Amplitude") -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(TIME_VALUES[0], TIME_VALUES[-1])
    ax.set_ylim(-FIXED_DISPLAY_LIMIT, FIXED_DISPLAY_LIMIT)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_local_block_axis(ax, title: str) -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(LOCAL_TIME_VALUES[0], LOCAL_TIME_VALUES[-1])
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(np.arange(0.0, WINDOW_DURATION_S + 0.01, 0.2))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Local time within frame [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_positive_axis(ax, title: str, ymax: float, y_label: str) -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(TIME_VALUES[0], TIME_VALUES[-1])
    ax.set_ylim(0.0, ymax)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_error_axis(ax, title: str, error_limit: float) -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(TIME_VALUES[0], TIME_VALUES[-1])
    ax.set_ylim(-error_limit, error_limit)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Error", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_spectrum_axis(ax, title: str, ymax: float) -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, VISIBLE_FREQ_MAX_HZ)
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 1.0))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|X[m,k]|$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_frame_boundaries(ax, frame_indices) -> None:
    for frame_index in frame_indices:
        ax.axvline(FRAME_TIMES_S[frame_index], color=INACTIVE_GREY, lw=1.0, zorder=0)
        ax.axvline(FRAME_STOPS_S[frame_index], color=INACTIVE_GREY, lw=1.0, zorder=0)


def draw_window_edges(ax, frame_indices, *, alpha: float = 0.95) -> None:
    for frame_index in frame_indices:
        ax.axvline(FRAME_TIMES_S[frame_index], color=WINDOW_GREEN, linestyle="--", lw=1.5, alpha=alpha, zorder=2)
        ax.axvline(FRAME_STOPS_S[frame_index], color=WINDOW_GREEN, linestyle="--", lw=1.5, alpha=alpha, zorder=2)


def plot_full_signal_background(ax) -> None:
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=ORIGINAL_SIGNAL_GREY, lw=2.0, zorder=1)


def shade_edge_regions(ax) -> None:
    left_edge_stop_s = max(0.0, VALID_DISPLAY_START_S - EDGE_SHADE_SHRINK_S)
    right_edge_start_s = min(DURATION_S, VALID_DISPLAY_STOP_S + EDGE_SHADE_SHRINK_S)
    if left_edge_stop_s > 0.0:
        ax.axvspan(0.0, left_edge_stop_s, color=EDGE_WARNING_RED, alpha=0.45, zorder=0)
    if right_edge_start_s < DURATION_S:
        ax.axvspan(right_edge_start_s, DURATION_S, color=EDGE_WARNING_RED, alpha=0.45, zorder=0)


def plot_embedded_block(ax, block_values: np.ndarray, color: str, lw: float, alpha: float) -> None:
    active_mask = np.abs(block_values) > 1e-7
    ax.plot(TIME_VALUES[active_mask], block_values[active_mask], color=color, lw=lw, alpha=alpha, zorder=3)


def draw_sample_stems(
    ax,
    sample_positions: np.ndarray,
    sample_values: np.ndarray,
    *,
    color: str = SIGNAL_BLUE,
    alpha: float = 0.85,
    zorder: int = 4,
) -> None:
    finite_mask = np.isfinite(sample_values)
    sample_positions = sample_positions[finite_mask]
    sample_values = sample_values[finite_mask]
    ax.vlines(sample_positions, 0.0, sample_values, color=color, lw=1.6, alpha=alpha, zorder=zorder)
    ax.scatter(
        sample_positions,
        sample_values,
        s=38,
        color=color,
        edgecolor="white",
        linewidth=0.7,
        zorder=zorder + 1,
    )


def plot_embedded_signal_sequence(
    ax,
    block_values: np.ndarray,
    color: str,
    alpha: float,
    *,
    zorder: int = 4,
) -> None:
    active_mask = np.isfinite(block_values) & (np.abs(block_values) > 1e-7)
    draw_sample_stems(
        ax,
        TIME_VALUES[active_mask],
        block_values[active_mask],
        color=color,
        alpha=alpha,
        zorder=zorder,
    )


def export_selected_frame_and_spectrum(frame_index: int, filename: str) -> None:
    fig, axes = create_pair_figure()
    ax_time, ax_spec = axes

    window_dense = shifted_window_dense(frame_index)
    frame_start = FRAME_STARTS[frame_index]
    frame_stop = frame_start + WINDOW_LENGTH
    sample_times = TIME_VALUES[frame_start:frame_stop]
    windowed_samples = ANALYSIS_BLOCKS[frame_index]

    for frame_time_s in FRAME_TIMES_S:
        ax_time.axvline(frame_time_s, color=INACTIVE_GREY, lw=1.0, alpha=0.45, zorder=0)
    draw_window_edges(ax_time, [frame_index])
    ax_time.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=ORIGINAL_SIGNAL_GREY, lw=2.0, zorder=1)
    draw_sample_stems(ax_time, sample_times, windowed_samples)
    ax_time.plot(DENSE_TIME_VALUES, 0.98 * window_dense, color=WINDOW_GREEN, lw=1.7, zorder=3)
    style_signal_axis(ax_time, f"Frame m = {frame_index}")

    magnitudes = DISPLAY_MAGNITUDES[frame_index]
    ax_spec.vlines(VISIBLE_FREQ_VALUES_HZ, 0.0, magnitudes, color=SIGNAL_BLUE, lw=2.4, zorder=2)
    ax_spec.plot(VISIBLE_FREQ_VALUES_HZ, magnitudes, "o", color=SIGNAL_BLUE, ms=6, zorder=2)
    style_spectrum_axis(ax_spec, "Frame spectrum", 1.15 * max(0.55, np.max(DISPLAY_MAGNITUDES)))
    save_figure(fig, filename)


def export_inverse_dft_of_one_frame() -> None:
    fig, ax = create_time_figure()
    ax.plot(LOCAL_TIME_VALUES, ANALYSIS_BLOCKS[SELECTED_FRAME_INDEX], color=OLD_BLOCK_GREY, lw=2.4, zorder=1)
    draw_sample_stems(ax, LOCAL_TIME_VALUES, LOCAL_RECONSTRUCTED_BLOCKS[SELECTED_FRAME_INDEX])
    style_local_block_axis(ax, "iDFT of frame 0 spectrum")
    save_figure(fig, "05_idft_ergibt_lokalen_block.png")


def export_shifted_blocks(filename: str, frame_indices, title: str) -> None:
    fig, ax = create_time_figure()
    plot_full_signal_background(ax)

    newest_frame_index = frame_indices[-1]
    for frame_index in frame_indices[:-1]:
        plot_embedded_signal_sequence(ax, SHIFTED_SYNTH_BLOCKS[frame_index], SIGNAL_LIGHT_BLUE, alpha=1.0, zorder=3)
    plot_embedded_signal_sequence(ax, SHIFTED_SYNTH_BLOCKS[newest_frame_index], SIGNAL_BLUE, alpha=0.9, zorder=5)

    style_fixed_signal_axis(ax, title)
    save_figure(fig, filename)


def export_all_shifted_blocks() -> None:
    fig, ax = create_time_figure()
    plot_full_signal_background(ax)
    last_frame_index = len(FRAME_STARTS) - 1
    for frame_index in range(len(FRAME_STARTS)):
        color = SIGNAL_BLUE if frame_index == last_frame_index else SIGNAL_LIGHT_BLUE
        alpha = 0.95 if frame_index == last_frame_index else 0.8
        zorder = 5 if frame_index == last_frame_index else 3
        plot_embedded_signal_sequence(ax, SHIFTED_SYNTH_BLOCKS[frame_index], color, alpha=alpha, zorder=zorder)
    style_fixed_signal_axis(ax, "All shifted synthesis blocks")
    save_figure(fig, "09_alle_frames_als_einzelbeitraege.png")


def export_raw_overlap_add_sum() -> None:
    fig, ax = create_time_figure()
    plot_full_signal_background(ax)
    for frame_index in range(len(FRAME_STARTS)):
        plot_embedded_signal_sequence(ax, SHIFTED_SYNTH_BLOCKS[frame_index], SIGNAL_LIGHT_BLUE, alpha=0.65, zorder=3)
    draw_sample_stems(ax, TIME_VALUES, RAW_OVERLAP_ADD, color=SIGNAL_BLUE, alpha=0.9, zorder=5)
    style_fixed_signal_axis(ax, "Raw overlap-add sum")
    save_figure(fig, "10_rohe_overlap_add_summe.png")


def export_window_overlap() -> None:
    fig, ax = create_time_figure()
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=ORIGINAL_SIGNAL_GREY, lw=2.0, zorder=1)
    for frame_index in range(len(FRAME_STARTS)):
        plot_embedded_block(ax, SHIFTED_WINDOW_OVERLAP_COMPONENTS[frame_index], WINDOW_GREEN, lw=1.2, alpha=0.95)
    draw_sample_stems(ax, TIME_VALUES, RAW_OVERLAP_ADD, color=SIGNAL_BLUE, alpha=0.9, zorder=4)
    ax.plot(TIME_VALUES, WINDOW_OVERLAP, color=WINDOW_GREEN, lw=2.6)
    style_fixed_signal_axis(ax, "Raw sum and window overlap", "Amplitude / weight")
    save_figure(fig, "11_fensterueberlappung.png")


def export_inverse_window_overlap() -> None:
    fig, ax = create_time_figure()
    clipped_inverse_weight = np.clip(DISPLAY_INVERSE_WINDOW_OVERLAP, 0.0, FIXED_DISPLAY_LIMIT)
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=ORIGINAL_SIGNAL_GREY, lw=2.0, zorder=1)
    draw_sample_stems(ax, TIME_VALUES, RAW_OVERLAP_ADD, color=SIGNAL_BLUE, alpha=0.9, zorder=4)
    ax.plot(TIME_VALUES, clipped_inverse_weight, color=WINDOW_GREEN, lw=2.6)
    style_fixed_signal_axis(ax, "Raw sum and inverse overlap weight", "Amplitude / weight")
    save_figure(fig, "12_inverse_fensterueberlappung.png")


def export_reconstruction_vs_original() -> None:
    fig, ax = create_time_figure()
    shade_edge_regions(ax)
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=ORIGINAL_SIGNAL_GREY, lw=2.0, zorder=1)
    draw_sample_stems(ax, TIME_VALUES, RECONSTRUCTED_SIGNAL, color=SIGNAL_BLUE, alpha=0.9, zorder=4)
    style_fixed_signal_axis(ax, "Reconstruction and original")
    save_figure(fig, "13_rekonstruktion_gegen_original.png")


def export_reconstruction_error() -> None:
    fig, ax = create_time_figure()
    shade_edge_regions(ax)
    draw_sample_stems(ax, TIME_VALUES, RECONSTRUCTION_ERROR, color=SIGNAL_BLUE, alpha=0.9, zorder=4)
    style_error_axis(ax, "Reconstruction error", ERROR_DISPLAY_LIMIT)
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    save_figure(fig, "14_rekonstruktionsfehler.png")


def main() -> None:
    clear_output_dir()
    export_selected_frame_and_spectrum(FRAME_SPECTRUM_SEQUENCE[0], "01_frame_0_und_spektrum.png")
    export_selected_frame_and_spectrum(FRAME_SPECTRUM_SEQUENCE[1], "02_frame_1_und_spektrum.png")
    export_selected_frame_and_spectrum(FRAME_SPECTRUM_SEQUENCE[2], "03_frame_2_und_spektrum.png")
    export_selected_frame_and_spectrum(len(FRAME_STARTS) - 1, "04_letztes_frame_und_spektrum.png")
    export_inverse_dft_of_one_frame()
    export_shifted_blocks("06_erster_block_an_position_mh.png", [SELECTED_FRAME_INDEX], "First block at position mH")
    export_shifted_blocks("07_zwei_bloecke_ueberlappen.png", [SELECTED_FRAME_INDEX, SELECTED_FRAME_INDEX + 1], "Two frames overlap")
    export_shifted_blocks(
        "08_drei_bloecke_ueberlagern_sich.png",
        [SELECTED_FRAME_INDEX, SELECTED_FRAME_INDEX + 1, SELECTED_FRAME_INDEX + 2],
        "Three frames overlap",
    )
    export_all_shifted_blocks()
    export_raw_overlap_add_sum()
    export_window_overlap()
    export_inverse_window_overlap()
    export_reconstruction_vs_original()
    export_reconstruction_error()
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
