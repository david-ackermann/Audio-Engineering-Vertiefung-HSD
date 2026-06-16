from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_6A_DIR = OUTPUT_ROOT / "06_biquad_audiofilter" / "06A_typical_audio_filters"
BLOCK_6B_DIR = OUTPUT_ROOT / "06_biquad_audiofilter" / "06B_biquad_cascades"
BLOCK_9A_DIR = BLOCK_6A_DIR
BLOCK_9B_DIR = BLOCK_6B_DIR
BLOCK_DIR = BLOCK_9A_DIR

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 22
LABEL_SIZE = 24
TICK_SIZE = 18

FS_HZ = 48_000.0
NYQUIST_HZ = FS_HZ / 2.0
LOG_MIN_HZ = 20.0

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
PREVIOUS_GREY = "0.72"
GROUP_PLOT_ADJUST = {
    "left": 0.12,
    "right": 0.98,
    "bottom": 0.18,
    "top": 0.82,
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class BiquadCoefficients:
    b0: float
    b1: float
    b2: float
    a1: float
    a2: float


@dataclass(frozen=True)
class FilterExample:
    group: str
    slug: str
    title: str
    kind: str
    frequency_hz: float
    q: float = 1.0 / np.sqrt(2.0)
    gain_db: float = 0.0
    shelf_slope: float = 1.0


@dataclass(frozen=True)
class CascadeExample:
    group: str
    slug: str
    title: str
    stages: tuple[FilterExample, ...]
    magnitude_ylim: tuple[float, float]
    magnitude_yticks: tuple[float, ...]


FILTER_EXAMPLES = (
    FilterExample("01_low_pass", "low_pass_fc_1000", "Low-pass: lower cutoff", "lowpass", 1_000.0),
    FilterExample("01_low_pass", "low_pass_fc_4000", "Low-pass: higher cutoff", "lowpass", 4_000.0),
    FilterExample("01_low_pass", "low_pass_fc_10000", "Low-pass: very high cutoff", "lowpass", 10_000.0),
    FilterExample("02_high_pass", "high_pass_fc_80", "High-pass: rumble removal", "highpass", 80.0),
    FilterExample("02_high_pass", "high_pass_fc_300", "High-pass: stronger cleanup", "highpass", 300.0),
    FilterExample("02_high_pass", "high_pass_fc_1000", "High-pass: thin sound", "highpass", 1_000.0),
    FilterExample("03_notch", "notch_1000_q1", "Notch: wider cut", "notch", 1_000.0, q=1.0),
    FilterExample("03_notch", "notch_4000_q1", "Notch: moved center", "notch", 4_000.0, q=1.0),
    FilterExample("03_notch", "notch_1000_q3", "Notch: wider cut", "notch", 1_000.0, q=3.0),
    FilterExample("04_band_pass", "band_pass_1000_q1", "Band-pass: mid band", "bandpass", 1_000.0, q=1.0),
    FilterExample("04_band_pass", "band_pass_4000_q1", "Band-pass: higher band", "bandpass", 4_000.0, q=1.0),
    FilterExample("04_band_pass", "band_pass_1000_q4", "Band-pass: narrow band", "bandpass", 1_000.0, q=4.0),
    FilterExample("05_low_shelf", "low_shelf_200_plus6", "Low-shelf: bass boost", "lowshelf", 200.0, gain_db=6.0),
    FilterExample("05_low_shelf", "low_shelf_500_plus6", "Low-shelf: higher corner", "lowshelf", 500.0, gain_db=6.0),
    FilterExample("05_low_shelf", "low_shelf_200_minus6", "Low-shelf: bass cut", "lowshelf", 200.0, gain_db=-6.0),
    FilterExample("06_high_shelf", "high_shelf_4000_plus6", "High-shelf: brightness boost", "highshelf", 4_000.0, gain_db=6.0),
    FilterExample("06_high_shelf", "high_shelf_8000_plus6", "High-shelf: air band boost", "highshelf", 8_000.0, gain_db=6.0),
    FilterExample("06_high_shelf", "high_shelf_4000_minus6", "High-shelf: brightness cut", "highshelf", 4_000.0, gain_db=-6.0),
    FilterExample("07_peaking_eq", "peaking_eq_1000_plus6_q1", "Peaking-EQ: boost", "peaking", 1_000.0, q=1.0, gain_db=6.0),
    FilterExample("07_peaking_eq", "peaking_eq_4000_plus6_q1", "Peaking-EQ: moved boost", "peaking", 4_000.0, q=1.0, gain_db=6.0),
    FilterExample("07_peaking_eq", "peaking_eq_1000_minus6_q4", "Peaking-EQ: narrow cut", "peaking", 1_000.0, q=4.0, gain_db=-6.0),
)


CASCADE_EXAMPLES = (
    CascadeExample(
        "01_low_pass_cascade",
        "low_pass_fourth_order",
        "Low-pass cascade: steeper slope",
        (
            FilterExample("01_low_pass_cascade", "lp_section_q054", "Stage 1", "lowpass", 2_000.0, q=0.54),
            FilterExample("01_low_pass_cascade", "lp_section_q131", "Stage 2", "lowpass", 2_000.0, q=1.31),
        ),
        (-12.0, 12.0),
        (-12.0, -6.0, 0.0, 6.0, 12.0),
    ),
    CascadeExample(
        "02_high_pass_cascade",
        "high_pass_fourth_order",
        "High-pass cascade: steeper slope",
        (
            FilterExample("02_high_pass_cascade", "hp_section_q054", "Stage 1", "highpass", 200.0, q=0.54),
            FilterExample("02_high_pass_cascade", "hp_section_q131", "Stage 2", "highpass", 200.0, q=1.31),
        ),
        (-12.0, 12.0),
        (-12.0, -6.0, 0.0, 6.0, 12.0),
    ),
    CascadeExample(
        "03_daw_eq_cascade",
        "daw_parametric_eq",
        "DAW-style EQ cascade",
        (
            FilterExample("03_daw_eq_cascade", "low_shelf_bass_boost", "Low-shelf", "lowshelf", 120.0, gain_db=4.0),
            FilterExample("03_daw_eq_cascade", "peq_low_mid_cut", "PEQ 1", "peaking", 320.0, q=1.1, gain_db=-3.5),
            FilterExample("03_daw_eq_cascade", "peq_mid_boost", "PEQ 2", "peaking", 850.0, q=0.9, gain_db=2.5),
            FilterExample("03_daw_eq_cascade", "peq_presence_cut", "PEQ 3", "peaking", 2_600.0, q=2.2, gain_db=-4.0),
            FilterExample("03_daw_eq_cascade", "peq_air_boost", "PEQ 4", "peaking", 7_000.0, q=1.2, gain_db=2.0),
            FilterExample("03_daw_eq_cascade", "high_shelf_brightness", "High-shelf", "highshelf", 10_000.0, gain_db=3.0),
        ),
        (-12.0, 12.0),
        (-12.0, -6.0, 0.0, 6.0, 12.0),
    ),
)


def clear_output_dir() -> None:
    for block_dir in (BLOCK_9A_DIR, BLOCK_9B_DIR):
        block_dir.mkdir(parents=True, exist_ok=True)
        for image_file in block_dir.rglob("*.png"):
            image_file.unlink()


def save_figure(fig, group: str, filename: str, block_dir: Path = BLOCK_9A_DIR) -> None:
    target_dir = block_dir / group
    target_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_dir / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def normalize(b0: float, b1: float, b2: float, a0: float, a1: float, a2: float) -> BiquadCoefficients:
    return BiquadCoefficients(b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def design_biquad(example: FilterExample) -> BiquadCoefficients:
    omega = 2.0 * np.pi * example.frequency_hz / FS_HZ
    cos_omega = np.cos(omega)
    sin_omega = np.sin(omega)
    alpha = sin_omega / (2.0 * example.q)

    if example.kind == "lowpass":
        b0 = (1.0 - cos_omega) / 2.0
        b1 = 1.0 - cos_omega
        b2 = (1.0 - cos_omega) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "highpass":
        b0 = (1.0 + cos_omega) / 2.0
        b1 = -(1.0 + cos_omega)
        b2 = (1.0 + cos_omega) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "bandpass":
        b0 = alpha
        b1 = 0.0
        b2 = -alpha
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "notch":
        b0 = 1.0
        b1 = -2.0 * cos_omega
        b2 = 1.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif example.kind == "peaking":
        amplitude = 10.0 ** (example.gain_db / 40.0)
        b0 = 1.0 + alpha * amplitude
        b1 = -2.0 * cos_omega
        b2 = 1.0 - alpha * amplitude
        a0 = 1.0 + alpha / amplitude
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha / amplitude
    elif example.kind in {"lowshelf", "highshelf"}:
        amplitude = 10.0 ** (example.gain_db / 40.0)
        shelf_alpha = (
            sin_omega
            / 2.0
            * np.sqrt((amplitude + 1.0 / amplitude) * (1.0 / example.shelf_slope - 1.0) + 2.0)
        )
        root_amplitude = np.sqrt(amplitude)
        if example.kind == "lowshelf":
            b0 = amplitude * ((amplitude + 1.0) - (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha)
            b1 = 2.0 * amplitude * ((amplitude - 1.0) - (amplitude + 1.0) * cos_omega)
            b2 = amplitude * ((amplitude + 1.0) - (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha)
            a0 = (amplitude + 1.0) + (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha
            a1 = -2.0 * ((amplitude - 1.0) + (amplitude + 1.0) * cos_omega)
            a2 = (amplitude + 1.0) + (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha
        else:
            b0 = amplitude * ((amplitude + 1.0) + (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha)
            b1 = -2.0 * amplitude * ((amplitude - 1.0) + (amplitude + 1.0) * cos_omega)
            b2 = amplitude * ((amplitude + 1.0) + (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha)
            a0 = (amplitude + 1.0) - (amplitude - 1.0) * cos_omega + 2.0 * root_amplitude * shelf_alpha
            a1 = 2.0 * ((amplitude - 1.0) - (amplitude + 1.0) * cos_omega)
            a2 = (amplitude + 1.0) - (amplitude - 1.0) * cos_omega - 2.0 * root_amplitude * shelf_alpha
    else:
        raise ValueError(f"Unknown filter kind: {example.kind}")

    return normalize(b0, b1, b2, a0, a1, a2)


def response_db(frequency_hz: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    magnitude = np.abs(complex_response(frequency_hz, coefficients))
    return 20.0 * np.log10(np.maximum(magnitude, 1e-8))


def complex_response(frequency_hz: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    z1 = np.exp(-1j * omega)
    z2 = np.exp(-2j * omega)
    numerator = coefficients.b0 + coefficients.b1 * z1 + coefficients.b2 * z2
    denominator = 1.0 + coefficients.a1 * z1 + coefficients.a2 * z2
    return numerator / denominator


def cascade_response(frequency_hz: np.ndarray, stages: tuple[FilterExample, ...]) -> np.ndarray:
    response = np.ones_like(frequency_hz, dtype=np.complex128)
    for stage in stages:
        response *= complex_response(frequency_hz, design_biquad(stage))
    return response


def response_db_from_complex(response: np.ndarray) -> np.ndarray:
    magnitude = np.abs(response)
    return 20.0 * np.log10(np.maximum(magnitude, 1e-8))


def phase_response(frequency_hz: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    return np.unwrap(np.angle(complex_response(frequency_hz, coefficients)))


def group_delay_samples(frequency_hz: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    return group_delay_from_complex_response(frequency_hz, complex_response(frequency_hz, coefficients))


def group_delay_from_complex_response(frequency_hz: np.ndarray, response: np.ndarray) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    phase = np.unwrap(np.angle(response))
    delay = -np.gradient(phase, omega)

    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))
    undefined_phase = magnitude_db < -50.0
    if np.any(undefined_phase):
        mask_width = 15
        expanded_mask = np.convolve(undefined_phase.astype(float), np.ones(mask_width), mode="same") > 0.0
        delay = delay.copy()
        delay[expanded_mask] = np.nan
    return delay


def format_frequency(value_hz: float) -> str:
    if value_hz >= 1_000.0:
        return f"{value_hz / 1_000.0:g} kHz"
    return f"{value_hz:g} Hz"


def parameter_text(example: FilterExample) -> str:
    parts = [rf"$f_0={format_frequency(example.frequency_hz)}$"]
    if example.kind in {"lowpass", "highpass", "bandpass", "notch", "peaking"}:
        parts.append(rf"$Q={example.q:.2g}$")
    if example.kind in {"lowshelf", "highshelf", "peaking"}:
        parts.append(rf"$G={example.gain_db:+.1f}\,\mathrm{{dB}}$")
    return ", ".join(parts)


def stage_label(stage: FilterExample, index: int) -> str:
    return f"{index}: {stage.title}, {parameter_text(stage)}"


def coefficient_text(coefficients: BiquadCoefficients) -> str:
    return (
        rf"$b_0={coefficients.b0:+.3f}$" + "\n"
        + rf"$b_1={coefficients.b1:+.3f}$" + "\n"
        + rf"$b_2={coefficients.b2:+.3f}$" + "\n"
        + rf"$a_1={coefficients.a1:+.3f}$" + "\n"
        + rf"$a_2={coefficients.a2:+.3f}$"
    )


def add_coefficient_box(ax, coefficients: BiquadCoefficients, location: str = "upper_right") -> None:
    if location == "lower_left":
        x_position = 0.035
        y_position = 0.055
        horizontal_alignment = "left"
        vertical_alignment = "bottom"
    else:
        x_position = 0.985
        y_position = 0.955
        horizontal_alignment = "right"
        vertical_alignment = "top"

    label = ax.text(
        x_position,
        y_position,
        coefficient_text(coefficients),
        transform=ax.transAxes,
        fontsize=13,
        color=SIGNAL_BLACK,
        ha=horizontal_alignment,
        va=vertical_alignment,
        zorder=10,
        bbox={
            "boxstyle": "square,pad=0.18",
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 1.0,
        },
    )
    label.set_path_effects([path_effects.withStroke(linewidth=1.2, foreground="white")])


def style_base_axis(ax, title: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(LOG_MIN_HZ, 20_000.0)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_magnitude_axis(ax, title: str) -> None:
    style_base_axis(ax, title, "Magnitude in dB")
    ax.set_ylim(-12.0, 12.0)
    ax.set_yticks([-12, -6, 0, 6, 12])


def style_cascade_magnitude_axis(ax, title: str, ylim: tuple[float, float], yticks: tuple[float, ...]) -> None:
    style_base_axis(ax, title, "Magnitude in dB")
    ax.set_ylim(*ylim)
    ax.set_yticks(list(yticks))


def style_phase_axis(ax, title: str) -> None:
    style_base_axis(ax, title, "Phase in rad")
    ax.set_ylim(-np.pi, np.pi)
    ax.set_yticks([-np.pi, -np.pi / 2.0, 0.0, np.pi / 2.0, np.pi])
    ax.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])


def nice_upper_limit(value: float) -> float:
    if value <= 1.0:
        return 1.0
    if value <= 5.0:
        return 5.0
    if value <= 10.0:
        return 10.0
    return float(np.ceil(value / 10.0) * 10.0)


def nice_lower_limit(value: float) -> float:
    if value >= 0.0:
        return 0.0
    return float(np.floor(value / 10.0) * 10.0)


def pi_tick_label(value: float) -> str:
    multiple = int(round(value / (np.pi / 2.0)))
    labels = {
        -8: r"$-4\pi$",
        -7: r"$-7\pi/2$",
        -6: r"$-3\pi$",
        -5: r"$-5\pi/2$",
        -4: r"$-2\pi$",
        -3: r"$-3\pi/2$",
        -2: r"$-\pi$",
        -1: r"$-\pi/2$",
        0: "0",
        1: r"$\pi/2$",
        2: r"$\pi$",
        3: r"$3\pi/2$",
        4: r"$2\pi$",
        5: r"$5\pi/2$",
        6: r"$3\pi$",
        7: r"$7\pi/2$",
        8: r"$4\pi$",
    }
    return labels.get(multiple, rf"${multiple}\pi/2$")


def style_cascade_phase_axis(ax, title: str, phase_values: tuple[np.ndarray, ...]) -> None:
    style_base_axis(ax, title, "Phase in rad")
    all_values = np.concatenate([values[np.isfinite(values)] for values in phase_values])
    lower_multiple = int(np.floor(np.min(all_values) / (np.pi / 2.0)))
    upper_multiple = int(np.ceil(np.max(all_values) / (np.pi / 2.0)))
    lower_multiple = min(lower_multiple, -1)
    upper_multiple = max(upper_multiple, 1)
    ticks = np.arange(lower_multiple, upper_multiple + 1) * (np.pi / 2.0)
    ax.set_ylim(ticks[0], ticks[-1])
    ax.set_yticks(ticks)
    ax.set_yticklabels([pi_tick_label(value) for value in ticks])


def style_group_delay_axis(ax, title: str, group_delays: tuple[np.ndarray, ...]) -> None:
    style_base_axis(ax, title, "Group delay in samples")
    all_values = np.concatenate([values[np.isfinite(values)] for values in group_delays])
    y_min = float(np.min(all_values))
    y_max = float(np.max(all_values))
    upper = nice_upper_limit(y_max * 1.08)
    lower = 0.0 if y_min >= -0.02 * upper else float(np.floor(y_min / 5.0) * 5.0)
    ax.set_ylim(lower, upper)


def group_title(group_examples: tuple[FilterExample, ...]) -> str:
    return group_examples[0].title.split(":", maxsplit=1)[0]


def add_parameter_legend(ax, location: str = "lower left") -> None:
    legend = ax.legend(loc=location, fontsize=10, frameon=True)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.92)


def add_cascade_legend(ax, compact: bool = False) -> None:
    if compact:
        handles = [
            Line2D([0], [0], color=PREVIOUS_GREY, lw=2.8, label="Single stages"),
            Line2D([0], [0], color=SYSTEM_GREEN, lw=3.8, label="Cascade sum"),
        ]
        legend = ax.legend(handles=handles, loc="lower right", fontsize=11, frameon=True)
    else:
        legend = ax.legend(loc="upper right", fontsize=10, frameon=True)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.92)


def export_filter_example(index: int, example: FilterExample, visible_examples: tuple[FilterExample, ...]) -> None:
    coefficients = design_biquad(example)
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(20_000.0), 4096)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**GROUP_PLOT_ADJUST)
    for visible_example in visible_examples[:-1]:
        visible_coefficients = design_biquad(visible_example)
        magnitude = response_db(frequency_hz, visible_coefficients)
        ax.plot(frequency_hz, magnitude, color=PREVIOUS_GREY, lw=2.5, alpha=0.85)

    magnitude = response_db(frequency_hz, coefficients)
    ax.plot(frequency_hz, magnitude, color=SYSTEM_GREEN, lw=3.4)
    style_magnitude_axis(ax, f"{example.title} | {parameter_text(example)}")
    coefficient_location = "lower_left" if example.group == "06_high_shelf" else "upper_right"
    add_coefficient_box(ax, coefficients, coefficient_location)
    save_figure(fig, example.group, f"{index:02d}_{example.slug}.png")


def export_phase_summary(group_examples: tuple[FilterExample, ...]) -> None:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(20_000.0), 4096)
    title = f"{group_title(group_examples)}: phase response"

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**GROUP_PLOT_ADJUST)
    for example in group_examples[:-1]:
        phase = phase_response(frequency_hz, design_biquad(example))
        ax.plot(frequency_hz, phase, color=PREVIOUS_GREY, lw=2.5, alpha=0.85, label=parameter_text(example))

    last_example = group_examples[-1]
    phase = phase_response(frequency_hz, design_biquad(last_example))
    ax.plot(frequency_hz, phase, color=SYSTEM_GREEN, lw=3.4, label=parameter_text(last_example))
    style_phase_axis(ax, title)
    add_parameter_legend(ax)
    save_figure(fig, last_example.group, f"{len(group_examples) + 1:02d}_{last_example.kind}_phase_all.png")


def export_group_delay_summary(group_examples: tuple[FilterExample, ...]) -> None:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(20_000.0), 4096)
    group_delays = tuple(group_delay_samples(frequency_hz, design_biquad(example)) for example in group_examples)
    title = f"{group_title(group_examples)}: group delay"

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**GROUP_PLOT_ADJUST)
    for example, delay in zip(group_examples[:-1], group_delays[:-1]):
        ax.plot(frequency_hz, delay, color=PREVIOUS_GREY, lw=2.5, alpha=0.85, label=parameter_text(example))

    last_example = group_examples[-1]
    ax.plot(frequency_hz, group_delays[-1], color=SYSTEM_GREEN, lw=3.4, label=parameter_text(last_example))
    style_group_delay_axis(ax, title, group_delays)
    add_parameter_legend(ax, "upper right")
    save_figure(fig, last_example.group, f"{len(group_examples) + 2:02d}_{last_example.kind}_group_delay_all.png")


def export_cascade_magnitude(example: CascadeExample) -> None:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(20_000.0), 4096)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**GROUP_PLOT_ADJUST)

    for index, stage in enumerate(example.stages, start=1):
        response = complex_response(frequency_hz, design_biquad(stage))
        ax.plot(
            frequency_hz,
            response_db_from_complex(response),
            color=PREVIOUS_GREY,
            lw=2.4,
            alpha=0.82,
            label=stage_label(stage, index),
        )

    total_response = cascade_response(frequency_hz, example.stages)
    ax.plot(
        frequency_hz,
        response_db_from_complex(total_response),
        color=SYSTEM_GREEN,
        lw=3.5,
        label="Cascade sum",
    )
    style_cascade_magnitude_axis(ax, f"{example.title}: magnitude response", example.magnitude_ylim, example.magnitude_yticks)
    add_cascade_legend(ax, compact=example.group == "03_daw_eq_cascade")
    save_figure(fig, example.group, f"01_{example.slug}_magnitude.png", BLOCK_9B_DIR)


