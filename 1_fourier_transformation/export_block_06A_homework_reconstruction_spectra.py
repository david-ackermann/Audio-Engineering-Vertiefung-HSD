from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

import storyboard_paths as paths


OUTPUT_DIR = paths.HOMEWORK_RECONSTRUCTION_DIR
DPI = 220
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
SPECTRUM_FIGSIZE = (12.4, 9.2)
TIME_OVERVIEW_FIGSIZE = (12.6, 13.2)
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
NEG_COLOR = "#26a043"
POS_COLOR = "tab:purple"
TIME_COLOR = "tab:blue"
LINEWIDTH = 3.2
POINT_SIZE = 10
PHASE_LIMITS = (-180.0, 180.0)
TIME_END = 1.0
SAMPLE_COUNT = 2000
TIME_VALUES = np.linspace(0.0, TIME_END, SAMPLE_COUNT)
PHASE_AXIS_VALUES = 2.0 * np.pi * TIME_VALUES
COMPONENT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']

CASES = [
    {
        "slug": "a_single_component",
        "title": "a: Two-sided spectrum",
        "freqs": np.array([-1.0, 1.0]),
        "mags": np.array([0.5, 0.5]),
        "phases": np.array([0.0, 0.0]),
        "solution_title": "Solution a",
        "template_title": "Sketch template a",
        "formula": r"$x_a(t)=\cos(2\pi\cdot 1\,t)$",
    },
    {
        "slug": "b_two_components",
        "title": "b: Two-sided spectrum",
        "freqs": np.array([-2.0, -1.0, 1.0, 2.0]),
        "mags": np.array([0.25, 0.5, 0.5, 0.25]),
        "phases": np.array([180.0, 0.0, 0.0, 180.0]),
        "solution_title": "Solution b",
        "template_title": "Sketch template b",
        "formula": r"$x_b(t)=\cos(2\pi\cdot 1\,t)+0.5\cos(2\pi\cdot 2\,t+180^\circ)$",
    },
    {
        "slug": "c_three_components",
        "title": "c: Two-sided spectrum",
        "freqs": np.array([-3.0, -2.0, -1.0, 1.0, 2.0, 3.0]),
        "mags": np.array([0.25, 0.25, 0.5, 0.5, 0.25, 0.25]),
        "phases": np.array([180.0, 90.0, 0.0, 0.0, -90.0, 180.0]),
        "solution_title": "Solution c",
        "template_title": "Sketch template c",
        "formula": r"$x_c(t)=\cos(2\pi\cdot 1\,t)+0.5\cos(2\pi\cdot 2\,t-90^\circ)+0.5\cos(2\pi\cdot 3\,t+180^\circ)$",
    },
]


def round_up(value, step):
    return step * np.ceil(value / step)


def normalize_phase_deg(values):
    return ((np.asarray(values) + 180.0) % 360.0) - 180.0


def colors_for_freqs(freqs):
    return [NEG_COLOR if f < 0 else POS_COLOR for f in freqs]


def positive_components(case):
    positive_mask = case["freqs"] > 0.0
    freqs = case["freqs"][positive_mask]
    amplitudes = 2.0 * case["mags"][positive_mask]
    phases_rad = np.deg2rad(case["phases"][positive_mask])
    return freqs, amplitudes, phases_rad


def build_time_signal(case):
    freqs, amplitudes, phases_rad = positive_components(case)
    signal = np.zeros_like(TIME_VALUES)
    for frequency_hz, amplitude, phase_rad in zip(freqs, amplitudes, phases_rad):
        signal += amplitude * np.cos(2.0 * np.pi * frequency_hz * TIME_VALUES + phase_rad)
    return signal


def build_component_signals(case):
    freqs, amplitudes, phases_rad = positive_components(case)
    components = []
    for frequency_hz, amplitude, phase_rad in zip(freqs, amplitudes, phases_rad):
        component = amplitude * np.cos(2.0 * np.pi * frequency_hz * TIME_VALUES + phase_rad)
        components.append((frequency_hz, amplitude, phase_rad, component))
    return components


COMMON_FREQ_LIMIT = float(round_up(max(np.max(np.abs(case["freqs"])) for case in CASES), 1.0) + 0.5)
COMMON_MAG_LIMIT = float(round_up(max(np.max(case["mags"]) for case in CASES), 0.25) + 0.25)
COMMON_TIME_LIMIT = float(round_up(1.15 * max(np.max(np.abs(build_time_signal(case))) for case in CASES), 0.25))


def save_figure(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def style_frequency_axis(ax, title, y_limits, y_label, y_major_step):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-COMMON_FREQ_LIMIT, COMMON_FREQ_LIMIT)
    ax.set_ylim(*y_limits)
    ax.grid(which="major", alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))


def style_time_axis(ax, title, with_fine_grid=False):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(0.0, TIME_END)
    ax.set_ylim(-COMMON_TIME_LIMIT, COMMON_TIME_LIMIT)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.grid(which="major", alpha=GRID_ALPHA)
    if with_fine_grid:
        ax.grid(which="minor", alpha=0.16)


