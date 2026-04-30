from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import fourier_phasor_core as core
import storyboard_paths as paths


OUTPUT_ROOT = paths.INVERSE_FOURIERTRANSFORMATION_WINDOWED_DIR
DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
TIME_FIGSIZE = (12.0, 4.8)
SPECTRUM_FIGSIZE = (11.0, 4.8)
PHASOR_FIGSIZE = (7.4, 7.0)
SNAPSHOT_TIMES = (0.18, 0.10, 0.0)
CURRENT_SNAPSHOT_TIME = SNAPSHOT_TIMES[0]
CURRENT_OUTPUT_DIR = None
DISPLAY_FREQ_MIN = -7.0
DISPLAY_FREQ_MAX = 7.0
DISPLAY_FREQ_COUNT = 2601
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
PHASE_LIMITS = (-190.0, 190.0)
WEIGHT_LIMITS = (-1.1, 1.1)
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
COMPLEX_COLOR = "crimson"
CURVE_COLOR = "0.35"
MAG_COLOR = "0.30"
PASTEL_RED = "#de8d8d"
NEGATIVE_FILL_COLOR = "tab:red"
PHASE_VIS_REL_THRESHOLD = 0.015


def snapshot_folder_name(snapshot_time):
    if abs(snapshot_time) < 1e-12:
        return "05A_inverse_ft_windowed_storyboard_t0"
    snapshot_token = f"{snapshot_time:.2f}".replace("-", "m").replace(".", "p")
    return f"05A_inverse_ft_windowed_storyboard_t{snapshot_token}"


def build_context():
    obs_duration = core.DEFAULT_OBS_DURATION
    window_start, window_end = core.observed_limits(obs_duration)
    sample_count = int(obs_duration * core.FS)
    time_values = np.linspace(window_start, window_end, sample_count, endpoint=False)

    signal_values, signal_label = core.build_selectable_signal(
        time_values, "Mixed signal", core.DEFAULT_SIGNAL_FREQ
    )
    window_values = core.build_window(time_values, obs_duration, core.DEFAULT_WINDOW_MODE)
    weighted_signal = signal_values * window_values

    freqs = np.linspace(DISPLAY_FREQ_MIN, DISPLAY_FREQ_MAX, DISPLAY_FREQ_COUNT)
    basis = np.exp(-1j * 2.0 * np.pi * freqs[:, None] * time_values[None, :])
    coefficients = np.trapezoid(weighted_signal[None, :] * basis, x=time_values, axis=1)
    magnitude = np.abs(coefficients)
    phase_rad = np.angle(coefficients)
    phase_deg = np.degrees(phase_rad)
    base_phase = 2.0 * np.pi * freqs * CURRENT_SNAPSHOT_TIME
    pure_real_weight = np.cos(base_phase)
    pure_imag_weight = np.sin(base_phase)
    real_weight = np.cos(base_phase + phase_rad)
    imag_weight = np.sin(base_phase + phase_rad)
    real_contribution = magnitude * real_weight
    imag_contribution = magnitude * imag_weight

    snapshot_complex = np.trapezoid(
        coefficients * np.exp(1j * 2.0 * np.pi * freqs * CURRENT_SNAPSHOT_TIME),
        x=freqs,
    )

    reconstructed_complex_signal = np.trapezoid(
        coefficients[:, None] * np.exp(1j * 2.0 * np.pi * freqs[:, None] * time_values[None, :]),
        x=freqs,
        axis=0,
    )

    return {
        "freqs": freqs,
        "magnitude": magnitude,
        "phase_deg": phase_deg,
        "phase_rad": phase_rad,
        "time_values": time_values,
        "signal_label": signal_label,
        "pure_real_weight": pure_real_weight,
        "pure_imag_weight": pure_imag_weight,
        "real_weight": real_weight,
        "imag_weight": imag_weight,
        "real_contribution": real_contribution,
        "imag_contribution": imag_contribution,
        "snapshot_complex": snapshot_complex,
        "reconstructed_complex_signal": reconstructed_complex_signal,
        "reconstructed_signal": np.real(reconstructed_complex_signal),
        "spectrum_limit": 1.15 * max(1.0, np.max(magnitude)),
        "contribution_limit": 1.15 * max(
            1.0,
            np.max(np.abs(real_contribution)),
            np.max(np.abs(imag_contribution)),
            abs(snapshot_complex.real),
            abs(snapshot_complex.imag),
        ),
        "complex_limit": 1.15 * max(
            1.0,
            abs(snapshot_complex.real),
            abs(snapshot_complex.imag),
        ),
        "signal_limit": 1.15 * max(
            1.0,
            np.max(np.abs(signal_values)),
            np.max(np.abs(np.real(reconstructed_complex_signal))),
        ),
    }


