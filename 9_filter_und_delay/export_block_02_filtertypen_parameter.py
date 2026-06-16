from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "02_filtertypen_parameter"

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18

SYSTEM_GREEN = "#66b77a"
STANDARD_BLUE = "#4c78a8"
SYSTEM_ORANGE = "#f28e2b"
REFERENCE_GREY = "0.70"

FS_HZ = 48_000.0
NYQUIST_HZ = FS_HZ / 2.0
FREQUENCY_MIN_HZ = 20.0
FREQUENCY_MAX_HZ = 20_000.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
REFERENCE_Q = 1.0 / np.sqrt(2.0)
HIGH_Q = 1.25
MAGNITUDE_DB_LIMITS = (-15.0, 5.0)
MAGNITUDE_DB_TICKS = [-15.0, -10.0, -5.0, 0.0, 5.0]
PHASE_Y_MIN = -np.pi
PHASE_Y_MAX = np.pi

LOW_CUT_FREQUENCY_HZ = 200.0
CENTER_FREQUENCY_HZ = 500.0
HIGH_CUT_FREQUENCY_HZ = 5_000.0

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
class FilterCurve:
    slug: str
    label: str
    kind: str
    frequency_hz: float
    q: float


FILTERS = (
    FilterCurve("low_pass", "Low-pass", "lowpass", HIGH_CUT_FREQUENCY_HZ, REFERENCE_Q),
    FilterCurve("high_pass", "High-pass", "highpass", LOW_CUT_FREQUENCY_HZ, REFERENCE_Q),
    FilterCurve("band_pass", "Band-pass", "bandpass", CENTER_FREQUENCY_HZ, REFERENCE_Q),
    FilterCurve("band_stop", "Band-stop", "notch", CENTER_FREQUENCY_HZ, REFERENCE_Q),
    FilterCurve("all_pass", "All-pass", "allpass", CENTER_FREQUENCY_HZ, REFERENCE_Q),
)

HIGH_Q_FILTER_KINDS = {"lowpass", "highpass", "bandpass", "notch", "allpass"}
HIGH_Q_LEGEND_LOCATIONS = {
    "lowpass": "lower left",
    "highpass": "lower right",
    "bandpass": "upper right",
    "notch": "lower right",
    "allpass": "lower right",
}
REFERENCE_LEGEND_LOCATIONS = {
    **HIGH_Q_LEGEND_LOCATIONS,
    "allpass": "lower right",
}


