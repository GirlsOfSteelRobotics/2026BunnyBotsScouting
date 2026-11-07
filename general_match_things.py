import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data
import plotly.graph_objects as go

scouted_data = load_scouted_data()
team_averages = (
    scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()
)

blue_stacked=["#0E3964","#236194","#619DC3"]

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
def general_match_server(input, output, session):

    def get_teams_in_selected_match():
        return ["3504", "340", "3015", "5667", "4467"]

    def get_box_plot_colors():
        teams = get_teams_in_selected_match()
        blue_teams = teams[0:3]
        red_teams = teams[3:6]
        color_map = {str(team): "#961410" for team in blue_teams}
        color_map.update({str(team): "4577b0" for team in red_teams})
        return dict(
            color="Team Number",
            color_discrete_map=color_map,
        )

    @render_widget
    def auto_carrot_cake_pantry_box():
        # L1, L2, L3 pantry carrot cake auto (stacked bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]

        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotCakeL1", "autoCarrotCakeL2", "autoCarrotCakeL3"],
            title="# of Carrot Cakes Scored in Pantry per Team in Auto",
            color_discrete_sequence=blue_stacked
        )
        return fig

    @render_widget
    def tele_carrot_cake_pantry_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotCakeL1", "telCarrotCakeL2", "telCarrotCakeL3"],
            title="# of Carrot Cakes Scored in Pantry Per Team in Tele",
        )
        return fig

    @render_widget
    def tele_carrot_oven():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotO"],
            title="# of Carrots Scored in Oven by a Team for Tele",
        )
        return fig

    @render_widget
    def auto_carrot_oven():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotO"],
            title="# of Carrots Scored in Oven by a Team for Auto",
        )
        return fig

    @render_widget
    def tele_carrot_pantry_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotL1", "telCarrotL2", "telCarrotL3"],
            title="# of cakes scored in pantry per team in tele",
        )
        return fig

    @render_widget
    def auto_carrot_pantry_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotL1", "autoCarrotL2", "autoCarrotL3"],
            title="# of carrots scored in pantry per team in auto",
        )
        return fig

