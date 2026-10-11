import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data

match_df = load_scouted_data().copy()

@module.ui
def team_pit_trend_ui():
    teams = sorted(
        [t for t in match_df["Team and Robot"].dropna().astype(str).str.strip().unique().tolist()],
        key=lambda x: int(x)
    )

    return ui.page_fluid(
        ui.input_select(
            "team_select",
            "Select Team:",
            choices=teams,
            selected=teams[0] if teams else None,
        ),
        ui.input_select(
            "y_axis_select",
            "Metric:",
            choices=[],
            selected="",
        ),
        ui.card(output_widget("team_trend_graph")),
    )
