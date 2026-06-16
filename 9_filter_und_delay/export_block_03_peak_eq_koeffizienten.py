from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "03_peak_eq_koeffizienten"

DPI = 200
FIGSIZE = (11.5, 4.8)
FIGSIZE_TALL = (11.5, 7.2)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18

SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.70"
DARK_GREY = "0.35"

FS_HZ = 48_000.0
NYQUIST_HZ = FS_HZ / 2.0
FREQUENCY_MIN_HZ = 20.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]

REFERENCE_Q = 1.0 / np.sqrt(2.0)
HIGH_Q = 1.25
PEAK_CENTER_HZ = 500.0
PEAK_GAINS_DB = (-12.0, -6.0, 6.0, 12.0)
PEAK_GAIN_LINE_STYLES = {
    -12.0: "-",
    -6.0: "--",
    6.0: "-.",
    12.0: ":",
}
SHELF_Q = REFERENCE_Q
SHELF_HIGH_Q = HIGH_Q
SHELF_Q_VALUES = (SHELF_Q, SHELF_HIGH_Q)
SHELF_GAINS_DB = (-12.0, -6.0, 6.0, 12.0)
SHELF_GAIN_LINE_STYLES = {
    -12.0: "-",
    -6.0: "--",
    6.0: "-.",
    12.0: ":",
}
LOW_SHELF_FREQUENCY_HZ = 200.0
HIGH_SHELF_FREQUENCY_HZ = 5_000.0

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
class EqBand:
    label: str
    kind: str
    frequency_hz: float
    q: float
    gain_db: float


def normalize(b0: float, b1: float, b2: float, a0: float, a1: float, a2: float) -> BiquadCoefficients:
    return BiquadCoefficients(b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def design_biquad(band: EqBand) -> BiquadCoefficients:
    omega = 2.0 * np.pi * band.frequency_hz / FS_HZ
    cos_omega = np.cos(omega)
    sin_omega = np.sin(omega)
    alpha = sin_omega / (2.0 * band.q)

    if band.kind == "highpass":
        b0 = (1.0 + cos_omega) / 2.0
        b1 = -(1.0 + cos_omega)
        b2 = (1.0 + cos_omega) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha
    elif band.kind == "peak":
        a_gain = 10.0 ** (band.gain_db / 40.0)
        b0 = 1.0 + alpha * a_gain
        b1 = -2.0 * cos_omega
        b2 = 1.0 - alpha * a_gain
        a0 = 1.0 + alpha / a_gain
        a1 = -2.0 * cos_omega
        a2 = 1.0 - alpha / a_gain
    elif band.kind == "low_shelf":
        a_gain = 10.0 ** (band.gain_db / 40.0)
        sqrt_a = np.sqrt(a_gain)
        b0 = a_gain * ((a_gain + 1.0) - (a_gain - 1.0) * cos_omega + 2.0 * sqrt_a * alpha)
        b1 = 2.0 * a_gain * ((a_gain - 1.0) - (a_gain + 1.0) * cos_omega)
        b2 = a_gain * ((a_gain + 1.0) - (a_gain - 1.0) * cos_omega - 2.0 * sqrt_a * alpha)
        a0 = (a_gain + 1.0) + (a_gain - 1.0) * cos_omega + 2.0 * sqrt_a * alpha
        a1 = -2.0 * ((a_gain - 1.0) + (a_gain + 1.0) * cos_omega)
        a2 = (a_gain + 1.0) + (a_gain - 1.0) * cos_omega - 2.0 * sqrt_a * alpha
    elif band.kind == "high_shelf":
        a_gain = 10.0 ** (band.gain_db / 40.0)
        sqrt_a = np.sqrt(a_gain)
        b0 = a_gain * ((a_gain + 1.0) + (a_gain - 1.0) * cos_omega + 2.0 * sqrt_a * alpha)
        b1 = -2.0 * a_gain * ((a_gain - 1.0) + (a_gain + 1.0) * cos_omega)
        b2 = a_gain * ((a_gain + 1.0) + (a_gain - 1.0) * cos_omega - 2.0 * sqrt_a * alpha)
        a0 = (a_gain + 1.0) - (a_gain - 1.0) * cos_omega + 2.0 * sqrt_a * alpha
        a1 = 2.0 * ((a_gain - 1.0) - (a_gain + 1.0) * cos_omega)
        a2 = (a_gain + 1.0) - (a_gain - 1.0) * cos_omega - 2.0 * sqrt_a * alpha
    else:
        raise ValueError(f"Unknown EQ band kind: {band.kind}")

    return normalize(b0, b1, b2, a0, a1, a2)


def frequency_grid() -> np.ndarray:
    return np.geomspace(FREQUENCY_MIN_HZ, NYQUIST_HZ, 4096)


def complex_response(frequency_hz: np.ndarray, coefficients: BiquadCoefficients) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    z1 = np.exp(-1j * omega)
    z2 = np.exp(-2j * omega)
    numerator = coefficients.b0 + coefficients.b1 * z1 + coefficients.b2 * z2
    denominator = 1.0 + coefficients.a1 * z1 + coefficients.a2 * z2
    return numerator / denominator


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def group_delay_samples(response: np.ndarray, frequency_hz: np.ndarray) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    phase = np.unwrap(np.angle(response))
    return -np.gradient(phase, omega)


def save_figure(fig, filename: str) -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.glob("*.png"):
        image_file.unlink()


def style_log_axis(ax, title: str, ylabel: str, y_limits: tuple[float, float], y_ticks: list[float]) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, 20_000.0)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_ylim(*y_limits)
    ax.set_yticks(y_ticks)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def add_frequency_marker(ax, frequency_hz: float) -> None:
    ax.axvline(frequency_hz, color="0.45", lw=1.8, ls="--", alpha=0.85, zorder=1)


