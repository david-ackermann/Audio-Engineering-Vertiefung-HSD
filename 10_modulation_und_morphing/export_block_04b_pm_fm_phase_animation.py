from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import FuncFormatter


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (
    LECTURE_DIR
    / "png_storyboards"
    / "04_pm_fm_delayline_modulation"
    / "04b_pm_fm_phase_animation"
)

FPS = 24
FRAMES = 240
FIG_DPI = 120
FIGSIZE = (14.4, 6.6)

SAMPLE_RATE_HZ = 60.0
N_SAMPLES = 120
DISPLAY_OVERSAMPLE = 8
MODULATOR_CYCLES = 1.0
CARRIER_CYCLES = 8.0
OMEGA_C = 2.0 * np.pi * CARRIER_CYCLES / N_SAMPLES
OMEGA_M = 2.0 * np.pi * MODULATOR_CYCLES / N_SAMPLES
F_C_HZ = CARRIER_CYCLES * SAMPLE_RATE_HZ / N_SAMPLES
F_M_HZ = MODULATOR_CYCLES * SAMPLE_RATE_HZ / N_SAMPLES

PM_BETA_RAD = np.pi
PM_RECTANGLE_BETA_RAD = np.pi
FM_DEVIATION_HZ = 2.0
PHASE_LIMITS_RAD = (-np.pi, np.pi)
PHASE_TICKS_RAD = [-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi]

TITLE_SIZE = 18
LABEL_SIZE = 15
TICK_SIZE = 12
SUPTITLE_SIZE = 24

PHASOR_LIGHT_BLUE = "#62b5e5"
POS_COLOR = PHASOR_LIGHT_BLUE
NEG_COLOR = PHASOR_LIGHT_BLUE
OUTPUT_BLUE = "tab:blue"
MODULATION_VIOLET = "#7b4ab8"
FM_PHASE_COLOR = MODULATION_VIOLET
REFERENCE_COLOR = "0.65"
MARKER_COLOR = "tab:red"
BASELINE_COLOR = "0.78"
GRID_ALPHA = 0.18

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