def save_figure(fig, filename):
    if CURRENT_OUTPUT_DIR is None:
        raise RuntimeError("CURRENT_OUTPUT_DIR is not set")
    CURRENT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(CURRENT_OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def finalize_frequency_axis(ax, title, y_limits, y_label):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(DISPLAY_FREQ_MIN, DISPLAY_FREQ_MAX)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def finalize_time_axis(ax, title, time_values, y_limits, y_label="Amplitude"):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(time_values[0], time_values[-1])
    ax.set_ylim(*y_limits)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def add_combined_legend(ax_left, ax_right):
    handles_left, labels_left = ax_left.get_legend_handles_labels()
    handles_right, labels_right = ax_right.get_legend_handles_labels()
    ax_left.legend(
        handles_left + handles_right,
        labels_left + labels_right,
        loc="upper right",
        fontsize=12,
        framealpha=0.95,
    )


def export_two_sided_magnitude(context):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(context["freqs"], context["magnitude"], color=CURVE_COLOR, lw=2.1, label=r"$|Y_T(f)|$")
    finalize_frequency_axis(
        ax,
        "Windowed two-sided magnitude spectrum of the mixed signal",
        (0.0, context["spectrum_limit"]),
        r"$|Y_T(f)|$",
    )
    save_figure(fig, "01_windowed_two_sided_magnitude_spectrum.png")


def export_two_sided_phase(context):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax.plot(context["freqs"], context["phase_deg"], color="0.45", lw=2.0, label=r"$\angle Y_T(f)$")
    finalize_frequency_axis(
        ax,
        "Windowed two-sided phase spectrum of the mixed signal",
        PHASE_LIMITS,
        r"$\angle Y_T(f)$ [deg]",
    )
    save_figure(fig, "02_windowed_two_sided_phase_spectrum.png")


def export_weighting_overlay(context, weight_key, color, title, ylabel_right, filename):
    fig, ax_mag = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    ax_mag.plot(context["freqs"], context["magnitude"], color=MAG_COLOR, lw=2.1, label=r"$|Y_T(f)|$")
    finalize_frequency_axis(
        ax_mag,
        title,
        (0.0, context["spectrum_limit"]),
        r"$|Y_T(f)|$",
    )

    ax_weight = ax_mag.twinx()
    ax_weight.plot(context["freqs"], context[weight_key], color=color, lw=2.0, ls="--", label=ylabel_right)
    ax_weight.axhline(0.0, color=color, lw=0.9, alpha=0.6)
    ax_weight.set_ylim(*WEIGHT_LIMITS)
    ax_weight.set_ylabel(ylabel_right, fontsize=LABEL_SIZE, color=color)
    ax_weight.tick_params(axis="y", colors=color, labelsize=TICK_SIZE)
    add_combined_legend(ax_mag, ax_weight)
    save_figure(fig, filename)


def export_contribution(context, contribution_key, color, title, ylabel, filename, with_integral_line):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    values = context[contribution_key]
    integral_value = context["snapshot_complex"].real if contribution_key == "real_contribution" else context["snapshot_complex"].imag
    ax.fill_between(
        context["freqs"],
        0.0,
        values,
        where=values >= 0.0,
        color=color,
        alpha=0.22,
        interpolate=True,
    )
    ax.fill_between(
        context["freqs"],
        0.0,
        values,
        where=values < 0.0,
        color=NEGATIVE_FILL_COLOR,
        alpha=0.18,
        interpolate=True,
    )
    ax.plot(context["freqs"], values, color=color, lw=2.1, label="Weighted spectrum")
    if with_integral_line:
        ax.plot(
            [context["freqs"][0], context["freqs"][-1]],
            [integral_value, integral_value],
            color=color,
            lw=2.0,
            ls="--",
            label="Integral value",
        )
    finalize_frequency_axis(
        ax,
        title,
        (-context["contribution_limit"], context["contribution_limit"]),
        ylabel,
    )
    if with_integral_line:
        ax.legend(loc="upper right", fontsize=12, framealpha=0.95)
    save_figure(fig, filename)


def export_complex_sample(context):
    value = context["snapshot_complex"]
    fig, ax = plt.subplots(figsize=PHASOR_FIGSIZE)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.plot([0.0, value.real], [0.0, value.imag], color=COMPLEX_COLOR, lw=3.0)
    ax.plot([value.real], [value.imag], "o", color=COMPLEX_COLOR, ms=8)
    ax.plot([0.0, value.real], [0.0, 0.0], color=RE_COLOR, lw=1.7, alpha=0.9)
    ax.plot([value.real, value.real], [0.0, value.imag], color=IM_COLOR, lw=1.7, alpha=0.9)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-context["complex_limit"], context["complex_limit"])
    ax.set_ylim(-context["complex_limit"], context["complex_limit"])
    ax.grid(alpha=0.22)
    ax.set_xlabel(r"Re$\{x_T(t_0)\}$", fontsize=LABEL_SIZE, color=RE_COLOR)
    ax.set_ylabel(r"Im$\{x_T(t_0)\}$", fontsize=LABEL_SIZE, color=IM_COLOR)
    ax.set_title(f"Complex signal value from the windowed spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s", pad=10, fontsize=TITLE_SIZE)
    ax.tick_params(axis="x", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=IM_COLOR, labelsize=TICK_SIZE)
    save_figure(fig, "11_complex_sample_from_windowed_inverse_ft.png")


