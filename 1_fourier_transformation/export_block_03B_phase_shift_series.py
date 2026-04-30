from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

import storyboard_paths as paths


OUTPUT_DIR = paths.PHASE_SHIFT_SERIES_DIR
FPS = 12
FRAMES = 120
OMEGA = 1.0
F0_HZ = OMEGA / (2.0 * np.pi)
T_START = 0.0
T_END = 4.0 * np.pi
FIG_DPI = 120
SPECTRUM_DPI = 220
FIGSIZE = (14.4, 7.8)
SPECTRUM_FIGSIZE = (12.4, 12.8)
TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12
SUPTITLE_SIZE = 24
SPEC_TITLE_SIZE = 24
SPEC_LABEL_SIZE = 20
SPEC_TICK_SIZE = 17
POS_COLOR = "tab:purple"
NEG_COLOR = "#26a043"
SUM_COLOR = "tab:blue"
REFERENCE_COLOR = "0.65"
PHASE_PLOT_COLOR = "tab:blue"
PHASOR_PHASE_COLOR = "tab:blue"
MARKER_COLOR = "tab:red"
BASELINE_COLOR = "0.75"
GRID_ALPHA = 0.18
POINT_SIZE = 10
STEM_LINEWIDTH = 3.2


CASES = [
    {
        "prefix": "01",
        "slug": "phi_0",
        "mode": "constant",
        "phi": 0.0,
        "phase_title": r"Phase over time: $\varphi(t)=0^\circ$",
        "suptitle": r"Constant phase offset in $x(t)=\cos(\omega t)$",
        "signal_label": r"$\cos(\omega t)$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t)$",
        "show_reference": False,
    },
    {
        "prefix": "04",
        "slug": "phi_minus_45",
        "mode": "constant",
        "phi": -np.pi / 4.0,
        "phase_title": r"Phase over time: $\varphi(t)=-45^\circ$",
        "suptitle": r"Constant phase offset in $x(t)=\cos(\omega t-45^\circ)$",
        "signal_label": r"$\cos(\omega t-45^\circ)$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t-45^\circ)$",
    },
    {
        "prefix": "07",
        "slug": "phi_minus_90",
        "mode": "constant",
        "phi": -np.pi / 2.0,
        "phase_title": r"Phase over time: $\varphi(t)=-90^\circ$",
        "suptitle": r"Constant phase offset in $x(t)=\cos(\omega t-90^\circ)$",
        "signal_label": r"$\cos(\omega t-90^\circ)$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t-90^\circ)$",
    },
    {
        "prefix": "10",
        "slug": "phi_plus_45_from_inverse_ft",
        "mode": "constant",
        "phi": np.pi / 4.0,
        "phase_title": r"Phase over time: $\varphi(t)=+45^\circ$",
        "suptitle": r"Phase from inverse FT spectrum: $x(t)=\cos(\omega t+45^\circ)$",
        "signal_label": r"$\cos(\omega t+45^\circ)$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t+45^\circ)$",
    },
    {
        "prefix": "13",
        "slug": "phi_variable_sine",
        "mode": "variable",
        "phi_amplitude": np.pi / 2.0,
        "phi_omega": 0.5,
        "spectrum_period": 4.0 * np.pi,
        "spectrum_x_limits": (-1.0, 1.0),
        "spectrum_phase_threshold": 0.01,
        "phase_title": r"Phase over time: $\varphi(t)=90^\circ\sin(0.5t)$",
        "suptitle": r"Time-varying phase in $x(t)=\cos(\omega t+\varphi(t))$",
        "signal_label": r"$\cos(\omega t+\varphi(t))$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t+\varphi(t))$",
    },
]


def phase_values(case, t):
    if case["mode"] == "constant":
        return np.full_like(np.asarray(t, dtype=float), case["phi"], dtype=float)
    return case["phi_amplitude"] * np.sin(case["phi_omega"] * np.asarray(t, dtype=float))


def format_phase_deg(value_deg):
    rounded = int(np.round(value_deg))
    return f"{rounded:+d}^\\circ"


def build_data(case):
    time_dense = np.linspace(T_START, T_END, 1200)
    time_frames = np.linspace(T_START, T_END, FRAMES, endpoint=False)

    phi_dense = phase_values(case, time_dense)
    z_pos_dense = 0.5 * np.exp(1j * (OMEGA * time_dense + phi_dense))
    z_neg_dense = 0.5 * np.exp(-1j * (OMEGA * time_dense + phi_dense))
    z_sum_dense = z_pos_dense + z_neg_dense
    reference_signal = np.cos(OMEGA * time_dense)
    shifted_signal = np.cos(OMEGA * time_dense + phi_dense)
    phi_deg = np.degrees(phi_dense)
    return {
        "time_dense": time_dense,
        "time_frames": time_frames,
        "z_pos_dense": z_pos_dense,
        "z_neg_dense": z_neg_dense,
        "z_sum_dense": z_sum_dense,
        "reference_signal": reference_signal,
        "shifted_signal": shifted_signal,
        "phi_deg": phi_deg,
    }


