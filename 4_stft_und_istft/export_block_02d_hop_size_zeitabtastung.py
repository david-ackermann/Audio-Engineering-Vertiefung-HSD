from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "02_stft_und_spektrogramm"
    / "02D_hop_size_zeitabtastung"
)
OUTPUT_DIR = OUTPUT_ROOT_DIR

DPI = 200
PAIR_FIGSIZE = (12.0, 7.8)
MATRIX_FIGSIZE = (10.4, 6.2)

TITLE_SIZE = 22
LABEL_SIZE = 20
TICK_SIZE = 17

SIGNAL_BLACK = "0.15"
SIGNAL_BLUE = "#2b7bbb"
WINDOW_GREEN = "#66b77a"
OLD_WINDOW_GREY = "0.87"
INACTIVE_GREY = "0.82"
GRID_GREY = "0.78"
ORIGINAL_SIGNAL_GREY = "0.72"

FS_HZ = 64.0
DURATION_S = 4.0
TOTAL_SAMPLES = int(FS_HZ * DURATION_S)
VISIBLE_FREQ_MAX_HZ = 12.0
DB_FLOOR = -60.0
WINDOW_LENGTH = 64

TIME_VALUES = np.arange(TOTAL_SAMPLES) / FS_HZ
DENSE_TIME_VALUES = np.linspace(0.0, DURATION_S, 5000)

BURST_CENTER_S = 0.90
BURST_SIGMA_S = 0.055
BURST_FREQ_HZ = 8.0

REPEATED_TONE_FREQ_HZ = 5.0
REPEATED_TONE_FADE_S = 0.10
REPEATED_TONE_SEGMENTS_S = (
    (2.05, 2.85),
    (3.05, 3.85),
)


@dataclass(frozen=True)
class HopConfig:
    title: str
    output_subdir: str
    hop_size: int


@dataclass(frozen=True)
class HopState:
    config: HopConfig
    frame_starts: np.ndarray
    frame_times_s: np.ndarray
    frame_centers_s: np.ndarray
    frame_indices: np.ndarray
    window_duration_s: float
    window_values: np.ndarray
    window_sample_positions_s: np.ndarray
    visible_freq_values_hz: np.ndarray
    visible_bin_indices: np.ndarray
    stft_magnitudes: np.ndarray
    delta_f_hz: float
    delta_t_s: float


LARGE_HOP_CONFIG = HopConfig(
    title="Large hop size",
    output_subdir="01_grosse_hopsize",
    hop_size=64,
)
PRACTICAL_HOP_CONFIG = HopConfig(
    title="Practical hop size",
    output_subdir="02_sinnvolle_hopsize",
    hop_size=16,
)


def smooth_step(time_values_s: np.ndarray, center_s: float, width_s: float) -> np.ndarray:
    normalized = (time_values_s - (center_s - 0.5 * width_s)) / width_s
    clipped = np.clip(normalized, 0.0, 1.0)
    return clipped * clipped * (3.0 - 2.0 * clipped)


def build_hopsize_signal(time_values_s: np.ndarray) -> np.ndarray:
    burst_envelope = np.exp(-0.5 * ((time_values_s - BURST_CENTER_S) / BURST_SIGMA_S) ** 2)
    burst = 0.98 * burst_envelope * np.cos(2.0 * np.pi * BURST_FREQ_HZ * time_values_s)

    tone_gate = np.zeros_like(time_values_s)
    for start_s, stop_s in REPEATED_TONE_SEGMENTS_S:
        tone_on = smooth_step(time_values_s, start_s + 0.5 * REPEATED_TONE_FADE_S, REPEATED_TONE_FADE_S)
        tone_off = 1.0 - smooth_step(time_values_s, stop_s - 0.5 * REPEATED_TONE_FADE_S, REPEATED_TONE_FADE_S)
        tone_gate += tone_on * tone_off
    tone_gate = np.clip(tone_gate, 0.0, 1.0)
    repeated_tone = 0.88 * tone_gate * np.cos(2.0 * np.pi * REPEATED_TONE_FREQ_HZ * time_values_s)

    return burst + repeated_tone


