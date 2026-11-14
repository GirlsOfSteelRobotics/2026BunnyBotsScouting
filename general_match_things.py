import pandas as pd
import numpy as np
import plotly.express as px
from numpy.f2py.f2py2e import show
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data
import plotly.graph_objects as go
from data_container import (
    load_scouted_data,
    match_numbers,
    team_numbers,
    match_sched,
    scouted_data,
)

team_averages = (
    scouted_data[~scouted_data["No Show"]]
    .groupby("Team and Robot")
    .mean(numeric_only=True)
    .reset_index()
)

blue_stacked = ["#0E3964", "#236194", "#619DC3"]
red_stacked = ["#730F1A", "#AB0D0C", "#D42626"]


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
                    ui.card(output_widget("auto_carrot_oven_bar")),
                    ui.card(output_widget("auto_carrot_cake_oven_box")),
                    ui.card(output_widget("auto_carrot_cake_oven_bar")),
                ),
                ui.nav_panel(
                    "Teleop",
                    ui.card(output_widget("tele_carrot_pantry_bar")),
                    ui.card(output_widget("tele_carrot_cake_pantry_bar")),
                    ui.card(output_widget("tele_carrot_pantry_box")),
                    ui.card(output_widget("tele_carrot_cake_pantry_box")),
                    ui.card(output_widget("tele_carrot_carrot_cake_oven")),
                    ui.card(output_widget("tele_carrot_oven_box")),
                    ui.card(output_widget("tele_carrot_oven_bar")),
                    ui.card(output_widget("tele_carrot_cake_oven_box")),
                    ui.card(output_widget("tele_carrot_cake_oven_bar")),
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

    def stacked_colors(fig):
        teams = get_teams_in_selected_match()
        red_teams = teams[0:3]
        for i, trace in enumerate(fig.data):
            trace.marker.color = [
                red_stacked[i] if str(x) in red_teams else blue_stacked[i]
                for x in trace.x
            ]
        fig.update_xaxes(
            categoryorder="array",
            categoryarray=[str(t) for t in teams],
        )

    def single_colors():
        teams = get_teams_in_selected_match()
        red_teams = teams[0:3]
        blue_teams = teams[3:6]
        color_map = {t: "#961410" for t in red_teams}
        color_map.update({t: "#4577B0" for t in blue_teams})
        return dict(
            color="Team and Robot",
            color_discrete_map=color_map,
            category_orders={"Team and Robot": teams},
        )

    @render_widget
    def teleop_vs_auto_scatter():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.scatter(
            small_team_averages,
            x="Teleop Points",
            y="Auto and Endgame Points",
            title="Average Teleop v. Auto and Endgame",
            hover_name="Team and Robot",
            hover_data={
                "Teleop Points": ":.1f",
                "Auto and Endgame Points": ":.1f",
                "Total Points": ":.1f",
                "Team and Robot": False,
            },
            labels={
                "Teleop Points": "Teleop Points",
                "Auto and Endgame Points": "Auto + Endgame Points",
                "Team and Robot": "Team",
                "Total Points": "Total Points",
            },
            **single_colors(),
        )

        fig.update_traces(
            marker=dict(size=8),
            textposition="top center",
        )

        return fig

    @render_widget
    def auto_cross_kitchen_line():
        # avg # times cross kitchen line
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y="Auto Cross Kitchen Line",
            title="Avg. Times Each Team Crossed Kitchen Line",
            **single_colors(),
        )
        fig.update_layout(showlegend=False)
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
            title="Number of Carrots Scored in Pantry per Team during Auto",
        )
        fig.update_layout(yaxis_title="Carrots per Level"),
        stacked_colors(fig)
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
            title="Number of Carrot Cakes Scored in Pantry per Team during Auto",
        )
        fig.update_layout(yaxis_title="Carrot Cakes per Level"),
        stacked_colors(fig)
        return fig

    @render_widget
    def auto_carrot_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrot"],
            title="Number of Carrots Scored in Pantry per Team during Auto",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrots", showlegend=False),
        return fig

    @render_widget
    def auto_carrot_cake_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrotCake"],
            title="Number of Carrot Cakes Scored in Pantry per Team during Auto",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrot Cakes", showlegend=False),
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
            title="Number of Carrots and Carrot Cakes Scored in Oven per Team during Auto",
        )
        fig.update_layout(yaxis_title="Carrots and Carrots Cakes"),
        stacked_colors(fig)
        return fig

    @render_widget
    def auto_carrot_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrotO"],
            title="Number of Carrots Scored in Oven per Team during Auto",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrots", showlegend=False),
        return fig

    @render_widget
    def auto_carrot_oven_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotO"],
            title="Number of Carrots Scored in Oven per Team during Auto",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrots", showlegend=False)
        return fig

    @render_widget
    def auto_carrot_cake_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["autoCarrotCakeO"],
            title="Number of Carrot Cakes Scored in Oven per Team during Auto",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrot Cakes", showlegend=False),
        return fig

    @render_widget
    def auto_carrot_cake_oven_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["autoCarrotCakeO"],
            title="Number of Carrot Cakes Scored in Oven per Team during Auto",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrot Cakes", showlegend=False)
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
            title="Number of Carrots Scored in Pantry per Team during Teleop",
        )
        fig.update_layout(yaxis_title="Carrots per Level"),
        stacked_colors(fig)
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
            title="Number of Carrot Cakes Scored in Pantry per Team during Teleop",
        )
        fig.update_layout(yaxis_title="Carrot Cakes per Level"),
        stacked_colors(fig)
        return fig

    @render_widget
    def tele_carrot_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrot"],
            title="Number of Carrots Scored in Pantry per Team during Teleop",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrots", showlegend=False),
        return fig

    @render_widget
    def tele_carrot_cake_pantry_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrotCake"],
            title="Number of Carrot Cakes Scored in Pantry per Team during Teleop",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrot Cakes", showlegend=False),
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
            title="Number of Carrots and Carrot Cakes Scored in Oven per Team during Teleop",
        )
        fig.update_layout(yaxis_title="Carrots and Carrot Cakes"),
        stacked_colors(fig)
        return fig

    @render_widget
    def tele_carrot_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrotO"],
            title="Number of Carrots Scored in Oven per Team during Teleop",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrots", showlegend=False),
        return fig

    @render_widget
    def tele_carrot_oven_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotO"],
            title="Number of Carrots Scored in Oven per Team during Teleop",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrot", showlegend=False)
        return fig

    @render_widget
    def tele_carrot_cake_oven_box():
        teams_in_match = get_teams_in_selected_match()
        result = scouted_data[scouted_data["Team and Robot"].isin(teams_in_match)]
        fig = px.box(
            result,
            x="Team and Robot",
            y=["telCarrotCakeO"],
            title="Number of Carrot Cakes Scored in Oven per Team during Teleop",
            **single_colors(),
        )
        fig.update_layout(yaxis_title="Carrot Cakes", showlegend=False),
        return fig

    @render_widget
    def tele_carrot_cake_oven_bar():
        teams_in_match = get_teams_in_selected_match()
        indices = team_averages["Team and Robot"].isin(teams_in_match)
        small_team_averages = team_averages[indices]
        fig = px.bar(
            small_team_averages,
            x="Team and Robot",
            y=["telCarrotCakeO"],
            title="Number of Carrot Cakes Scored in Oven per Team during Teleop",
            **single_colors(),
        )
        fig.update_layout(xaxis_title="Carrot Cakes", showlegend=False)
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
        fig.update_layout(yaxis_title="Park, Carrots, and Carrot Cake Points"),
        stacked_colors(fig)
        return fig
