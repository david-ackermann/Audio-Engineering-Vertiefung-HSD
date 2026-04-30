from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import fourier_phasor_core as core
import storyboard_paths as paths


OUTPUT_DIR = paths.ONE_SIDED_WINDOWED_MIXED_SIGNAL_DIR
MAG_PATH = OUTPUT_DIR / "01_one_sided_windowed_magnitude_spectrum.png"
PHASE_PATH = OUTPUT_DIR / "02_one_sided_windowed_phase_spectrum.png"
DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
FIGSIZE = (11.0, 4.8)


def build_context():
    obs_duration = core.DEFAULT_OBS_DURATION
    window_start, window_end = core.observed_limits(obs_duration)
    sample_count = int(obs_duration * core.FS)
    time_values = np.linspace(window_start, window_end, sample_count, endpoint=False)

    signal_values, _ = core.build_selectable_signal(time_values, "Mixed signal", core.DEFAULT_SIGNAL_FREQ)
    window_values = core.build_window(time_values, obs_duration, core.DEFAULT_WINDOW_MODE)
    weighted_signal = signal_values * window_values

    freqs = core.DISPLAY_FINE_FREQS
    basis = np.exp(-1j * 2.0 * np.pi * freqs[:, None] * time_values[None, :])
    coefficients = np.trapezoid(weighted_signal[None, :] * basis, x=time_values, axis=1)

    return {
        "freqs": freqs,
        "magnitude": np.abs(coefficients),
        "phase_deg": np.degrees(np.angle(coefficients)),
    }


def style_axis(ax, title, y_label, y_limits):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(core.ANALYSIS_FREQ_MIN, core.ANALYSIS_FREQ_MAX)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def export_magnitude(context):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(context["freqs"], context["magnitude"], color="0.35", lw=2.1)
    style_axis(
        ax,
        "One-sided windowed magnitude spectrum of the mixed signal",
        r"$|X_+(f)|$",
        (0.0, 1.15 * max(1.0, np.max(context["magnitude"]))),
    )
    fig.savefig(MAG_PATH, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def export_phase(context):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(context["freqs"], context["phase_deg"], color="0.45", lw=2.0)
    style_axis(
        ax,
        "One-sided windowed phase spectrum of the mixed signal",
        r"$\angle X_+(f)$ [deg]",
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
