from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "02_stft_und_spektrogramm"
    / "02B_stft_mit_hann_fenster"
)
OUTPUT_DIR = OUTPUT_ROOT_DIR

DPI = 200
TIME_FIGSIZE = (12.0, 4.6)
PAIR_FIGSIZE = (12.0, 7.8)
MATRIX_FIGSIZE = (10.4, 6.2)

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
OLD_WINDOW_GREY = "0.87"
INACTIVE_GREY = "0.82"
GRID_GREY = "0.78"

FS_HZ = 24.0
DURATION_S = 6.0
TOTAL_SAMPLES = int(FS_HZ * DURATION_S)

WINDOW_LENGTH = 48
HOP_SIZE = 24
TRANSITION_WIDTH_S = 0.18
LOW_FREQUENCY_HZ = 2.35
HIGH_FREQUENCY_HZ = 5.40
DB_FLOOR = -60.0

FRAME_STARTS = np.arange(0, TOTAL_SAMPLES - WINDOW_LENGTH + 1, HOP_SIZE)
FRAME_TIMES_S = FRAME_STARTS / FS_HZ
WINDOW_DURATION_S = WINDOW_LENGTH / FS_HZ
FRAME_CENTERS_S = FRAME_TIMES_S + 0.5 * WINDOW_DURATION_S
FRAME_INDICES = np.arange(len(FRAME_STARTS))

FIRST_FRAME_INDEX = 0
SECOND_FRAME_INDEX = 1
LOCAL_SPECTRUM_FRAME_SEQUENCE = (0, 1, 2, 3, 4)
MATRIX_BUILD_FRAME_SEQUENCE = (0, 1, 2, 3, 4)

TIME_VALUES = np.arange(TOTAL_SAMPLES) / FS_HZ
DENSE_TIME_VALUES = np.linspace(0.0, (TOTAL_SAMPLES - 1) / FS_HZ, 4000)

WINDOW_DISPLAY_NAME = "Hann"
WINDOW_FILENAME_STEM = "hannfenster"
WINDOW_VALUES = np.hanning(WINDOW_LENGTH)
FULL_WINDOW_VALUES = np.hanning(TOTAL_SAMPLES)
DENSE_FULL_WINDOW_VALUES = np.interp(DENSE_TIME_VALUES, TIME_VALUES, FULL_WINDOW_VALUES)
WINDOW_SAMPLE_POSITIONS = np.arange(WINDOW_LENGTH) / FS_HZ

FREQ_VALUES_HZ = np.fft.rfftfreq(WINDOW_LENGTH, d=1.0 / FS_HZ)
VISIBLE_FREQ_MAX_HZ = 12.0
VISIBLE_FREQ_MASK = FREQ_VALUES_HZ <= VISIBLE_FREQ_MAX_HZ
VISIBLE_FREQ_VALUES_HZ = FREQ_VALUES_HZ[VISIBLE_FREQ_MASK]
VISIBLE_BIN_INDICES = np.arange(len(FREQ_VALUES_HZ))[VISIBLE_FREQ_MASK]


def clear_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def clear_legacy_output_files():
    OUTPUT_ROOT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_ROOT_DIR.glob("*.png"):
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


def shifted_window_dense(frame_start: int) -> np.ndarray:
    frame_start_s = frame_start / FS_HZ
    frame_stop_s = frame_start_s + WINDOW_DURATION_S
    window_dense = np.zeros_like(DENSE_TIME_VALUES)
    inside_mask = (DENSE_TIME_VALUES >= frame_start_s) & (DENSE_TIME_VALUES <= frame_stop_s)
    relative_positions_s = DENSE_TIME_VALUES[inside_mask] - frame_start_s
    window_dense[inside_mask] = np.interp(relative_positions_s, WINDOW_SAMPLE_POSITIONS, WINDOW_VALUES)
    return window_dense


def coherent_gain_normalized_spectrum(frame_values: np.ndarray) -> np.ndarray:
    coherent_gain = np.mean(WINDOW_VALUES)
    coefficients = np.fft.rfft(frame_values * WINDOW_VALUES) / (WINDOW_LENGTH * coherent_gain)
    coefficients = one_sided_amplitude_scaled_coefficients(coefficients, WINDOW_LENGTH)
    return coefficients[VISIBLE_FREQ_MASK]


