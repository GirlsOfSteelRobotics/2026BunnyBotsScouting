import os
from shinywidgets import output_widget, render_widget
from shiny import App, ui
from shiny import reactive, render, module
from data_container import load_scouted_data, match_numbers, team_numbers, scouted_data
import pandas as pd
import plotly.express as px
import numpy as np

pd.set_option("display.max_columns", None)

team_averages = (
    scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()
)
# don't include data for no-show so it doesn't skew the data?
# team_averages = (
#     scouted_data[~scouted_data["No Show"]].groupby("Team and Robot").mean(numeric_only=True).reset_index()
# )


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        ui.input_select(
            "y_axis_select",
            "Y Axis:",
            choices=[
                "Total Auto Points",
                "Total Teleop Points",
                "Endgame Points",
                "Total Points",
                "Carrots",
                "Carrot Cakes",
            ],
        ),
        ui.input_radio_buttons(
            "selection_mode",
            "Select By:",
            choices=["Team Number", "Stat"],
            selected="Team Number",
        ),
        ui.card(output_widget("robot_stat")),
        ui.card(output_widget("teleop_v_autoend_all")),
    )


@module.server
def overview_tab_server(input, output, session):
    @render_widget()
    def robot_stat():
        new_averages = team_averages.copy()

        y_axis = str(input.y_axis_select())

        if input.selection_mode() == "Team Number":
            sorted_df = new_averages.sort_values(
                by="Team and Robot", key=lambda x: x.astype(int)
            )
        else:
            sorted_df = new_averages.sort_values(by=y_axis, ascending=False)

        fig = px.bar(
            sorted_df,
            x=sorted_df["Team and Robot"],
            y=y_axis,
            title=f"{y_axis} (Averages) by Team",
            color_discrete_sequence=["#F87828"],
        )
        fig.update_traces(
            hovertemplate=(
                "<b>Team %{x}</b><br>" f"{y_axis}: %{{y:.1f}}<br>" "<extra></extra>"
            ),
        )

        fig.update_layout(
            xaxis_title="Team Number",
            yaxis_title=y_axis,
            hovermode="closest",
            showlegend=False,
        )
        return fig

    @render_widget
    def teleop_v_autoend_all():

        fig = px.scatter(
            team_averages,
            x="Total Teleop Points",
            y="Auto and Endgame Points",
            color="Total Points",
            color_continuous_scale="ylorrd_r",
            title="Teleop v. Auto + Endgame Points",
            text="Team and Robot",
            hover_name="Team and Robot",
            hover_data={
                "Total Teleop Points": ":.1f",
                "Auto and Endgame Points": ":.1f",
                "Total Points": ":.1f",
                "Team and Robot": False,
            },
            labels={
                "Total Teleop Points": "Teleop Points",
                "Auto and Endgame Points": "Auto + Endgame Points",
                "Team and Robot": "Team",
                "Total Points": "Total Points",
            },
        )

        fig.update_traces(marker=dict(size=8), textposition="middle left")
        fig.update_layout(
            coloraxis_colorbar=dict(title="Total Points"),
        )

        return fig