def setup_complex_axis(ax):
    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.86", lw=2.0)
    ax.axhline(0.0, color="0.78", lw=0.9)
    ax.axvline(0.0, color="0.78", lw=0.9)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=GRID_ALPHA)
    ax.set_xlabel(r"Re$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Im$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def create_overview_figure(case):
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 0.68])
    ax_complex = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_phi = fig.add_subplot(grid[1, 1], sharex=ax_signal)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24, hspace=0.22)
    fig.suptitle(case["suptitle"], fontsize=SUPTITLE_SIZE, y=0.965)
    return fig, ax_complex, ax_signal, ax_phi


def draw_background(case, data, ax_complex, ax_signal, ax_phi):
    setup_complex_axis(ax_complex)
    ax_complex.set_title("Phasor sum", pad=12, fontsize=TITLE_SIZE)

    show_reference = case.get("show_reference", True)
    time_dense = data["time_dense"]
    if show_reference:
        ax_signal.plot(
            time_dense,
            data["reference_signal"],
            color=REFERENCE_COLOR,
            lw=2.0,
            label=r"$\cos(\omega t)$",
        )
    ax_signal.plot(time_dense, data["shifted_signal"], color=SUM_COLOR, lw=2.7, label=case["signal_label"])
    ax_signal.axhline(0.0, color="0.78", lw=0.9)
    ax_signal.grid(alpha=GRID_ALPHA)
    ax_signal.set_xlim(T_START, T_END)
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_title("Time signal", pad=10, fontsize=TITLE_SIZE)
    ax_signal.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax_signal.tick_params(labelsize=TICK_SIZE)
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    linestyle = "--"
    ax_phi.plot(time_dense, data["phi_deg"], color=PHASE_PLOT_COLOR, lw=2.5, ls=linestyle)
    ax_phi.axhline(0.0, color="0.78", lw=0.9)
    ax_phi.grid(alpha=GRID_ALPHA)
    ax_phi.set_xlim(T_START, T_END)
    ax_phi.set_ylim(-180.0, 180.0)
    ax_phi.set_yticks([-180.0, -90.0, 0.0, 90.0, 180.0])
    ax_phi.set_title(case["phase_title"], pad=10, fontsize=TITLE_SIZE)
    ax_phi.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax_phi.set_ylabel(r"$\varphi$ [deg]", fontsize=LABEL_SIZE)
    ax_phi.tick_params(labelsize=TICK_SIZE)