def one_sided_amplitude_scaled_coefficients(coefficients: np.ndarray, n_samples: int) -> np.ndarray:
    scaled_coefficients = coefficients.copy()
    if n_samples % 2 == 0:
        scaled_coefficients[1:-1] *= 2.0
    else:
        scaled_coefficients[1:] *= 2.0
    return scaled_coefficients


def magnitude_to_db(magnitudes: np.ndarray) -> np.ndarray:
    minimum_magnitude = 10.0 ** (DB_FLOOR / 20.0)
    return 20.0 * np.log10(np.maximum(magnitudes, minimum_magnitude))


FRAME_BLOCKS = np.vstack([SIGNAL_VALUES[start : start + WINDOW_LENGTH] for start in FRAME_STARTS])
STFT_COEFFICIENTS = np.vstack([coherent_gain_normalized_spectrum(block) for block in FRAME_BLOCKS])
STFT_MAGNITUDES = np.abs(STFT_COEFFICIENTS)

FULL_FREQ_VALUES_HZ = np.fft.rfftfreq(TOTAL_SAMPLES, d=1.0 / FS_HZ)
FULL_VISIBLE_FREQ_MASK = FULL_FREQ_VALUES_HZ <= VISIBLE_FREQ_MAX_HZ
FULL_VISIBLE_FREQ_VALUES_HZ = FULL_FREQ_VALUES_HZ[FULL_VISIBLE_FREQ_MASK]
FULL_SPECTRUM_COEFFICIENTS = one_sided_amplitude_scaled_coefficients(
    np.fft.rfft(SIGNAL_VALUES * FULL_WINDOW_VALUES) / (TOTAL_SAMPLES * np.mean(FULL_WINDOW_VALUES)),
    TOTAL_SAMPLES,
)
FULL_SPECTRUM_MAGNITUDES = np.abs(FULL_SPECTRUM_COEFFICIENTS)[FULL_VISIBLE_FREQ_MASK]
MATRIX_TIGHT_BBOXES = {}


def configure_window_variant(window_kind: str):
    global OUTPUT_DIR
    global WINDOW_DISPLAY_NAME
    global WINDOW_FILENAME_STEM
    global WINDOW_VALUES
    global FULL_WINDOW_VALUES
    global DENSE_FULL_WINDOW_VALUES
    global STFT_COEFFICIENTS
    global STFT_MAGNITUDES
    global FULL_SPECTRUM_COEFFICIENTS
    global FULL_SPECTRUM_MAGNITUDES

    if window_kind == "rectangular":
        OUTPUT_DIR = OUTPUT_ROOT_DIR / "01_rechteckfenster_nicht_binzentriert"
        WINDOW_DISPLAY_NAME = "Rectangular"
        WINDOW_FILENAME_STEM = "rechteckfenster"
        WINDOW_VALUES = np.ones(WINDOW_LENGTH)
        FULL_WINDOW_VALUES = np.ones(TOTAL_SAMPLES)
    elif window_kind == "hann":
        OUTPUT_DIR = OUTPUT_ROOT_DIR / "02_hannfenster_nicht_binzentriert"
        WINDOW_DISPLAY_NAME = "Hann"
        WINDOW_FILENAME_STEM = "hannfenster"
        WINDOW_VALUES = np.hanning(WINDOW_LENGTH)
        FULL_WINDOW_VALUES = np.hanning(TOTAL_SAMPLES)
    else:
        raise ValueError(f"Unknown window kind: {window_kind}")

    DENSE_FULL_WINDOW_VALUES = np.interp(DENSE_TIME_VALUES, TIME_VALUES, FULL_WINDOW_VALUES)
    STFT_COEFFICIENTS = np.vstack([coherent_gain_normalized_spectrum(block) for block in FRAME_BLOCKS])
    STFT_MAGNITUDES = np.abs(STFT_COEFFICIENTS)
    FULL_SPECTRUM_COEFFICIENTS = one_sided_amplitude_scaled_coefficients(
        np.fft.rfft(SIGNAL_VALUES * FULL_WINDOW_VALUES) / (TOTAL_SAMPLES * np.mean(FULL_WINDOW_VALUES)),
        TOTAL_SAMPLES,
    )
    FULL_SPECTRUM_MAGNITUDES = np.abs(FULL_SPECTRUM_COEFFICIENTS)[FULL_VISIBLE_FREQ_MASK]


