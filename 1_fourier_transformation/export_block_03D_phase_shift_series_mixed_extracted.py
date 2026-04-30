from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

import export_block_03B_phase_shift_series as base
import export_mixed_signal_two_sided_spectrum as mixed_spectrum
import storyboard_paths as paths


OUTPUT_DIR = paths.PHASE_SHIFT_SERIES_MIXED_EXTRACTED_DIR
REAL_MIXED_PHASE_OVERVIEW_PATH = OUTPUT_DIR / "07_mixed_like_variable_phase_real_mixed_phase_overview.png"
REAL_MIXED_PHASE_GIF_PATH = OUTPUT_DIR / "08_mixed_like_variable_phase_real_mixed_phase.gif"
REAL_MIXED_PHASE_COLOR = "0.45"
PHASE_FREQ_MIN = -6.5
PHASE_FREQ_MAX = 6.5
PHASE_FREQ_TICKS = np.arange(-6.0, 6.1, 2.0)


def sawtooth_descending(t, period):
    phase = (np.asarray(t, dtype=float) % period) / period
    return 1.0 - 2.0 * phase


def mixed_like_phase_values(case, t):
    t = np.asarray(t, dtype=float)
    if case["mode"] == "mixed_like":
        return (
            np.deg2rad(60.0) * np.sin(0.45 * t)
            + np.deg2rad(28.0) * np.sin(1.35 * t - 0.6)
            + np.deg2rad(14.0) * np.sin(2.1 * t + 0.9)
        )
    if case["mode"] == "saw_modeled":
        target = sawtooth_descending(t, 2.0 * np.pi / base.OMEGA)
        theta = np.arccos(np.clip(target, -1.0, 1.0))
        phi = theta - base.OMEGA * t
        return (phi + np.pi) % (2.0 * np.pi) - np.pi
    return base_phase_values_original(case, t)


SERIES_CASES = [
    {
        "prefix": "01",
        "slug": "mixed_like_variable_phase",
        "mode": "mixed_like",
        "spectrum_period": 40.0 * np.pi,
        "spectrum_x_limits": (-1.0, 1.0),
        "spectrum_phase_threshold": 0.01,
        "phase_title": r"Phase over time: mixed-like $\varphi(t)$",
        "suptitle": r"Didactic mixed-like phase in $x(t)=\cos(\omega t+\varphi(t))$",
        "signal_label": r"$\cos(\omega t+\varphi(t))$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t+\varphi(t))$",
    },
    {
        "prefix": "04",
        "slug": "saw_modeled_by_phase",
        "mode": "saw_modeled",
        "spectrum_period": 2.0 * np.pi,
        "spectrum_x_limits": (-1.0, 1.0),
        "spectrum_phase_threshold": 0.01,
        "spectrum_time_full": True,
        "phase_title": r"Phase over time: sawtooth-modeled $\varphi(t)$",
        "suptitle": r"Sawtooth modeled via phase in $x(t)=\cos(\omega t+\varphi(t))$",
        "signal_label": r"$\cos(\omega t+\varphi(t))$",
        "spectrum_signal_title": r"Time signal $x(t)=\cos(\omega t+\varphi(t))$",
    },
]

base_phase_values_original = base.phase_values
base.phase_values = mixed_like_phase_values


def build_real_mixed_phase_time_mapping():
    mixed_context = mixed_spectrum.build_context()
    time_dense = np.linspace(base.T_START, base.T_END, 1200)
    time_frames = np.linspace(base.T_START, base.T_END, base.FRAMES, endpoint=False)

    phase_axis_time = np.linspace(base.T_START, base.T_END, len(mixed_context["freqs"]))
    phase_freq_dense = np.interp(time_dense, [base.T_START, base.T_END], [PHASE_FREQ_MIN, PHASE_FREQ_MAX])
    phase_freq_frames = np.interp(time_frames, [base.T_START, base.T_END], [PHASE_FREQ_MIN, PHASE_FREQ_MAX])
    phi_deg_dense = np.interp(time_dense, phase_axis_time, mixed_context["phase_deg"])
    phi_deg_frames = np.interp(time_frames, phase_axis_time, mixed_context["phase_deg"])
    phi_dense = np.deg2rad(phi_deg_dense)
    phi_frames = np.deg2rad(phi_deg_frames)

    return {
        "time_dense": time_dense,
        "time_frames": time_frames,
        "phi_deg_dense": phi_deg_dense,
        "phi_deg_frames": phi_deg_frames,
        "phase_freq_dense": phase_freq_dense,
        "phase_freq_frames": phase_freq_frames,
        "phi_dense": phi_dense,
        "phi_frames": phi_frames,
        "reference_signal": np.ones_like(time_dense),
        "shifted_signal": np.cos(phi_dense),
    }