def build_overview_animation(case, data):
    fig, ax_complex, ax_signal, ax_phi = create_overview_figure(case)
    draw_background(case, data, ax_complex, ax_signal, ax_phi)

    show_reference = case.get("show_reference", True)
    if show_reference:
        reference_line, = ax_complex.plot([], [], color=REFERENCE_COLOR, lw=2.5, label=r"$\cos(\omega t)$")
        reference_tip, = ax_complex.plot([], [], "o", color=REFERENCE_COLOR, ms=6.5)
    else:
        reference_line = None
        reference_tip = None
    pos_line, = ax_complex.plot([], [], color=POS_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{j(\omega t+\varphi(t))}$")
    neg_line, = ax_complex.plot([], [], color=NEG_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{-j(\omega t+\varphi(t))}$")
    sum_line, = ax_complex.plot([], [], color=SUM_COLOR, lw=2.9, label=r"$x(t)$")
    pos_tip, = ax_complex.plot([], [], "o", color=POS_COLOR, ms=7)
    neg_tip, = ax_complex.plot([], [], "o", color=NEG_COLOR, ms=7)
    sum_tip, = ax_complex.plot([], [], "o", color=SUM_COLOR, ms=7)
    phase_arc, = ax_complex.plot([], [], color=PHASOR_PHASE_COLOR, lw=2.0)
    phase_text = ax_complex.text(-0.15, -0.24, "", color=PHASOR_PHASE_COLOR, fontsize=13)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    time_marker_signal = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_signal_point, = ax_signal.plot([], [], "o", color=MARKER_COLOR, ms=8)
    time_marker_phi = ax_phi.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_phi_point, = ax_phi.plot([], [], "o", color=MARKER_COLOR, ms=8)

    def draw_state(current_t):
        current_phi = float(phase_values(case, np.array([current_t]))[0])
        if show_reference:
            reference_value = 0.5 * np.exp(1j * OMEGA * current_t)
        z_pos = 0.5 * np.exp(1j * (OMEGA * current_t + current_phi))
        z_neg = 0.5 * np.exp(-1j * (OMEGA * current_t + current_phi))
        z_sum = z_pos + z_neg
        signal_value = np.cos(OMEGA * current_t + current_phi)
        phi_value_deg = np.degrees(current_phi)

        artists = []
        if show_reference:
            reference_line.set_data([0.0, reference_value.real], [0.0, reference_value.imag])
            reference_tip.set_data([reference_value.real], [reference_value.imag])
            artists.extend([reference_line, reference_tip])
        pos_line.set_data([0.0, z_pos.real], [0.0, z_pos.imag])
        neg_line.set_data([0.0, z_neg.real], [0.0, z_neg.imag])
        sum_line.set_data([0.0, z_sum.real], [0.0, 0.0])
        pos_tip.set_data([z_pos.real], [z_pos.imag])
        neg_tip.set_data([z_neg.real], [z_neg.imag])
        sum_tip.set_data([z_sum.real], [0.0])

        theta = np.linspace(OMEGA * current_t, OMEGA * current_t + current_phi, 100)
        phase_arc.set_data(0.32 * np.cos(theta), 0.32 * np.sin(theta))
        phase_text.set_text(fr"$\varphi={format_phase_deg(phi_value_deg)}$")

        time_marker_signal.set_xdata([current_t, current_t])
        moving_signal_point.set_data([current_t], [signal_value])
        time_marker_phi.set_xdata([current_t, current_t])
        moving_phi_point.set_data([current_t], [phi_value_deg])

        artists.extend([
            pos_line,
            neg_line,
            sum_line,
            pos_tip,
            neg_tip,
            sum_tip,
            phase_arc,
            phase_text,
            time_marker_signal,
            moving_signal_point,
            time_marker_phi,
            moving_phi_point,
        ])
        return tuple(artists)

    def update(frame_index):
        return draw_state(data["time_frames"][frame_index])

    animation = FuncAnimation(fig, update, frames=len(data["time_frames"]), interval=1000 / FPS, blit=False)
    return fig, animation, draw_state

def style_time_axis(ax, title):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(T_START, T_END)
    ax.set_ylim(-1.15, 1.15)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=SPEC_TITLE_SIZE)
    ax.set_xlabel("Time t [s]", fontsize=SPEC_LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=SPEC_LABEL_SIZE)
    ax.tick_params(labelsize=SPEC_TICK_SIZE)


def style_frequency_axis(ax, title, y_limits, y_label, x_limits=(-0.8, 0.8)):
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    ax.grid(alpha=0.25)
    ax.set_title(title, pad=10, fontsize=SPEC_TITLE_SIZE)
    ax.set_xlabel("Frequency f [Hz]", fontsize=SPEC_LABEL_SIZE)
    ax.set_ylabel(y_label, fontsize=SPEC_LABEL_SIZE)
    ax.tick_params(labelsize=SPEC_TICK_SIZE)


def plot_line_spectrum(ax, freqs, values, colors, y_limits, y_label, title):
    for frequency_hz, value, color in zip(freqs, values, colors):
        ax.vlines(frequency_hz, 0.0, value, color=color, lw=STEM_LINEWIDTH)
        ax.plot([frequency_hz], [value], "o", color=color, ms=POINT_SIZE)
    style_frequency_axis(ax, title, y_limits, y_label)


def compute_ideal_variable_line_spectrum(case):
    period = case.get("spectrum_period", T_END - T_START)
    x_limits = case.get("spectrum_x_limits", (-1.0, 1.0))
    phase_threshold = case.get("spectrum_phase_threshold", 0.01)
    max_frequency_hz = max(abs(x_limits[0]), abs(x_limits[1]))
    harmonic_limit = int(np.floor(max_frequency_hz * period + 1e-12))
    harmonic_indices = np.arange(-harmonic_limit, harmonic_limit + 1)
    freqs_hz = harmonic_indices / period

    sample_count = max(32768, int(np.ceil(period * 800.0)))
    time_period = np.linspace(0.0, period, sample_count, endpoint=False)
    phi_var = phase_values(case, time_period)
    signal_var = np.cos(OMEGA * time_period + phi_var)

    coefficients = []
    for frequency_hz in freqs_hz:
        basis = np.exp(-1j * 2.0 * np.pi * frequency_hz * time_period)
        coefficient = np.trapezoid(signal_var * basis, x=time_period) / period
        coefficients.append(coefficient)

    coefficients = np.asarray(coefficients, dtype=complex)
    magnitude = np.abs(coefficients)
    phase_deg = np.degrees(np.angle(coefficients))
    phase_deg = np.where(magnitude > phase_threshold * np.max(magnitude), phase_deg, np.nan)
    colors = np.where(freqs_hz < 0.0, NEG_COLOR, POS_COLOR)
    colors = np.where(freqs_hz == 0.0, SUM_COLOR, colors)

    return {
        "time_period": time_period,
        "signal_period": signal_var,
        "freqs_hz": freqs_hz,
        "magnitude": magnitude,
        "phase_deg": phase_deg,
        "colors": colors,
        "x_limits": x_limits,
    }


def save_constant_spectrum(case, data, output_path):
    phi_deg = np.degrees(case["phi"])
    spectrum_freqs = np.array([-F0_HZ, F0_HZ])
    spectrum_mags = np.array([0.5, 0.5])
    spectrum_phases = np.array([-phi_deg, phi_deg])
    colors = [NEG_COLOR, POS_COLOR]

    fig, axes = plt.subplots(3, 1, figsize=SPECTRUM_FIGSIZE, dpi=SPECTRUM_DPI)
    axes[0].plot(data["time_dense"], data["shifted_signal"], color=SUM_COLOR, lw=2.8)
    style_time_axis(axes[0], case["spectrum_signal_title"])
    plot_line_spectrum(axes[1], spectrum_freqs, spectrum_mags, colors, (0.0, 0.62), r"$|X(f)|$", "Two-sided magnitude spectrum")
    plot_line_spectrum(axes[2], spectrum_freqs, spectrum_phases, colors, (-180.0, 180.0), r"$\angle X(f)$ [deg]", "Two-sided phase spectrum")
    fig.subplots_adjust(left=0.12, right=0.96, top=0.96, bottom=0.07, hspace=0.45)
    fig.savefig(output_path, dpi=SPECTRUM_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_variable_spectrum(case, data, output_path):
    spectrum = compute_ideal_variable_line_spectrum(case)

    fig, axes = plt.subplots(3, 1, figsize=SPECTRUM_FIGSIZE, dpi=SPECTRUM_DPI)
    if case.get("spectrum_time_full", False):
        axes[0].plot(data["time_dense"], data["shifted_signal"], color=SUM_COLOR, lw=2.8)
    else:
        axes[0].plot(spectrum["time_period"], spectrum["signal_period"], color=SUM_COLOR, lw=2.8)
    style_time_axis(axes[0], case["spectrum_signal_title"])

    plot_line_spectrum(
        axes[1],
        spectrum["freqs_hz"],
        spectrum["magnitude"],
        spectrum["colors"],
        (0.0, 1.05 * np.max(spectrum["magnitude"])),
        r"$|X(f)|$",
        "Two-sided magnitude spectrum",
    )
    axes[1].set_xlim(*spectrum["x_limits"])

    plot_line_spectrum(
        axes[2],
        spectrum["freqs_hz"],
        spectrum["phase_deg"],
        spectrum["colors"],
        (-180.0, 180.0),
        r"$\angle X(f)$ [deg]",
        "Two-sided phase spectrum",
    )
    axes[2].set_xlim(*spectrum["x_limits"])

    fig.subplots_adjust(left=0.12, right=0.96, top=0.96, bottom=0.07, hspace=0.45)
    fig.savefig(output_path, dpi=SPECTRUM_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def export_case(case):
    data = build_data(case)
    overview_path = OUTPUT_DIR / f"{case['prefix']}_{case['slug']}_overview.png"
    gif_path = OUTPUT_DIR / f"{int(case['prefix']) + 1:02d}_{case['slug']}.gif"
    spectrum_path = OUTPUT_DIR / f"{int(case['prefix']) + 2:02d}_{case['slug']}_spectrum.png"

    fig, animation, draw_state = build_overview_animation(case, data)
    draw_state(data["time_frames"][0])
    fig.savefig(overview_path, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    writer = PillowWriter(fps=FPS)
    animation.save(str(gif_path.resolve()), writer=writer)
    plt.close(fig)

    if case["mode"] == "constant":
        save_constant_spectrum(case, data, spectrum_path)
    else:
        save_variable_spectrum(case, data, spectrum_path)

    return overview_path, gif_path, spectrum_path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.is_file():
            old_file.unlink()

    saved_paths = []
    for case in CASES:
        saved_paths.extend(export_case(case))

    print(f"Saved outputs to: {OUTPUT_DIR}")
    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