SIGNAL_VALUES = build_hopsize_signal(TIME_VALUES)
DENSE_SIGNAL_VALUES = build_hopsize_signal(DENSE_TIME_VALUES)
SIGNAL_LIMIT = 1.15 * max(1.0, np.max(np.abs(DENSE_SIGNAL_VALUES)))


def one_sided_amplitude_scaled_coefficients(coefficients: np.ndarray, n_samples: int) -> np.ndarray:
    scaled_coefficients = coefficients.copy()
    if n_samples % 2 == 0:
        scaled_coefficients[1:-1] *= 2.0
    else:
        scaled_coefficients[1:] *= 2.0
    return scaled_coefficients


def build_hop_state(config: HopConfig) -> HopState:
    frame_starts = np.arange(0, TOTAL_SAMPLES - WINDOW_LENGTH + 1, config.hop_size)
    frame_times_s = frame_starts / FS_HZ
    window_duration_s = WINDOW_LENGTH / FS_HZ
    frame_centers_s = frame_times_s + 0.5 * window_duration_s
    frame_indices = np.arange(len(frame_starts))

    window_values = np.hanning(WINDOW_LENGTH)
    window_sample_positions_s = np.arange(WINDOW_LENGTH) / FS_HZ

    freq_values_hz = np.fft.rfftfreq(WINDOW_LENGTH, d=1.0 / FS_HZ)
    visible_freq_mask = freq_values_hz <= VISIBLE_FREQ_MAX_HZ
    visible_freq_values_hz = freq_values_hz[visible_freq_mask]
    visible_bin_indices = np.arange(len(freq_values_hz))[visible_freq_mask]

    frame_blocks = np.vstack([SIGNAL_VALUES[start : start + WINDOW_LENGTH] for start in frame_starts])
    coherent_gain = np.mean(window_values)
    stft_coefficients = np.vstack(
        [
            one_sided_amplitude_scaled_coefficients(
                np.fft.rfft(block * window_values) / (WINDOW_LENGTH * coherent_gain),
                WINDOW_LENGTH,
            )
            for block in frame_blocks
        ]
    )
    stft_magnitudes = np.abs(stft_coefficients[:, visible_freq_mask])

    return HopState(
        config=config,
        frame_starts=frame_starts,
        frame_times_s=frame_times_s,
        frame_centers_s=frame_centers_s,
        frame_indices=frame_indices,
        window_duration_s=window_duration_s,
        window_values=window_values,
        window_sample_positions_s=window_sample_positions_s,
        visible_freq_values_hz=visible_freq_values_hz,
        visible_bin_indices=visible_bin_indices,
        stft_magnitudes=stft_magnitudes,
        delta_f_hz=FS_HZ / WINDOW_LENGTH,
        delta_t_s=config.hop_size / FS_HZ,
    )


LARGE_HOP_STATE = build_hop_state(LARGE_HOP_CONFIG)
PRACTICAL_HOP_STATE = build_hop_state(PRACTICAL_HOP_CONFIG)
DB_REFERENCE_MAGNITUDE = max(
    float(np.max(LARGE_HOP_STATE.stft_magnitudes)),
    float(np.max(PRACTICAL_HOP_STATE.stft_magnitudes)),
)


def magnitude_to_db(magnitudes: np.ndarray) -> np.ndarray:
    relative = magnitudes / max(DB_REFERENCE_MAGNITUDE, np.finfo(float).eps)
    return 20.0 * np.log10(np.maximum(relative, 10.0 ** (DB_FLOOR / 20.0)))


def clear_output_dirs() -> None:
    OUTPUT_ROOT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_ROOT_DIR.glob("*.png"):
        png_file.unlink()
    for config in (LARGE_HOP_CONFIG, PRACTICAL_HOP_CONFIG):
        output_dir = OUTPUT_ROOT_DIR / config.output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        for png_file in output_dir.glob("*.png"):
            png_file.unlink()


def configure_output_dir(state: HopState) -> None:
    global OUTPUT_DIR
    OUTPUT_DIR = OUTPUT_ROOT_DIR / state.config.output_subdir


def create_pair_figure():
    fig, axes = plt.subplots(2, 1, figsize=PAIR_FIGSIZE)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.10, top=0.92, hspace=0.52)
    return fig, axes


def create_matrix_figure():
    fig, ax = plt.subplots(figsize=MATRIX_FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.90, bottom=0.12, top=0.90)
    return fig, ax