def export_signal_sample(context):
    time_values = context["time_values"]
    reconstructed = context["reconstructed_signal"]
    sample_index = int(np.argmin(np.abs(time_values - CURRENT_SNAPSHOT_TIME)))
    sample_value = reconstructed[sample_index]

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    ax.plot(time_values, reconstructed, color=PASTEL_RED, lw=2.5)
    ax.plot(
        [CURRENT_SNAPSHOT_TIME, CURRENT_SNAPSHOT_TIME],
        [0.0, sample_value],
        color="tab:red",
        lw=2.2,
    )
    ax.plot([CURRENT_SNAPSHOT_TIME], [sample_value], "o", color="tab:red", ms=9)
    finalize_time_axis(
        ax,
        f"Signal value from the windowed inverse FT at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
        time_values,
        (-context["signal_limit"], context["signal_limit"]),
    )
    save_figure(fig, "12_signal_sample_from_windowed_inverse_ft.png")


def main():
    global CURRENT_SNAPSHOT_TIME, CURRENT_OUTPUT_DIR

    exported_dirs = []
    for snapshot_time in SNAPSHOT_TIMES:
        CURRENT_SNAPSHOT_TIME = snapshot_time
        CURRENT_OUTPUT_DIR = OUTPUT_ROOT / snapshot_folder_name(snapshot_time)
        CURRENT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        for old_png in CURRENT_OUTPUT_DIR.glob("*.png"):
            old_png.unlink()

        context = build_context()
        export_two_sided_magnitude(context)
        export_two_sided_phase(context)
        export_weighting_overlay(
            context,
            weight_key="pure_real_weight",
            color=RE_COLOR,
            title=f"Windowed magnitude spectrum with cos(2pi f t_0) at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\cos(2\pi f t_0)$",
            filename="03_real_weighting_without_phase_overlay_at_t0.png",
        )
        export_weighting_overlay(
            context,
            weight_key="real_weight",
            color=RE_COLOR,
            title=f"Windowed magnitude spectrum with real weighting at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\cos(2\pi f t_0 + \angle Y_T(f))$",
            filename="04_real_weighting_overlay_at_t0.png",
        )
        export_contribution(
            context,
            contribution_key="real_contribution",
            color=RE_COLOR,
            title=f"Windowed real weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|Y_T(f)|\cos(2\pi f t_0 + \angle Y_T(f))$",
            filename="05_real_contribution_at_t0.png",
            with_integral_line=False,
        )
        export_contribution(
            context,
            contribution_key="real_contribution",
            color=RE_COLOR,
            title=f"Windowed real weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|Y_T(f)|\cos(2\pi f t_0 + \angle Y_T(f))$",
            filename="06_real_contribution_with_integral_at_t0.png",
            with_integral_line=True,
        )
        export_weighting_overlay(
            context,
            weight_key="pure_imag_weight",
            color=IM_COLOR,
            title=f"Windowed magnitude spectrum with sin(2pi f t_0) at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\sin(2\pi f t_0)$",
            filename="07_imag_weighting_without_phase_overlay_at_t0.png",
        )
        export_weighting_overlay(
            context,
            weight_key="imag_weight",
            color=IM_COLOR,
            title=f"Windowed magnitude spectrum with imaginary weighting at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\sin(2\pi f t_0 + \angle Y_T(f))$",
            filename="08_imag_weighting_overlay_at_t0.png",
        )
        export_contribution(
            context,
            contribution_key="imag_contribution",
            color=IM_COLOR,
            title=f"Windowed imaginary weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|Y_T(f)|\sin(2\pi f t_0 + \angle Y_T(f))$",
            filename="09_imag_contribution_at_t0.png",
            with_integral_line=False,
        )
        export_contribution(
            context,
            contribution_key="imag_contribution",
            color=IM_COLOR,
            title=f"Windowed imaginary weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|Y_T(f)|\sin(2\pi f t_0 + \angle Y_T(f))$",
            filename="10_imag_contribution_with_integral_at_t0.png",
            with_integral_line=True,
        )
        export_complex_sample(context)
        export_signal_sample(context)
        exported_dirs.append(str(CURRENT_OUTPUT_DIR))

    print("Windowed inverse-FT storyboard exported to:")
    for directory in exported_dirs:
        print(directory)


if __name__ == "__main__":
    main()
