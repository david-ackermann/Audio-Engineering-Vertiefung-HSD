from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from PIL import Image

import fourier_phasor_core as core
import storyboard_paths as paths


OUTPUT_DIR = paths.INVERSE_FT_ONE_SIDED_STORYBOARD_T0P18_DIR
DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
TIME_FIGSIZE = (12.0, 4.8)
SPECTRUM_FIGSIZE = (11.0, 4.8)
PHASOR_FIGSIZE = (7.4, 7.0)
HELIX_FIGSIZE = (14.2, 8.8)
HELIX_TITLE_SIZE = 25
HELIX_LABEL_SIZE = 21
HELIX_TICK_SIZE = 18
SNAPSHOT_TIME = 0.18
DISPLAY_FREQ_MIN = -7.0
DISPLAY_FREQ_MAX = 7.0
DISPLAY_FREQ_COUNT = 2601
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.25
PHASE_LIMITS = (-190.0, 190.0)
WEIGHT_LIMITS = (-1.1, 1.1)
MAG_COLOR = "0.30"
RE_COLOR = "tab:blue"
IM_COLOR = "tab:orange"
NEGATIVE_FILL_COLOR = "tab:red"
SIGNAL_COLOR = "0.45"
MARKER_COLOR = "tab:red"
OBSERVED_COLOR = "0.20"
PHASOR_COLOR = "crimson"
HELIX_SUM_COLOR = "#de8d8d"
HELIX_PNG_NAME = "12_complex_signal_helix.png"
HELIX_GIF_NAME = "12_complex_signal_helix.gif"


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

    signal_values, _ = core.build_selectable_signal(
        time_values, "Mixed signal", core.DEFAULT_SIGNAL_FREQ
    )

    freqs_full = np.linspace(DISPLAY_FREQ_MIN, DISPLAY_FREQ_MAX, DISPLAY_FREQ_COUNT)
    ideal_line_spectrum = core.build_ideal_positive_frequency_spectrum(
        core.selectable_signal_components("Mixed signal", core.DEFAULT_SIGNAL_FREQ)
    )
    line_freqs = np.array(sorted(ideal_line_spectrum), dtype=float)
    line_coeffs = np.array([ideal_line_spectrum[freq] for freq in line_freqs], dtype=complex)
    line_magnitude = np.abs(line_coeffs)
    line_phase_rad = np.angle(line_coeffs)
    line_phase_deg = np.degrees(line_phase_rad)

    base_phase_full = 2.0 * np.pi * freqs_full * SNAPSHOT_TIME
    real_weight_without_phase_full = np.cos(base_phase_full)
    imag_weight_without_phase_full = np.sin(base_phase_full)
    line_base_phase = 2.0 * np.pi * line_freqs * SNAPSHOT_TIME
    real_weight_full = np.cos(line_base_phase + line_phase_rad)
    imag_weight_full = np.sin(line_base_phase + line_phase_rad)

    real_weighted_spectrum_full = line_magnitude * real_weight_full
    imag_weighted_spectrum_full = line_magnitude * imag_weight_full

    snapshot_real = np.sum(real_weighted_spectrum_full)
    snapshot_imag = np.sum(imag_weighted_spectrum_full)
    snapshot_complex = snapshot_real + 1j * snapshot_imag

    analytic_signal = np.sum(
        line_coeffs[:, None] * np.exp(1j * 2.0 * np.pi * line_freqs[:, None] * time_values[None, :]),
        axis=0,
    )
    reconstructed_signal = np.real(analytic_signal)

    return {
        "freqs_full": freqs_full,
        "time_values": time_values,
        "observed_signal": signal_values,
        "line_freqs": line_freqs,
        "line_magnitude": line_magnitude,
        "line_phase_deg": line_phase_deg,
        "real_weight_without_phase_full": real_weight_without_phase_full,
        "imag_weight_without_phase_full": imag_weight_without_phase_full,
        "real_weight_full": real_weight_full,
        "imag_weight_full": imag_weight_full,
        "real_weighted_spectrum_full": real_weighted_spectrum_full,
        "imag_weighted_spectrum_full": imag_weighted_spectrum_full,
        "snapshot_real": snapshot_real,
        "snapshot_imag": snapshot_imag,
        "snapshot_complex": snapshot_complex,
        "analytic_signal": analytic_signal,
        "reconstructed_signal": reconstructed_signal,
        "spectrum_limit": 1.15 * max(1.0, np.max(line_magnitude)),
        "weighted_limit": 1.15 * max(
            1.0,
            np.max(np.abs(real_weighted_spectrum_full)),
            np.max(np.abs(imag_weighted_spectrum_full)),
            abs(snapshot_real),
            abs(snapshot_imag),
        ),
        "signal_limit": 1.15 * max(
            1.0,
            np.max(np.abs(signal_values)),
            np.max(np.abs(reconstructed_signal)),
        ),
        "complex_limit": 1.15 * max(
            1.0,
            abs(snapshot_real),
            abs(snapshot_imag),
            np.max(np.abs(np.real(analytic_signal))),
            np.max(np.abs(np.imag(analytic_signal))),
        ),
    }


