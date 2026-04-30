from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import fourier_phasor_core as core
import storyboard_paths as paths


PROBE_FREQUENCIES = (0.0, 0.5, 2.0, 3.0, 5.0)
OUTPUT_ROOT = paths.FOURIER_PROBE_SERIES_DIR
DPI = 200
TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17


def freq_slug(value):
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return text.replace(".", "p")


def freq_text(value):
    return f"{value:.1f}".rstrip("0").rstrip(".")


def prepare_context():
    obs_duration = core.DEFAULT_OBS_DURATION
    window_start, window_end = core.observed_limits(obs_duration)
    sample_count = int(obs_duration * core.FS)
    time_values = np.linspace(window_start, window_end, sample_count, endpoint=False)

    signal_values, signal_label = core.build_selectable_signal(
        time_values, "Mixed signal", core.DEFAULT_SIGNAL_FREQ
    )
    ideal_line_spectrum = core.build_ideal_positive_frequency_spectrum(
        core.selectable_signal_components("Mixed signal", core.DEFAULT_SIGNAL_FREQ)
    )
    ideal_line_freqs = np.array(sorted(ideal_line_spectrum), dtype=float)
    ideal_line_coeffs = np.array([ideal_line_spectrum[freq] for freq in ideal_line_freqs], dtype=complex)
    window_values = core.build_window(time_values, obs_duration, core.DEFAULT_WINDOW_MODE)

    probe_results = {}
    max_product = 0.0
    max_integral = 0.0
    max_complex = np.max(np.abs(ideal_line_coeffs)) if ideal_line_coeffs.size else 1.0

    for probe_freq in PROBE_FREQUENCIES:
        (
            signal_plot,
            _window_plot,
            basis_real_plot,
            basis_imag_plot,
            real_product_plot,
            imag_product_plot,
            real_integral,
            imag_integral,
            coefficient,
        ) = core.evaluate_frequency(
            probe_freq,
            time_values,
            signal_values,
            window_values,
            obs_duration,
            core.NORMALIZE_BY_WINDOW,
        )

        ideal_coefficient = core.lookup_discrete_spectrum_coefficient(ideal_line_spectrum, probe_freq)

        probe_results[probe_freq] = {
            "signal_plot": signal_plot,
            "basis_real_plot": basis_real_plot,
            "basis_imag_plot": basis_imag_plot,
            "real_product_plot": real_product_plot,
            "imag_product_plot": imag_product_plot,
            "real_integral": real_integral,
            "imag_integral": imag_integral,
            "coefficient": coefficient,
            "ideal_coefficient": ideal_coefficient,
        }

        max_product = max(
            max_product,
            np.nanmax(np.abs(real_product_plot)),
            np.nanmax(np.abs(imag_product_plot)),
        )
        max_integral = max(max_integral, abs(real_integral), abs(imag_integral))
        max_complex = max(max_complex, abs(ideal_coefficient.real), abs(ideal_coefficient.imag))

    return {
        "obs_duration": obs_duration,
        "window_start": window_start,
        "window_end": window_end,
        "time_values": time_values,
        "signal_values": signal_values,
        "signal_label": signal_label,
        "window_values": window_values,
        "ideal_line_freqs": ideal_line_freqs,
        "ideal_line_coeffs": ideal_line_coeffs,
        "probe_results": probe_results,
        "signal_limit": 1.15 * max(1.0, np.max(np.abs(signal_values))),
        "product_limit": 1.15 * max(1.0, max_product),
        "integral_limit": 1.15 * max(1.0, max(max_product, max_integral)),
        "complex_limit": 1.15 * max(1.0, max_complex),
        "spectrum_limit": 1.15 * max(1.0, np.max(np.abs(ideal_line_coeffs))),
    }


