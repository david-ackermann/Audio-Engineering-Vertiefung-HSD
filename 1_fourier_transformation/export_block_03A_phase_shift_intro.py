from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

import storyboard_paths as paths


OUTPUT_DIR = paths.PHASE_SHIFT_INTRO_DIR
GIF_PATH = OUTPUT_DIR / "01_cosine_phase_shift_minus_45deg.gif"
OVERVIEW_PATH = OUTPUT_DIR / "00_overview.png"
VARIABLE_OVERVIEW_PATH = OUTPUT_DIR / "02_overview_time_varying_phase.png"
VARIABLE_GIF_PATH = OUTPUT_DIR / "03_time_varying_phase.gif"
SPECTRUM_OVERVIEW_PATH = OUTPUT_DIR / "04_two_sided_spectrum_overview.png"

FPS = 12
FRAMES = 120
OMEGA = 1.0
PHI = -np.pi / 4.0
PHI_VAR_AMPLITUDE = np.pi / 2.0
PHI_VAR_OMEGA = 0.5
PHI_VAR_HIGHLIGHT_T = np.pi
T_START = 0.0
T_END = 4.0 * np.pi
FIG_DPI = 120
FIGSIZE = (14.4, 7.8)
SPECTRUM_OVERVIEW_FIGSIZE = (12.4, 12.8)
SPEC_TITLE_SIZE = 24
SPEC_LABEL_SIZE = 20
SPEC_TICK_SIZE = 17
BASELINE_COLOR = "0.75"
FREQ_AXIS_LIMIT = 0.8
MAG_LINEWIDTH = 3.0
POINT_SIZE = 9
TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12
SUPTITLE_SIZE = 24
FORMULA_SIZE = 21
POS_COLOR = "tab:purple"
NEG_COLOR = "#26a043"
SUM_COLOR = "tab:blue"
REFERENCE_COLOR = "0.65"
PHASE_COLOR = "tab:purple"
PHASE_PLOT_COLOR = "tab:blue"
PHASOR_PHASE_COLOR = "tab:blue"
MARKER_COLOR = "tab:red"
GRID_ALPHA = 0.18


# cos(omega t + phi) = 1/2 * e^{j(omega t + phi)} + 1/2 * e^{-j(omega t + phi)}

def build_data():
    time_dense = np.linspace(T_START, T_END, 1200)
    time_frames = np.linspace(T_START, T_END, FRAMES)
    z_pos_dense = 0.5 * np.exp(1j * (OMEGA * time_dense + PHI))
    z_neg_dense = 0.5 * np.exp(-1j * (OMEGA * time_dense + PHI))
    z_sum_dense = z_pos_dense + z_neg_dense
    reference_signal = np.cos(OMEGA * time_dense)
    shifted_signal = np.cos(OMEGA * time_dense + PHI)
    phi_deg = np.full_like(time_dense, np.degrees(PHI))
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



def add_phase_arc(ax, radius=0.34):
    theta = np.linspace(0.0, PHI, 140)
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=PHASOR_PHASE_COLOR, lw=2.0)
    ax.text(0.22, -0.18, r"$\varphi=-45^\circ$", color=PHASOR_PHASE_COLOR, fontsize=13)




def create_figure():
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 0.68])
    ax_complex = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_phi = fig.add_subplot(grid[1, 1], sharex=ax_signal)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24, hspace=0.22)
    fig.suptitle(r"Constant phase offset in $x(t)=\cos(\omega t-45^\circ)$", fontsize=SUPTITLE_SIZE, y=0.965)
    return fig, ax_complex, ax_signal, ax_phi