def save_figure(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, bbox_inches="tight")
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


def finalize_time_axis(ax, title, time_values, y_limits):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(time_values[0], time_values[-1])
    ax.set_ylim(*y_limits)
    ax.grid(alpha=GRID_ALPHA)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
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


def export_one_sided_magnitude(context):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    draw_discrete_spectrum(ax, context["line_freqs"], context["line_magnitude"], MAG_COLOR, r"$|X_+(f)|$")
    finalize_frequency_axis(
        ax,
        "One-sided magnitude spectrum of the mixed signal",
        (0.0, context["spectrum_limit"]),
        r"$|X_+(f)|$",
    )
    save_figure(fig, "01_one_sided_magnitude_spectrum.png")


def export_one_sided_phase(context):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    draw_discrete_spectrum(ax, context["line_freqs"], context["line_phase_deg"], "0.45", r"$\angle X_+(f)$")
    finalize_frequency_axis(
        ax,
        "One-sided phase spectrum of the mixed signal",
        PHASE_LIMITS,
        r"$\angle X_+(f)$ [deg]",
    )
    save_figure(fig, "02_one_sided_phase_spectrum.png")


def export_weight_overlay(
    context,
    weight_key,
    color,
    title,
    right_label,
    filename,
    discrete_weight,
    draw_weight_zero_line=False,
    continuous_weight_key=None,
    continuous_weight_label=None,
):
    fig, ax_mag = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    draw_discrete_spectrum(ax_mag, context["line_freqs"], context["line_magnitude"], MAG_COLOR, r"$|X_+(f)|$")
    finalize_frequency_axis(ax_mag, title, (0.0, context["spectrum_limit"]), r"$|X_+(f)|$")

    ax_weight = ax_mag.twinx()
    if discrete_weight:
        draw_discrete_spectrum(ax_weight, context["line_freqs"], context[weight_key], color, right_label)
        if continuous_weight_key is not None:
            ax_weight.plot(
                context["freqs_full"],
                context[continuous_weight_key],
                color=color,
                lw=2.0,
                ls="--",
                label=continuous_weight_label if continuous_weight_label is not None else right_label,
            )
    else:
        ax_weight.plot(
            context["freqs_full"],
            context[weight_key],
            color=color,
            lw=2.0,
            ls="--",
            label=right_label,
        )
    if draw_weight_zero_line:
        ax_weight.axhline(0.0, color=color, lw=0.9, alpha=0.6)
    ax_weight.set_ylim(*WEIGHT_LIMITS)
    ax_weight.set_ylabel(right_label, fontsize=LABEL_SIZE, color=color)
    ax_weight.tick_params(axis="y", colors=color, labelsize=TICK_SIZE)
    add_combined_legend(ax_mag, ax_weight)
    save_figure(fig, filename)


