import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data

scouted_data = load_scouted_data()
team_averages = scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()

@module.ui
def general_match_ui():
    return ui.page_fluid(
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_radio_buttons(
                    "selection_mode",
                    "Select By:",
                    choices=["Match Number", "Pick 6 Teams"],
                    selected="Match Number",
                ),
                ui.output_ui("match_list_combobox"),
            ),
            ui.navset_tab(
                ui.nav_panel(
                    "Overall",
                    ui.card(output_widget("teleop_vs_auto_scatter")),
                ),
                ui.nav_panel(
                    "Auto",
                    ui.card(output_widget("auto_cross_kitchen_line")),
                    ui.card(output_widget("auto_carrot_pantry_bar")),
                    ui.card(output_widget("auto_carrot_cake_pantry_bar")),
                    ui.card(output_widget("auto_carrot_pantry_box")),
                    ui.card(output_widget("auto_carrot_cake_pantry_box")),
                    ui.card(output_widget("auto_carrot_oven")),
                    ui.card(output_widget("auto_carrot_cake_oven")),
                ),
                ui.nav_panel(
                    "Teleop",
                    ui.card(output_widget("tele_carrot_pantry_bar")),
                    ui.card(output_widget("tele_carrot_cake_pantry_bar")),
                    ui.card(output_widget("tele_carrot_pantry_box")),
                    ui.card(output_widget("tele_carrot_cake_pantry_box")),
                    ui.card(output_widget("tele_carrot_oven")),
                    ui.card(output_widget("tele_carrot_cake_oven")),
                ),
                ui.nav_panel(
                    "Endgame",
                    ui.card(output_widget("park_harvest_haul")),
                ),
            ),
        )
    )

@module.server
def general_match_server(input,output,session):

    def get_teams_in_selected_match():
        return ["3504","340","3015","5667","4467"]

    @render_widget
    def auto_carrot_cake_pantry_box():
        # L1, L2, L3 pantry carrot cake auto (stacked bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(small_team_averages, x="Team and Robot",
                     y=["autoCarrotCakeL1", "autoCarrotCakeL2", "autoCarrotCakeL3"],
                     title="# of Carrot Cakes Scored in Pantry per Team in Auto")
        return fig
    @render_widget
    def tele_carrot_cake_pantry_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(small_team_averages, x="Team and Robot", y=["telCarrotCakeL1", "telCarrotCakeL2", "telCarrotCakeL3"],
                     title="# of Carrot Cakes Scored in Pantry Per Team in Tele")
        return fig

