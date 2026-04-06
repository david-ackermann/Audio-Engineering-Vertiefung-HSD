import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import fourier_phasor_interactive as core


@st.cache_data
def prepare_basis_arrays():
    full_window_start, full_window_end = core.full_time_limits()
    time_values = np.linspace(full_window_start, full_window_end, int(core.T_MAX * core.FS), endpoint=False)
    basis_limit = np.exp(-1j * 2.0 * np.pi * core.LIMIT_FREQS[:, None] * time_values[None, :])
    basis_fine = np.exp(-1j * 2.0 * np.pi * core.FINE_FREQS[:, None] * time_values[None, :])
    return time_values, basis_limit, basis_fine


def build_figure(signal_mode, window_mode, signal_freq, analysis_freq, obs_duration):
    time_values, basis_limit, basis_fine = prepare_basis_arrays()

    signal_values, signal_label = core.build_selectable_signal(time_values, signal_mode, signal_freq)
    window_values = core.build_window(time_values, obs_duration, window_mode)

    cache = core.compute_signal_cache(
        signal_values,
        window_values,
        time_values,
        obs_duration,
        core.NORMALIZE_BY_WINDOW,
        basis_limit,
        basis_fine,
    )
    display_cache = core.compute_display_limits(
        signal_values,
        time_values,
        core.NORMALIZE_BY_WINDOW,
        basis_limit,
        basis_fine,
    )
    (
        signal_plot,
        window_plot,
        basis_real_plot,
        basis_imag_plot,
        real_product,
        imag_product,
        real_integral,
        imag_integral,
        coefficient,
    ) = core.evaluate_frequency(
        analysis_freq,
        time_values,
        signal_values,
        window_values,
        obs_duration,
        core.NORMALIZE_BY_WINDOW,
    )

    if core.NORMALIZE_BY_WINDOW:
        formula_line_1 = r"$X_{T_{\mathrm{obs}},w}(f)=\frac{1}{T_{\mathrm{obs}}}\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)e^{-j 2 \pi f t}\,\mathrm{d}t$"
    else:
        formula_line_1 = r"$X_{T_{\mathrm{obs}},w}(f)=\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)e^{-j 2 \pi f t}\,\mathrm{d}t$"

    fig = plt.figure(figsize=(18.6, 10.6))
    grid = fig.add_gridspec(
        2,
        4,
        width_ratios=[1.0, 1.0, 1.05, 0.95],
        height_ratios=[0.88, 1.12],
    )

    ax_real_time = fig.add_subplot(grid[0, 0])
    ax_imag_time = fig.add_subplot(grid[0, 1], sharex=ax_real_time, sharey=ax_real_time)
    ax_real_prod = fig.add_subplot(grid[1, 0], sharex=ax_real_time)
    ax_imag_prod = fig.add_subplot(grid[1, 1], sharex=ax_real_time, sharey=ax_real_prod)
    ax_complex = fig.add_subplot(grid[:, 2])
    spectrum_grid = grid[:, 3].subgridspec(2, 1, hspace=0.34)
    ax_magnitude = fig.add_subplot(spectrum_grid[0, 0])
    ax_phase = fig.add_subplot(spectrum_grid[1, 0], sharex=ax_magnitude)

    fig.subplots_adjust(left=0.05, right=0.985, top=0.89, bottom=0.23, wspace=0.42, hspace=0.34)
    fig.suptitle("Fourier Analysis as a Split into Cosine and Sine Components", fontsize=15)

    window_start, window_end = core.observed_limits(obs_duration)
    signal_limit = max(display_cache["signal_limit"], 1.15)

    ax_real_time.plot(time_values, signal_plot, color="0.10", lw=2.1)
    ax_real_time.plot(time_values, window_plot, color=core.WINDOW_COLOR, lw=1.8)
    ax_real_time.plot(time_values, basis_real_plot, color="tab:blue", lw=1.8, ls="--")
    ax_real_time.axhline(0.0, color="0.75", lw=0.9)
    ax_real_time.axvline(window_start, color="0.55", lw=1.1, ls=":")
    ax_real_time.axvline(window_end, color="0.55", lw=1.1, ls=":")
    ax_real_time.set_xlim(window_start, window_end)
    ax_real_time.set_ylim(-signal_limit, signal_limit)
    ax_real_time.grid(alpha=0.25)
    ax_real_time.set_title("1a. Time domain: x(t), w(t), and cos(2pi f t)", pad=10)
    ax_real_time.set_ylabel("Amplitude")
    ax_real_time.tick_params(axis="x", labelbottom=False)

    ax_real_prod.plot(time_values, real_product, color="tab:blue", lw=2.0)
    real_integral_ax = ax_real_prod.twinx()
    real_integral_ax.plot([window_start, window_end], [real_integral, real_integral], color="tab:blue", lw=2.0, ls="--")
    ax_real_prod.fill_between(
        time_values,
        0.0,
        real_product,
        where=real_product >= 0.0,
        color="tab:blue",
        alpha=0.22,
        interpolate=True,
    )
    ax_real_prod.fill_between(
        time_values,
        0.0,
        real_product,
        where=real_product < 0.0,
        color="tab:red",
        alpha=0.18,
        interpolate=True,
    )
    ax_real_prod.axhline(0.0, color="0.75", lw=0.9)
    ax_real_prod.axvline(window_start, color="0.55", lw=1.1, ls=":")
    ax_real_prod.axvline(window_end, color="0.55", lw=1.1, ls=":")
    ax_real_prod.set_xlim(window_start, window_end)
    ax_real_prod.set_ylim(-display_cache["product_limit"], display_cache["product_limit"])
    real_integral_ax.set_ylim(-display_cache["real_integral_limit"], display_cache["real_integral_limit"])
    ax_real_prod.grid(alpha=0.25)
    ax_real_prod.set_title("1b. Windowed product and integral value", pad=10)
    ax_real_prod.set_xlabel("Time t [s]")
    ax_real_prod.set_ylabel(r"$x(t)w(t)\cos(2\pi f t)$", color="tab:blue")
    real_integral_ax.set_ylabel("Real-part integral value", color="tab:blue")
    ax_real_prod.tick_params(axis="y", colors="tab:blue")
    real_integral_ax.tick_params(axis="y", colors="tab:blue")
    real_integral_ax.patch.set_alpha(0.0)

    ax_imag_time.plot(time_values, signal_plot, color="0.10", lw=2.1)
    ax_imag_time.plot(time_values, window_plot, color=core.WINDOW_COLOR, lw=1.8)
    ax_imag_time.plot(time_values, basis_imag_plot, color="tab:orange", lw=1.8, ls="--")
    ax_imag_time.axhline(0.0, color="0.75", lw=0.9)
    ax_imag_time.axvline(window_start, color="0.55", lw=1.1, ls=":")
    ax_imag_time.axvline(window_end, color="0.55", lw=1.1, ls=":")
    ax_imag_time.set_xlim(window_start, window_end)
    ax_imag_time.set_ylim(-signal_limit, signal_limit)
    ax_imag_time.grid(alpha=0.25)
    ax_imag_time.set_title("2a. Time domain: x(t), w(t), and -sin(2pi f t)", pad=10)
    ax_imag_time.tick_params(axis="x", labelbottom=False)

    ax_imag_prod.plot(time_values, imag_product, color="tab:orange", lw=2.0)
    imag_integral_ax = ax_imag_prod.twinx()
    imag_integral_ax.plot([window_start, window_end], [imag_integral, imag_integral], color="tab:orange", lw=2.0, ls="--")
    ax_imag_prod.fill_between(
        time_values,
        0.0,
        imag_product,
        where=imag_product >= 0.0,
        color="tab:orange",
        alpha=0.24,
        interpolate=True,
    )
    ax_imag_prod.fill_between(
        time_values,
        0.0,
        imag_product,
        where=imag_product < 0.0,
        color="tab:red",
        alpha=0.18,
        interpolate=True,
    )
    ax_imag_prod.axhline(0.0, color="0.75", lw=0.9)
    ax_imag_prod.axvline(window_start, color="0.55", lw=1.1, ls=":")
    ax_imag_prod.axvline(window_end, color="0.55", lw=1.1, ls=":")
    ax_imag_prod.set_xlim(window_start, window_end)
    ax_imag_prod.set_ylim(-display_cache["product_limit"], display_cache["product_limit"])
    imag_integral_ax.set_ylim(-display_cache["imag_integral_limit"], display_cache["imag_integral_limit"])
    ax_imag_prod.grid(alpha=0.25)
    ax_imag_prod.set_title("2b. Windowed product and integral value", pad=10)
    ax_imag_prod.set_xlabel("Time t [s]")
    ax_imag_prod.set_ylabel(r"$x(t)w(t)(-\sin(2\pi f t))$", color="tab:orange")
    imag_integral_ax.set_ylabel("Imaginary-part integral value", color="tab:orange")
    ax_imag_prod.tick_params(axis="y", colors="tab:orange")
    imag_integral_ax.tick_params(axis="y", colors="tab:orange")
    imag_integral_ax.patch.set_alpha(0.0)

    ax_complex.axhline(0.0, color="0.75", lw=0.9)
    ax_complex.axvline(0.0, color="0.75", lw=0.9)
    ax_complex.plot([0.0, coefficient.real], [0.0, coefficient.imag], color="crimson", lw=3.0)
    ax_complex.plot([coefficient.real], [coefficient.imag], "o", color="crimson", ms=7)
    ax_complex.plot([0.0, coefficient.real], [0.0, 0.0], color="tab:blue", lw=1.4, alpha=0.85)
    ax_complex.plot([coefficient.real, coefficient.real], [0.0, coefficient.imag], color="tab:orange", lw=1.4, alpha=0.85)
    ax_complex.set_aspect("equal", adjustable="box")
    ax_complex.set_xlim(-display_cache["complex_limit"], display_cache["complex_limit"])
    ax_complex.set_ylim(-display_cache["complex_limit"], display_cache["complex_limit"])
    ax_complex.grid(alpha=0.22)
    ax_complex.set_xlabel(r"Re$\{X_T(f)\}$")
    ax_complex.set_ylabel(r"Im$\{X_T(f)\}$")
    ax_complex.set_title("3. Complex coefficient from both integral values", pad=10)

    complex_pos = ax_complex.get_position()

    ax_magnitude.plot(core.FINE_FREQS, cache["spectrum_fine"], color="0.25", lw=2.0)
    ax_magnitude.axvline(analysis_freq, color="tab:blue", lw=1.5, alpha=0.85)
    ax_magnitude.plot([analysis_freq], [abs(coefficient)], "o", color="crimson", ms=8)
    ax_magnitude.axhline(0.0, color="0.75", lw=0.9)
    ax_magnitude.set_xlim(core.FREQ_MIN, core.FREQ_MAX)
    ax_magnitude.set_ylim(0.0, display_cache["spectrum_limit"])
    ax_magnitude.grid(alpha=0.25)
    ax_magnitude.set_ylabel(r"$|X_T(f)|$")
    ax_magnitude.set_title("4a. Magnitude spectrum", pad=10)
    ax_magnitude.tick_params(axis="x", labelbottom=False)

    ax_phase.plot(core.FINE_FREQS, cache["phase_fine"], color="0.45", lw=1.9)
    ax_phase.axvline(analysis_freq, color="tab:blue", lw=1.5, alpha=0.85)
    ax_phase.plot([analysis_freq], [np.degrees(np.angle(coefficient))], "o", color="crimson", ms=8)
    ax_phase.axhline(0.0, color="0.75", lw=0.9)
    ax_phase.set_xlim(core.FREQ_MIN, core.FREQ_MAX)
    ax_phase.set_ylim(-190.0, 190.0)
    ax_phase.set_yticks([-180, -90, 0, 90, 180])
    ax_phase.grid(alpha=0.25)
    ax_phase.set_xlabel("Frequency f [Hz]")
    ax_phase.set_ylabel("Phase [deg]")
    ax_phase.set_title("4b. Phase spectrum", pad=10)

    result_lines = [
        "Result",
        f"X_T(f) = {core.fmt_complex(coefficient)}",
        f"|X_T(f)| = {abs(coefficient):.3f}",
        f"Phase = {np.degrees(np.angle(coefficient)):+.1f} deg",
    ]
    fig.text(
        complex_pos.x0,
        complex_pos.y0 - 0.060,
        "\n".join(result_lines),
        ha="left",
        va="top",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.92, edgecolor="0.85"),
    )

    fig.text(0.50, 0.205, formula_line_1, ha="center", fontsize=13)
    if core.NORMALIZE_BY_WINDOW:
        formula_segments = [
            (r"$=\frac{1}{T_{\mathrm{obs}}}\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)\,$", "black"),
            (r"$\cos(2\pi f t)$", "tab:blue"),
            (r"$\,\mathrm{d}t + j\,\frac{1}{T_{\mathrm{obs}}}\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)(-\,$", "black"),
            (r"$\sin(2\pi f t)$", "tab:orange"),
            (r"$)\,\mathrm{d}t$", "black"),
        ]
    else:
        formula_segments = [
            (r"$=\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)\,$", "black"),
            (r"$\cos(2\pi f t)$", "tab:blue"),
            (r"$\,\mathrm{d}t + j\int_{-T_{\mathrm{obs}}/2}^{T_{\mathrm{obs}}/2} x(t)w(t)(-\,$", "black"),
            (r"$\sin(2\pi f t)$", "tab:orange"),
            (r"$)\,\mathrm{d}t$", "black"),
        ]
    core.add_centered_formula_segments(fig, 0.177, formula_segments, fontsize=12)

    return fig, signal_label