def add_peak_curves(
    ax,
    plot_frequency_hz: np.ndarray,
    q_value: float,
    color: str,
    zorder: int,
    alpha_scale: float = 1.0,
) -> None:
    for gain_db in PEAK_GAINS_DB:
        band = EqBand(f"{gain_db:+.0f} dB", "peak", PEAK_CENTER_HZ, q_value, gain_db)
        response = complex_response(plot_frequency_hz, design_biquad(band))
        ax.plot(
            plot_frequency_hz,
            magnitude_db(response),
            color=color,
            lw=3.0,
            ls=PEAK_GAIN_LINE_STYLES[gain_db],
            alpha=0.95 * alpha_scale,
            zorder=zorder,
        )


def add_peak_legends(ax, q_handles: list[Line2D]) -> None:
    gain_legend_handles = [
        Line2D([0], [0], color=DARK_GREY, lw=2.6, ls=PEAK_GAIN_LINE_STYLES[gain_db], label=f"{gain_db:+.0f} dB")
        for gain_db in PEAK_GAINS_DB
    ]
    q_legend = ax.legend(handles=q_handles, loc="upper right", fontsize=13, frameon=True)
    q_legend.get_frame().set_facecolor("white")
    q_legend.get_frame().set_edgecolor("none")
    q_legend.get_frame().set_alpha(0.95)
    ax.add_artist(q_legend)

    gain_legend = ax.legend(handles=gain_legend_handles, loc="lower right", fontsize=12, frameon=True)
    gain_legend.get_frame().set_facecolor("white")
    gain_legend.get_frame().set_edgecolor("none")
    gain_legend.get_frame().set_alpha(0.95)


def export_peak_gain_variation() -> None:
    frequency_hz = frequency_grid()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    add_peak_curves(ax, frequency_hz, REFERENCE_Q, SYSTEM_GREEN, 4)

    add_frequency_marker(ax, PEAK_CENTER_HZ)
    style_log_axis(ax, "Peak EQ magnitude response", r"$|H(f)|$ in dB", (-14.0, 14.0), [-12.0, -6.0, 0.0, 6.0, 12.0])
    ax.axhline(0.0, color="black", lw=1.0, alpha=0.55)
    add_peak_legends(
        ax,
        [Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$Q=1/\sqrt{2}$")],
    )
    save_figure(fig, "01_peak_eq_gain_variation.png")


def export_peak_higher_q() -> None:
    frequency_hz = frequency_grid()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    add_peak_curves(ax, frequency_hz, REFERENCE_Q, REFERENCE_GREY, 2, alpha_scale=0.86)
    add_peak_curves(ax, frequency_hz, HIGH_Q, SYSTEM_GREEN, 4)

    add_frequency_marker(ax, PEAK_CENTER_HZ)
    style_log_axis(ax, "Peak EQ magnitude response, higher Q", r"$|H(f)|$ in dB", (-14.0, 14.0), [-12.0, -6.0, 0.0, 6.0, 12.0])
    ax.axhline(0.0, color="black", lw=1.0, alpha=0.55)
    add_peak_legends(
        ax,
        [
            Line2D([0], [0], color=REFERENCE_GREY, lw=3.0, label=r"$Q=1/\sqrt{2}$"),
            Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=rf"$Q={HIGH_Q:g}$"),
        ],
    )
    save_figure(fig, "02_peak_eq_higher_q.png")


