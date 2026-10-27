import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data, match_numbers, team_numbers, match_sched

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
                ),
                ui.nav_panel(
                    "Auto",
                    ui.card(output_widget("auto_cross_kitchen_line")),
                    ui.card(output_widget("auto_carrot_pantry_bar")),
                    ui.card(output_widget("auto_carrot_cake_pantry_bar")),
                    ui.card(output_widget("auto_carrot_pantry_box")),
                    ui.card(output_widget("auto_carrot_cake_pantry_box")),
                    ui.card(output_widget("auto_carrot_carrot_cake_oven_bar")),
                    ui.card(output_widget("auto_carrot_oven_box")),
                    ui.card(output_widget("auto_carrot_cake_oven_box")),
                ),
                ui.nav_panel(
                    "Teleop",
                    ui.card(output_widget("tele_carrot_pantry_bar")),
                    ui.card(output_widget("tele_carrot_cake_pantry_bar")),
                    ui.card(output_widget("tele_carrot_pantry_box")),
                    ui.card(output_widget("tele_carrot_cake_pantry_box")),
                    ui.card(output_widget("tele_carrot_carrot_cake_oven")),
                    ui.card(output_widget("tele_carrot_oven_box")),
                    ui.card(output_widget("tele_carrot_cake_oven_box")),
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
    @render.ui
    def match_list_combobox():
        if input.selection_mode() == "Match Number":
            return ui.input_select(
                "match_select", "Match Number:", choices=match_numbers
            )
        else:
            return ui.div(
                ui.input_select(
                    "team1", "Team 1:", choices=team_numbers, selected=team_numbers[0]
                ),
                ui.input_select(
                    "team2", "Team 2:", choices=team_numbers, selected=team_numbers[1]
                ),
                ui.input_select(
                    "team3", "Team 3:", choices=team_numbers, selected=team_numbers[2]
                ),
                ui.input_select(
                    "team4", "Team 4:", choices=team_numbers, selected=team_numbers[3]
                ),
                ui.input_select(
                    "team5", "Team 5:", choices=team_numbers, selected=team_numbers[4]
                ),
                ui.input_select(
                    "team6", "Team 6:", choices=team_numbers, selected=team_numbers[5]
                ),
                ui.input_select(
                    "team1", "Team 1:", choices=team_numbers, selected="3504"
                ),
                ui.input_select(
                    "team2", "Team 2:", choices=team_numbers, selected=team_numbers[0]
                ),
                ui.input_select(
                    "team3", "Team 3:", choices=team_numbers, selected=team_numbers[1]
                ),
                ui.input_select(
                    "team4", "Team 4:", choices=team_numbers, selected=team_numbers[2]
                ),
                ui.input_select(
                    "team5", "Team 5:", choices=team_numbers, selected=team_numbers[3]
                ),
                ui.input_select(
                    "team6", "Team 6:", choices=team_numbers, selected=team_numbers[4]
                )
            )

    def get_teams_in_selected_match():
        if input.selection_mode() == "Match Number":
            match_number = str(input.match_select())
            indices = match_sched["Match Number"] == match_number
            teams = match_sched[indices]
            return teams.values.tolist()[0][1:]
        else:
            teams = [
                str(input.team1()),
                str(input.team2()),
                str(input.team3()),
                str(input.team4()),
                str(input.team5()),
                str(input.team6()),
            ]
        return teams

    def get_teams_in_match_data():
        teams = get_teams_in_selected_match()
        return scouted_data().loc[team_numbers.isin(teams)]

    @render_widget
    def teleop_vs_auto_scatter():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.scatter(small_team_averages, x="")

    @render_widget
    def auto_cross_kitchen_line():
        # avg # times cross kitchen line
        teams_in_match = get_teams_in_selected_match()

    def auto_carrot_cake_pantry_box():
        # L1, L2, L3 pantry carrot cake auto (stacked bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        # small_team_averages = small_team_averages.sort_values("Auto Cross Kitchen Line", ascending=False)
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y="Auto Cross Kitchen Line",
            title="Average Times Each Team Crosses the Kitchen Line",
        )
        return fig

    @render_widget
    def auto_carrot_pantry_bar():
        # L1, L2, L3 pantry carrot auto (stacked bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotL1", "autoCarrotL2", "autoCarrotL3"],
            title="Number of Carrot Scored in Pantry Per Team in Auto",
        )
        return fig

    @render_widget
    def auto_carrot_cake_pantry_bar():
        # L1, L2, L3 pantry carrot cake auto (stacked bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotCakeL1", "autoCarrotCakeL2", "autoCarrotCakeL3"],
            title="Number of Carrot Cakes Scored in Pantry per Team in Auto",
        )
        return fig

    @render_widget
    def auto_carrot_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrot"],
            title="Number of Carrots Scored in Pantry during Auto",
        )
        return fig

    @render_widget
    def auto_carrot_cake_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrotCake"],
            title="Number of Carrot Cakes Scored in Pantry during Auto",
        )
        return fig

    @render_widget
    def auto_carrot_carrot_cake_oven_bar():
        # pantry carrot auto (stacked bar)
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotO", "autoCarrotCakeO"],
            title="Number of Carrots and Carrot Cakes Scored in Oven per Team in Auto",
        )
        return fig

    @render_widget
    def auto_carrot_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrotO"],
            title="Number of Carrots Scored in Oven during Auto",
        )
        return fig

    @render_widget
    def auto_carrot_cake_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrotCakeO"],
            title="Number of Carrot Cakes Scored in Oven during Auto",
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
            title="Number of Carrots Scored in Pantry per Team in Teleop",
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
            title="Number of Carrot Cakes Scored in Pantry Per Team in Teleop",
        )
        return fig

    @render_widget
    def tele_carrot_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrot"],
            title="Number of Carrots Scored in Pantry during Teleop",
        )
        return fig

    @render_widget
    def tele_carrot_cake_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrot"],
            title="Number of Carrot Cakes Scored in Pantry during Teleop",
        )
        return fig

    @render_widget
    def tele_carrot_carrot_cake_oven():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotO", "telCarrotCakeO"],
            title="Number of Carrots and Carrot Cakes Scored in Oven per Team in Teleop",
        )
        return fig

    @render_widget
    def tele_carrot_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrotO"],
            title="Number of Carrots Scored in Oven during Teleop",
        )
        return fig

    @render_widget
    def tele_carrot_cake_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrotCakeO"],
            title="Number of Carrot Cakes Scored in Oven during Teleop",
        )
        return fig

    @render_widget
    def park_harvest_haul():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=[
                "parkPoints",
                "Harvest Haul Carrot Points",
                "Harvest Haul Carrot Cake Points",
            ],
            title="Harvest Haul Carrots and Carrot Cake Points while Parked in Endgame per Team",
        )
        return fig
