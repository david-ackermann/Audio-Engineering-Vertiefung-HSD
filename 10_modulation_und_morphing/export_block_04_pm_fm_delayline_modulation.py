from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "04_pm_fm_delayline_modulation" / "04a_angle_modulation_pm_fm"

DPI = 200
FIGSIZE = (12.0, 4.4)

MODULATION_VIOLET = "#7b4ab8"
OUTPUT_BLUE = "#2b7bbb"
INPUT_BLACK = "0.12"
PHASE_BLACK = "0.12"
SIGNAL_MODULATOR_GREY = "0.68"
GRID_GREY = "0.75"
REFERENCE_GREY = "0.55"
PHASE_REFERENCE_GREY = "0.72"

TITLE_SIZE = 24
LABEL_SIZE = 20
TICK_SIZE = 17
LEGEND_SIZE = 14

SAMPLE_RATE_HZ = 1000.0
DURATION_S = 6.0
MODULATION_FREQUENCY_HZ = 0.5
CARRIER_FREQUENCY_HZ = 8.0
PM_INDEX_RAD = 1.5 * np.pi
# For a sine modulator, phi_FM amplitude is k_FM / f_m.
# This choice makes the sine FM phase amplitude match the PM phase reference.
FM_DEVIATION_HZ = PM_INDEX_RAD * MODULATION_FREQUENCY_HZ
OUTPUT_PHASE_GAIN = 2.0

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


CASES = [
    ("pm", "sine", "PM sine"),
    ("fm", "sine", "FM sine"),
    ("pm", "triangle", "PM triangle"),
    ("fm", "triangle", "FM triangle"),
    ("pm", "rectangle", "PM rectangular"),
    ("fm", "rectangle", "FM rectangular"),
]


def modulation_signal(kind: str, time_s: np.ndarray) -> np.ndarray:
    phase = 2.0 * np.pi * MODULATION_FREQUENCY_HZ * time_s
    if kind == "sine":
        return np.sin(phase)
    if kind == "triangle":
        return (2.0 / np.pi) * np.arcsin(np.sin(phase))
    if kind == "rectangle":
        return np.where(np.sin(phase) >= 0.0, 1.0, -1.0)
    raise ValueError(f"Unsupported modulation kind: {kind}")


def phase_term(mode: str, modulation: np.ndarray) -> np.ndarray:
    if mode == "pm":
        return PM_INDEX_RAD * modulation
    if mode == "fm":
        dt = 1.0 / SAMPLE_RATE_HZ
        zero_mean_modulation = modulation - float(np.mean(modulation))
        increments = 0.5 * (zero_mean_modulation[1:] + zero_mean_modulation[:-1]) * dt
        integral = np.concatenate(([0.0], np.cumsum(increments)))
        phase = 2.0 * np.pi * FM_DEVIATION_HZ * integral
        return phase - float(np.mean(phase))
    raise ValueError(f"Unsupported modulation mode: {mode}")


def build_case_data(mode: str, kind: str) -> dict[str, np.ndarray]:
    time_s = np.arange(int(round(DURATION_S * SAMPLE_RATE_HZ))) / SAMPLE_RATE_HZ
    modulation = modulation_signal(kind, time_s)
    phi = phase_term(mode, modulation)
    carrier_phase = 2.0 * np.pi * CARRIER_FREQUENCY_HZ * time_s
    carrier = np.cos(carrier_phase)
    output = np.cos(carrier_phase + OUTPUT_PHASE_GAIN * phi)
    return {
        "time_s": time_s,
        "modulation": modulation,
        "phase": phi,
        "carrier": carrier,
        "output": output,
    }


