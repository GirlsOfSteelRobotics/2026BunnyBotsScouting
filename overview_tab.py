import os
from shinywidgets import output_widget, render_widget
from shiny import App, ui
from shiny import reactive, render, module
from data_container import load_scouted_data, match_numbers, team_numbers
import pandas as pd
import plotly.express as px
import numpy as np

pd.set_option("display.max_columns", None)

scouted_data = load_scouted_data()
team_averages = (
    scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()
)


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        ui.card(output_widget("teleop_vs_auto_endgame")),
        ui.card(output_widget("placeholder")),
    )


@module.server
def overview_tab_server(input, output, session):
    @render_widget
    def placeholder():
        print("hello, world!")