def main():
    st.set_page_config(page_title="Fourier Phasor Explorer", layout="wide")
    st.title("Fourier Phasor Explorer")
    st.caption("Interactive Fourier analysis in the browser. No local Python setup required for students.")

    with st.sidebar:
        st.header("Controls")
        signal_mode = st.radio("Signal x(t)", core.SIGNAL_MODES, index=core.SIGNAL_MODES.index(core.DEFAULT_SIGNAL_MODE))
        window_mode = st.radio("Window w(t)", core.WINDOW_MODES, index=core.WINDOW_MODES.index(core.DEFAULT_WINDOW_MODE))
        obs_duration = st.slider(
            "Observation duration T_obs [s]",
            min_value=float(core.OBS_DURATION_MIN),
            max_value=float(core.T_MAX),
            value=float(core.DEFAULT_OBS_DURATION),
            step=float(core.SLIDER_STEP),
        )
        signal_freq = st.slider(
            "Signal frequency f_x [Hz]",
            min_value=float(core.FREQ_MIN),
            max_value=float(core.FREQ_MAX),
            value=float(core.DEFAULT_SIGNAL_FREQ),
            step=float(core.SLIDER_STEP),
        )
        analysis_freq = st.slider(
            "Probe frequency f [Hz]",
            min_value=float(core.FREQ_MIN),
            max_value=float(core.FREQ_MAX),
            value=float(core.DEFAULT_ANALYSIS_FREQ),
            step=float(core.SLIDER_STEP),
        )

        if signal_mode == "Constant":
            st.info("With x(t) = 1, the magnitude spectrum shows the spectrum of the selected window.")
        elif signal_mode not in ("Cosine", "Sine"):
            st.caption("The signal frequency slider is only used for Cosine and Sine.")

    fig, signal_label = build_figure(signal_mode, window_mode, signal_freq, analysis_freq, obs_duration)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption(signal_label)


if __name__ == "__main__":
    main()