def save_figure(fig, filename: str, *, tight: bool = False) -> None:
    if tight:
        fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    else:
        fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def style_time_axis(ax, title: str) -> None:
    ax.axhline(0.0, color=GRID_GREY, lw=0.9)
    ax.set_xlim(0.0, DURATION_S)
    ax.set_ylim(-SIGNAL_LIMIT, SIGNAL_LIMIT)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_local_spectrum_db_axis(ax, title: str) -> None:
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


def draw_signal(ax) -> None:
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=SIGNAL_BLACK, lw=2.4, zorder=2)


def draw_discrete_samples(ax, sample_positions: np.ndarray, sample_values: np.ndarray) -> None:
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


def draw_frame_grid(ax, state: HopState, alpha: float = 1.0) -> None:
    for frame_start_s in state.frame_times_s:
        ax.axvline(frame_start_s, color=INACTIVE_GREY, lw=1.15, alpha=alpha, zorder=0)


def shifted_window_dense(state: HopState, frame_index: int) -> np.ndarray:
    frame_start_s = state.frame_times_s[frame_index]
    frame_stop_s = frame_start_s + state.window_duration_s
    window_dense = np.zeros_like(DENSE_TIME_VALUES)
    inside_mask = (DENSE_TIME_VALUES >= frame_start_s) & (DENSE_TIME_VALUES <= frame_stop_s)
    relative_positions_s = DENSE_TIME_VALUES[inside_mask] - frame_start_s
    window_dense[inside_mask] = np.interp(relative_positions_s, state.window_sample_positions_s, state.window_values)
    return window_dense


def draw_window_band(ax, state: HopState, frame_index: int, color: str, alpha: float, lw: float) -> None:
    window_dense = shifted_window_dense(state, frame_index)
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


def draw_previous_windows(ax, state: HopState, previous_frame_indices) -> None:
    for frame_index in previous_frame_indices:
        draw_window_band(ax, state, frame_index, OLD_WINDOW_GREY, alpha=0.14, lw=1.2)


def draw_signal_with_active_segment(ax, state: HopState, active_frame_index: int) -> None:
    frame_start = state.frame_starts[active_frame_index]
    frame_stop = frame_start + WINDOW_LENGTH
    sample_times_s = TIME_VALUES[frame_start:frame_stop]
    sample_values = SIGNAL_VALUES[frame_start:frame_stop] * state.window_values
    ax.plot(DENSE_TIME_VALUES, DENSE_SIGNAL_VALUES, color=ORIGINAL_SIGNAL_GREY, lw=2.2, zorder=1)
    draw_discrete_samples(ax, sample_times_s, sample_values)


def export_signal_with_empty_spectrum_axis(state: HopState) -> int:
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_signal(ax_time)
    style_time_axis(ax_time, r"Signal over observation time $T$")
    style_local_spectrum_db_axis(ax_spectrum, "Frequency axis")

    save_figure(fig, "01_signal_und_frequenzachse.png")
    return 2


def export_frame_spectrum_db_step(
    image_number: int,
    state: HopState,
    frame_index: int,
    previous_frame_indices,
) -> int:
    fig, axes = create_pair_figure()
    ax_time, ax_spectrum = axes

    draw_frame_grid(ax_time, state, alpha=0.25)
    draw_previous_windows(ax_time, state, previous_frame_indices)
    draw_window_band(ax_time, state, frame_index, WINDOW_GREEN, alpha=0.16, lw=1.8)
    draw_signal_with_active_segment(ax_time, state, frame_index)
    style_time_axis(ax_time, f"{state.config.title}: frame m = {frame_index}")

    active_db = magnitude_to_db(state.stft_magnitudes[frame_index])
    ax_spectrum.vlines(state.visible_freq_values_hz, DB_FLOOR, active_db, color=SIGNAL_BLUE, lw=2.4, zorder=2)
    ax_spectrum.scatter(
        state.visible_freq_values_hz,
        active_db,
        s=65,
        color=SIGNAL_BLUE,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )
    style_local_spectrum_db_axis(
        ax_spectrum,
        rf"Local spectrum in dB ($\Delta f={state.delta_f_hz:.1f}$ Hz, $\Delta t={state.delta_t_s:.3g}$ s)",
    )
    save_figure(fig, f"{image_number:02d}_frame_{frame_index}_lokales_spektrum_db.png")
    return image_number + 1