def setup_axis(ax: plt.Axes) -> None:
    ax.set_xlim(0.0, DURATION_S)
    ax.grid(True, color=GRID_GREY, alpha=0.25)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=0.9)
    ax.tick_params(axis="both", labelsize=TICK_SIZE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def pi_formatter(value: float, _position: int) -> str:
    if np.isclose(value, 0.0):
        return "0"

    multiple = value / np.pi
    rounded = int(round(multiple))
    if not np.isclose(multiple, rounded):
        return ""

    sign = "-" if rounded < 0 else ""
    magnitude = abs(rounded)
    if magnitude == 1:
        return rf"${sign}\pi$"
    return rf"${sign}{magnitude}\pi$"


def phase_tick_values(max_phase_abs: float) -> tuple[list[float], tuple[float, float]]:
    max_multiple = max(1, int(np.ceil(max_phase_abs / np.pi)))
    ticks = [k * np.pi for k in range(-max_multiple, max_multiple + 1)]
    limit = 1.08 * max_multiple * np.pi
    return ticks, (-limit, limit)


def save_input_plot(data: dict[str, np.ndarray], prefix: str) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(data["time_s"], data["carrier"], color=INPUT_BLACK, lw=1.35)
    ax.set_title("Input carrier", fontsize=TITLE_SIZE, pad=14)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("Time (s)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    setup_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    path = OUTPUT_DIR / f"{prefix}_input_carrier.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_modulator_plot(mode: str, kind: str, title: str, data: dict[str, np.ndarray], prefix: str) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(data["time_s"], data["modulation"], color=MODULATION_VIOLET, lw=2.6)
    ax.set_title(f"{title}: modulator", fontsize=TITLE_SIZE, pad=14)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("Time (s)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    setup_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    path = OUTPUT_DIR / f"{prefix}_{mode}_{kind}_modulator.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_signal_plot(mode: str, kind: str, title: str, data: dict[str, np.ndarray], prefix: str) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(data["time_s"], data["modulation"], color=SIGNAL_MODULATOR_GREY, lw=2.4, label="modulator", zorder=1)
    ax.plot(data["time_s"], data["output"], color=OUTPUT_BLUE, lw=1.35, label=f"{mode.upper()} output", zorder=2)
    ax.set_title(f"{title}: modulator and output", fontsize=TITLE_SIZE, pad=14)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("Time (s)", fontsize=LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=LABEL_SIZE)
    setup_axis(ax)
    ax.legend(loc="upper right", fontsize=LEGEND_SIZE, framealpha=0.92)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    path = OUTPUT_DIR / f"{prefix}_{mode}_{kind}_signal.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_phase_plot(
    mode: str,
    kind: str,
    title: str,
    data: dict[str, np.ndarray],
    prefix: str,
    *,
    ticks: list[float],
    y_limit: tuple[float, float],
) -> Path:
    fig, ax = plt.subplots(figsize=FIGSIZE)

    if mode == "fm":
        pm_phase_reference = phase_term("pm", data["modulation"])
        ax.plot(
            data["time_s"],
            pm_phase_reference,
            color=PHASE_REFERENCE_GREY,
            lw=3.0,
            label="PM phase reference",
            zorder=1,
        )

    ax.plot(data["time_s"], data["phase"], color=PHASE_BLACK, lw=2.4, label="phase term", zorder=2)
    ax.set_title(f"{title}: phase term", fontsize=TITLE_SIZE, pad=14)
    ax.set_ylim(*y_limit)
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(FuncFormatter(pi_formatter))
    ax.set_xlabel("Time (s)", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$\varphi(t)$", fontsize=LABEL_SIZE)
    setup_axis(ax)
    if mode == "fm":
        ax.legend(loc="upper right", fontsize=LEGEND_SIZE, framealpha=0.92)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.84)
    path = OUTPUT_DIR / f"{prefix}_{mode}_{kind}_phase.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*"):
        if old_file.is_file() and old_file.suffix.lower() in {".png", ".gif"}:
            old_file.unlink()

    case_data = [(mode, kind, title, build_case_data(mode, kind)) for mode, kind, title in CASES]
    global_max_phase = max(float(np.max(np.abs(data["phase"]))) for _mode, _kind, _title, data in case_data)
    phase_ticks, phase_y_limit = phase_tick_values(global_max_phase)

    paths: list[Path] = [save_input_plot(case_data[0][3], "01")]
    for case_index, (mode, kind, title, data) in enumerate(case_data, start=1):
        modulator_prefix = f"{3 * case_index - 1:02d}"
        signal_prefix = f"{3 * case_index:02d}"
        phase_prefix = f"{3 * case_index + 1:02d}"
        paths.append(save_modulator_plot(mode, kind, title, data, modulator_prefix))
        paths.append(save_signal_plot(mode, kind, title, data, signal_prefix))
        paths.append(
            save_phase_plot(
                mode,
                kind,
                title,
                data,
                phase_prefix,
                ticks=phase_ticks,
                y_limit=phase_y_limit,
            )
        )

    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