CASES = [
    {
        "slug": "pm_sine",
        "preview": "01_pm_sine_phase_modulation_preview.png",
        "gif": "02_pm_sine_phase_modulation.gif",
        "mode": "pm",
        "modulator": "sine",
        "suptitle": r"Phase modulation: $y_\mathrm{PM}[n]=\cos(\Omega_c n+\Delta\varphi_\mathrm{PM}[n])$",
        "signal_label": r"$y_\mathrm{PM}[n]$",
        "control_title": r"Phase offset: $\Delta\varphi_\mathrm{PM}[n]=\beta m[n]$",
    },
    {
        "slug": "pm_triangle",
        "preview": "03_pm_triangle_phase_modulation_preview.png",
        "gif": "04_pm_triangle_phase_modulation.gif",
        "mode": "pm",
        "modulator": "triangle",
        "suptitle": r"Phase modulation with a triangular phase control",
        "signal_label": r"$y_\mathrm{PM,tri}[n]$",
        "control_title": r"Phase offset: $\Delta\varphi_\mathrm{PM}[n]=\beta m_\triangle[n]$",
    },
    {
        "slug": "pm_rectangle",
        "preview": "05_pm_rectangle_phase_modulation_preview.png",
        "gif": "06_pm_rectangle_phase_modulation.gif",
        "mode": "pm",
        "modulator": "rectangle",
        "suptitle": r"Phase switching with a rectangular phase control",
        "signal_label": r"$y_\mathrm{PM,rect}[n]$",
        "control_title": r"Phase offset: $\Delta\varphi_\mathrm{PM}[n]\in\{0,\pi\}$",
    },
    {
        "slug": "fm_sine",
        "preview": "07_fm_sine_frequency_modulation_preview.png",
        "gif": "08_fm_sine_frequency_modulation.gif",
        "mode": "fm",
        "modulator": "sine",
        "suptitle": r"Frequency modulation: $f_i[n]$ controls the phase accumulation",
        "signal_label": r"$y_\mathrm{FM}[n]$",
        "control_title": r"Instantaneous frequency $f_i[n]$ and accumulated phase term",
    },
    {
        "slug": "fm_triangle",
        "preview": "09_fm_triangle_frequency_modulation_preview.png",
        "gif": "10_fm_triangle_frequency_modulation.gif",
        "mode": "fm",
        "modulator": "triangle",
        "suptitle": r"Frequency modulation with a triangular frequency control",
        "signal_label": r"$y_\mathrm{FM,tri}[n]$",
        "control_title": r"Instantaneous frequency $f_i[n]$ and accumulated phase term",
    },
    {
        "slug": "fm_rectangle",
        "preview": "11_fm_rectangle_frequency_modulation_preview.png",
        "gif": "12_fm_rectangle_frequency_modulation.gif",
        "mode": "fm",
        "modulator": "rectangle",
        "suptitle": r"Frequency modulation with a rectangular frequency control",
        "signal_label": r"$y_\mathrm{FM,rect}[n]$",
        "control_title": r"Instantaneous frequency $f_i[n]$ and accumulated phase term",
    },
    {
        "slug": "pm_constant_zero",
        "preview": "13_pm_constant_phase_0_preview.png",
        "gif": "14_pm_constant_phase_0.gif",
        "mode": "pm",
        "modulator": "constant",
        "phase_constant": 0.0,
        "suptitle": r"Phase modulation with constant phase offset: $\Delta\varphi_\mathrm{PM}[n]=0$",
        "signal_label": r"$y_{\Delta\varphi=0}[n]$",
        "control_title": r"Constant phase offset: $\Delta\varphi_\mathrm{PM}[n]=0$",
    },
    {
        "slug": "pm_constant_minus_pi_over_2",
        "preview": "15_pm_constant_phase_minus_pi_over_2_preview.png",
        "gif": "16_pm_constant_phase_minus_pi_over_2.gif",
        "mode": "pm",
        "modulator": "constant",
        "phase_constant": -0.5 * np.pi,
        "suptitle": r"Phase modulation with constant phase offset: $\Delta\varphi_\mathrm{PM}[n]=-\pi/2$",
        "signal_label": r"$y_{\Delta\varphi=-\pi/2}[n]$",
        "signal_title": "Output signal",
        "control_title": r"Constant phase offset: $\Delta\varphi_\mathrm{PM}[n]=-\pi/2$",
    },
]


def sample_axis() -> np.ndarray:
    return np.arange(N_SAMPLES, dtype=float)


def display_axis() -> np.ndarray:
    point_count = (N_SAMPLES - 1) * DISPLAY_OVERSAMPLE + 1
    return np.linspace(0.0, N_SAMPLES - 1, point_count)


def modulator_value(kind: str, n: np.ndarray | float) -> np.ndarray | float:
    phase = OMEGA_M * np.asarray(n, dtype=float)
    if kind == "constant":
        return np.zeros_like(phase)
    if kind == "sine":
        return np.sin(phase)
    if kind == "triangle":
        return (2.0 / np.pi) * np.arcsin(np.sin(phase))
    if kind == "rectangle":
        return np.where(np.sin(phase) >= 0.0, 1.0, -1.0)
    raise ValueError(f"Unsupported modulator kind: {kind}")


def wrap_phase_pi(phase: np.ndarray | float) -> np.ndarray | float:
    return (np.asarray(phase) + np.pi) % (2.0 * np.pi) - np.pi