def create_time_figure():
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    fig.subplots_adjust(left=LEFT_MARGIN, right=RIGHT_MARGIN, bottom=BOTTOM_MARGIN, top=TOP_MARGIN)
    return fig, ax


def create_pair_figure():
    fig, axes = plt.subplots(2, 1, figsize=PAIR_FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.10, top=0.92, hspace=0.52)
    return fig, axes


def create_matrix_figure():
    fig, ax = plt.subplots(figsize=MATRIX_FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.90, bottom=0.12, top=0.90)
    return fig, ax


def save_figure(fig, filename: str, *, tight: bool = False, store_bbox_key: str | None = None, bbox_key: str | None = None):
    if store_bbox_key is not None:
        fig.canvas.draw()
        MATRIX_TIGHT_BBOXES[store_bbox_key] = fig.get_tightbbox(fig.canvas.get_renderer()).padded(0.015)

    if bbox_key is not None:
        fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches=MATRIX_TIGHT_BBOXES[bbox_key], pad_inches=0.0)
    elif tight:
        fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    else:
        fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def style_time_axis(ax, title: str):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(TIME_VALUES[0], TIME_VALUES[-1])
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_local_index_axis(ax, title: str, reference_frame_index: int):
    frame_start = FRAME_STARTS[reference_frame_index]
    x_min = -frame_start
    x_max = TOTAL_SAMPLES - frame_start
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(np.arange(x_min, x_max + HOP_SIZE, HOP_SIZE))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Local sample index n", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_local_spectrum_axis(ax, title: str):
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


def style_local_spectrum_db_axis(ax, title: str):
    ax.axhline(DB_FLOOR, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, VISIBLE_FREQ_MAX_HZ)
    ax.set_ylim(DB_FLOOR, 0.0)
    ax.set_xticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 1.0))
    ax.set_yticks(np.arange(DB_FLOOR, 0.01, 10.0))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude [dB]", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_local_bin_spectrum_axis(ax, title: str):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, VISIBLE_BIN_INDICES[-1])
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks(np.arange(0, VISIBLE_BIN_INDICES[-1] + 1, 2))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel(r"DFT bin $k$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|X[m,k]|$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_full_spectrum_axis(ax, title: str):
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, VISIBLE_FREQ_MAX_HZ)
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 1.0))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|X[k]|$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def draw_signal(ax):
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.4, zorder=2)


def draw_discrete_samples(ax, sample_positions: np.ndarray, sample_values: np.ndarray):
    ax.vlines(sample_positions, 0.0, sample_values, color=SIGNAL_BLUE, lw=1.6, alpha=0.85, zorder=4)
    ax.scatter(
        sample_positions,
        sample_values,
        s=38,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=0.7,
        zorder=5,
    )


def draw_frame_grid(ax, alpha: float = 1.0):
    for frame_start_s in FRAME_TIMES_S:
        ax.axvline(frame_start_s, color=INACTIVE_GREY, lw=1.15, alpha=alpha, zorder=0)


def draw_window_band(ax, frame_index: int, color: str, alpha: float, lw: float):
    window_dense = shifted_window_dense(FRAME_STARTS[frame_index])
    window_band = 0.98 * window_dense
    ax.fill_between(
        DENSE_TIME_VALUES,
        0.0,
        window_band,
        color=color,
        alpha=alpha,
        zorder=1,
    )
    ax.plot(DENSE_TIME_VALUES, window_band, color=color, lw=lw, zorder=3)


def draw_window_band_local_index(ax, frame_index: int, reference_frame_index: int, color: str, alpha: float, lw: float):
    frame_start = FRAME_STARTS[reference_frame_index]
    local_dense_indices = DENSE_TIME_VALUES * FS_HZ - frame_start
    window_dense = shifted_window_dense(FRAME_STARTS[frame_index])
    window_band = 0.98 * window_dense
    ax.fill_between(
        local_dense_indices,
        0.0,
        window_band,
        color=color,
        alpha=alpha,
        zorder=1,
    )
    ax.plot(local_dense_indices, window_band, color=color, lw=lw, zorder=3)


def draw_full_observation_window(ax):
    window_band = 0.98 * DENSE_FULL_WINDOW_VALUES
    ax.fill_between(DENSE_TIME_VALUES, 0.0, window_band, color=WINDOW_GREEN, alpha=0.14, zorder=1)
    ax.plot(DENSE_TIME_VALUES, window_band, color=WINDOW_GREEN, lw=1.8, zorder=3)