def draw_static_axes(ax_complex, ax_signal, ax_phi, data):
    setup_complex_axis(ax_complex)
    ax_complex.set_title(r"Phasor sum", pad=12, fontsize=TITLE_SIZE)
    add_phase_arc(ax_complex)

    time_dense = data["time_dense"]
    ax_signal.plot(time_dense, data["reference_signal"], color=REFERENCE_COLOR, lw=2.0, label=r"$\cos(\omega t)$")
    ax_signal.plot(time_dense, data["shifted_signal"], color=SUM_COLOR, lw=2.7, label=r"$\cos(\omega t-45^\circ)$")
    ax_signal.axhline(0.0, color="0.78", lw=0.9)
    ax_signal.grid(alpha=GRID_ALPHA)
    ax_signal.set_xlim(T_START, T_END)
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_title("Time signal", pad=10, fontsize=TITLE_SIZE)
    ax_signal.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax_signal.tick_params(labelsize=TICK_SIZE)
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    ax_phi.plot(time_dense, data["phi_deg"], color=PHASE_PLOT_COLOR, lw=2.5, ls="--")
    ax_phi.axhline(0.0, color="0.78", lw=0.9)
    ax_phi.grid(alpha=GRID_ALPHA)
    ax_phi.set_xlim(T_START, T_END)
    ax_phi.set_ylim(-180.0, 180.0)
    ax_phi.set_yticks([-180.0, -90.0, 0.0, 90.0, 180.0])
    ax_phi.set_title(r"Phase over time: $\varphi(t)=-45^\circ$", pad=10, fontsize=TITLE_SIZE)
    ax_phi.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax_phi.set_ylabel(r"$\varphi$ [deg]", fontsize=LABEL_SIZE)
    ax_phi.tick_params(labelsize=TICK_SIZE)