def finalize_time_axis(ax, title, x_limits, y_limits, y_label):
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def save_figure(fig, target_path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def export_signal_plot(context, output_dir, probe_freq):
    fig, ax = plt.subplots(figsize=(12.0, 4.4))
    ax.plot(context["time_values"], context["signal_values"], color="0.10", lw=2.2)
    finalize_time_axis(
        ax,
        f"Mixed signal x(t) for f_probe = {freq_text(probe_freq)} Hz",
        (context["window_start"], context["window_end"]),
        (-context["signal_limit"], context["signal_limit"]),
        "Amplitude",
    )
    save_figure(fig, output_dir / "01_mixed_signal.png")


def export_basis_plot(context, output_dir, probe_freq, basis_values, color, title_prefix, filename):
    fig, ax = plt.subplots(figsize=(12.0, 4.4))
    ax.plot(context["time_values"], context["signal_values"], color="0.10", lw=2.2)
    ax.plot(context["time_values"], basis_values, color=color, lw=1.9, ls="--")
    finalize_time_axis(
        ax,
        f"{title_prefix} at {freq_text(probe_freq)} Hz",
        (context["window_start"], context["window_end"]),
        (-context["signal_limit"], context["signal_limit"]),
        "Amplitude",
    )
    save_figure(fig, output_dir / filename)


def export_product_plot(context, output_dir, probe_freq, probe_data, part_name, color, title_prefix, filename):
    if part_name == "real":
        product = probe_data["real_product_plot"]
        ylabel = r"$x(t)\cos(2\pi f t)$"
    else:
        product = probe_data["imag_product_plot"]
        ylabel = r"$x(t)(-\sin(2\pi f t))$"

    fig, ax = plt.subplots(figsize=(12.0, 4.4))
    ax.plot(context["time_values"], product, color=color, lw=2.2)
    finalize_time_axis(
        ax,
        f"{title_prefix} for f_probe = {freq_text(probe_freq)} Hz",
        (context["window_start"], context["window_end"]),
        (-context["product_limit"], context["product_limit"]),
        ylabel,
    )
    save_figure(fig, output_dir / filename)


def export_integral_plot(
    context, output_dir, probe_freq, product, integral_value, color, ylabel, title_prefix, filename
):
    fig, ax = plt.subplots(figsize=(12.0, 4.4))
    ax.plot(context["time_values"], product, color=color, lw=2.1)
    ax.fill_between(
        context["time_values"],
        0.0,
        product,
        where=product >= 0.0,
        color=color,
        alpha=0.22,
        interpolate=True,
    )
    ax.fill_between(
        context["time_values"],
        0.0,
        product,
        where=product < 0.0,
        color="tab:red",
        alpha=0.16,
        interpolate=True,
    )
    ax.plot(
        [context["window_start"], context["window_end"]],
        [integral_value, integral_value],
        color=color,
        lw=2.0,
        ls="--",
    )
    finalize_time_axis(
        ax,
        f"{title_prefix} for f_probe = {freq_text(probe_freq)} Hz",
        (context["window_start"], context["window_end"]),
        (-context["integral_limit"], context["integral_limit"]),
        ylabel,
    )
    save_figure(fig, output_dir / filename)


def export_phasor_plot(context, output_dir, probe_freq, probe_data):
    coefficient = probe_data["ideal_coefficient"]
    phasor_title_size = TITLE_SIZE + 2
    phasor_label_size = LABEL_SIZE + 2
    phasor_tick_size = TICK_SIZE + 2

    fig, ax = plt.subplots(figsize=(6.8, 6.8))
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.axvline(0.0, color="0.75", lw=0.9)
    ax.plot([0.0, coefficient.real], [0.0, coefficient.imag], color="crimson", lw=3.0)
    ax.plot([coefficient.real], [coefficient.imag], "o", color="crimson", ms=8)
    ax.plot([0.0, coefficient.real], [0.0, 0.0], color="tab:blue", lw=1.5, alpha=0.85)
    ax.plot([coefficient.real, coefficient.real], [0.0, coefficient.imag], color="tab:orange", lw=1.5, alpha=0.85)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-context["complex_limit"], context["complex_limit"])
    ax.set_ylim(-context["complex_limit"], context["complex_limit"])
    ax.grid(alpha=0.22)
    ax.set_xlabel(r"Re$\{X(f)\}$", fontsize=phasor_label_size, color="tab:blue")
    ax.set_ylabel(r"Im$\{X(f)\}$", fontsize=phasor_label_size, color="tab:orange")
    ax.set_title(f"Complex phasor for f_probe = {freq_text(probe_freq)} Hz", pad=10, fontsize=phasor_title_size)
    ax.tick_params(axis="x", colors="tab:blue", labelsize=phasor_tick_size)
    ax.tick_params(axis="y", colors="tab:orange", labelsize=phasor_tick_size)
    save_figure(fig, output_dir / "08_complex_phasor.png")


def draw_ideal_magnitude_spectrum(ax, context):
    magnitudes = np.abs(context["ideal_line_coeffs"])
    ax.vlines(context["ideal_line_freqs"], 0.0, magnitudes, color="0.5", lw=2.4)
    ax.plot(context["ideal_line_freqs"], magnitudes, "o", color="0.5", ms=7)