def build_case_data(case: dict) -> dict[str, np.ndarray]:
    n = sample_axis()
    carrier_phase = OMEGA_C * n
    carrier = np.cos(carrier_phase)
    modulation = np.asarray(modulator_value(case["modulator"], n), dtype=float)

    if case["mode"] == "pm":
        if "phase_constant" in case:
            phase_term = np.full_like(n, float(case["phase_constant"]))
        elif case["modulator"] == "rectangle":
            phase_term = 0.5 * PM_RECTANGLE_BETA_RAD * (modulation + 1.0)
        else:
            phase_term = PM_BETA_RAD * modulation
        instantaneous_frequency_hz = np.full_like(n, F_C_HZ)
    else:
        instantaneous_frequency_hz = F_C_HZ + FM_DEVIATION_HZ * modulation
        phase_increments = 2.0 * np.pi * instantaneous_frequency_hz / SAMPLE_RATE_HZ
        carrier_increments = np.full_like(phase_increments, OMEGA_C)
        total_phase = np.cumsum(phase_increments) - phase_increments[0]
        carrier_phase = np.cumsum(carrier_increments) - carrier_increments[0]
        phase_term = total_phase - carrier_phase

    total_phase = carrier_phase + phase_term
    displayed_phase_term = wrap_phase_pi(phase_term) if case["mode"] == "fm" else phase_term
    displayed_total_phase = wrap_phase_pi(total_phase)
    output = np.cos(total_phase)

    return {
        "n": n,
        "carrier": carrier,
        "modulation": modulation,
        "phase_term": phase_term,
        "displayed_phase_term": displayed_phase_term,
        "displayed_total_phase": displayed_total_phase,
        "total_phase": total_phase,
        "output": output,
        "instantaneous_frequency_hz": instantaneous_frequency_hz,
    }


def state_at(case: dict, data: dict[str, np.ndarray], current_n: float) -> dict[str, float]:
    carrier_phase = OMEGA_C * current_n
    carrier = float(np.cos(carrier_phase))
    modulation = float(modulator_value(case["modulator"], current_n))

    if case["mode"] == "pm":
        if "phase_constant" in case:
            phase_term = float(case["phase_constant"])
        elif case["modulator"] == "rectangle":
            phase_term = 0.5 * PM_RECTANGLE_BETA_RAD * (modulation + 1.0)
        else:
            phase_term = PM_BETA_RAD * modulation
        instantaneous_frequency_hz = F_C_HZ
        displayed_phase_term = phase_term
    else:
        instantaneous_frequency_hz = F_C_HZ + FM_DEVIATION_HZ * modulation
        phase_term = float(np.interp(current_n, data["n"], data["phase_term"]))
        displayed_phase_term = float(wrap_phase_pi(phase_term))

    total_phase = carrier_phase + phase_term
    displayed_total_phase = float(wrap_phase_pi(total_phase))
    output = float(np.cos(total_phase))
    return {
        "carrier_phase": float(carrier_phase),
        "carrier": carrier,
        "modulation": modulation,
        "phase_term": float(phase_term),
        "displayed_phase_term": displayed_phase_term,
        "displayed_total_phase": displayed_total_phase,
        "total_phase": float(total_phase),
        "output": output,
        "instantaneous_frequency_hz": float(instantaneous_frequency_hz),
    }


def setup_complex_axis(ax: plt.Axes) -> None:
    unit_circle_t = np.linspace(0.0, 2.0 * np.pi, 500)
    ax.plot(np.cos(unit_circle_t), np.sin(unit_circle_t), color="0.86", lw=2.0)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.axvline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=GRID_ALPHA)
    ax.set_xlabel(r"Re$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Im$\{\cdot\}$", fontsize=LABEL_SIZE)
    ax.set_title("Phasor sum", pad=12, fontsize=TITLE_SIZE)
    ax.tick_params(labelsize=TICK_SIZE)


def style_discrete_axis(ax: plt.Axes) -> None:
    ax.set_xlim(0.0, N_SAMPLES - 1)
    ax.set_xticks([0, 30, 60, 90, 119])
    ax.grid(alpha=GRID_ALPHA)
    ax.axhline(0.0, color=BASELINE_COLOR, lw=0.9)
    ax.tick_params(labelsize=TICK_SIZE)


def phase_formatter(value: float, _position: int) -> str:
    if np.isclose(value, 0.0):
        return "0"
    multiple = value / np.pi
    if np.isclose(multiple, -0.5):
        return r"$-\pi/2$"
    if np.isclose(multiple, 0.5):
        return r"$\pi/2$"
    rounded = int(round(multiple))
    if not np.isclose(multiple, rounded):
        return ""
    sign = "-" if rounded < 0 else ""
    magnitude = abs(rounded)
    if magnitude == 1:
        return rf"${sign}\pi$"
    return rf"${sign}{magnitude}\pi$"