def export_weighted_spectrum(context, values_key, color, title, ylabel, filename, with_integral_line, integral_value):
    fig, ax = plt.subplots(figsize=SPECTRUM_FIGSIZE)
    values = context[values_key]
    draw_discrete_spectrum(ax, context["line_freqs"], values, color, "Weighted spectrum")
    if with_integral_line:
        ax.plot(
            [context["freqs_full"][0], context["freqs_full"][-1]],
            [integral_value, integral_value],
            color=color,
            lw=2.0,
            ls="--",
            label="Integral sum",
        )
    finalize_frequency_axis(
        ax,
        title,
        (-context["weighted_limit"], context["weighted_limit"]),
        ylabel,
    )
    if with_integral_line:
        ax.legend(loc="upper right", fontsize=12, framealpha=0.95)
    save_figure(fig, filename)


def export_complex_phasor(context):
    value = context["snapshot_complex"]
    fig, ax = plt.subplots(figsize=PHASOR_FIGSIZE)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.plot([0.0, value.real], [0.0, value.imag], color=PHASOR_COLOR, lw=3.0)
    ax.plot([value.real], [value.imag], "o", color=PHASOR_COLOR, ms=8)
    ax.plot([0.0, value.real], [0.0, 0.0], color=RE_COLOR, lw=1.7, alpha=0.9)
    ax.plot([value.real, value.real], [0.0, value.imag], color=IM_COLOR, lw=1.7, alpha=0.9)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-context["complex_limit"], context["complex_limit"])
    ax.set_ylim(-context["complex_limit"], context["complex_limit"])
    ax.grid(alpha=0.22)
    ax.set_xlabel(r"Re$\{x_+(t_0)\}$", fontsize=LABEL_SIZE, color=RE_COLOR)
    ax.set_ylabel(r"Im$\{x_+(t_0)\}$", fontsize=LABEL_SIZE, color=IM_COLOR)
    ax.set_title(f"One-sided phasor at t = {SNAPSHOT_TIME:.2f} s", pad=10, fontsize=TITLE_SIZE)
    ax.tick_params(axis="x", colors=RE_COLOR, labelsize=TICK_SIZE)
    ax.tick_params(axis="y", colors=IM_COLOR, labelsize=TICK_SIZE)
    save_figure(fig, "11_complex_phasor_at_t0.png")


