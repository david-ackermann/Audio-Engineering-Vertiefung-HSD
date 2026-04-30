from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "03_aliasing"
    / "03B_rechteckzug_zum_dirac_kamm"
)

DPI = 200
FIGSIZE = (11.0, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 19
TICK_SIZE = 15

FS_KHZ = 6.0
T_PERIOD_MS = 1.0 / FS_KHZ
TIME_START_MS = 0.0
TIME_END_MS = 3.0
TIME_VALUES_MS = np.linspace(TIME_START_MS, TIME_END_MS, 6000)
TIME_VALUES_S = TIME_VALUES_MS * 1e-3
SAMPLE_TIMES_MS = np.arange(TIME_START_MS, TIME_END_MS + 0.5 * T_PERIOD_MS, T_PERIOD_MS)
SAMPLE_TIMES_S = SAMPLE_TIMES_MS * 1e-3

FREQ_MIN_KHZ = -24.5
FREQ_MAX_KHZ = 24.5
FREQ_TICKS_KHZ = np.arange(-24.0, 24.1, 6.0)
FREQ_AXIS_VALUES_KHZ = np.linspace(FREQ_MIN_KHZ, FREQ_MAX_KHZ, 4000)
HARMONIC_INDICES = np.arange(-4, 5)
REPLICA_INDICES = np.arange(-2, 3)
FULL_RANGE_REPLICA_INDICES = np.arange(-4, 5)

RECT_DUTY_CYCLES = [0.45, 0.22, 0.08]
SYMMETRIC_ODD_HARMONICS = np.array([-3, -1, 1, 3], dtype=int)
SIGNAL_COMPONENTS = [
    {"frequency_khz": 0.8, "amplitude": 1.0, "phase": 0.00 * np.pi},
    {"frequency_khz": 1.4, "amplitude": 0.75, "phase": 0.55 * np.pi},
    {"frequency_khz": 2.2, "amplitude": 0.52, "phase": -0.30 * np.pi},
]

RECT_GREEN = "#66b77a"
RECT_GREEN_FILL = "#d7efde"
SIGNAL_GREY = "0.45"
GUIDE_GREY = "0.84"
ENVELOPE_GREY = "0.55"
COMB_GREY = "0.50"
BASE_BLUE = "#2b7bbb"
LIGHT_BLUE = "#eaf4fb"
TEXT_GREY = "0.25"
BLACK = "0.15"


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for png_file in OUTPUT_DIR.glob("*.png"):
        png_file.unlink()


def create_figure():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.20, top=0.86)
    return fig, ax


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def style_time_axis(ax, title: str, y_limits=(-0.12, 1.18)) -> None:
    ax.axhline(0.0, color=GUIDE_GREY, lw=0.9)
    ax.set_xlim(TIME_START_MS, TIME_END_MS)
    ax.set_ylim(*y_limits)
    ax.set_xticks(np.arange(0.0, 3.1, 0.5))
    ax.grid(alpha=0.22)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Time [ms]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_frequency_axis(ax, title: str) -> None:
    ax.axhline(0.0, color=GUIDE_GREY, lw=0.9)
    ax.set_xlim(FREQ_MIN_KHZ, FREQ_MAX_KHZ)
    ax.set_ylim(0.0, 1.18)
    ax.set_xticks(FREQ_TICKS_KHZ)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=10)
    ax.set_xlabel("Frequency [kHz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def add_double_arrow(ax, x_start: float, x_end: float, y_pos: float, label: str, label_offset: float = 0.06) -> None:
    ax.annotate(
        "",
        xy=(x_start, y_pos),
        xytext=(x_end, y_pos),
        arrowprops=dict(arrowstyle="<->", lw=1.6, color=TEXT_GREY),
    )
    ax.text(
        0.5 * (x_start + x_end),
        y_pos - label_offset,
        label,
        ha="center",
        va="top",
        fontsize=15,
        color=TEXT_GREY,
    )


def rectangle_train(time_ms: np.ndarray, duty_cycle: float) -> np.ndarray:
    pulse_width_ms = duty_cycle * T_PERIOD_MS
    return (np.mod(time_ms, T_PERIOD_MS) < pulse_width_ms).astype(float)


def rectangle_envelope(frequencies_khz: np.ndarray, duty_cycle: float) -> np.ndarray:
    return np.abs(np.sinc((frequencies_khz / FS_KHZ) * duty_cycle))


def rectangle_line_magnitudes(duty_cycle: float) -> np.ndarray:
    return np.abs(np.sinc(HARMONIC_INDICES * duty_cycle))


def pulse_width_percent_label(duty_cycle: float) -> str:
    return f"{int(round(100.0 * duty_cycle))}% pulse width"


def pulse_train_time_title(duty_cycle: float) -> str:
    return f"Periodic rectangular pulse train ({pulse_width_percent_label(duty_cycle)})"


def pulse_train_spectrum_title(duty_cycle: float) -> str:
    return f"Line spectrum under a sinc envelope ({pulse_width_percent_label(duty_cycle)})"


def symmetric_square_wave(time_ms: np.ndarray) -> np.ndarray:
    return np.where(np.mod(time_ms, T_PERIOD_MS) < 0.5 * T_PERIOD_MS, 1.0, -1.0)


def symmetric_square_envelope(frequencies_khz: np.ndarray) -> np.ndarray:
    abs_freq = np.abs(frequencies_khz)
    envelope = np.full_like(abs_freq, np.nan, dtype=float)
    valid = abs_freq >= 0.5 * FS_KHZ
    envelope[valid] = np.clip(FS_KHZ / abs_freq[valid], 0.0, 1.0)
    return envelope


def symmetric_square_line_magnitudes() -> np.ndarray:
    return 1.0 / np.abs(SYMMETRIC_ODD_HARMONICS.astype(float))


def sampling_signal(time_s: np.ndarray) -> np.ndarray:
    signal = np.zeros_like(time_s)
    for component in SIGNAL_COMPONENTS:
        signal += component["amplitude"] * np.cos(
            2.0 * np.pi * component["frequency_khz"] * 1e3 * time_s + component["phase"]
        )
    return 0.95 * signal / np.max(np.abs(signal))


def component_magnitudes() -> np.ndarray:
    amplitudes = np.array([component["amplitude"] for component in SIGNAL_COMPONENTS], dtype=float)
    return amplitudes / np.max(amplitudes)


def draw_line_spectrum(ax, centers_khz, heights, color, lw=2.6, alpha=1.0, zorder=3) -> None:
    centers_khz = np.asarray(centers_khz, dtype=float)
    heights = np.asarray(heights, dtype=float)
    ax.vlines(centers_khz, 0.0, heights, color=color, lw=lw, alpha=alpha, zorder=zorder)
    ax.scatter(
        centers_khz,
        heights,
        s=60,
        color=color,
        edgecolor="white",
        linewidth=0.8,
        alpha=alpha,
        zorder=zorder + 1,
    )


def draw_component_group(ax, center_khz: float, color: str, alpha: float = 1.0, lw: float = 2.6, zorder: int = 3) -> None:
    component_freqs = np.array([component["frequency_khz"] for component in SIGNAL_COMPONENTS], dtype=float)
    heights = component_magnitudes()
    frequencies = np.concatenate((center_khz - component_freqs[::-1], center_khz + component_freqs))
    all_heights = np.concatenate((heights[::-1], heights))
    draw_line_spectrum(ax, frequencies, all_heights, color=color, lw=lw, alpha=alpha, zorder=zorder)


def replica_label(replica_index: int) -> str:
    if replica_index == 0:
        return "0"
    sign = "+" if replica_index > 0 else "-"
    magnitude = abs(replica_index)
    if magnitude == 1:
        return rf"${sign}f_s$"
    return rf"${sign}{magnitude}f_s$"


def export_rectangular_train_time(filename: str, title: str, duty_cycle: float) -> None:
    fig, ax = create_figure()
    values = rectangle_train(TIME_VALUES_MS, duty_cycle)
    ax.fill_between(TIME_VALUES_MS, 0.0, values, step="post", color=RECT_GREEN_FILL, zorder=1)
    ax.step(TIME_VALUES_MS, values, where="post", color=RECT_GREEN, lw=2.2, zorder=2)
    style_time_axis(ax, title)
    save_figure(fig, filename)


def export_rectangular_train_spectrum(filename: str, title: str, duty_cycle: float) -> None:
    fig, ax = create_figure()
    envelope = rectangle_envelope(FREQ_AXIS_VALUES_KHZ, duty_cycle)
    ax.plot(FREQ_AXIS_VALUES_KHZ, envelope, color=ENVELOPE_GREY, lw=1.8, zorder=1)
    draw_line_spectrum(
        ax,
        HARMONIC_INDICES * FS_KHZ,
        rectangle_line_magnitudes(duty_cycle),
        color=RECT_GREEN,
        lw=2.8,
    )
    style_frequency_axis(ax, title)
    add_double_arrow(ax, 0.0, FS_KHZ, y_pos=0.54, label=r"$f_s = 1/T$")
    save_figure(fig, filename)


def export_symmetric_square_time() -> None:
    fig, ax = create_figure()
    values = symmetric_square_wave(TIME_VALUES_MS)
    ax.fill_between(TIME_VALUES_MS, 0.0, values, step="post", color=RECT_GREEN_FILL, zorder=1)
    ax.step(TIME_VALUES_MS, values, where="post", color=RECT_GREEN, lw=2.2, zorder=2)
    style_time_axis(ax, f"Symmetric rectangular signal ({pulse_width_percent_label(0.5)})", y_limits=(-1.18, 1.18))
    save_figure(fig, "01_symmetric_square_wave_time.png")


def export_symmetric_square_spectrum() -> None:
    fig, ax = create_figure()
    draw_line_spectrum(
        ax,
        SYMMETRIC_ODD_HARMONICS * FS_KHZ,
        symmetric_square_line_magnitudes(),
        color=RECT_GREEN,
        lw=2.8,
    )
    style_frequency_axis(ax, f"Spectrum of the symmetric rectangular signal ({pulse_width_percent_label(0.5)})")
    add_double_arrow(ax, 0.0, FS_KHZ, y_pos=0.54, label=r"$f_0 = 1/T$")
    save_figure(fig, "02_symmetric_square_wave_spectrum.png")


def export_unipolar_half_duty_time() -> None:
    fig, ax = create_figure()
    values = rectangle_train(TIME_VALUES_MS, 0.5)
    ax.fill_between(TIME_VALUES_MS, 0.0, values, step="post", color=RECT_GREEN_FILL, zorder=1)
    ax.step(TIME_VALUES_MS, values, where="post", color=RECT_GREEN, lw=2.2, zorder=2)
    style_time_axis(ax, pulse_train_time_title(0.5))
    save_figure(fig, "03_unipolar_half_duty_time.png")


def export_unipolar_half_duty_spectrum() -> None:
    fig, ax = create_figure()
    envelope = rectangle_envelope(FREQ_AXIS_VALUES_KHZ, 0.5)
    ax.plot(FREQ_AXIS_VALUES_KHZ, envelope, color=ENVELOPE_GREY, lw=1.8, zorder=1)
    draw_line_spectrum(
        ax,
        HARMONIC_INDICES * FS_KHZ,
        rectangle_line_magnitudes(0.5),
        color=RECT_GREEN,
        lw=2.8,
    )
    style_frequency_axis(ax, pulse_train_spectrum_title(0.5))
    add_double_arrow(ax, 0.0, FS_KHZ, y_pos=0.54, label=r"$f_0 = 1/T$")
    save_figure(fig, "04_unipolar_half_duty_spectrum.png")


def export_dirac_comb_time() -> None:
    fig, ax = create_figure()
    ax.vlines(SAMPLE_TIMES_MS, 0.0, 1.0, color=BLACK, lw=1.6)
    ax.scatter(SAMPLE_TIMES_MS, np.ones_like(SAMPLE_TIMES_MS), s=16, color=BLACK, zorder=3)
    style_time_axis(ax, "Periodic rectangular pulse train (0% pulse width limit)")
    save_figure(fig, "11_dirac_comb_limit_time.png")


def export_dirac_comb_spectrum() -> None:
    fig, ax = create_figure()
    ax.vlines(HARMONIC_INDICES * FS_KHZ, 0.0, 1.0, color=BLACK, lw=1.6)
    ax.scatter(HARMONIC_INDICES * FS_KHZ, np.ones_like(HARMONIC_INDICES), s=20, color=BLACK, zorder=3)
    style_frequency_axis(ax, "Line spectrum under a sinc envelope (0% pulse width limit)")
    add_double_arrow(ax, 0.0, FS_KHZ, y_pos=0.54, label=r"$f_s = 1/T$")
    ax.text(FREQ_MIN_KHZ + 0.8, 0.60, r"$\cdots$", ha="left", va="center", fontsize=20, color=TEXT_GREY)
    ax.text(FREQ_MAX_KHZ - 0.8, 0.60, r"$\cdots$", ha="right", va="center", fontsize=20, color=TEXT_GREY)
    save_figure(fig, "12_dirac_comb_limit_spectrum.png")


def export_signal_time() -> None:
    fig, ax = create_figure()
    ax.plot(TIME_VALUES_MS, sampling_signal(TIME_VALUES_S), color=BASE_BLUE, lw=2.0)
    style_time_axis(ax, "Band-limited analog signal x(t)", y_limits=(-1.12, 1.12))
    save_figure(fig, "13_bandlimited_signal_x_t.png")


def export_signal_spectrum() -> None:
    fig, ax = create_figure()
    ax.axvspan(-FS_KHZ / 2.0, FS_KHZ / 2.0, color=LIGHT_BLUE, alpha=0.95, zorder=0)
    ax.axvline(-FS_KHZ / 2.0, color="0.88", lw=1.0, ls="--")
    ax.axvline(FS_KHZ / 2.0, color="0.88", lw=1.0, ls="--")

    component_freqs = [component["frequency_khz"] for component in SIGNAL_COMPONENTS]
    component_heights = component_magnitudes()
    frequencies = [-frequency for frequency in component_freqs[::-1]] + component_freqs
    heights = list(component_heights[::-1]) + list(component_heights)

    draw_line_spectrum(ax, frequencies, heights, color=BASE_BLUE, lw=2.8)
    style_frequency_axis(ax, "Band-limited analog spectrum X(f)")
    ax.text(0.0, 1.10, "baseband", ha="center", va="top", fontsize=15, color=TEXT_GREY)
    save_figure(fig, "14_bandlimited_spectrum_x_f.png")


def export_sampled_signal_time() -> None:
    fig, ax = create_figure()
    signal_values = sampling_signal(TIME_VALUES_S)
    sample_values = sampling_signal(SAMPLE_TIMES_S)
    ax.plot(TIME_VALUES_MS, signal_values, color=SIGNAL_GREY, lw=1.8, zorder=1)
    ax.vlines(SAMPLE_TIMES_MS, 0.0, sample_values, color=BASE_BLUE, lw=1.6, zorder=2)
    ax.scatter(
        SAMPLE_TIMES_MS,
        sample_values,
        s=26,
        color=BASE_BLUE,
        edgecolor="white",
        linewidth=0.7,
        zorder=3,
    )
    style_time_axis(ax, "Ideal impulse sampling", y_limits=(-1.12, 1.12))
    ax.text(2.92, -0.68, r"$x_s(t)$", ha="right", va="center", fontsize=18, color=TEXT_GREY)
    save_figure(fig, "15_ideal_impulse_sampling_x_s_t.png")


def export_sampled_spectrum() -> None:
    fig, ax = create_figure()
    for replica_index in FULL_RANGE_REPLICA_INDICES:
        center_frequency = replica_index * FS_KHZ
        ax.axvline(center_frequency, color="0.92", lw=1.0, ls="--", zorder=0)
        draw_component_group(ax, center_frequency, color=COMB_GREY, alpha=0.78, lw=2.2, zorder=2)

    draw_component_group(ax, 0.0, color=BASE_BLUE, alpha=1.0, lw=2.8, zorder=4)

    style_frequency_axis(ax, r"Sampling replicates the spectrum every $f_s$")
    add_double_arrow(ax, 0.0, FS_KHZ, y_pos=0.18, label=r"$f_s$")
    for replica_index in REPLICA_INDICES:
        ax.text(
            replica_index * FS_KHZ,
            1.15,
            replica_label(replica_index),
            ha="center",
            va="top",
            fontsize=13,
            color=TEXT_GREY,
        )
    save_figure(fig, "16_sampled_spectrum_x_s_f.png")


def main() -> None:
    clear_output_dir()

    export_symmetric_square_time()
    export_symmetric_square_spectrum()
    export_unipolar_half_duty_time()
    export_unipolar_half_duty_spectrum()
    export_rectangular_train_time(
        "05_rectangular_train_wide_time.png",
        pulse_train_time_title(RECT_DUTY_CYCLES[0]),
        RECT_DUTY_CYCLES[0],
    )
    export_rectangular_train_spectrum(
        "06_rectangular_train_wide_spectrum.png",
        pulse_train_spectrum_title(RECT_DUTY_CYCLES[0]),
        RECT_DUTY_CYCLES[0],
    )
    export_rectangular_train_time(
        "07_rectangular_train_narrower_time.png",
        pulse_train_time_title(RECT_DUTY_CYCLES[1]),
        RECT_DUTY_CYCLES[1],
    )
    export_rectangular_train_spectrum(
        "08_rectangular_train_narrower_spectrum.png",
        pulse_train_spectrum_title(RECT_DUTY_CYCLES[1]),
        RECT_DUTY_CYCLES[1],
    )
    export_rectangular_train_time(
        "09_rectangular_train_very_narrow_time.png",
        pulse_train_time_title(RECT_DUTY_CYCLES[2]),
        RECT_DUTY_CYCLES[2],
    )
    export_rectangular_train_spectrum(
        "10_rectangular_train_very_narrow_spectrum.png",
        pulse_train_spectrum_title(RECT_DUTY_CYCLES[2]),
        RECT_DUTY_CYCLES[2],
    )
    export_dirac_comb_time()
    export_dirac_comb_spectrum()
    export_signal_time()
    export_signal_spectrum()
    export_sampled_signal_time()
    export_sampled_spectrum()

    print(f"PNG storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
