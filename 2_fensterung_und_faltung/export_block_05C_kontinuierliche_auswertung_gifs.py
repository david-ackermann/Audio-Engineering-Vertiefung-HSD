from pathlib import Path
import importlib.util

from PIL import Image, ImageSequence


CORE_SCRIPT = Path(__file__).resolve().parent / "export_block_05B_rueckweg_zur_faltung.py"


def load_core_module():
    spec = importlib.util.spec_from_file_location("block05b_core", CORE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = load_core_module()
DISCRETE_OUTPUT_ROOT = core.OUTPUT_ROOT
BLOCK_05C_OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "05_herleitung_und_dualitaet"
    / "05C_kontinuierliche_auswertung"
)
core.OUTPUT_ROOT = BLOCK_05C_OUTPUT_DIR.parent


def remove_temp_reference_pngs():
    for filename in (
        "15_complex_value_Y_f_from_frequency.png",
        "_temp_observed_magnitude_reference.png",
        "16_observed_magnitude_spectrum_Y_f.png",
    ):
        file_path = core.OUTPUT_DIR / filename
        if file_path.exists():
            file_path.unlink()


def save_manual_tight_gif_with_external_reference(fig, update_func, filename, reference_path, frame_indices):
    frames = []
    durations = []
    for frame_idx in range(len(frame_indices)):
        update_func(frame_idx)
        frames.append(core.render_figure_tight(fig))
        durations.append(int(round(1000 / core.ANIMATION_FPS)))

    durations[0] = core.GIF_HOLD_FIRST_MS
    durations[-1] = core.GIF_HOLD_LAST_MS

    with Image.open(reference_path) as ref:
        target_size = ref.size

    padded_frames = []
    for frame in frames:
        canvas = Image.new("RGBA", target_size, (255, 255, 255, 255))
        offset = (
            max(0, (target_size[0] - frame.width) // 2),
            max(0, (target_size[1] - frame.height) // 2),
        )
        canvas.alpha_composite(frame, dest=offset)
        padded_frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE))

    gif_path = core.OUTPUT_DIR / filename
    padded_frames[0].save(
        gif_path,
        save_all=True,
        append_images=padded_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def save_tight_png_with_external_reference(fig, update_func, filename, reference_path, frame_idx):
    update_func(frame_idx)
    frame = core.render_figure_tight(fig)

    with Image.open(reference_path) as ref:
        target_size = ref.size

    canvas = Image.new("RGBA", target_size, (255, 255, 255, 255))
    offset = (
        max(0, (target_size[0] - frame.width) // 2),
        max(0, (target_size[1] - frame.height) // 2),
    )
    canvas.alpha_composite(frame, dest=offset)
    canvas.convert("RGB").save(core.OUTPUT_DIR / filename, dpi=(core.DPI, core.DPI))


def save_gif_frame_as_png(gif_filename, png_filename, which="first"):
    gif_path = core.OUTPUT_DIR / gif_filename
    png_path = core.OUTPUT_DIR / png_filename
    with Image.open(gif_path) as gif:
        frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif)]
    frame = frames[0] if which == "first" else frames[-1]
    frame.convert("RGB").save(png_path, dpi=(core.DPI, core.DPI))


def export_single_axis_weighting_sweep_animation(
    filename,
    base_values,
    output_values,
    active_color,
    title,
    y_label,
    base_label,
    weighted_label,
    output_label,
    reference_filename,
):
    fig, ax = core.create_figure(core.SPECTRUM_FIGSIZE)
    core.draw_spectral_lines(ax, core.X_LINE_FREQS, base_values, core.FUTURE_GREY, lw=2.2)
    kernel_line, = ax.plot(core.FREQ_VALUES, core.G_VALUES, color=core.ACTIVE_RED, lw=1.8)
    weighted_lines = ax.vlines(
        core.X_LINE_FREQS,
        0.0,
        base_values * core.G_AT_LINE_FREQS,
        color=active_color,
        lw=3.2,
    )
    output_reference, = ax.plot(core.FREQ_VALUES, output_values, color=core.FUTURE_GREY, lw=1.8, ls="--")
    output_trace, = ax.plot([], [], color=active_color, lw=2.4)
    current_freq_line = ax.axvline(core.PROBE_F, color="0.65", lw=1.0)
    current_value_line = ax.axhline(0.0, color=active_color, lw=2.0, ls="--")
    current_value_point, = ax.plot([], [], "o", color=core.ACTIVE_RED, ms=7)

    core.style_signed_frequency_axis(ax, title, core.COMMON_SPECTRUM_LIMIT, y_label)
    core.add_inset_legend(
        ax,
        [
            core.Line2D([0], [0], color=core.FUTURE_GREY, lw=1.8, label=base_label),
            core.Line2D([0], [0], color=core.ACTIVE_RED, lw=1.8, label=r"$G_f(\nu)$"),
            core.Line2D([0], [0], color=active_color, lw=2.2, label=weighted_label),
            core.Line2D([0], [0], color=active_color, lw=2.0, ls="--", label=output_label),
        ],
        loc="upper right",
    )

    def update(frame_idx):
        freq_idx = core.FREQ_ANIMATION_INDICES[frame_idx]
        current_f = core.FREQ_VALUES[freq_idx]
        current_kernel = core.WINDOW_DURATION * core.np.sinc(core.WINDOW_DURATION * (current_f - core.FREQ_VALUES))
        kernel_at_lines = core.WINDOW_DURATION * core.np.sinc(core.WINDOW_DURATION * (current_f - core.X_LINE_FREQS))
        weighted_values = base_values * kernel_at_lines
        current_output = core.np.interp(current_f, core.FREQ_VALUES, output_values)

        kernel_line.set_data(core.FREQ_VALUES, current_kernel)
        weighted_lines.set_segments(
            [((freq, 0.0), (freq, value)) for freq, value in zip(core.X_LINE_FREQS, weighted_values)]
        )
        current_freq_line.set_xdata([current_f, current_f])
        output_trace.set_data(core.FREQ_VALUES[: freq_idx + 1], output_values[: freq_idx + 1])
        current_value_line.set_ydata([current_output, current_output])
        current_value_point.set_data([current_f], [current_output])
        return (
            kernel_line,
            weighted_lines,
            output_trace,
            current_freq_line,
            current_value_line,
            current_value_point,
        )

    reference_path = DISCRETE_OUTPUT_ROOT / "2Hz" / reference_filename
    save_tight_png_with_external_reference(
        fig,
        update,
        filename.replace(".gif", "_f_min.png"),
        reference_path,
        0,
    )
    save_manual_tight_gif_with_external_reference(
        fig,
        update,
        filename,
        reference_path,
        core.FREQ_ANIMATION_INDICES,
    )
    core.plt.close(fig)
    save_gif_frame_as_png(filename, filename.replace(".gif", "_f_max.png"), which="last")


def export_real_weighting_sweep_animation():
    export_single_axis_weighting_sweep_animation(
        "01_real_weighting_sweep.gif",
        core.np.real(core.X_LINE_COEFFS),
        core.np.real(core.Y_VALUES),
        core.SPECTRUM_BLUE,
        r"Real part with sum value",
        r"Re$\{X(\nu)G_f(\nu)\}$",
        r"Re$\{X(\nu)\}$",
        r"Re$\{X(\nu)G_f(\nu)\}$",
        r"Re$\{Y(f)\}$",
        "13_real_weighted_spectrum_XG_with_sum.png",
    )


def export_imag_weighting_sweep_animation():
    export_single_axis_weighting_sweep_animation(
        "02_imaginary_weighting_sweep.gif",
        core.np.imag(core.X_LINE_COEFFS),
        core.np.imag(core.Y_VALUES),
        core.IMAG_ORANGE,
        r"Imaginary part with sum value",
        r"Im$\{X(\nu)G_f(\nu)\}$",
        r"Im$\{X(\nu)\}$",
        r"Im$\{X(\nu)G_f(\nu)\}$",
        r"Im$\{Y(f)\}$",
        "14_imaginary_weighted_spectrum_XG_with_sum.png",
    )


def export_kernel_spectrum_animation():
    fig, ax = core.create_figure(core.SPECTRUM_FIGSIZE)
    ax.plot(core.FREQ_VALUES, core.W_VALUES, color=core.WINDOW_GREEN, lw=1.9)
    kernel_line, = ax.plot(core.FREQ_VALUES, core.G_VALUES, color=core.ACTIVE_RED, lw=2.4)
    current_freq_line = ax.axvline(core.FREQ_VALUES[0], color="0.65", lw=1.0)
    current_freq_text = ax.text(
        0.985,
        0.96,
        "",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=core.LEGEND_SIZE,
        bbox={"facecolor": "white", "edgecolor": "0.80", "alpha": 0.95},
    )

    core.style_signed_frequency_axis(
        ax,
        r"Analysis kernel spectrum $G_f(\nu)=W(f-\nu)$",
        core.KERNEL_SPECTRUM_LIMIT,
        r"$G_f(\nu)$",
    )
    core.add_inset_legend(
        ax,
        [
            core.Line2D([0], [0], color=core.WINDOW_GREEN, lw=1.9, label=r"$W(\nu)$"),
            core.Line2D([0], [0], color=core.ACTIVE_RED, lw=2.4, label=r"$G_f(\nu)$"),
        ],
        loc="upper left",
    )

    def update(frame_idx):
        freq_idx = core.FREQ_ANIMATION_INDICES[frame_idx]
        current_f = core.FREQ_VALUES[freq_idx]
        current_kernel = core.WINDOW_DURATION * core.np.sinc(core.WINDOW_DURATION * (current_f - core.FREQ_VALUES))
        kernel_line.set_data(core.FREQ_VALUES, current_kernel)
        current_freq_line.set_xdata([current_f, current_f])
        current_freq_text.set_text(rf"$f={core.frequency_label(current_f)}$ Hz")
        return kernel_line, current_freq_line, current_freq_text

    reference_path = DISCRETE_OUTPUT_ROOT / "2Hz" / "08_analysis_kernel_spectrum_G_f_nu.png"
    save_manual_tight_gif_with_external_reference(
        fig,
        update,
        "05_analysis_kernel_spectrum_sweep.gif",
        reference_path,
        core.FREQ_ANIMATION_INDICES,
    )
    core.plt.close(fig)
    save_gif_frame_as_png(
        "05_analysis_kernel_spectrum_sweep.gif",
        "05_analysis_kernel_spectrum_sweep_f_min.png",
        which="first",
    )
    save_gif_frame_as_png(
        "05_analysis_kernel_spectrum_sweep.gif",
        "05_analysis_kernel_spectrum_sweep_f_max.png",
        which="last",
    )


def export_complex_value_animation():
    core.export_complex_value(
        "15_complex_value_Y_f_from_frequency.png",
        core.Y_FIXED_FREQ,
        rf"Complex value $Y(f)$ at $f={core.frequency_label(core.PROBE_F)}$ Hz",
    )
    core.export_complex_value_animation()
    (core.OUTPUT_DIR / "15A_complex_value_Y_f_animation.gif").rename(
        core.OUTPUT_DIR / "03_complex_value_Y_f_animation.gif"
    )
    save_gif_frame_as_png(
        "03_complex_value_Y_f_animation.gif",
        "03_complex_value_Y_f_animation_f_min.png",
        which="first",
    )
    save_gif_frame_as_png(
        "03_complex_value_Y_f_animation.gif",
        "03_complex_value_Y_f_animation_f_max.png",
        which="last",
    )


def export_observed_magnitude_projection_animation():
    core.export_observed_magnitude_spectrum_summary()
    core.export_observed_magnitude_spectrum_animation()
    (core.OUTPUT_DIR / "16A_observed_magnitude_projection.gif").rename(
        core.OUTPUT_DIR / "04_observed_magnitude_projection.gif"
    )
    save_gif_frame_as_png(
        "04_observed_magnitude_projection.gif",
        "04_observed_magnitude_projection_f_min.png",
        which="first",
    )
    save_gif_frame_as_png(
        "04_observed_magnitude_projection.gif",
        "04_observed_magnitude_projection_f_max.png",
        which="last",
    )


def export_continuous_gifs():
    export_real_weighting_sweep_animation()
    export_imag_weighting_sweep_animation()
    export_complex_value_animation()
    export_observed_magnitude_projection_animation()
    export_kernel_spectrum_animation()
    remove_temp_reference_pngs()
    print(f"Continuous GIFs exported to: {core.OUTPUT_DIR}")


def main():
    core.configure_series(2.0, BLOCK_05C_OUTPUT_DIR.name)
    core.clear_owned_outputs()
    export_continuous_gifs()


if __name__ == "__main__":
    main()
