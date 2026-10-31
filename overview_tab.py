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


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        ui.card(output_widget("placeholder")),
        ui.card(output_widget("teleop_v_autoend_all")),
    )


@module.server
def overview_tab_server(input, output, session):

    @render_widget
    def teleop_v_autoend_all():

        fig = px.scatter(team_averages, x = "allTeleop", y = "autoEnd", color = "allPoints", color_continuous_scale = "Plasma",
                     title = "Teleop v. Auto + Endgame Points", text = "Team and Robot", hover_name="Team and Robot",
                     hover_data={
                         "allTeleop": ":.1f",
                         "autoEnd": ":.1f",
                         "allPoints": ":.1f",
                         "Team and Robot": False
                     },
                     labels={
                         "allTeleop": "Teleop Points",
                         "autoEnd": "Auto + Endgame Points",
                         "Team and Robot": "Team",
                         "allPoints": "Total Points"
                     },

                         )

        fig.update_traces(
            marker=dict(size=8),
            textposition='middle left'
        )
        fig.update_layout(
            coloraxis_colorbar=dict(title="Total Points"),
        )

        return fig