def format_phase_pi(value: float) -> str:
    if np.isclose(value, 0.0, atol=1e-3):
        return "0"

    multiple = value / np.pi
    common_values = [
        (-1.0, r"-\pi"),
        (-0.5, r"-\pi/2"),
        (0.5, r"+\pi/2"),
        (1.0, r"+\pi"),
    ]
    for target, label in common_values:
        if np.isclose(multiple, target, atol=0.03):
            return label

    return f"{multiple:+.2f}\\pi"


def create_figure(case: dict) -> tuple[plt.Figure, plt.Axes, plt.Axes, plt.Axes]:
    fig = plt.figure(figsize=FIGSIZE, dpi=FIG_DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.45], height_ratios=[1.0, 1.0])
    ax_complex = fig.add_subplot(grid[:, 0])
    ax_signal = fig.add_subplot(grid[0, 1])
    ax_control = fig.add_subplot(grid[1, 1], sharex=ax_signal)
    fig.subplots_adjust(left=0.06, right=0.91, top=0.86, bottom=0.11, wspace=0.24, hspace=0.42)
    fig.suptitle(case["suptitle"], fontsize=SUPTITLE_SIZE, y=0.965)
    return fig, ax_complex, ax_signal, ax_control


def draw_background(case: dict, data: dict, ax_complex: plt.Axes, ax_signal: plt.Axes, ax_control: plt.Axes):
    n = data["n"]
    n_dense = display_axis()
    dense_states = [state_at(case, data, float(n_value)) for n_value in n_dense]
    output_dense = np.array([state["output"] for state in dense_states])
    carrier_dense = np.array([state["carrier"] for state in dense_states])
    phase_dense = np.array([state["phase_term"] for state in dense_states])
    displayed_phase_dense = np.array([state["displayed_phase_term"] for state in dense_states])
    displayed_total_phase_dense = np.array([state["displayed_total_phase"] for state in dense_states])
    frequency_dense = np.array([state["instantaneous_frequency_hz"] for state in dense_states])
    setup_complex_axis(ax_complex)

    if case["slug"] == "pm_constant_minus_pi_over_2":
        ax_signal.plot(
            n_dense,
            carrier_dense,
            color=REFERENCE_COLOR,
            lw=2.0,
            alpha=0.75,
            zorder=1,
            label="_nolegend_",
        )
    ax_signal.plot(
        n_dense,
        output_dense,
        color=OUTPUT_BLUE,
        lw=2.7,
        zorder=2,
        label=case["signal_label"],
    )
    ax_signal.plot(
        n[::8],
        data["output"][::8],
        linestyle="",
        color=OUTPUT_BLUE,
        marker="o",
        ms=2.8,
    )
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_title(case.get("signal_title", "Output signal"), pad=10, fontsize=TITLE_SIZE)
    ax_signal.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    style_discrete_axis(ax_signal)
    ax_signal.legend(loc="upper right", fontsize=11, framealpha=0.95)

    if case["mode"] == "fm":
        frequency_line = ax_control.plot(
            n_dense,
            frequency_dense,
            color=MODULATION_VIOLET,
            lw=2.7,
            ls="--",
            label=r"$f_i[n]=f_c+\Delta f\,m[n]$",
        )[0]
        ax_control.plot(
            n[::8],
            data["instantaneous_frequency_hz"][::8],
            linestyle="",
            color=MODULATION_VIOLET,
            marker="o",
            ms=2.8,
        )
        ax_phase = ax_control.twinx()
        phase_line = ax_phase.plot(
            n_dense,
            displayed_phase_dense,
            color=FM_PHASE_COLOR,
            lw=2.4,
            label=r"$\varphi_\mathrm{FM}[n]$",
        )[0]
        ax_control.set_ylim(F_C_HZ - 1.6 * FM_DEVIATION_HZ, F_C_HZ + 1.6 * FM_DEVIATION_HZ)
        ax_phase.set_ylim(*PHASE_LIMITS_RAD)
        ax_phase.set_yticks(PHASE_TICKS_RAD)
        ax_phase.yaxis.set_major_formatter(FuncFormatter(phase_formatter))
        ax_phase.set_ylabel(r"$\varphi_\mathrm{FM}[n]$ in rad", fontsize=LABEL_SIZE)
        ax_phase.tick_params(labelsize=TICK_SIZE)
        ax_phase.spines["top"].set_visible(False)
        ax_phase.spines["left"].set_visible(False)
        ax_phase.spines["right"].set_color(FM_PHASE_COLOR)
        ax_phase.yaxis.label.set_color(FM_PHASE_COLOR)
        ax_phase.tick_params(axis="y", colors=FM_PHASE_COLOR)
        legend = ax_control.legend(
            [frequency_line, phase_line],
            [frequency_line.get_label(), phase_line.get_label()],
            loc="upper right",
            fontsize=10.5,
            framealpha=0.95,
        )
        control_extra = {"ax_phase": ax_phase, "phase_line": phase_line, "legend": legend}
        ax_control.set_ylabel(r"$f_i[n]$ in Hz", fontsize=LABEL_SIZE, color=MODULATION_VIOLET)
        ax_control.tick_params(axis="y", colors=MODULATION_VIOLET)
    else:
        ax_control.plot(
            n_dense,
            phase_dense,
            color=MODULATION_VIOLET,
            lw=2.7,
            label=r"$\Delta\varphi_\mathrm{PM}[n]$",
        )
        ax_control.plot(
            n[::8],
            data["phase_term"][::8],
            linestyle="",
            color=MODULATION_VIOLET,
            marker="o",
            ms=2.8,
        )
        ax_control.set_ylim(*PHASE_LIMITS_RAD)
        ax_control.set_yticks(PHASE_TICKS_RAD)
        ax_control.yaxis.set_major_formatter(FuncFormatter(phase_formatter))
        ax_control.set_ylabel(r"$\Delta\varphi_\mathrm{PM}[n]$ in rad", fontsize=LABEL_SIZE)
        ax_control.tick_params(axis="y", colors=MODULATION_VIOLET)
        ax_control.yaxis.label.set_color(MODULATION_VIOLET)
        ax_control.legend(loc="upper right", fontsize=11, framealpha=0.95)
        control_extra = {}

    ax_control.set_title(case["control_title"], pad=10, fontsize=TITLE_SIZE)
    ax_control.set_xlabel("Sample index n", fontsize=LABEL_SIZE)
    style_discrete_axis(ax_control)
    return control_extra