def draw_ideal_phase_spectrum(ax, context):
    phases_deg = np.degrees(np.angle(context["ideal_line_coeffs"]))
    ax.vlines(context["ideal_line_freqs"], 0.0, phases_deg, color="0.5", lw=2.4)
    ax.plot(context["ideal_line_freqs"], phases_deg, "o", color="0.5", ms=7)


def export_spectrum_plot(context, output_dir, probe_freq, probe_data):
    magnitude = abs(probe_data["ideal_coefficient"])

    fig, ax = plt.subplots(figsize=(11.0, 4.8))
    draw_ideal_magnitude_spectrum(ax, context)
    ax.vlines(probe_freq, 0.0, magnitude, color="crimson", lw=2.5)
    ax.plot([probe_freq], [magnitude], "o", color="crimson", ms=8)
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(core.FREQ_MIN, core.FREQ_MAX)
    ax.set_ylim(0.0, context["spectrum_limit"])
    ax.grid(alpha=0.25)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|X(f)|$", fontsize=LABEL_SIZE)
    ax.set_title(f"Magnitude spectrum for f_probe = {freq_text(probe_freq)} Hz", pad=10, fontsize=TITLE_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    save_figure(fig, output_dir / "09_magnitude_spectrum.png")


def export_phase_plot(context, output_dir, probe_freq, probe_data):
    phase_value = np.degrees(np.angle(probe_data["ideal_coefficient"]))

    fig, ax = plt.subplots(figsize=(11.0, 4.8))
    draw_ideal_phase_spectrum(ax, context)
    ax.vlines(probe_freq, 0.0, phase_value, color="crimson", lw=2.5)
    ax.plot([probe_freq], [phase_value], "o", color="crimson", ms=8)
    ax.axhline(0.0, color="0.75", lw=0.9)
    ax.set_xlim(core.FREQ_MIN, core.FREQ_MAX)
    ax.set_ylim(-190.0, 190.0)
    ax.grid(alpha=0.25)
    ax.set_xlabel("Frequency f [Hz]", fontsize=LABEL_SIZE)
    ax.set_ylabel("Phase [deg]", fontsize=LABEL_SIZE)
    ax.set_title(f"Phase spectrum for f_probe = {freq_text(probe_freq)} Hz", pad=10, fontsize=TITLE_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)
    save_figure(fig, output_dir / "10_phase_spectrum.png")


def export_frequency_series(context, probe_freq):
    probe_data = context["probe_results"][probe_freq]
    output_dir = paths.fourier_probe_dir(freq_slug(probe_freq))
    output_dir.mkdir(parents=True, exist_ok=True)
    for old_png in output_dir.glob("*.png"):
        old_png.unlink()

    export_signal_plot(context, output_dir, probe_freq)
    export_basis_plot(
        context,
        output_dir,
        probe_freq,
        probe_data["basis_real_plot"],
        "tab:blue",
        "Signal with cos(2pi f t)",
        "02_signal_with_cos.png",
    )
    export_basis_plot(
        context,
        output_dir,
        probe_freq,
        probe_data["basis_imag_plot"],
        "tab:orange",
        "Signal with -sin(2pi f t)",
        "03_signal_with_minus_sin.png",
    )
    export_product_plot(
        context,
        output_dir,
        probe_freq,
        probe_data,
        part_name="real",
        color="tab:blue",
        title_prefix="Product x(t) cos(2pi f t)",
        filename="04_product_cos.png",
    )
    export_product_plot(
        context,
        output_dir,
        probe_freq,
        probe_data,
        part_name="imag",
        color="tab:orange",
        title_prefix="Product x(t) (-sin(2pi f t))",
        filename="05_product_minus_sin.png",
    )
    export_integral_plot(
        context,
        output_dir,
        probe_freq,
        probe_data["real_product_plot"],
        probe_data["real_integral"],
        "tab:blue",
        r"$x(t)\cos(2\pi f t)$",
        "Integral of x(t) cos(2pi f t)",
        "06_integral_cos.png",
    )
    export_integral_plot(
        context,
        output_dir,
        probe_freq,
        probe_data["imag_product_plot"],
        probe_data["imag_integral"],
        "tab:orange",
        r"$x(t)(-\sin(2\pi f t))$",
        "Integral of x(t) (-sin(2pi f t))",
        "07_integral_minus_sin.png",
    )
    export_phasor_plot(context, output_dir, probe_freq, probe_data)
    export_spectrum_plot(context, output_dir, probe_freq, probe_data)
    export_phase_plot(context, output_dir, probe_freq, probe_data)


def main():
    context = prepare_context()
    for probe_freq in PROBE_FREQUENCIES:
        export_frequency_series(context, probe_freq)
    print(f"PNG storyboard exported to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()


