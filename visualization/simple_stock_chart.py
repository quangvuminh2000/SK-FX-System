from math import pi

from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.models import HoverTool, ColumnDataSource

import yfinance as yf


def simple_stock_chart(market="AAPL", name="Apple"):
    stock_data = yf.download(market, period="max", interval="1d").reset_index(
        drop=False
    )

    source = ColumnDataSource(
        data=dict(
            x=stock_data.index,
            open=stock_data["Open"],
            high=stock_data["High"],
            low=stock_data["Low"],
            close=stock_data["Close"],
            volume=stock_data["Volume"],
        )
    )

    # p = figure(x_axis_type="datetime", title=f"{name} Candlestick Chart")
    # p.segment(
    #     x0="x",
    #     y0="low",
    #     x1="x",
    #     y1="high",
    #     source=source,
    #     line_width=2,
    #     line_color="black",
    # )
    # p.vbar(
    #     x="x",
    #     width=0.5,
    #     top="open",
    #     bottom="close",
    #     source=source,
    #     fill_color="#2A9445",
    #     line_color="black",
    # )
    # p.vbar(
    #     x="x",
    #     width=0.5,
    #     top="close",
    #     bottom="open",
    #     source=source,
    #     fill_color="#DC2422",
    #     line_color="black",
    # )

    # show(p)

    hover = HoverTool(
        tooltips=[
            ("date", "@x{%F}"),
            ("close", "@close{%0.2f}"),  # use @{ } for field names with spaces
            ("open", "@open{%0.2f}"),  # use @{ } for field names with spaces
            ("high", "@high{%0.2f}"),  # use @{ } for field names with spaces
            ("low", "@low{%0.2f}"),  # use @{ } for field names with spaces
            ("volume", "@volume{0.00 a}"),
        ],
        formatters={
            "@x": "datetime",  # use 'datetime' formatter for '@date' field
            "@close": "printf",  # use 'printf' formatter for '@{adj close}' field
            "@open": "printf",  # use 'printf' formatter for '@{adj close}' field
            "@high": "printf",  # use 'printf' formatter for '@{adj close}' field
            "@low": "printf",  # use 'printf' formatter for '@{adj close}' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
    )

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(
        x_axis_type="datetime",
        tools=TOOLS,
        width=1000,
        title=f"{name}-{market} Candlestick",
    )
    p.add_tools(hover)
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3

    p.segment(
        x0="x",
        y0="low",
        x1="x",
        y1="high",
        source=source,
        line_width=2,
        line_color="black",
    )
    p.vbar(
        x="x",
        width=0.5,
        top="open",
        bottom="close",
        source=source,
        fill_color="#2A9445",
        line_color="black",
    )
    p.vbar(
        x="x",
        width=0.5,
        top="close",
        bottom="open",
        source=source,
        fill_color="#DC2422",
        line_color="black",
    )
    show(p)


if __name__ == "__main__":
    simple_stock_chart(market="AAPL", name="Apple Inc.")