def draw_previous_windows(ax, previous_frame_indices):
    for frame_index in previous_frame_indices:
        draw_window_band(ax, frame_index, OLD_WINDOW_GREY, alpha=0.14, lw=1.2)


def draw_previous_windows_local_index(ax, previous_frame_indices, reference_frame_index: int):
    for frame_index in previous_frame_indices:
        draw_window_band_local_index(ax, frame_index, reference_frame_index, OLD_WINDOW_GREY, alpha=0.14, lw=1.2)


def draw_signal_with_active_segment(ax, active_frame_index: int):
    frame_start = FRAME_STARTS[active_frame_index]
    frame_stop = frame_start + WINDOW_LENGTH
    sample_times_s = TIME_VALUES[frame_start:frame_stop]
    sample_values = SIGNAL_VALUES[frame_start:frame_stop] * WINDOW_VALUES
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color="0.72", lw=2.2, zorder=1)
    draw_discrete_samples(ax, sample_times_s, sample_values)


def draw_full_signal_as_active_segment(ax):
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color="0.72", lw=2.2, zorder=1)
    draw_discrete_samples(ax, TIME_VALUES, SIGNAL_VALUES * FULL_WINDOW_VALUES)


def draw_signal_with_active_segment_local_index(ax, frame_index: int):
    frame_start = FRAME_STARTS[frame_index]
    frame_stop = frame_start + WINDOW_LENGTH
    local_dense_indices = DENSE_TIME_VALUES * FS_HZ - frame_start
    local_sample_indices = np.arange(TOTAL_SAMPLES) - frame_start
    active_local_indices = np.arange(frame_start, frame_stop) - frame_start
    active_sample_values = SIGNAL_VALUES[frame_start:frame_stop] * WINDOW_VALUES

    ax.plot(local_dense_indices, DENSE_SIGNAL_VALUES, color="0.72", lw=2.2, zorder=1)
    draw_discrete_samples(ax, active_local_indices, active_sample_values)
    ax.scatter(
        local_sample_indices,
        SIGNAL_VALUES,
        s=14,
        color="0.70",
        edgecolor="white",
        linewidth=0.35,
        alpha=0.65,
        zorder=2,
    )


def add_rightward_hop_annotation(ax, source_frame_index: int, target_frame_index: int):
    source_time_s = FRAME_TIMES_S[source_frame_index]
    target_time_s = FRAME_TIMES_S[target_frame_index]
    y_position = -0.88 * SIGNAL_LIMIT
    ax.annotate(
        "",
        xy=(target_time_s, y_position),
        xytext=(source_time_s, y_position),
        arrowprops=dict(arrowstyle="->", color=SIGNAL_BLUE, lw=1.8),
    )
    ax.text(
        0.5 * (target_time_s + source_time_s),
        y_position + 0.10,
        r"Hop $H$",
        color=SIGNAL_BLUE,
        fontsize=17,
        ha="center",
        va="bottom",
    )


def export_signal_with_empty_spectrum_axis():
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_signal(ax_time)
    style_time_axis(ax_time, r"Signal over observation time $T$")
    style_full_spectrum_axis(ax_spectrum, "Frequency axis")

    save_figure(fig, "01_signal_und_frequenzachse.png")