def style_phase_time_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(0.0, 2.0 * np.pi)
    ax.set_ylim(-COMMON_TIME_LIMIT, COMMON_TIME_LIMIT)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel(r"Fundamental phase $\varphi_0$ [rad]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.xaxis.set_major_locator(MultipleLocator(np.pi / 2.0))
    ax.xaxis.set_minor_locator(MultipleLocator(np.pi / 4.0))
    ax.set_xticks([0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2.0 * np.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.grid(which="major", alpha=GRID_ALPHA)
    ax.grid(which="minor", alpha=0.16)


def plot_line_spectrum(ax, freqs, values, title, y_limits, y_label, y_major_step):
    for frequency_hz, value, color in zip(freqs, values, colors_for_freqs(freqs)):
        ax.vlines(frequency_hz, 0.0, value, color=color, lw=LINEWIDTH)
        ax.plot([frequency_hz], [value], "o", color=color, ms=POINT_SIZE)
    style_frequency_axis(ax, title, y_limits, y_label, y_major_step)


def add_formula_box(ax, formula):
    ax.text(
        0.01,
        0.96,
        formula,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=13,
        bbox=dict(facecolor="white", alpha=0.90, edgecolor="0.85"),
    )


def export_spectrum_case(case_index, case):
    fig, axes = plt.subplots(2, 1, figsize=SPECTRUM_FIGSIZE)

    plot_line_spectrum(
        axes[0],
        case["freqs"],
        case["mags"],
        "Magnitude spectrum",
        (0.0, COMMON_MAG_LIMIT),
        r"$|X(f)|$",
        0.25,
    )

    plot_line_spectrum(
        axes[1],
        case["freqs"],
        case["phases"],
        "Phase spectrum",
        PHASE_LIMITS,
        r"$\angle X(f)$ [deg]",
        45.0,
    )

    fig.suptitle(case["title"], fontsize=TITLE_SIZE + 2, y=0.98)
    fig.subplots_adjust(left=0.12, right=0.96, top=0.90, bottom=0.08, hspace=0.42)
    save_figure(fig, f"{case_index:02d}_{case['slug']}.png")


def export_time_solutions_overview():
    fig, axes = plt.subplots(len(CASES), 1, figsize=TIME_OVERVIEW_FIGSIZE)

    for ax, case in zip(axes, CASES):
        signal = build_time_signal(case)
        components = build_component_signals(case)
        for color, (frequency_hz, _amplitude, _phase_rad, component) in zip(COMPONENT_COLORS, components):
            ax.plot(
                TIME_VALUES,
                component,
                color=color,
                lw=1.8,
                ls="--",
                alpha=0.9,
                label=fr"{frequency_hz:g} Hz component",
            )
        ax.plot(TIME_VALUES, signal, color=TIME_COLOR, lw=2.7, label="Sum")
        style_time_axis(ax, case["solution_title"], with_fine_grid=False)
        add_formula_box(ax, case["formula"])
        ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

    fig.subplots_adjust(left=0.10, right=0.98, top=0.97, bottom=0.06, hspace=0.40)
    save_figure(fig, "04_time_domain_solutions.png")


def export_blank_templates_overview():
    fig, ax = plt.subplots(1, 1, figsize=(12.6, 4.8))
    style_time_axis(ax, "Sketch template", with_fine_grid=True)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.90, bottom=0.14)
    save_figure(fig, "05_time_domain_templates_blank.png")


def export_phase_axis_solutions_overview():
    fig, axes = plt.subplots(len(CASES), 1, figsize=TIME_OVERVIEW_FIGSIZE)

    for ax, case in zip(axes, CASES):
        signal = build_time_signal(case)
        components = build_component_signals(case)
        for color, (frequency_hz, _amplitude, _phase_rad, component) in zip(COMPONENT_COLORS, components):
            ax.plot(
                PHASE_AXIS_VALUES,
                component,
                color=color,
                lw=1.8,
                ls="--",
                alpha=0.9,
                label=fr"{frequency_hz:g} Hz component",
            )
        ax.plot(PHASE_AXIS_VALUES, signal, color=TIME_COLOR, lw=2.7, label="Sum")
        style_phase_time_axis(ax, case["solution_title"] + " on harmonic axis")
        add_formula_box(ax, case["formula"])
        ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

    fig.subplots_adjust(left=0.10, right=0.98, top=0.97, bottom=0.06, hspace=0.40)
    save_figure(fig, "06_time_domain_solutions_phase_axis.png")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in OUTPUT_DIR.glob("*.png"):
        old_png.unlink()

    for index, case in enumerate(CASES, start=1):
        export_spectrum_case(index, case)

    export_time_solutions_overview()
    export_blank_templates_overview()
    export_phase_axis_solutions_overview()
    print(f"Saved outputs to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()