def build_animation(case: dict, data: dict):
    fig, ax_complex, ax_signal, ax_control = create_figure(case)
    control_extra = draw_background(case, data, ax_complex, ax_signal, ax_control)

    reference_line, = ax_complex.plot([], [], color=REFERENCE_COLOR, lw=2.5, label=r"$x_c[n]$")
    reference_tip, = ax_complex.plot([], [], "o", color=REFERENCE_COLOR, ms=6.5)
    pos_line, = ax_complex.plot([], [], color=POS_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{j\theta[n]}$")
    neg_line, = ax_complex.plot([], [], color=NEG_COLOR, lw=2.7, label=r"$\frac{1}{2}e^{-j\theta[n]}$")
    sum_line, = ax_complex.plot([], [], color=OUTPUT_BLUE, lw=2.9, label=r"$y[n]$")
    pos_tip, = ax_complex.plot([], [], "o", color=POS_COLOR, ms=7)
    neg_tip, = ax_complex.plot([], [], "o", color=NEG_COLOR, ms=7)
    sum_tip, = ax_complex.plot([], [], "o", color=OUTPUT_BLUE, ms=7)
    phase_arc, = ax_complex.plot([], [], color=MODULATION_VIOLET, lw=2.0)
    phase_text = ax_complex.text(-0.16, -0.24, "", color=MODULATION_VIOLET, fontsize=13)
    ax_complex.legend(loc="lower left", fontsize=10.5, framealpha=0.95)

    time_marker_signal = ax_signal.axvline(0.0, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_signal_point, = ax_signal.plot([], [], "o", color=MARKER_COLOR, ms=8)
    time_marker_control = ax_control.axvline(0.0, color=MARKER_COLOR, lw=2.0, alpha=0.9)
    moving_control_point, = ax_control.plot([], [], "o", color=MARKER_COLOR, ms=8)
    if "ax_phase" in control_extra:
        moving_phase_point, = control_extra["ax_phase"].plot([], [], "o", color=FM_PHASE_COLOR, ms=6)
    else:
        moving_phase_point = None

    frame_positions = np.linspace(0.0, N_SAMPLES - 1, FRAMES)

    def draw_state(current_n: float):
        state = state_at(case, data, current_n)
        carrier_angle = state["carrier_phase"]
        total_angle = state["total_phase"]
        phase_term = state["phase_term"]
        displayed_phase_term = state["displayed_phase_term"]
        displayed_total_phase = state["displayed_total_phase"]

        reference_value = 0.5 * np.exp(1j * carrier_angle)
        z_pos = 0.5 * np.exp(1j * total_angle)
        z_neg = 0.5 * np.exp(-1j * total_angle)
        z_sum = z_pos + z_neg

        reference_line.set_data([0.0, reference_value.real], [0.0, reference_value.imag])
        reference_tip.set_data([reference_value.real], [reference_value.imag])
        pos_line.set_data([0.0, z_pos.real], [0.0, z_pos.imag])
        neg_line.set_data([0.0, z_neg.real], [0.0, z_neg.imag])
        sum_line.set_data([0.0, z_sum.real], [0.0, 0.0])
        pos_tip.set_data([z_pos.real], [z_pos.imag])
        neg_tip.set_data([z_neg.real], [z_neg.imag])
        sum_tip.set_data([z_sum.real], [0.0])

        arc_steps = max(16, int(abs(displayed_phase_term) / np.pi * 80))
        theta = np.linspace(carrier_angle, carrier_angle + displayed_phase_term, arc_steps)
        phase_arc.set_data(0.32 * np.cos(theta), 0.32 * np.sin(theta))
        phase_symbol = r"\varphi_\mathrm{FM}" if case["mode"] == "fm" else r"\Delta\varphi_\mathrm{PM}"
        phase_text.set_text(fr"${phase_symbol}={format_phase_pi(displayed_phase_term)}$")

        time_marker_signal.set_xdata([current_n, current_n])
        moving_signal_point.set_data([current_n], [state["output"]])
        time_marker_control.set_xdata([current_n, current_n])
        if case["mode"] == "fm":
            moving_control_point.set_data([current_n], [state["instantaneous_frequency_hz"]])
            moving_phase_point.set_data([current_n], [displayed_phase_term])
        else:
            moving_control_point.set_data([current_n], [phase_term])

        artists = [
            reference_line,
            reference_tip,
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
            time_marker_control,
            moving_control_point,
        ]
        if moving_phase_point is not None:
            artists.append(moving_phase_point)
        return tuple(artists)

    def update(frame_index: int):
        return draw_state(float(frame_positions[frame_index]))

    animation = FuncAnimation(fig, update, frames=FRAMES, interval=1000 / FPS, blit=False)
    return fig, animation, draw_state


def export_case(case: dict) -> list[Path]:
    data = build_case_data(case)
    fig, animation, draw_state = build_animation(case, data)
    preview_n = 0.18 * (N_SAMPLES - 1)
    draw_state(preview_n)

    preview_path = OUTPUT_DIR / case["preview"]
    gif_path = OUTPUT_DIR / case["gif"]
    fig.savefig(preview_path, dpi=FIG_DPI, facecolor=fig.get_facecolor())
    writer = PillowWriter(fps=FPS)
    animation.save(str(gif_path.resolve()), writer=writer)
    plt.close(fig)
    return [preview_path, gif_path]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.is_file() and old_file.suffix.lower() in {".png", ".gif"}:
            old_file.unlink()

    saved_paths: list[Path] = []
    for case in CASES:
        saved_paths.extend(export_case(case))

    for path in saved_paths:
        print(path)


if __name__ == "__main__":
    main()