def add_shelf_curves(
    ax,
    kind: str,
    plot_frequency_hz: np.ndarray,
    shelf_frequency_hz: float,
    q_value: float,
    color: str,
    zorder: int,
    alpha_scale: float = 1.0,
) -> None:
    max_abs_gain = max(abs(value) for value in SHELF_GAINS_DB)
    for gain_db in SHELF_GAINS_DB:
        band = EqBand(f"{gain_db:+.0f} dB", kind, shelf_frequency_hz, q_value, gain_db)
        response = complex_response(plot_frequency_hz, design_biquad(band))
        alpha = (0.95 if abs(gain_db) == max_abs_gain else 0.74) * alpha_scale
        ax.plot(
            plot_frequency_hz,
            magnitude_db(response),
            color=color,
            lw=2.7,
            ls=SHELF_GAIN_LINE_STYLES[gain_db],
            alpha=alpha,
            zorder=zorder,
        )


def export_shelf_family(kind: str, filename: str, title: str, frequency_hz: float, include_higher_q: bool) -> None:
    plot_frequency_hz = frequency_grid()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    if include_higher_q:
        add_shelf_curves(ax, kind, plot_frequency_hz, frequency_hz, SHELF_Q, REFERENCE_GREY, 2, alpha_scale=0.88)
        add_shelf_curves(ax, kind, plot_frequency_hz, frequency_hz, SHELF_HIGH_Q, SYSTEM_GREEN, 4)
        q_legend_handles = [
            Line2D([0], [0], color=REFERENCE_GREY, lw=3.0, label=r"$Q=1/\sqrt{2}$"),
            Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=rf"$Q={HIGH_Q:g}$"),
        ]
    else:
        add_shelf_curves(ax, kind, plot_frequency_hz, frequency_hz, SHELF_Q, SYSTEM_GREEN, 4)
        q_legend_handles = [
            Line2D([0], [0], color=SYSTEM_GREEN, lw=3.0, label=r"$Q=1/\sqrt{2}$"),
        ]

    add_frequency_marker(ax, frequency_hz)
    style_log_axis(ax, title, r"$|H(f)|$ in dB", (-14.0, 14.0), [-12.0, -6.0, 0.0, 6.0, 12.0])
    ax.axhline(0.0, color="black", lw=1.0, alpha=0.55)

    gain_legend_handles = [
        Line2D([0], [0], color=DARK_GREY, lw=2.4, ls=SHELF_GAIN_LINE_STYLES[gain_db], label=f"{gain_db:+.0f} dB")
        for gain_db in SHELF_GAINS_DB
    ]
    q_legend = ax.legend(
        handles=q_legend_handles,
        loc="upper right" if kind == "low_shelf" else "upper left",
        fontsize=13,
        frameon=True,
    )
    q_legend.get_frame().set_facecolor("white")
    q_legend.get_frame().set_edgecolor("none")
    q_legend.get_frame().set_alpha(0.95)
    ax.add_artist(q_legend)

    gain_legend = ax.legend(
        handles=gain_legend_handles,
        loc="lower right" if kind == "low_shelf" else "lower left",
        fontsize=12,
        frameon=True,
        ncol=2,
    )
    gain_legend.get_frame().set_facecolor("white")
    gain_legend.get_frame().set_edgecolor("none")
    gain_legend.get_frame().set_alpha(0.95)
    save_figure(fig, filename)


def cascade_bands() -> tuple[EqBand, ...]:
    return (
        EqBand("High-pass", "highpass", 80.0, 0.707, 0.0),
        EqBand("Peak EQ 1", "peak", 250.0, 1.1, -4.0),
        EqBand("Peak EQ 2", "peak", 900.0, 2.0, 5.0),
        EqBand("Peak EQ 3", "peak", 3_200.0, 1.4, -3.0),
        EqBand("High-shelf", "high_shelf", 7_000.0, 0.707, 4.0),
    )


def cascade_responses(frequency_hz: np.ndarray) -> tuple[list[np.ndarray], np.ndarray]:
    individual_responses = [
        complex_response(frequency_hz, design_biquad(band))
        for band in cascade_bands()
    ]
    total_response = np.prod(individual_responses, axis=0)
    return individual_responses, total_response