def create_real_mixed_phase_figure():
    fig = plt.figure(figsize=base.FIGSIZE, dpi=base.FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 0.68])
    ax_complex = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_phase = fig.add_subplot(grid[1, 1])
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.10, wspace=0.24, hspace=0.22)
    return fig, ax_complex, ax_signal, ax_phase


def draw_real_mixed_phase_background(ax_complex, ax_signal, ax_phase, data):
    base.setup_complex_axis(ax_complex)
    ax_complex.set_title("Phasor sum", pad=12, fontsize=base.TITLE_SIZE)

    ax_signal.plot(
        data["time_dense"],
        data["reference_signal"],
        color=base.REFERENCE_COLOR,
        lw=2.0,
        label=r"$\cos(0)=1$",
    )
    ax_signal.plot(
        data["time_dense"],
        data["shifted_signal"],
        color=base.SUM_COLOR,
        lw=2.7,
        label=r"$\cos(\varphi_{\mathrm{mapped}}(t))$",
    )
    ax_signal.axhline(0.0, color="0.78", lw=0.9)
    ax_signal.grid(alpha=base.GRID_ALPHA)
    ax_signal.set_xlim(base.T_START, base.T_END)
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_title("Time signal", pad=10, fontsize=base.TITLE_SIZE)
    ax_signal.set_ylabel("Amplitude", fontsize=base.LABEL_SIZE)
    ax_signal.set_xlabel("Frequency f [Hz]", fontsize=base.LABEL_SIZE)
    mapped_signal_ticks = np.interp(PHASE_FREQ_TICKS, [PHASE_FREQ_MIN, PHASE_FREQ_MAX], [base.T_START, base.T_END])
    ax_signal.set_xticks(mapped_signal_ticks)
    ax_signal.set_xticklabels([f"{v:.0f}" for v in PHASE_FREQ_TICKS])
    ax_signal.tick_params(labelsize=base.TICK_SIZE)
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    ax_phase.plot(data["phase_freq_dense"], data["phi_deg_dense"], color=REAL_MIXED_PHASE_COLOR, lw=2.4)
    ax_phase.axhline(0.0, color="0.78", lw=0.9)
    ax_phase.grid(alpha=base.GRID_ALPHA)
    ax_phase.set_xlim(PHASE_FREQ_MIN, PHASE_FREQ_MAX)
    ax_phase.set_ylim(-190.0, 190.0)
    ax_phase.set_yticks([-180.0, -90.0, 0.0, 90.0, 180.0])
    ax_phase.set_xticks(PHASE_FREQ_TICKS)
    ax_phase.set_xlabel("Frequency f [Hz]", fontsize=base.LABEL_SIZE)
    ax_phase.set_ylabel(r"$\angle X(f)$ [deg]", fontsize=base.LABEL_SIZE)
    ax_phase.tick_params(labelsize=base.TICK_SIZE)