def export_complex_signal_helix(context):
    time_values = context["time_values"]
    analytic_signal = context["analytic_signal"]
    real_values = np.real(analytic_signal)
    imag_values = np.imag(analytic_signal)
    sample_index = int(np.argmin(np.abs(time_values - SNAPSHOT_TIME)))

    fig = plt.figure(figsize=HELIX_FIGSIZE, facecolor="white")
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(1.0)
    fig.subplots_adjust(left=0.04, right=0.86, bottom=0.08, top=0.90)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")
    ax.set_box_aspect((3.9, 1.55, 1.55))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 1.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 1.0))

    ax.plot(time_values, real_values, imag_values, color=HELIX_SUM_COLOR, lw=2.8)
    ax.plot(time_values, real_values, np.zeros_like(time_values), color=RE_COLOR, lw=1.7, alpha=0.8)
    ax.plot(time_values, np.zeros_like(time_values), imag_values, color=IM_COLOR, lw=1.7, alpha=0.8)
    ax.scatter([time_values[sample_index]], [real_values[sample_index]], [imag_values[sample_index]], color=MARKER_COLOR, s=50)
    ax.plot(
        [time_values[sample_index], time_values[sample_index]],
        [real_values[sample_index], real_values[sample_index]],
        [0.0, imag_values[sample_index]],
        color=IM_COLOR,
        lw=1.6,
        alpha=0.9,
    )
    ax.plot(
        [time_values[sample_index], time_values[sample_index]],
        [0.0, real_values[sample_index]],
        [imag_values[sample_index], imag_values[sample_index]],
        color=RE_COLOR,
        lw=1.6,
        alpha=0.9,
    )
    ax.set_xlim(time_values[0], time_values[-1])
    ax.set_ylim(-context["complex_limit"], context["complex_limit"])
    ax.set_zlim(-context["complex_limit"], context["complex_limit"])
    component_tick_extent = np.floor(context["complex_limit"])
    component_ticks = np.arange(-component_tick_extent, component_tick_extent + 0.5, 1.0)
    ax.set_yticks(component_ticks)
    ax.set_zticks(component_ticks)
    ax.yaxis.set_major_locator(MultipleLocator(1.0))
    ax.zaxis.set_major_locator(MultipleLocator(1.0))
    ax.set_xlabel("Time t [s]", fontsize=HELIX_LABEL_SIZE, labelpad=22)
    ax.set_ylabel(r"Re$\{x_+(t)\}$", fontsize=HELIX_LABEL_SIZE, color=RE_COLOR, labelpad=18)
    ax.set_zlabel(r"Im$\{x_+(t)\}$", fontsize=HELIX_LABEL_SIZE, color=IM_COLOR, labelpad=18)
    ax.set_title("Complex signal from the one-sided spectrum", y=0.92, pad=-6, fontsize=HELIX_TITLE_SIZE)
    ax.tick_params(axis="x", labelsize=HELIX_TICK_SIZE, pad=4)
    ax.tick_params(axis="y", labelsize=HELIX_TICK_SIZE, colors=RE_COLOR, pad=4)
    ax.tick_params(axis="z", labelsize=HELIX_TICK_SIZE, colors=IM_COLOR, pad=4)
    ax.view_init(elev=24, azim=-62)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUTPUT_DIR / HELIX_PNG_NAME
    gif_path = OUTPUT_DIR / HELIX_GIF_NAME
    fig.savefig(png_path, dpi=DPI, facecolor="white", edgecolor="white")
    plt.close(fig)

    helix_image = Image.open(png_path).convert("RGB")
    helix_image.save(gif_path, save_all=True, loop=0, duration=1000)


def export_signal_sample(context):
    time_values = context["time_values"]
    reconstructed = context["reconstructed_signal"]
    sample_index = int(np.argmin(np.abs(time_values - SNAPSHOT_TIME)))
    sample_value = reconstructed[sample_index]

    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    ax.plot(time_values, reconstructed, color=SIGNAL_COLOR, lw=2.5)
    ax.plot([SNAPSHOT_TIME, SNAPSHOT_TIME], [0.0, sample_value], color=MARKER_COLOR, lw=2.2)
    ax.plot([SNAPSHOT_TIME], [sample_value], "o", color=MARKER_COLOR, ms=9)
    finalize_time_axis(
        ax,
        f"Real signal value from the one-sided spectrum at t = {SNAPSHOT_TIME:.2f} s",
        time_values,
        (-context["signal_limit"], context["signal_limit"]),
    )
    save_figure(fig, "13_signal_sample_from_one_sided_inverse.png")