def plot_stft_matrix_db(ax, state: HopState, matrix_data_db: np.ndarray, title: str, *, interpolation: str):
    cmap = plt.get_cmap("magma").copy()
    cmap.set_bad(color="white")
    image = ax.imshow(
        np.ma.masked_invalid(matrix_data_db).T,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        interpolation=interpolation,
        extent=(-0.5, len(state.frame_indices) - 0.5, 0.0, VISIBLE_FREQ_MAX_HZ),
        vmin=DB_FLOOR,
        vmax=0.0,
    )
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frame index m", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    tick_step = 2 if state.config.hop_size == PRACTICAL_HOP_CONFIG.hop_size else 1
    ax.set_xticks(state.frame_indices[::tick_step])
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 2.0))
    ax.grid(False)
    ax.tick_params(labelsize=TICK_SIZE)
    return image


def add_db_colorbar(fig, ax, image) -> None:
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.ax.tick_params(labelsize=TICK_SIZE - 4, pad=0)
    colorbar.set_label("Magnitude [dB]", fontsize=LABEL_SIZE - 3, labelpad=1)


def export_stft_matrix_progress_db(image_number: int, state: HopState, max_frame_index: int) -> int:
    fig, ax = create_matrix_figure()
    matrix_data_db = np.full_like(state.stft_magnitudes, np.nan)
    matrix_data_db[: max_frame_index + 1, :] = magnitude_to_db(state.stft_magnitudes[: max_frame_index + 1, :])
    image = plot_stft_matrix_db(
        ax,
        state,
        matrix_data_db,
        rf"STFT samples in dB up to frame $m={max_frame_index}$",
        interpolation="nearest",
    )
    add_db_colorbar(fig, ax, image)
    save_figure(fig, f"{image_number:02d}_stft_matrix_bis_frame_{max_frame_index}_db.png", tight=True)
    return image_number + 1


def export_stft_matrix_all_db(image_number: int, state: HopState) -> int:
    fig, ax = create_matrix_figure()
    image = plot_stft_matrix_db(
        ax,
        state,
        magnitude_to_db(state.stft_magnitudes),
        r"STFT samples $20\log_{10}|X[m,k]|$",
        interpolation="nearest",
    )
    add_db_colorbar(fig, ax, image)
    save_figure(fig, f"{image_number:02d}_stft_matrix_alle_frames_db.png", tight=True)
    return image_number + 1


def export_spectrogram_db(image_number: int, state: HopState) -> int:
    fig, ax = create_matrix_figure()
    image = ax.imshow(
        magnitude_to_db(state.stft_magnitudes).T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        interpolation="bilinear",
        extent=(0.0, DURATION_S, 0.0, VISIBLE_FREQ_MAX_HZ),
        vmin=DB_FLOOR,
        vmax=0.0,
    )
    ax.set_title("Spectrogram in dB", fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_xticks(np.arange(0.0, DURATION_S + 0.01, 0.5))
    ax.set_yticks(np.arange(0.0, VISIBLE_FREQ_MAX_HZ + 0.01, 2.0))
    ax.tick_params(labelsize=TICK_SIZE)
    add_db_colorbar(fig, ax, image)
    save_figure(fig, f"{image_number:02d}_spektrogramm_db.png", tight=True)
    return image_number + 1


def export_storyboard_for_state(state: HopState) -> None:
    configure_output_dir(state)
    image_number = export_signal_with_empty_spectrum_axis(state)

    shown_frames = []
    for frame_index in state.frame_indices:
        image_number = export_frame_spectrum_db_step(image_number, state, int(frame_index), shown_frames)
        shown_frames.append(int(frame_index))

    for frame_index in state.frame_indices:
        image_number = export_stft_matrix_progress_db(image_number, state, int(frame_index))

    image_number = export_stft_matrix_all_db(image_number, state)
    export_spectrogram_db(image_number, state)
    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


def main() -> None:
    clear_output_dirs()
    export_storyboard_for_state(LARGE_HOP_STATE)
    export_storyboard_for_state(PRACTICAL_HOP_STATE)


if __name__ == "__main__":
    main()
