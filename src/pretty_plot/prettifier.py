from datetime import datetime
from importlib import resources

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.text import Text

from pretty_plot.anchor import AnchorCoordinates, AnchorPoint, ShiftType
from pretty_plot.style import Color


class Prettifier:
    def __init__(self, font: str):
        # TODO: read logo from .ini
        self._logo = plt.imread(
            resources.files("pretty_plot.logo").joinpath(f"logo.png")
        )
        self._font = font
        self._pad = 0.025
        self._extra_shift = 0.06

    def add_logo(
        self,
        fig: Figure,
        ax: Axes,
        anchor_point: AnchorPoint,
        outside: bool,
        scale: float,
    ):
        imagebox = OffsetImage(
            self._logo, zoom=self._get_logo_zoom(fig, ax, scale), interpolation="none"
        )
        imagebox.image.axes = ax

        shift_type = ShiftType.move_out if outside else ShiftType.pad
        logo_anchor: tuple[float, float] = self._get_anchor_with_shift(
            anchor_point, shift_type, shift_y=self._extra_shift
        )
        anchor_coordinates: tuple[float, float] = AnchorCoordinates.from_anchor_point(
            anchor_point
        )
        box_alignment: tuple[float, float] = (
            anchor_coordinates.inverted if outside else anchor_coordinates.value
        )
        annotation_box = AnnotationBbox(
            imagebox,
            xy=logo_anchor,
            xybox=logo_anchor,
            pad=self._pad,
            xycoords="axes fraction",
            box_alignment=box_alignment,
            frameon=False,
            annotation_clip=False,
        )
        ax.add_artist(annotation_box)

    def add_date(self, ax: Axes, date_format: str, anchor_point: AnchorPoint):
        date = datetime.today().strftime(date_format)
        self._add_text(
            ax,
            date,
            anchor_point,
            Color.pheni,
            fontsize="small",
        )

    def add_warning(
        self,
        ax: Axes,
        color: str,
        anchor_point: AnchorPoint,
        text: str,
        fontsize: int | str,
    ):
        self._add_text(
            ax,
            text,
            anchor_point,
            color,
            fontweight="bold",
            fontstyle="italic",
            fontsize=fontsize,
        )

    def set_style(self, fig: Figure, axes: list[Axes], color: str):
        text_items_font_only, text_items_full_style = self._get_axes_text_items(axes)

        if len(fig.texts) > 0:
            text_items_full_style.append(fig.texts[0])
        if len(fig.legends) > 0:
            text_items_font_only += fig.legends[0].get_texts()

        all_text_items = text_items_font_only + text_items_full_style

        for text in all_text_items:
            text.set_fontfamily(self._font)
            if text in text_items_full_style:
                text.set_color(color)
                text.set_fontweight("bold")

        for ax in axes:
            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_fontfamily(self._font)

    def set_format(self, axes: list[Axes]):
        for ax in axes:
            ax.set_axisbelow(True)
            ax.grid(linestyle="--", zorder=0)

    def _add_text(
        self, ax: Axes, text: str, anchor_point: AnchorPoint, color: str, **kwargs
    ):
        anchor = self._get_anchor_with_shift(anchor_point, ShiftType.pad)
        va, ha = anchor_point.name.split("_")

        ax.annotate(
            text,
            xy=anchor,
            xytext=anchor,
            font=self._font,
            color=color,
            xycoords="axes fraction",
            ha=ha,
            va=va,
            annotation_clip=True,
            **kwargs,
        )

    def _get_axes_text_items(self, axes: list[Axes]) -> tuple[list[Text], list[Text]]:
        text_items_font_only: list[Text] = []
        text_items_full_style: list[Text] = []

        for ax in axes:
            legend = ax.get_legend()
            if legend is not None:
                text_items_font_only += legend.get_texts()

            text_items_full_style += [ax.xaxis.label, ax.yaxis.label, ax.title]
            zaxis = getattr(ax, "zaxis", None)
            if zaxis is not None:
                text_items_full_style.append(ax.zaxis.label)

        return text_items_font_only, text_items_full_style

    def _get_anchor_with_shift(
        self,
        anchor_point: AnchorPoint,
        shift_type: ShiftType,
        shift_x: float | None = None,
        shift_y: float | None = None,
    ) -> tuple[float, float]:
        if shift_x is None:
            shift_x = self._pad
        if shift_y is None:
            shift_y = shift_x

        ret = AnchorCoordinates.from_anchor_point(anchor_point).with_shift(
            shift_x, shift_y, shift_type
        )
        return ret

    def _get_logo_zoom(self, fig: Figure, ax: Axes, scale: float) -> float:
        # FIXME: scale relative to image area does not work properly
        # (still relative to original image size not reresenting fraction/%)
        renderer = fig.canvas.get_renderer()
        bbox = ax.get_window_extent(renderer)
        ax_height, ax_width = bbox.height, bbox.width
        ax_area = ax_height * ax_width
        logo_height, logo_width = self._logo.shape[0], self._logo.shape[1]
        logo_area = logo_height * logo_width

        ratio_area = ax_area / logo_area
        ratio_height = ax_height / logo_height

        zoom_area = scale * ratio_area
        zoom_height = scale * ratio_height

        logo_zoom = min(zoom_area, zoom_height)
        ret = logo_zoom * fig.dpi
        return ret