def export_reconstructed_signal(context):
    fig, ax = plt.subplots(figsize=TIME_FIGSIZE)
    ax.plot(
        context["time_values"],
        context["observed_signal"],
        color=OBSERVED_COLOR,
        lw=2.2,
        alpha=0.65,
        label="Original signal",
    )
    ax.plot(
        context["time_values"],
        context["reconstructed_signal"],
        color=MARKER_COLOR,
        lw=2.6,
        label="One-sided reconstruction",
    )
    finalize_time_axis(
        ax,
        "Original signal and one-sided reconstruction",
        context["time_values"],
        (-context["signal_limit"], context["signal_limit"]),
    )
    ax.legend(loc="upper right", fontsize=12, framealpha=0.95)
    save_figure(fig, "14_reconstructed_signal.png")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in OUTPUT_DIR.glob("*.png"):
        old_png.unlink()

    context = build_context()
    export_one_sided_magnitude(context)
    export_one_sided_phase(context)
    export_weight_overlay(
        context,
        weight_key="real_weight_without_phase_full",
        color=RE_COLOR,
        title=f"One-sided magnitude with cos(2pi f t_0) at t = {SNAPSHOT_TIME:.2f} s",
        right_label=r"$\cos(2\pi f t_0)$",
        filename="03_real_weighting_without_phase_overlay_at_t0.png",
        discrete_weight=False,
    )
    export_weight_overlay(
        context,
        weight_key="real_weight_full",
        color=RE_COLOR,
        title=f"One-sided magnitude with real weighting at t = {SNAPSHOT_TIME:.2f} s",
        right_label=r"$\cos(2\pi f t_0 + \angle X_+(f))$",
        filename="04_real_weighting_overlay_at_t0.png",
        discrete_weight=True,
        draw_weight_zero_line=True,
        continuous_weight_key="real_weight_without_phase_full",
        continuous_weight_label=r"$\cos(2\pi f t_0)$",
    )
    export_weighted_spectrum(
        context,
        values_key="real_weighted_spectrum_full",
        color=RE_COLOR,
        title=f"One-sided real weighted spectrum at t = {SNAPSHOT_TIME:.2f} s",
        ylabel=r"$|X_+(f)|\cos(2\pi f t_0 + \angle X_+(f))$",
        filename="05_real_weighted_spectrum_at_t0.png",
        with_integral_line=False,
        integral_value=context["snapshot_real"],
    )
    export_weighted_spectrum(
        context,
        values_key="real_weighted_spectrum_full",
        color=RE_COLOR,
        title=f"One-sided real weighted spectrum at t = {SNAPSHOT_TIME:.2f} s",
        ylabel=r"$|X_+(f)|\cos(2\pi f t_0 + \angle X_+(f))$",
        filename="06_real_weighted_spectrum_with_integral_at_t0.png",
        with_integral_line=True,
        integral_value=context["snapshot_real"],
    )
    export_weight_overlay(
        context,
        weight_key="imag_weight_without_phase_full",
        color=IM_COLOR,
        title=f"One-sided magnitude with sin(2pi f t_0) at t = {SNAPSHOT_TIME:.2f} s",
        right_label=r"$\sin(2\pi f t_0)$",
        filename="07_imag_weighting_without_phase_overlay_at_t0.png",
        discrete_weight=False,
    )
    export_weight_overlay(
        context,
        weight_key="imag_weight_full",
        color=IM_COLOR,
        title=f"One-sided magnitude with imaginary weighting at t = {SNAPSHOT_TIME:.2f} s",
        right_label=r"$\sin(2\pi f t_0 + \angle X_+(f))$",
        filename="08_imag_weighting_overlay_at_t0.png",
        discrete_weight=True,
        draw_weight_zero_line=True,
        continuous_weight_key="imag_weight_without_phase_full",
        continuous_weight_label=r"$\sin(2\pi f t_0)$",
    )
    export_weighted_spectrum(
        context,
        values_key="imag_weighted_spectrum_full",
        color=IM_COLOR,
        title=f"One-sided imaginary weighted spectrum at t = {SNAPSHOT_TIME:.2f} s",
        ylabel=r"$|X_+(f)|\sin(2\pi f t_0 + \angle X_+(f))$",
        filename="09_imag_weighted_spectrum_at_t0.png",
        with_integral_line=False,
        integral_value=context["snapshot_imag"],
    )
    export_weighted_spectrum(
        context,
        values_key="imag_weighted_spectrum_full",
        color=IM_COLOR,
        title=f"One-sided imaginary weighted spectrum at t = {SNAPSHOT_TIME:.2f} s",
        ylabel=r"$|X_+(f)|\sin(2\pi f t_0 + \angle X_+(f))$",
        filename="10_imag_weighted_spectrum_with_integral_at_t0.png",
        with_integral_line=True,
        integral_value=context["snapshot_imag"],
    )
    export_complex_phasor(context)
    export_complex_signal_helix(context)
    export_signal_sample(context)
    export_reconstructed_signal(context)
    print(f"One-sided inverse storyboard exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()