def normalize(b0: float, b1: float, b2: float, a0: float, a1: float, a2: float) -> BiquadCoefficients:
    return BiquadCoefficients(b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def design_biquad(curve: FilterCurve) -> BiquadCoefficients:
    omega = 2.0 * np.pi * curve.frequency_hz / FS_HZ
    cos_omega = np.cos(omega)
    sin_omega = np.sin(omega)
    alpha = sin_omega / (2.0 * curve.q)

    if curve.kind == "lowpass":
        b0 = (1.0 - cos_omega) / 2.0
        b1 = 1.0 - cos_omega
        b2 = (1.0 - cos_omega) / 2.0
    elif curve.kind == "highpass":
        b0 = (1.0 + cos_omega) / 2.0
        b1 = -(1.0 + cos_omega)
        b2 = (1.0 + cos_omega) / 2.0
    elif curve.kind == "bandpass":
        b0 = alpha
        b1 = 0.0
        b2 = -alpha
    elif curve.kind == "notch":
        b0 = 1.0
        b1 = -2.0 * cos_omega
        b2 = 1.0
    elif curve.kind == "allpass":
        b0 = 1.0 - alpha
        b1 = -2.0 * cos_omega
        b2 = 1.0 + alpha
    else:
        raise ValueError(f"Unknown filter kind: {curve.kind}")

    a0 = 1.0 + alpha
    a1 = -2.0 * cos_omega
    a2 = 1.0 - alpha
    return normalize(b0, b1, b2, a0, a1, a2)


def complex_response(normalized_omega: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    omega = normalized_omega * np.pi
    z1 = np.exp(-1j * omega)
    z2 = np.exp(-2j * omega)
    numerator = coefficients.b0 + coefficients.b1 * z1 + coefficients.b2 * z2
    denominator = 1.0 + coefficients.a1 * z1 + coefficients.a2 * z2
    return numerator / denominator


def first_order_allpass_response(frequency_hz: np.ndarray, allpass_frequency_hz: float) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    z1 = np.exp(-1j * omega)
    g = np.tan(np.pi * allpass_frequency_hz / FS_HZ)
    coefficient = (1.0 - g) / (1.0 + g)
    return (coefficient - z1) / (1.0 - coefficient * z1)


def frequency_grid() -> np.ndarray:
    return np.geomspace(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ, 4096)


def normalized_omega_from_frequency(frequency_hz: np.ndarray) -> np.ndarray:
    return frequency_hz / NYQUIST_HZ


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def with_q(curve: FilterCurve, q: float) -> FilterCurve:
    return FilterCurve(curve.slug, curve.label, curve.kind, curve.frequency_hz, q)


def reference_legend_labels(curve: FilterCurve) -> list[str]:
    return [r"Magnitude $Q=1/\sqrt{2}$", r"Phase $Q=1/\sqrt{2}$"]


def save_figure(fig, filename: str) -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.glob("*.png"):
        image_file.unlink()


def style_frequency_axis(ax, title: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_magnitude_axis(ax, title: str) -> None:
    style_frequency_axis(ax, title, r"$|H(f)|$ in dB")
    ax.set_ylim(*MAGNITUDE_DB_LIMITS)
    ax.set_yticks(MAGNITUDE_DB_TICKS)


def style_common_axis(ax, title: str, ylabel: str) -> None:
    style_frequency_axis(ax, title, ylabel)
    ax.set_ylim(*MAGNITUDE_DB_LIMITS)
    ax.set_yticks(MAGNITUDE_DB_TICKS)


def phase_axis_settings(curve: FilterCurve) -> tuple[float, float, list[float], list[str], tuple[float, ...]]:
    return (
        PHASE_Y_MIN,
        PHASE_Y_MAX,
        [-np.pi, -np.pi / 2.0, 0.0, np.pi / 2.0, np.pi],
        [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"],
        (-np.pi / 2.0, np.pi / 2.0),
    )


def phase_for_plot(response: np.ndarray, curve: FilterCurve) -> np.ndarray:
    phase = np.angle(response)
    if curve.kind != "allpass":
        return np.unwrap(phase)

    phase = phase.copy()
    wrap_jumps = np.abs(np.diff(phase)) > np.pi
    phase[1:][wrap_jumps] = np.nan
    return phase


def style_phase_axis(ax, curve: FilterCurve) -> None:
    phase_y_min, phase_y_max, ticks, ticklabels, _ = phase_axis_settings(curve)
    ax.set_ylim(phase_y_min, phase_y_max)
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticklabels)
    ax.set_ylabel("Phase in rad", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    ax.spines["top"].set_visible(False)


def add_phase_half_pi_grid(ax, curve: FilterCurve) -> None:
    phase_y_min, phase_y_max, _, _, grid_values = phase_axis_settings(curve)
    for phase_value in grid_values:
        ax.axhline(
            phase_value,
            color=REFERENCE_GREY,
            lw=1.25,
            ls=":",
            alpha=0.55,
            zorder=0,
        )


def add_cutoff_frequency_line(ax, curve: FilterCurve) -> None:
    ax.axvline(
        curve.frequency_hz,
        color="black",
        lw=1.8,
        ls="--",
        alpha=0.85,
        zorder=1,
    )


def filter_response(curve: FilterCurve) -> tuple[np.ndarray, np.ndarray]:
    frequency_hz = frequency_grid()
    normalized_omega = normalized_omega_from_frequency(frequency_hz)
    coefficients = design_biquad(curve)
    return frequency_hz, complex_response(normalized_omega, coefficients)


def export_filter_response(index: int, curve: FilterCurve) -> None:
    frequency_hz, response = filter_response(curve)
    response_db = magnitude_db(response)
    phase = phase_for_plot(response, curve)
    phase[response_db < -55.0] = np.nan

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax_phase = ax.twinx()

    magnitude_line = ax.plot(
        frequency_hz,
        response_db,
        color=SYSTEM_GREEN,
        lw=3.0,
        label="Magnitude",
    )[0]

    phase_line = ax_phase.plot(
        frequency_hz,
        phase,
        color=SYSTEM_GREEN,
        lw=3.0,
        ls="--",
        label="Phase",
    )[0]

    style_common_axis(ax, f"{curve.label} filter response", r"$|H(f)|$ in dB")
    style_phase_axis(ax_phase, curve)
    add_phase_half_pi_grid(ax_phase, curve)
    add_cutoff_frequency_line(ax, curve)

    legend = ax.legend(
        [magnitude_line, phase_line],
        reference_legend_labels(curve),
        loc=REFERENCE_LEGEND_LOCATIONS[curve.kind],
        ncol=1,
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    save_figure(fig, f"{index:02d}_{curve.slug}_filter_response.png")


def export_first_order_allpass_response() -> None:
    frequency_hz = frequency_grid()
    response = first_order_allpass_response(frequency_hz, CENTER_FREQUENCY_HZ)
    response_db = magnitude_db(response)
    phase = phase_for_plot(response, FilterCurve("all_pass_first_order", "All-pass 1st-order", "allpass", CENTER_FREQUENCY_HZ, REFERENCE_Q))
    phase[response_db < -55.0] = np.nan
    curve = FilterCurve("all_pass_first_order", "All-pass 1st-order", "allpass", CENTER_FREQUENCY_HZ, REFERENCE_Q)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax_phase = ax.twinx()

    magnitude_line = ax.plot(
        frequency_hz,
        response_db,
        color=SYSTEM_GREEN,
        lw=3.0,
        label="Magnitude",
    )[0]

    phase_line = ax_phase.plot(
        frequency_hz,
        phase,
        color=SYSTEM_GREEN,
        lw=3.0,
        ls="--",
        label="Phase",
    )[0]

    style_common_axis(ax, "All-pass 1st-order filter response", r"$|H(f)|$ in dB")
    style_phase_axis(ax_phase, curve)
    add_phase_half_pi_grid(ax_phase, curve)
    add_cutoff_frequency_line(ax, curve)

    legend = ax.legend(
        [magnitude_line, phase_line],
        ["Magnitude 1st order", "Phase 1st order"],
        loc=REFERENCE_LEGEND_LOCATIONS["allpass"],
        ncol=1,
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    save_figure(fig, "05a_all_pass_first_order_filter_response.png")


def export_high_q_filter_response(index: int, reference_curve: FilterCurve) -> None:
    active_curve = with_q(reference_curve, HIGH_Q)
    frequency_hz, reference_response = filter_response(reference_curve)
    _, active_response = filter_response(active_curve)
    reference_response_db = magnitude_db(reference_response)
    active_response_db = magnitude_db(active_response)
    reference_phase = phase_for_plot(reference_response, reference_curve)
    active_phase = phase_for_plot(active_response, reference_curve)
    reference_phase[reference_response_db < -55.0] = np.nan
    active_phase[active_response_db < -55.0] = np.nan

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax_phase = ax.twinx()

    reference_magnitude_line = ax.plot(
        frequency_hz,
        reference_response_db,
        color=REFERENCE_GREY,
        lw=2.8,
        alpha=0.85,
        label="Reference magnitude",
        zorder=2,
    )[0]

    active_magnitude_line = ax.plot(
        frequency_hz,
        active_response_db,
        color=SYSTEM_GREEN,
        lw=3.0,
        label="Magnitude",
        zorder=4,
    )[0]

    reference_phase_line = ax_phase.plot(
        frequency_hz,
        reference_phase,
        color=REFERENCE_GREY,
        lw=2.8,
        ls="--",
        alpha=0.85,
        label="Reference phase",
        zorder=2,
    )[0]

    active_phase_line = ax_phase.plot(
        frequency_hz,
        active_phase,
        color=SYSTEM_GREEN,
        lw=3.0,
        ls="--",
        label="Phase",
        zorder=4,
    )[0]

    style_common_axis(ax, f"{reference_curve.label} filter response, higher Q", r"$|H(f)|$ in dB")
    style_phase_axis(ax_phase, reference_curve)
    add_phase_half_pi_grid(ax_phase, reference_curve)
    add_cutoff_frequency_line(ax, reference_curve)

    legend = ax.legend(
        [active_magnitude_line, active_phase_line, reference_magnitude_line, reference_phase_line],
        [rf"Magnitude $Q={HIGH_Q:g}$", rf"Phase $Q={HIGH_Q:g}$", r"Magnitude $Q=1/\sqrt{2}$", r"Phase $Q=1/\sqrt{2}$"],
        loc=HIGH_Q_LEGEND_LOCATIONS[reference_curve.kind],
        ncol=1,
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    save_figure(fig, f"{index:02d}_{reference_curve.slug}_high_q_response.png")


def main() -> None:
    clear_output_dir()
    for index, curve in enumerate(FILTERS, start=1):
        export_filter_response(index, curve)
    export_first_order_allpass_response()
    high_q_filters = [curve for curve in FILTERS if curve.kind in HIGH_Q_FILTER_KINDS]
    for index, curve in enumerate(high_q_filters, start=len(FILTERS) + 1):
        export_high_q_filter_response(index, curve)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
