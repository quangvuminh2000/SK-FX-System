import pandas as pd
from datetime import datetime

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import vnstock as vns

from sk_fx.indicators.oscillators.divergence_oscillator import StochasticOscillator
from sk_fx.indicators.idtypes import TimeFrame


def divergence_figure(data: pd.DataFrame, row_name: str = "divergence"):
    # Create figure
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_width=[0.25, 0.75],
        subplot_titles=("Price Data", "Stochastic"),
    )

    # Create Candlestick chart for price data
    fig.add_trace(
        go.Candlestick(
            x=data["time"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            increasing_line_color="#55B748",
            decreasing_line_color="#ED3F3C",
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Create scatter plot chart for stochastic
    fig.add_trace(
        go.Scatter(
            x=data["time"],
            y=data[row_name],
            line=dict(color="#ff9900", width=2),
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    # Add min/max line for the RSI
    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)

    # Add overbought/oversold
    fig.add_hline(
        y=30, col=1, row=2, line_color="#336699", line_width=2, line_dash="dash"
    )
    fig.add_hline(
        y=70, col=1, row=2, line_color="#336699", line_width=2, line_dash="dash"
    )

    # Customize font, colors, hide range slider
    layout = go.Layout(
        plot_bgcolor="#efefef",
        # Font Families
        font_family="Monospace",
        font_color="#000000",
        font_size=20,
        xaxis=dict(rangeslider=dict(visible=False)),
    )

    # update and display
    fig.update_layout(layout, showlegend=False)
    fig.show()


if __name__ == "__main__":
    today_str = datetime.today().strftime("%Y-%m-%d")
    stock_data = vns.stock_historical_data(
        symbol="CII",
        start_date="2018-01-01",
        end_date=today_str,
        resolution="1D",
        type="stock",
        beautify=False,
    )

    stochastic = StochasticOscillator(
        "Stochastic Oscillator",
        time_frame=TimeFrame.D1,
        ohlcv=stock_data,
        k_length=13,
        d_length=8,
    )

    stock_data["stochastic"] = stochastic.calculate()

    divergence_figure(stock_data, row_name="stochastic")
