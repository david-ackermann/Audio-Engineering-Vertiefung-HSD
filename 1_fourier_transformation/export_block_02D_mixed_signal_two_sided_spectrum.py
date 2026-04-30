from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import fourier_phasor_core as core
import storyboard_paths as paths


OUTPUT_DIR = paths.MIXED_SIGNAL_TWO_SIDED_SPECTRUM_DIR
MAG_PATH = OUTPUT_DIR / "01_two_sided_magnitude_spectrum.png"
PHASE_PATH = OUTPUT_DIR / "02_two_sided_phase_spectrum.png"
DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
FIGSIZE = (11.0, 4.8)
FREQ_AXIS_LIMIT = core.FREQ_MAX
LINEWIDTH = 3.2
POINT_SIZE = 10


def build_context():
    line_spectrum = core.build_ideal_two_sided_spectrum(
        core.selectable_signal_components("Mixed signal", core.DEFAULT_SIGNAL_FREQ)
    )
    freqs = np.array(sorted(line_spectrum), dtype=float)
    coefficients = np.array([line_spectrum[freq] for freq in freqs], dtype=complex)

    return {
        "freqs": freqs,
        "magnitude": np.abs(coefficients),
        "phase_deg": np.degrees(np.angle(coefficients)),
        "colors": ["#26a043" if freq < 0.0 else "tab:purple" for freq in freqs],
    }


def style_axis(ax, title, y_label, y_limits):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(-FREQ_AXIS_LIMIT, FREQ_AXIS_LIMIT)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def plot_line_spectrum(ax, freqs, values, colors):
    for frequency_hz, value, color in zip(freqs, values, colors):
        ax.vlines(frequency_hz, 0.0, value, color=color, lw=LINEWIDTH)
        ax.plot([frequency_hz], [value], "o", color=color, ms=POINT_SIZE)


def export_magnitude(context):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_line_spectrum(ax, context["freqs"], context["magnitude"], context["colors"])
    style_axis(
        ax,
        "Ideal two-sided magnitude spectrum of the mixed signal",
        r"$|X(f)|$",
        (0.0, 1.15 * max(1.0, np.max(context["magnitude"]))),
    )
    fig.savefig(MAG_PATH, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def export_phase(context):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot_line_spectrum(ax, context["freqs"], context["phase_deg"], context["colors"])
    style_axis(
        ax,
        "Ideal two-sided phase spectrum of the mixed signal",
        r"$\angle X(f)$ [deg]",
        (-190.0, 190.0),
    )
    fig.savefig(PHASE_PATH, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    context = build_context()
    export_magnitude(context)
    export_phase(context)
    print(f"Saved magnitude to: {MAG_PATH}")
    print(f"Saved phase to: {PHASE_PATH}")


if __name__ == "__main__":
    main()