def export_full_window_spectrum():
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_full_observation_window(ax_time)
    draw_full_signal_as_active_segment(ax_time)
    style_time_axis(ax_time, rf"One {WINDOW_DISPLAY_NAME} window over $T$")

    ax_spectrum.vlines(FULL_VISIBLE_FREQ_VALUES_HZ, 0.0, FULL_SPECTRUM_MAGNITUDES, color=SIGNAL_BLUE, lw=2.0, zorder=2)
    ax_spectrum.scatter(
        FULL_VISIBLE_FREQ_VALUES_HZ,
        FULL_SPECTRUM_MAGNITUDES,
        s=45,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    style_full_spectrum_axis(ax_spectrum, r"Spectrum over $T$")

    save_figure(fig, f"02_{WINDOW_FILENAME_STEM}_ueber_T_und_spektrum.png")


def export_local_index_bridge(image_number: int, frame_index: int, previous_frame_indices):
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_previous_windows_local_index(ax_time, previous_frame_indices, frame_index)
    draw_window_band_local_index(ax_time, frame_index, frame_index, WINDOW_GREEN, alpha=0.16, lw=1.8)
    draw_signal_with_active_segment_local_index(ax_time, frame_index)
    style_local_index_axis(ax_time, rf"Frame $m={frame_index}$ with moving local index", frame_index)

    active_magnitude = STFT_MAGNITUDES[frame_index]
    ax_spectrum.vlines(VISIBLE_BIN_INDICES, 0.0, active_magnitude, color=SIGNAL_BLUE, lw=2.4, zorder=2, clip_on=False)
    ax_spectrum.scatter(
        VISIBLE_BIN_INDICES,
        active_magnitude,
        s=65,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
        clip_on=False,
    )
    style_local_bin_spectrum_axis(ax_spectrum, "Local spectrum")

    save_figure(fig, f"{image_number:02d}_frame_{frame_index}_lokaler_index_n.png")


def export_single_analysis_window():
    fig, ax = create_time_figure()
    draw_frame_grid(ax, alpha=0.45)
    draw_window_band(ax, FIRST_FRAME_INDEX, WINDOW_GREEN, alpha=0.14, lw=1.8)
    draw_signal_with_active_segment(ax, FIRST_FRAME_INDEX)
    style_time_axis(ax, f"One {WINDOW_DISPLAY_NAME} window")
    save_figure(fig, "02_einzelnes_analysefenster.png")


def export_hop_shift():
    fig, ax = create_time_figure()
    draw_frame_grid(ax, alpha=0.35)
    draw_window_band(ax, FIRST_FRAME_INDEX, SIGNAL_LIGHT_BLUE, alpha=0.18, lw=1.5)
    draw_window_band(ax, SECOND_FRAME_INDEX, WINDOW_GREEN, alpha=0.16, lw=1.8)
    draw_signal_with_active_segment(ax, SECOND_FRAME_INDEX)
    add_rightward_hop_annotation(ax, FIRST_FRAME_INDEX, SECOND_FRAME_INDEX)
    style_time_axis(ax, "Hop shifts the window")
    save_figure(fig, "03_hop_verschiebt_das_fenster.png")


def export_overlapping_frames():
    fig, ax = create_time_figure()
    draw_frame_grid(ax, alpha=0.30)
    for frame_index in FRAME_INDICES:
        draw_window_band(ax, frame_index, WINDOW_GREEN, alpha=0.08, lw=1.2)
    ax.scatter(FRAME_CENTERS_S, np.full_like(FRAME_CENTERS_S, -0.97 * SIGNAL_LIMIT), s=22, color=SIGNAL_BLUE, zorder=4)
    draw_signal(ax)
    style_time_axis(ax, f"Many overlapping {WINDOW_DISPLAY_NAME} frames")
    save_figure(fig, "04_mehrere_ueberlappte_fenster.png")


def export_frame_spectrum_step(image_number: int, frame_index: int, previous_frame_indices):
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_frame_grid(ax_time, alpha=0.25)
    draw_previous_windows(ax_time, previous_frame_indices)
    draw_window_band(ax_time, frame_index, WINDOW_GREEN, alpha=0.16, lw=1.8)
    draw_signal_with_active_segment(ax_time, frame_index)
    style_time_axis(ax_time, f"Frame m = {frame_index}")

    active_magnitude = STFT_MAGNITUDES[frame_index]
    ax_spectrum.vlines(VISIBLE_FREQ_VALUES_HZ, 0.0, active_magnitude, color=SIGNAL_BLUE, lw=2.4, zorder=2)
    ax_spectrum.scatter(
        VISIBLE_FREQ_VALUES_HZ,
        active_magnitude,
        s=65,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )
    style_local_spectrum_axis(ax_spectrum, "Local spectrum")
    save_figure(fig, f"{image_number:02d}_frame_{frame_index}_lokales_spektrum.png")


def export_frame_spectrum_db_step(image_number: int, frame_index: int, previous_frame_indices):
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_frame_grid(ax_time, alpha=0.25)
    draw_previous_windows(ax_time, previous_frame_indices)
    draw_window_band(ax_time, frame_index, WINDOW_GREEN, alpha=0.16, lw=1.8)
    draw_signal_with_active_segment(ax_time, frame_index)
    style_time_axis(ax_time, f"Frame m = {frame_index}")

    active_db = magnitude_to_db(STFT_MAGNITUDES[frame_index])
    ax_spectrum.vlines(VISIBLE_FREQ_VALUES_HZ, DB_FLOOR, active_db, color=SIGNAL_BLUE, lw=2.4, zorder=2)
    ax_spectrum.scatter(
        VISIBLE_FREQ_VALUES_HZ,
        active_db,
        s=65,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )
    style_local_spectrum_db_axis(ax_spectrum, "Local spectrum in dB")
    save_figure(fig, f"{image_number:02d}_frame_{frame_index}_lokales_spektrum_db.png")


def export_stft_matrix_progress(image_number: int, max_frame_index: int):
    fig, ax = create_matrix_figure()
    matrix_data = np.full_like(STFT_MAGNITUDES, np.nan)
    matrix_data[: max_frame_index + 1, :] = STFT_MAGNITUDES[: max_frame_index + 1, :]
    cmap = plt.get_cmap("magma").copy()
    cmap.set_bad(color="white")
    image = ax.imshow(
        np.ma.masked_invalid(matrix_data).T,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        interpolation="nearest",
        extent=(-0.5, len(FRAME_INDICES) - 0.5, 0.0, VISIBLE_BIN_INDICES[-1]),
        vmin=0.0,
        vmax=1.0,
    )
    ax.set_title(rf"STFT samples up to frame $m={max_frame_index}$", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Bin index k", fontsize=LABEL_SIZE)
    ax.set_xticks(FRAME_INDICES)
    ax.set_yticks(np.arange(0, len(VISIBLE_FREQ_VALUES_HZ), 2))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 1)
    colorbar.set_label("Magnitude", fontsize=LABEL_SIZE - 1)
    save_figure(
        fig,
        f"{image_number:02d}_stft_matrix_bis_frame_{max_frame_index}.png",
        tight=True,
    )


def export_stft_matrix_progress_frequency_axis(image_number: int, max_frame_index: int):
    fig, ax = create_matrix_figure()
    matrix_data = np.full_like(STFT_MAGNITUDES, np.nan)
    matrix_data[: max_frame_index + 1, :] = STFT_MAGNITUDES[: max_frame_index + 1, :]
    cmap = plt.get_cmap("magma").copy()
    cmap.set_bad(color="white")
    image = ax.imshow(
        np.ma.masked_invalid(matrix_data).T,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        interpolation="nearest",
        extent=(-0.5, len(FRAME_INDICES) - 0.5, 0.0, VISIBLE_FREQ_MAX_HZ),
        vmin=0.0,
        vmax=1.0,
    )
    ax.set_title(rf"STFT samples up to frame $m={max_frame_index}$", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_xticks(FRAME_INDICES)
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 2.0))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 1)
    colorbar.set_label("Magnitude", fontsize=LABEL_SIZE - 1)
    save_figure(fig, f"{image_number:02d}_stft_matrix_bis_frame_{max_frame_index}_hz.png", tight=True)