def export_cascade_phase(example: CascadeExample) -> None:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(20_000.0), 4096)
    stage_phases = tuple(np.unwrap(np.angle(complex_response(frequency_hz, design_biquad(stage)))) for stage in example.stages)
    total_response = cascade_response(frequency_hz, example.stages)
    total_phase = np.unwrap(np.angle(total_response))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**GROUP_PLOT_ADJUST)
    for index, (stage, phase) in enumerate(zip(example.stages, stage_phases), start=1):
        ax.plot(frequency_hz, phase, color=PREVIOUS_GREY, lw=2.4, alpha=0.82, label=stage_label(stage, index))

    ax.plot(frequency_hz, total_phase, color=SYSTEM_GREEN, lw=3.5, label="Cascade sum")
    style_cascade_phase_axis(ax, f"{example.title}: phase response", stage_phases + (total_phase,))
    add_cascade_legend(ax, compact=example.group == "03_daw_eq_cascade")
    save_figure(fig, example.group, f"02_{example.slug}_phase.png", BLOCK_9B_DIR)


def export_cascade_group_delay(example: CascadeExample) -> None:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(20_000.0), 4096)
    stage_delays = tuple(
        group_delay_from_complex_response(frequency_hz, complex_response(frequency_hz, design_biquad(stage)))
        for stage in example.stages
    )
    total_delay = group_delay_from_complex_response(frequency_hz, cascade_response(frequency_hz, example.stages))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**GROUP_PLOT_ADJUST)
    for index, (stage, delay) in enumerate(zip(example.stages, stage_delays), start=1):
        ax.plot(frequency_hz, delay, color=PREVIOUS_GREY, lw=2.4, alpha=0.82, label=stage_label(stage, index))

    ax.plot(frequency_hz, total_delay, color=SYSTEM_GREEN, lw=3.5, label="Cascade sum")
    style_group_delay_axis(ax, f"{example.title}: group delay", stage_delays + (total_delay,))
    add_cascade_legend(ax, compact=example.group == "03_daw_eq_cascade")
    save_figure(fig, example.group, f"03_{example.slug}_group_delay.png", BLOCK_9B_DIR)


def export_cascade_example(example: CascadeExample) -> None:
    export_cascade_magnitude(example)
    export_cascade_phase(example)
    export_cascade_group_delay(example)


def main() -> None:
    clear_output_dir()
    index = 1
    groups = tuple(dict.fromkeys(example.group for example in FILTER_EXAMPLES))
    for group in groups:
        group_examples = tuple(example for example in FILTER_EXAMPLES if example.group == group)
        for step, example in enumerate(group_examples, start=1):
            export_filter_example(index, example, group_examples[:step])
            index += 1
        export_phase_summary(group_examples)
        export_group_delay_summary(group_examples)
    for cascade_example in CASCADE_EXAMPLES:
        export_cascade_example(cascade_example)
    print(f"PNG figures exported to: {OUTPUT_ROOT / '06_biquad_audiofilter'}")


if __name__ == "__main__":
    main()
