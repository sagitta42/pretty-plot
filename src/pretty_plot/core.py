from matplotlib.axes import Axes
from matplotlib.figure import Figure

from pretty_plot.anchor import AnchorPoint
from pretty_plot.style import Color, Font
from pretty_plot.prettifier import Prettifier


# TODO: group properties into dataclasses / OOP to clean up
def prettify(
    fig: Figure,
    axis_main: Axes,
    axes_secondary: list[Axes] = [],
    logo: bool = True,
    logo_location: str = AnchorPoint.bottom_right,
    logo_outside: bool = False,
    logo_scale: float = 0.05,
    date: bool = True,
    date_location: str = AnchorPoint.bottom_left,
    warning: bool = True,
    warning_text: str = "PRELIMINARY",
    warning_fontsize: int | str = "large",
    warning_color: str = "red",
    warning_location: str = AnchorPoint.top_left,
    font: str = Font.neo,
):
    prettifier = Prettifier(font)
    all_axes = [axis_main] + axes_secondary

    prettifier.set_format(all_axes)
    prettifier.set_style(fig, all_axes, color=Color.pheni)

    if logo:
        prettifier.add_logo(
            fig,
            axis_main,
            anchor_point=AnchorPoint(logo_location),
            outside=logo_outside,
            scale=logo_scale,
        )

    if date:
        prettifier.add_date(
            axis_main, date_format="%Y-%m-%d", anchor_point=AnchorPoint(date_location)
        )

    if warning:
        prettifier.add_warning(
            axis_main,
            color=warning_color,
            anchor_point=AnchorPoint(warning_location),
            text=warning_text,
            fontsize=warning_fontsize,
        )