def export_stft_matrix_all(image_number: int):
    fig, ax = create_matrix_figure()
    image = ax.imshow(
        STFT_MAGNITUDES.T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="nearest",
        extent=(-0.5, len(FRAME_INDICES) - 0.5, 0.0, VISIBLE_BIN_INDICES[-1]),
    )
    ax.set_title(r"STFT samples $|X[m,k]|$", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Bin index k", fontsize=LABEL_SIZE)
    ax.set_xticks(FRAME_INDICES)
    ax.set_yticks(np.arange(0, len(VISIBLE_FREQ_VALUES_HZ), 2))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 1)
    colorbar.set_label("Magnitude", fontsize=LABEL_SIZE - 1)
    image.set_clim(0.0, 1.0)
    save_figure(fig, f"{image_number:02d}_stft_matrix_alle_frames.png", tight=True, store_bbox_key="matrix_k")


def export_stft_matrix_all_frequency_axis(image_number: int):
    fig, ax = create_matrix_figure()
    image = ax.imshow(
        STFT_MAGNITUDES.T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="nearest",
        extent=(
            -0.5,
            len(FRAME_INDICES) - 0.5,
            0.0,
            VISIBLE_FREQ_MAX_HZ,
        ),
        vmin=0.0,
        vmax=1.0,
    )
    ax.set_title(r"STFT samples $|X[m,k]|$", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_xticks(FRAME_INDICES)
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 2.0))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 1)
    colorbar.set_label("Magnitude", fontsize=LABEL_SIZE - 1)
    save_figure(fig, f"{image_number:02d}_stft_matrix_alle_frames_hz.png", tight=True, store_bbox_key="matrix_hz")


