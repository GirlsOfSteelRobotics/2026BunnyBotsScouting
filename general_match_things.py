import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data

scouted_data = load_scouted_data()
team_averages = (
    scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()
)


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
                    ui.card(output_widget("one_team_pantry_progress_stacked_scatter")),
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
                    ui.card(output_widget("cross_kitchen_line_bar")),
                ),
                ui.nav_panel(
                    "Teleop",
                    ui.card(output_widget("tele_carrot_pantry_bar")),
                    ui.card(output_widget("tele_carrot_cake_pantry_bar")),
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

    @render_widget
    def auto_carrot_pantry_box():
        # L1, L2, L3 pantry carrot auto (box and whisker)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.box(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotL1", "autoCarrotL2", "autoCarrotL3"],
            title="# of Carrots Scored in Pantry per Team in Auto",
        )
        return fig

    @render_widget
    def tele_carrot_pantry_bar():
        # L1, L2, L3 pantry carrot tele (box and whisker)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotL1", "telCarrotL2", "telCarrotL3"],
            title="# of Carrots Scored in Pantry per Team in Teleop",
        )
        return fig

    @render_widget
    def cross_kitchen_line_bar():
        # cross kitchen line (bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["Auto Cross Kitchen Line"],
            title="Average Times each Team Crosses the Kitchen Line",
        )
        return fig

    @render_widget
    def one_team_pantry_progress_stacked_scatter():
        # progress of one team scoring in L1, L2, L3 pantry over time (stacked scatter plot)
        teamdata = scouted_data["Team and Robot"] == "3504"
        indices = scouted_data[teamdata]
        fig = px.area(
            indices,
            x="Match Number",
            y=["telCarrotL1", "telCarrotL2", "telCarrotL3"],
            title="Progression of Team Performance Scoring in Pantry",
        )
        return fig

    @render_widget
    def park_harvest_haul():
        # park, carrots, carrot cakes (stacked bar) #19
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["Park", "Harvest Haul Carrots", "Harvest Haul Carrot Cakes"],
            title="# of Harvest Haul Carrots and Carrot Cakes per Team",
        )
        return fig