def build_real_mixed_phase_animation(data):
    fig, ax_complex, ax_signal, ax_phase = create_real_mixed_phase_figure()
    draw_real_mixed_phase_background(ax_complex, ax_signal, ax_phase, data)

    reference_line, = ax_complex.plot([], [], color=base.REFERENCE_COLOR, lw=2.5, label=r"$\cos(0)=1$",
)
    pos_line, = ax_complex.plot([], [], color=base.POS_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{j\varphi(t)}$")
    neg_line, = ax_complex.plot([], [], color=base.NEG_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{-j\varphi(t)}$")
    sum_line, = ax_complex.plot([], [], color=base.SUM_COLOR, lw=2.9, label=r"$x(t)$")
    reference_tip, = ax_complex.plot([], [], "o", color=base.REFERENCE_COLOR, ms=6.5)
    pos_tip, = ax_complex.plot([], [], "o", color=base.POS_COLOR, ms=7)
    neg_tip, = ax_complex.plot([], [], "o", color=base.NEG_COLOR, ms=7)
    sum_tip, = ax_complex.plot([], [], "o", color=base.SUM_COLOR, ms=7)
    phase_arc, = ax_complex.plot([], [], color=REAL_MIXED_PHASE_COLOR, lw=2.0)
    phase_text = ax_complex.text(-0.15, -0.24, "", color=REAL_MIXED_PHASE_COLOR, fontsize=13)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    time_marker_signal = ax_signal.axvline(base.T_START, color=base.MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_signal_point, = ax_signal.plot([], [], "o", color=base.MARKER_COLOR, ms=8)
    time_marker_phi = ax_phase.axvline(base.T_START, color=base.MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_phi_point, = ax_phase.plot([], [], "o", color=base.MARKER_COLOR, ms=8)

    def draw_state(frame_index):
        current_t = data["time_frames"][frame_index]
        current_phase_freq = data["phase_freq_frames"][frame_index]
        current_phi = data["phi_frames"][frame_index]
        phi_value_deg = data["phi_deg_frames"][frame_index]
        reference_value = 0.5 + 0j
        z_pos = 0.5 * np.exp(1j * current_phi)
        z_neg = 0.5 * np.exp(-1j * current_phi)
        z_sum = z_pos + z_neg
        signal_value = np.cos(current_phi)

        reference_line.set_data([0.0, reference_value.real], [0.0, reference_value.imag])
        pos_line.set_data([0.0, z_pos.real], [0.0, z_pos.imag])
        neg_line.set_data([0.0, z_neg.real], [0.0, z_neg.imag])
        sum_line.set_data([0.0, z_sum.real], [0.0, 0.0])
        reference_tip.set_data([reference_value.real], [reference_value.imag])
        pos_tip.set_data([z_pos.real], [z_pos.imag])
        neg_tip.set_data([z_neg.real], [z_neg.imag])
        sum_tip.set_data([z_sum.real], [0.0])

        theta = np.linspace(0.0, current_phi, 100)
        phase_arc.set_data(0.32 * np.cos(theta), 0.32 * np.sin(theta))
        phase_text.set_text(fr"$\varphi={base.format_phase_deg(phi_value_deg)}$")

        time_marker_signal.set_xdata([current_t, current_t])
        moving_signal_point.set_data([current_t], [signal_value])
        time_marker_phi.set_xdata([current_phase_freq, current_phase_freq])
        moving_phi_point.set_data([current_phase_freq], [phi_value_deg])

        return (
            reference_line,
            pos_line,
            neg_line,
            sum_line,
            reference_tip,
            pos_tip,
            neg_tip,
            sum_tip,
            phase_arc,
            phase_text,
            time_marker_signal,
            moving_signal_point,
            time_marker_phi,
            moving_phi_point,
        )

    animation = FuncAnimation(
        fig,
        lambda idx: draw_state(idx),
        frames=len(data["time_frames"]),
        interval=1000 / base.FPS,
        blit=False,
    )
    return fig, animation, draw_state


def save_real_mixed_phase_overview_and_gif():
    data = build_real_mixed_phase_time_mapping()
    fig, animation, draw_state = build_real_mixed_phase_animation(data)
    draw_state(0)
    fig.savefig(REAL_MIXED_PHASE_OVERVIEW_PATH, dpi=base.FIG_DPI, facecolor=fig.get_facecolor())
    writer = PillowWriter(fps=base.FPS)
    animation.save(str(REAL_MIXED_PHASE_GIF_PATH.resolve()), writer=writer)
    plt.close(fig)
    return [REAL_MIXED_PHASE_OVERVIEW_PATH, REAL_MIXED_PHASE_GIF_PATH]


def main():
    base.OUTPUT_DIR = OUTPUT_DIR
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.is_file():
            old_file.unlink()

    saved_paths = []
    for case in SERIES_CASES:
        saved_paths.extend(base.export_case(case))

    print(f"Saved outputs to: {OUTPUT_DIR}")
    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