def export_daw_eq_cascade_magnitude() -> None:
    frequency_hz = frequency_grid()
    individual_responses, total_response = cascade_responses(frequency_hz)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    bands = cascade_bands()
    for band, response in zip(bands, individual_responses):
        ax.plot(
            frequency_hz,
            magnitude_db(response),
            color=REFERENCE_GREY,
            lw=2.2,
            alpha=0.85,
            label=band.label,
            zorder=2,
        )
        add_frequency_marker(ax, band.frequency_hz)

    ax.plot(
        frequency_hz,
        magnitude_db(total_response),
        color=SYSTEM_GREEN,
        lw=3.6,
        label="Cascade sum",
        zorder=4,
    )

    style_log_axis(ax, "DAW EQ cascade magnitude response", r"$|H(f)|$ in dB", (-16.0, 10.0), [-12.0, -6.0, 0.0, 6.0])
    ax.axhline(0.0, color="black", lw=1.0, alpha=0.55)
    legend = ax.legend(loc="lower right", fontsize=12, frameon=True, ncol=2)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    save_figure(fig, "07_daw_eq_cascade_magnitude.png")


def group_delay_limits(delay: np.ndarray) -> tuple[tuple[float, float], list[float]]:
    finite_delay = delay[np.isfinite(delay)]
    y_min = min(float(np.min(finite_delay)), 0.0)
    y_max = max(float(np.max(finite_delay)), 0.0)
    padding = max(1.0, 0.08 * (y_max - y_min))
    lower = np.floor(y_min - padding)
    upper = np.ceil(y_max + padding)
    raw_step = max((upper - lower) / 5.0, 1.0)
    base = 10.0 ** np.floor(np.log10(raw_step))
    tick_step = next(step for step in (base, 2.0 * base, 5.0 * base, 10.0 * base) if step >= raw_step)
    tick_start = tick_step * np.floor(lower / tick_step)
    tick_stop = tick_step * np.ceil(upper / tick_step)
    ticks = np.arange(tick_start, tick_stop + 0.1 * tick_step, tick_step).tolist()
    return (lower, upper), ticks


def export_daw_eq_phase_response() -> None:
    frequency_hz = frequency_grid()
    _, total_response = cascade_responses(frequency_hz)
    phase = np.angle(total_response)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    ax.plot(frequency_hz, phase, color=SYSTEM_GREEN, lw=3.0)
    style_log_axis(ax, "DAW EQ cascade phase response", "Phase in rad", (-np.pi, np.pi), [-np.pi, -np.pi / 2.0, 0.0, np.pi / 2.0, np.pi])
    ax.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])

    for band in cascade_bands():
        add_frequency_marker(ax, band.frequency_hz)

    save_figure(fig, "08_daw_eq_cascade_phase_response.png")


def export_daw_eq_group_delay() -> None:
    frequency_hz = frequency_grid()
    _, total_response = cascade_responses(frequency_hz)
    delay = group_delay_samples(total_response, frequency_hz)
    y_limits, y_ticks = group_delay_limits(delay)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)

    ax.plot(frequency_hz, delay, color=SYSTEM_GREEN, lw=3.0)
    style_log_axis(ax, "DAW EQ cascade group delay", "Group delay in samples", y_limits, y_ticks)
    ax.axhline(0.0, color="black", lw=1.0, alpha=0.55)
    for band in cascade_bands():
        add_frequency_marker(ax, band.frequency_hz)

    save_figure(fig, "09_daw_eq_cascade_group_delay.png")


def main() -> None:
    clear_output_dir()
    export_peak_gain_variation()
    export_peak_higher_q()
    export_shelf_family("low_shelf", "03_low_shelf_reference_q.png", "Low-shelf magnitude response", LOW_SHELF_FREQUENCY_HZ, include_higher_q=False)
    export_shelf_family("low_shelf", "04_low_shelf_higher_q.png", "Low-shelf magnitude response", LOW_SHELF_FREQUENCY_HZ, include_higher_q=True)
    export_shelf_family("high_shelf", "05_high_shelf_reference_q.png", "High-shelf magnitude response", HIGH_SHELF_FREQUENCY_HZ, include_higher_q=False)
    export_shelf_family("high_shelf", "06_high_shelf_higher_q.png", "High-shelf magnitude response", HIGH_SHELF_FREQUENCY_HZ, include_higher_q=True)
    export_daw_eq_cascade_magnitude()
    export_daw_eq_phase_response()
    export_daw_eq_group_delay()
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