def export_stft_matrix_all_db(image_number: int):
    fig, ax = create_matrix_figure()
    image = ax.imshow(
        magnitude_to_db(STFT_MAGNITUDES).T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="nearest",
        extent=(-0.5, len(FRAME_INDICES) - 0.5, 0.0, VISIBLE_BIN_INDICES[-1]),
        vmin=DB_FLOOR,
        vmax=0.0,
    )
    ax.set_title(r"STFT samples $20\log_{10}|X[m,k]|$", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Bin index k", fontsize=LABEL_SIZE)
    ax.set_xticks(FRAME_INDICES)
    ax.set_yticks(np.arange(0, len(VISIBLE_FREQ_VALUES_HZ), 2))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 4, pad=0)
    colorbar.set_label("Magnitude [dB]", fontsize=LABEL_SIZE - 3, labelpad=1)
    save_figure(fig, f"{image_number:02d}_stft_matrix_alle_frames_db.png", bbox_key="matrix_k")


def export_stft_matrix_all_db_frequency_axis(image_number: int):
    fig, ax = create_matrix_figure()
    image = ax.imshow(
        magnitude_to_db(STFT_MAGNITUDES).T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="nearest",
        extent=(-0.5, len(FRAME_INDICES) - 0.5, 0.0, VISIBLE_FREQ_MAX_HZ),
        vmin=DB_FLOOR,
        vmax=0.0,
    )
    ax.set_title(r"STFT samples $20\log_{10}|X[m,k]|$", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_xticks(FRAME_INDICES)
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 2.0))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 4, pad=0)
    colorbar.set_label("Magnitude [dB]", fontsize=LABEL_SIZE - 3, labelpad=1)
    save_figure(fig, f"{image_number:02d}_stft_matrix_alle_frames_db_hz.png", bbox_key="matrix_hz")


def export_spectrogram(image_number: int):
    fig, ax = create_matrix_figure()
    image = ax.imshow(
        STFT_MAGNITUDES.T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="bilinear",
        extent=(0.0, DURATION_S, VISIBLE_FREQ_VALUES_HZ[0], VISIBLE_FREQ_VALUES_HZ[-1]),
        vmin=0.0,
        vmax=1.0,
    )
    ax.set_title("Spectrogram", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 2.0))
    ax.tick_params(labelsize=TICK_SIZE)
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 1)
    colorbar.set_label("Magnitude", fontsize=LABEL_SIZE - 1)
    save_figure(fig, f"{image_number:02d}_spektrogramm_als_betragssicht.png", tight=True)


def export_storyboard_for_current_window():
    clear_output_dir()
    export_signal_with_empty_spectrum_axis()
    export_full_window_spectrum()
    shown_frames = []
    image_number = 3
    for frame_index in LOCAL_SPECTRUM_FRAME_SEQUENCE:
        export_frame_spectrum_step(image_number, frame_index, shown_frames)
        image_number += 1
        if frame_index == LOCAL_SPECTRUM_FRAME_SEQUENCE[-1]:
            export_frame_spectrum_db_step(image_number, frame_index, shown_frames)
            image_number += 1
        export_local_index_bridge(image_number, frame_index, shown_frames)
        image_number += 1
        shown_frames.append(frame_index)
    for max_frame_index in MATRIX_BUILD_FRAME_SEQUENCE:
        export_stft_matrix_progress(image_number, max_frame_index)
        image_number += 1
        export_stft_matrix_progress_frequency_axis(image_number, max_frame_index)
        image_number += 1
    export_stft_matrix_all(image_number)
    image_number += 1
    export_stft_matrix_all_frequency_axis(image_number)
    image_number += 1
    export_stft_matrix_all_db(image_number)
    image_number += 1
    export_stft_matrix_all_db_frequency_axis(image_number)
    image_number += 1
    export_spectrogram(image_number)
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


def main():
    clear_legacy_output_files()
    for window_kind in ("rectangular", "hann"):
        configure_window_variant(window_kind)
        export_storyboard_for_current_window()


if __name__ == "__main__":
    main()
