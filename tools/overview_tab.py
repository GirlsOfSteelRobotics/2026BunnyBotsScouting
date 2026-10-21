import os
from shinywidgets import output_widget, render_widget
from shiny import App, ui
from shiny import reactive, render, module
from data_container import load_scouted_data, match_numbers, team_numbers
import pandas as pd
import plotly.express as px
import numpy as np

pd.set_option('display.max_columns', None)

scouted_data = load_scouted_data()
team_averages = (
    scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()
)


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        ui.card(output_widget("teleop_vs_auto_endgame")),
        ui.card(output_widget()),
    )

@module.server
def overview_tab_server(input, output, session):
    @render.ui
    def match_list_combobox():
        if input.selection_mode() == "Match Number":
            return ui.input_select(
                "match_select",
                "Match Number:",
                choices=match_numbers
            )
        else:
            return ui.div(
                ui.input_select("team1", "Team 1:", choices=team_numbers, selected="3504"),
                ui.input_select("team2", "Team 2:", choices=team_numbers, selected=team_numbers[0]),
                ui.input_select("team3", "Team 3:", choices=team_numbers, selected=team_numbers[1]),
                ui.input_select("team4", "Team 4:", choices=team_numbers, selected=team_numbers[2]),
                ui.input_select("team5", "Team 5:", choices=team_numbers, selected=team_numbers[3]),
                ui.input_select("team6", "Team 6:", choices=team_numbers, selected=team_numbers[4]),
            )

    @render_widget
    def placeholder():
        print("hello, world!")