def create_time_varying_phase_overview(data):
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 0.68])
    ax_complex = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_phi = fig.add_subplot(grid[1, 1], sharex=ax_signal)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24, hspace=0.22)
    fig.suptitle(r"Time-varying phase in $x(t)=\cos(\omega t+\varphi(t))$", fontsize=SUPTITLE_SIZE, y=0.965)

    setup_complex_axis(ax_complex)
    ax_complex.set_title(r"Phasor state at $t_0$", pad=12, fontsize=TITLE_SIZE)

    time_dense = data["time_dense"]
    phi_var = PHI_VAR_AMPLITUDE * np.sin(PHI_VAR_OMEGA * time_dense)
    signal_var = np.cos(OMEGA * time_dense + phi_var)
    phi_var_deg = np.degrees(phi_var)

    highlight_t = PHI_VAR_HIGHLIGHT_T
    highlight_phi = PHI_VAR_AMPLITUDE * np.sin(PHI_VAR_OMEGA * highlight_t)
    reference_value = np.exp(1j * OMEGA * highlight_t)
    shifted_value = np.exp(1j * (OMEGA * highlight_t + highlight_phi))
    signal_value = np.cos(OMEGA * highlight_t + highlight_phi)

    ax_complex.plot([0.0, reference_value.real], [0.0, reference_value.imag], color=REFERENCE_COLOR, lw=2.2, label=r"reference $e^{j\omega t_0}$")
    ax_complex.plot([0.0, shifted_value.real], [0.0, shifted_value.imag], color=SUM_COLOR, lw=2.8, label=r"shifted $e^{j(\omega t_0+\varphi(t_0))}$")
    ax_complex.plot([shifted_value.real, shifted_value.real], [shifted_value.imag, 0.0], color=PHASE_PLOT_COLOR, lw=2.0, label=r"real projection")
    ax_complex.plot([reference_value.real], [reference_value.imag], "o", color=REFERENCE_COLOR, ms=7)
    ax_complex.plot([shifted_value.real], [shifted_value.imag], "o", color=SUM_COLOR, ms=7)
    ax_complex.plot([signal_value], [0.0], "o", color=PHASE_PLOT_COLOR, ms=6)

    theta = np.linspace(OMEGA * highlight_t, OMEGA * highlight_t + highlight_phi, 140)
    arc_radius = 0.32
    ax_complex.plot(arc_radius * np.cos(theta), arc_radius * np.sin(theta), color=PHASOR_PHASE_COLOR, lw=2.0)
    phi_label = fr"$\varphi(t_0)={np.degrees(highlight_phi):+.0f}^\circ$"
    ax_complex.text(-0.18, -0.26, phi_label, color=PHASOR_PHASE_COLOR, fontsize=13)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    ax_signal.plot(time_dense, data["reference_signal"], color=REFERENCE_COLOR, lw=2.0, label=r"$\cos(\omega t)$")
    ax_signal.plot(time_dense, signal_var, color=SUM_COLOR, lw=2.7, label=r"$\cos(\omega t+\varphi(t))$")
    ax_signal.axhline(0.0, color="0.78", lw=0.9)
    ax_signal.axvline(highlight_t, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    ax_signal.plot([highlight_t], [signal_value], "o", color=MARKER_COLOR, ms=8)
    ax_signal.grid(alpha=GRID_ALPHA)
    ax_signal.set_xlim(T_START, T_END)
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_title("Time signal", pad=10, fontsize=TITLE_SIZE)
    ax_signal.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax_signal.tick_params(labelsize=TICK_SIZE)
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    ax_phi.plot(time_dense, phi_var_deg, color=PHASE_PLOT_COLOR, lw=2.5, ls="--")
    ax_phi.axhline(0.0, color="0.78", lw=0.9)
    ax_phi.axvline(highlight_t, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    ax_phi.plot([highlight_t], [np.degrees(highlight_phi)], "o", color=MARKER_COLOR, ms=8)
    ax_phi.grid(alpha=GRID_ALPHA)
    ax_phi.set_xlim(T_START, T_END)
    ax_phi.set_ylim(-180.0, 180.0)
    ax_phi.set_yticks([-180.0, -90.0, 0.0, 90.0, 180.0])
    ax_phi.set_title(r"Phase over time: $\varphi(t)=90^\circ\sin(0.5t)$", pad=10, fontsize=TITLE_SIZE)
    ax_phi.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax_phi.set_ylabel(r"$\varphi$ [deg]", fontsize=LABEL_SIZE)
    ax_phi.tick_params(labelsize=TICK_SIZE)

    fig.savefig(VARIABLE_OVERVIEW_PATH, dpi=FIG_DPI, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def create_time_varying_phase_spectrum_overview(data):
    time_period = np.linspace(T_START, T_END, 8000, endpoint=False)
    phi_var = PHI_VAR_AMPLITUDE * np.sin(PHI_VAR_OMEGA * time_period)
    signal_var = np.cos(OMEGA * time_period + phi_var)

    freq_dense_hz = np.linspace(-1.0, 1.0, 2601)
    basis = np.exp(-1j * 2.0 * np.pi * freq_dense_hz[:, None] * time_period[None, :])
    spectrum_dense = np.trapezoid(signal_var[None, :] * basis, x=time_period, axis=1) / (T_END - T_START)
    magnitude_dense = np.abs(spectrum_dense)
    phase_dense = np.degrees(np.angle(spectrum_dense))
    phase_dense = np.where(magnitude_dense > 0.02 * np.max(magnitude_dense), phase_dense, np.nan)

    fig, axes = plt.subplots(3, 1, figsize=SPECTRUM_OVERVIEW_FIGSIZE, dpi=FIG_DPI)

    axes[0].plot(time_period, signal_var, color=SUM_COLOR, lw=2.8)
    axes[0].axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    axes[0].set_xlim(T_START, T_END)
    axes[0].set_ylim(-1.15, 1.15)
    axes[0].grid(alpha=GRID_ALPHA)
    axes[0].set_title(r"Time signal $x(t)=\cos(\omega t+\varphi(t))$", pad=10, fontsize=SPEC_TITLE_SIZE)
    axes[0].set_xlabel("Time t [s]", fontsize=SPEC_LABEL_SIZE)
    axes[0].set_ylabel("Amplitude", fontsize=SPEC_LABEL_SIZE)
    axes[0].tick_params(labelsize=SPEC_TICK_SIZE)

    axes[1].plot(freq_dense_hz, magnitude_dense, color="0.35", lw=2.4)
    axes[1].axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    axes[1].set_xlim(-1.0, 1.0)
    axes[1].set_ylim(0.0, 1.05 * np.max(magnitude_dense))
    axes[1].grid(alpha=GRID_ALPHA)
    axes[1].set_title("Two-sided magnitude spectrum", pad=10, fontsize=SPEC_TITLE_SIZE)
    axes[1].set_xlabel("Frequency f [Hz]", fontsize=SPEC_LABEL_SIZE)
    axes[1].set_ylabel(r"$|X(f)|$", fontsize=SPEC_LABEL_SIZE)
    axes[1].tick_params(labelsize=SPEC_TICK_SIZE)

    axes[2].plot(freq_dense_hz, phase_dense, color="0.35", lw=2.2)
    axes[2].axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    axes[2].set_xlim(-1.0, 1.0)
    axes[2].set_ylim(-180.0, 180.0)
    axes[2].grid(alpha=GRID_ALPHA)
    axes[2].set_title("Two-sided phase spectrum", pad=10, fontsize=SPEC_TITLE_SIZE)
    axes[2].set_xlabel("Frequency f [Hz]", fontsize=SPEC_LABEL_SIZE)
    axes[2].set_ylabel(r"$ngle X(f)$ [deg]", fontsize=SPEC_LABEL_SIZE)
    axes[2].set_ylabel(r"$\angle X(f)$ [deg]", fontsize=SPEC_LABEL_SIZE)

    fig.subplots_adjust(left=0.12, right=0.96, top=0.96, bottom=0.07, hspace=0.45)
    fig.savefig(SPECTRUM_OVERVIEW_PATH, dpi=FIG_DPI, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def build_variable_phase_animation(data):
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 0.68])
    ax_complex = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_phi = fig.add_subplot(grid[1, 1], sharex=ax_signal)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24, hspace=0.22)
    fig.suptitle(r"Time-varying phase in $x(t)=\cos(\omega t+\varphi(t))$", fontsize=SUPTITLE_SIZE, y=0.965)

    setup_complex_axis(ax_complex)
    ax_complex.set_title(r"Phasor state", pad=12, fontsize=TITLE_SIZE)

    time_dense = data["time_dense"]
    phi_var = PHI_VAR_AMPLITUDE * np.sin(PHI_VAR_OMEGA * time_dense)
    signal_var = np.cos(OMEGA * time_dense + phi_var)
    phi_var_deg = np.degrees(phi_var)

    ax_signal.plot(time_dense, data["reference_signal"], color=REFERENCE_COLOR, lw=2.0, label=r"$\cos(\omega t)$")
    ax_signal.plot(time_dense, signal_var, color=SUM_COLOR, lw=2.7, label=r"$\cos(\omega t+\varphi(t))$")
    ax_signal.axhline(0.0, color="0.78", lw=0.9)
    ax_signal.grid(alpha=GRID_ALPHA)
    ax_signal.set_xlim(T_START, T_END)
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_title("Time signal", pad=10, fontsize=TITLE_SIZE)
    ax_signal.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    ax_signal.tick_params(labelsize=TICK_SIZE)
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    ax_phi.plot(time_dense, phi_var_deg, color=PHASE_PLOT_COLOR, lw=2.5, ls="--")
    ax_phi.axhline(0.0, color="0.78", lw=0.9)
    ax_phi.grid(alpha=GRID_ALPHA)
    ax_phi.set_xlim(T_START, T_END)
    ax_phi.set_ylim(-180.0, 180.0)
    ax_phi.set_yticks([-180.0, -90.0, 0.0, 90.0, 180.0])
    ax_phi.set_title(r"Phase over time: $\varphi(t)=90^\circ\sin(0.5t)$", pad=10, fontsize=TITLE_SIZE)
    ax_phi.set_xlabel("Time t [s]", fontsize=LABEL_SIZE)
    ax_phi.set_ylabel(r"$\varphi$ [deg]", fontsize=LABEL_SIZE)
    ax_phi.tick_params(labelsize=TICK_SIZE)

    reference_line, = ax_complex.plot([], [], color=REFERENCE_COLOR, lw=2.2, label=r"reference $e^{j\omega t}$")
    shifted_line, = ax_complex.plot([], [], color=SUM_COLOR, lw=2.8, label=r"shifted $e^{j(\omega t+\varphi(t))}$")
    projection_line, = ax_complex.plot([], [], color=PHASE_PLOT_COLOR, lw=2.0, label=r"real projection")
    reference_tip, = ax_complex.plot([], [], "o", color=REFERENCE_COLOR, ms=7)
    shifted_tip, = ax_complex.plot([], [], "o", color=SUM_COLOR, ms=7)
    projection_tip, = ax_complex.plot([], [], "o", color=PHASE_PLOT_COLOR, ms=6)
    phase_arc, = ax_complex.plot([], [], color=PHASOR_PHASE_COLOR, lw=2.0)
    phase_text = ax_complex.text(-0.18, -0.26, "", color=PHASOR_PHASE_COLOR, fontsize=13)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    time_marker_signal = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_signal_point, = ax_signal.plot([], [], "o", color=MARKER_COLOR, ms=8)
    time_marker_phi = ax_phi.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_phi_point, = ax_phi.plot([], [], "o", color=MARKER_COLOR, ms=8)

    def draw_state(current_t):
        current_phi = PHI_VAR_AMPLITUDE * np.sin(PHI_VAR_OMEGA * current_t)
        reference_value = np.exp(1j * OMEGA * current_t)
        shifted_value = np.exp(1j * (OMEGA * current_t + current_phi))
        signal_value = np.cos(OMEGA * current_t + current_phi)
        phi_value_deg = np.degrees(current_phi)

        reference_line.set_data([0.0, reference_value.real], [0.0, reference_value.imag])
        shifted_line.set_data([0.0, shifted_value.real], [0.0, shifted_value.imag])
        projection_line.set_data([shifted_value.real, shifted_value.real], [shifted_value.imag, 0.0])
        reference_tip.set_data([reference_value.real], [reference_value.imag])
        shifted_tip.set_data([shifted_value.real], [shifted_value.imag])
        projection_tip.set_data([signal_value], [0.0])

        theta = np.linspace(OMEGA * current_t, OMEGA * current_t + current_phi, 100)
        arc_radius = 0.32
        phase_arc.set_data(arc_radius * np.cos(theta), arc_radius * np.sin(theta))
        phase_text.set_text(fr"$\varphi(t)={phi_value_deg:+.0f}^\circ$")

        time_marker_signal.set_xdata([current_t, current_t])
        moving_signal_point.set_data([current_t], [signal_value])
        time_marker_phi.set_xdata([current_t, current_t])
        moving_phi_point.set_data([current_t], [phi_value_deg])

        return (
            reference_line,
            shifted_line,
            projection_line,
            reference_tip,
            shifted_tip,
            projection_tip,
            phase_arc,
            phase_text,
            time_marker_signal,
            moving_signal_point,
            time_marker_phi,
            moving_phi_point,
        )

    def update(frame_index):
        return draw_state(data["time_frames"][frame_index])

    animation = FuncAnimation(fig, update, frames=len(data["time_frames"]), interval=1000 / FPS, blit=False)
    return fig, animation, draw_state


def build_animation(data):
    fig, ax_complex, ax_signal, ax_phi = create_figure()
    draw_static_axes(ax_complex, ax_signal, ax_phi, data)

    pos_line, = ax_complex.plot([], [], color=POS_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{j(\omega t-45^\circ)}$")
    neg_line, = ax_complex.plot([], [], color=NEG_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{-j(\omega t-45^\circ)}$")
    sum_line, = ax_complex.plot([], [], color=SUM_COLOR, lw=2.9, label=r"$\cos(\omega t-45^\circ)$")
    pos_tip, = ax_complex.plot([], [], "o", color=POS_COLOR, ms=7)
    neg_tip, = ax_complex.plot([], [], "o", color=NEG_COLOR, ms=7)
    sum_tip, = ax_complex.plot([], [], "o", color=SUM_COLOR, ms=7)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    time_marker_signal = ax_signal.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_signal_point, = ax_signal.plot([], [], "o", color=MARKER_COLOR, ms=8)

    time_marker_phi = ax_phi.axvline(T_START, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_phi_point, = ax_phi.plot([], [], "o", color=MARKER_COLOR, ms=8)

    def draw_state(current_t):
        z_pos = 0.5 * np.exp(1j * (OMEGA * current_t + PHI))
        z_neg = 0.5 * np.exp(-1j * (OMEGA * current_t + PHI))
        z_sum = z_pos + z_neg
        signal_value = np.cos(OMEGA * current_t + PHI)
        phi_value = np.degrees(PHI)

        pos_line.set_data([0.0, z_pos.real], [0.0, z_pos.imag])
        neg_line.set_data([0.0, z_neg.real], [0.0, z_neg.imag])
        sum_line.set_data([0.0, z_sum.real], [0.0, 0.0])
        pos_tip.set_data([z_pos.real], [z_pos.imag])
        neg_tip.set_data([z_neg.real], [z_neg.imag])
        sum_tip.set_data([z_sum.real], [0.0])

        time_marker_signal.set_xdata([current_t, current_t])
        moving_signal_point.set_data([current_t], [signal_value])
        time_marker_phi.set_xdata([current_t, current_t])
        moving_phi_point.set_data([current_t], [phi_value])

        return (
            pos_line,
            neg_line,
            sum_line,
            pos_tip,
            neg_tip,
            sum_tip,
            time_marker_signal,
            moving_signal_point,
            time_marker_phi,
            moving_phi_point,
        )

    def update(frame_index):
        return draw_state(data["time_frames"][frame_index])

    animation = FuncAnimation(fig, update, frames=len(data["time_frames"]), interval=1000 / FPS, blit=False)
    return fig, animation, draw_state



def main():
    data = build_data()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.is_file():
            old_file.unlink()
    create_time_varying_phase_overview(data)
    create_time_varying_phase_spectrum_overview(data)
    fig, animation, draw_state = build_animation(data)
    draw_state(data["time_frames"][0])
    fig.savefig(OVERVIEW_PATH, dpi=FIG_DPI, bbox_inches="tight", pad_inches=0.18)
    writer = PillowWriter(fps=FPS)
    animation.save(str(GIF_PATH.resolve()), writer=writer)
    plt.close(fig)

    variable_fig, variable_animation, variable_draw_state = build_variable_phase_animation(data)
    variable_draw_state(PHI_VAR_HIGHLIGHT_T)
    variable_writer = PillowWriter(fps=FPS)
    variable_animation.save(str(VARIABLE_GIF_PATH.resolve()), writer=variable_writer)
    plt.close(variable_fig)
    print(f"Saved overview to: {OVERVIEW_PATH}")
    print(f"Saved GIF to: {GIF_PATH}")
    print(f"Saved variable-phase overview to: {VARIABLE_OVERVIEW_PATH}")
    print(f"Saved variable-phase GIF to: {VARIABLE_GIF_PATH}")
    print(f"Saved spectrum overview to: {SPECTRUM_OVERVIEW_PATH}")


if __name__ == "__main__":
    main()
