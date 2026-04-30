from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import fourier_phasor_core as core
import storyboard_paths as paths


OUTPUT_ROOT = paths.INVERSE_FT_STORYBOARD_SERIES_DIR
DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
TIME_FIGSIZE = (12.0, 4.8)
SPECTRUM_FIGSIZE = (11.0, 4.8)
PHASOR_FIGSIZE = (7.4, 7.0)
SUMMARY_FIGSIZE = (16.0, 4.8)
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
OBSERVED_COLOR = "0.20"
MAG_COLOR = "0.30"
NEGATIVE_FILL_COLOR = "tab:red"
PASTEL_RED = "#de8d8d"


def snapshot_folder_name(snapshot_time):
    if abs(snapshot_time) < 1e-12:
        return "04A_inverse_ft_storyboard_t0"
    snapshot_token = f"{snapshot_time:.2f}".replace("-", "m").replace(".", "p")
    return f"04A_inverse_ft_storyboard_t{snapshot_token}"


def cumulative_trapezoid(values, x_values):
    cumulative = np.zeros_like(values, dtype=float)
    increments = 0.5 * (values[1:] + values[:-1]) * np.diff(x_values)
    cumulative[1:] = np.cumsum(increments)
    return cumulative


def build_context():
    obs_duration = core.DEFAULT_OBS_DURATION
    window_start, window_end = core.observed_limits(obs_duration)
    sample_count = int(obs_duration * core.FS)
    time_values = np.linspace(window_start, window_end, sample_count, endpoint=False)

    signal_values, signal_label = core.build_selectable_signal(
        time_values, "Mixed signal", core.DEFAULT_SIGNAL_FREQ
    )

    freqs = np.linspace(DISPLAY_FREQ_MIN, DISPLAY_FREQ_MAX, DISPLAY_FREQ_COUNT)
    ideal_line_spectrum = core.build_ideal_two_sided_spectrum(
        core.selectable_signal_components("Mixed signal", core.DEFAULT_SIGNAL_FREQ)
    )
    line_freqs = np.array(sorted(ideal_line_spectrum), dtype=float)
    line_coeffs = np.array([ideal_line_spectrum[freq] for freq in line_freqs], dtype=complex)
    line_magnitude = np.abs(line_coeffs)
    line_phase_rad = np.angle(line_coeffs)
    line_phase_deg = np.degrees(line_phase_rad)

    base_phase = 2.0 * np.pi * freqs * CURRENT_SNAPSHOT_TIME
    pure_real_weight = np.cos(base_phase)
    pure_imag_weight = np.sin(base_phase)
    line_base_phase = 2.0 * np.pi * line_freqs * CURRENT_SNAPSHOT_TIME
    pure_real_weight_lines = np.cos(line_base_phase)
    pure_imag_weight_lines = np.sin(line_base_phase)
    real_weight_lines = np.cos(line_base_phase + line_phase_rad)
    imag_weight_lines = np.sin(line_base_phase + line_phase_rad)
    real_contribution_lines = line_magnitude * real_weight_lines
    imag_contribution_lines = line_magnitude * imag_weight_lines

    cumulative_real_lines = np.cumsum(real_contribution_lines)
    cumulative_imag_lines = np.cumsum(imag_contribution_lines)
    snapshot_complex = np.sum(line_coeffs * np.exp(1j * 2.0 * np.pi * line_freqs * CURRENT_SNAPSHOT_TIME))

    reconstructed_complex_signal = np.sum(
        line_coeffs[:, None] * np.exp(1j * 2.0 * np.pi * line_freqs[:, None] * time_values[None, :]),
        axis=0,
    )

    return {
        "freqs": freqs,
        "line_freqs": line_freqs,
        "line_coeffs": line_coeffs,
        "line_magnitude": line_magnitude,
        "line_phase_deg": line_phase_deg,
        "time_values": time_values,
        "signal_label": signal_label,
        "pure_real_weight": pure_real_weight,
        "pure_imag_weight": pure_imag_weight,
        "pure_real_weight_lines": pure_real_weight_lines,
        "pure_imag_weight_lines": pure_imag_weight_lines,
        "real_weight_lines": real_weight_lines,
        "imag_weight_lines": imag_weight_lines,
        "real_contribution_lines": real_contribution_lines,
        "imag_contribution_lines": imag_contribution_lines,
        "cumulative_real_lines": cumulative_real_lines,
        "cumulative_imag_lines": cumulative_imag_lines,
        "snapshot_complex": snapshot_complex,
        "reconstructed_complex_signal": reconstructed_complex_signal,
        "reconstructed_signal": np.real(reconstructed_complex_signal),
        "spectrum_limit": 1.15 * max(1.0, np.max(line_magnitude)),
        "contribution_limit": 1.15 * max(
            1.0,
            np.max(np.abs(real_contribution_lines)),
            np.max(np.abs(imag_contribution_lines)),
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


def draw_discrete_spectrum(ax, line_freqs, values, color, label):
    ax.vlines(line_freqs, 0.0, values, color=color, lw=2.4, label=label)
    ax.plot(line_freqs, values, "o", color=color, ms=7)


def export_two_sided_magnitude(context):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    draw_discrete_spectrum(ax, context["line_freqs"], context["line_magnitude"], CURVE_COLOR, r"$|X(f)|$")
    finalize_frequency_axis(
        ax,
        "Two-sided magnitude spectrum of the mixed signal",
        (0.0, context["spectrum_limit"]),
        r"$|X(f)|$",
    )
    save_figure(fig, "01_two_sided_magnitude_spectrum.png")


def export_two_sided_phase(context):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    draw_discrete_spectrum(ax, context["line_freqs"], context["line_phase_deg"], "0.45", r"$\angle X(f)$")
    finalize_frequency_axis(
        ax,
        "Two-sided phase spectrum of the mixed signal",
        PHASE_LIMITS,
        r"$\angle X(f)$ [deg]",
    )
    save_figure(fig, "02_two_sided_phase_spectrum.png")


def export_weighting_overlay(
    context,
    weight_key,
    color,
    title,
    ylabel_right,
    filename,
    discrete_weight,
    draw_weight_zero_line=False,
    continuous_weight_key=None,
    continuous_weight_label=None,
):
    fig, ax_mag = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    draw_discrete_spectrum(ax_mag, context["line_freqs"], context["line_magnitude"], MAG_COLOR, r"$|X(f)|$")
    finalize_frequency_axis(
        ax_mag,
        title,
        (0.0, context["spectrum_limit"]),
        r"$|X(f)|$",
    )

    ax_weight = ax_mag.twinx()
    if discrete_weight:
        draw_discrete_spectrum(ax_weight, context["line_freqs"], context[weight_key], color, ylabel_right)
        if continuous_weight_key is not None:
            ax_weight.plot(
                context["freqs"],
                context[continuous_weight_key],
                color=color,
                lw=2.0,
                ls="--",
                label=continuous_weight_label if continuous_weight_label is not None else ylabel_right,
            )
    else:
        ax_weight.plot(context["freqs"], context[weight_key], color=color, lw=2.0, ls="--", label=ylabel_right)
    if draw_weight_zero_line:
        ax_weight.axhline(0.0, color=color, lw=0.9, alpha=0.6)
    ax_weight.set_ylim(*WEIGHT_LIMITS)
    ax_weight.set_ylabel(ylabel_right, fontsize=LABEL_SIZE, color=color)
    ax_weight.tick_params(axis="y", colors=color, labelsize=TICK_SIZE)
    add_combined_legend(ax_mag, ax_weight)
    save_figure(fig, filename)


def export_contribution(context, contribution_key, color, title, ylabel, filename, with_integral_line):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    values = context[contribution_key]
    integral_value = context["snapshot_complex"].real if contribution_key == "real_contribution_lines" else context["snapshot_complex"].imag
    draw_discrete_spectrum(ax, context["line_freqs"], values, color, "Weighted spectrum")
    if with_integral_line:
        ax.plot(
            [context["freqs"][0], context["freqs"][-1]],
            [integral_value, integral_value],
            color=color,
            lw=2.0,
            ls="--",
            label="Integral sum",
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
    ax.set_xlabel(r"Re$\{x(t_0)\}$", fontsize=LABEL_SIZE, color=RE_COLOR)
    ax.set_ylabel(r"Im$\{x(t_0)\}$", fontsize=LABEL_SIZE, color=IM_COLOR)
    ax.set_title(f"Complex signal value at t = {CURRENT_SNAPSHOT_TIME:.2f} s", pad=10, fontsize=TITLE_SIZE)
    ax.tick_params(axis="x", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=IM_COLOR, labelsize=TICK_SIZE)
    save_figure(fig, "11_complex_sample_at_t0.png")


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
        f"Real signal value from the inverse FT at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
        time_values,
        (-context["signal_limit"], context["signal_limit"]),
    )
    save_figure(fig, "12_signal_sample_from_inverse_ft.png")


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
            title=f"Magnitude spectrum with cos(2pi f t_0) at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\cos(2\pi f t_0)$",
            filename="03_real_weighting_without_phase_overlay_at_t0.png",
            discrete_weight=False,
        )
        export_weighting_overlay(
            context,
            weight_key="real_weight_lines",
            color=RE_COLOR,
            title=f"Magnitude spectrum with real weighting at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\cos(2\pi f t_0 + \angle X(f))$",
            filename="04_real_weighting_overlay_at_t0.png",
            discrete_weight=True,
            draw_weight_zero_line=True,
            continuous_weight_key="pure_real_weight",
            continuous_weight_label=r"$\cos(2\pi f t_0)$",
        )
        export_contribution(
            context,
            contribution_key="real_contribution_lines",
            color=RE_COLOR,
            title=f"Real weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|X(f)|\cos(2\pi f t_0 + \angle X(f))$",
            filename="05_real_contribution_at_t0.png",
            with_integral_line=False,
        )
        export_contribution(
            context,
            contribution_key="real_contribution_lines",
            color=RE_COLOR,
            title=f"Real weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|X(f)|\cos(2\pi f t_0 + \angle X(f))$",
            filename="06_real_contribution_with_integral_at_t0.png",
            with_integral_line=True,
        )
        export_weighting_overlay(
            context,
            weight_key="pure_imag_weight",
            color=IM_COLOR,
            title=f"Magnitude spectrum with sin(2pi f t_0) at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\sin(2\pi f t_0)$",
            filename="07_imag_weighting_without_phase_overlay_at_t0.png",
            discrete_weight=False,
        )
        export_weighting_overlay(
            context,
            weight_key="imag_weight_lines",
            color=IM_COLOR,
            title=f"Magnitude spectrum with imaginary weighting at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel_right=r"$\sin(2\pi f t_0 + \angle X(f))$",
            filename="08_imag_weighting_overlay_at_t0.png",
            discrete_weight=True,
            draw_weight_zero_line=True,
            continuous_weight_key="pure_imag_weight",
            continuous_weight_label=r"$\sin(2\pi f t_0)$",
        )
        export_contribution(
            context,
            contribution_key="imag_contribution_lines",
            color=IM_COLOR,
            title=f"Imaginary weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|X(f)|\sin(2\pi f t_0 + \angle X(f))$",
            filename="09_imag_contribution_at_t0.png",
            with_integral_line=False,
        )
        export_contribution(
            context,
            contribution_key="imag_contribution_lines",
            color=IM_COLOR,
            title=f"Imaginary weighted spectrum at t = {CURRENT_SNAPSHOT_TIME:.2f} s",
            ylabel=r"$|X(f)|\sin(2\pi f t_0 + \angle X(f))$",
            filename="10_imag_contribution_with_integral_at_t0.png",
            with_integral_line=True,
        )
        export_complex_sample(context)
        export_signal_sample(context)
        exported_dirs.append(str(CURRENT_OUTPUT_DIR))

    print("Inverse-FT storyboard exported to:")
    for directory in exported_dirs:
        print(directory)



if __name__ == "__main__":
    main()

