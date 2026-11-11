import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data

match_df = load_scouted_data().copy()


def add_breakdown_columns(df):
    df["Pantry Carrots"] = df["autoCarrot"] + df["telCarrot"]
    df["Oven Carrots"] = df["autoCarrotO"] + df["telCarrotO"]

    df["Pantry Carrot Cakes"] = df["autoCarrotCake"] + df["telCarrotCake"]
    df["Oven Carrot Cakes"] = df["autoCarrotCakeO"] + df["telCarrotCakeO"]

    for lvl in ("L1", "L2", "L3"):
        df[f"Teleop Pantry {lvl} (carrots + cakes)"] = (
            df[f"telCarrot{lvl}"] + df[f"telCarrotCake{lvl}"]
        )
    df["Auto Pantry (total, no levels tracked)"] = (
        df["autoCarrot"] + df["autoCarrotCake"]
    )

    return df


match_df = add_breakdown_columns(match_df)


BREAKDOWNS = {
    # multi-line metrics: total + components
    "Carrots": [
        ("Carrots", "Total carrots"),
        ("Pantry Carrots", "Pantry carrots"),
        ("Oven Carrots", "Oven carrots"),
        ("Harvest Haul Carrots", "Harvest Haul carrots"),
    ],
    "Carrot Cakes": [
        ("Carrot Cakes", "Total carrot cakes"),
        ("Pantry Carrot Cakes", "Pantry carrot cakes"),
        ("Oven Carrot Cakes", "Oven carrot cakes"),
        ("Harvest Haul Carrot Cakes", "Harvest Haul carrot cakes"),
    ],
    "Pantry Scoring": [
        ("Pantry Scoring", "Total pantry"),
        ("Teleop Pantry L1 (carrots + cakes)", "Teleop L1"),
        ("Teleop Pantry L2 (carrots + cakes)", "Teleop L2"),
        ("Teleop Pantry L3 (carrots + cakes)", "Teleop L3"),
        ("Auto Pantry (total, no levels tracked)", "Auto pantry (no levels)"),
    ],
    "Oven Scoring": [
        ("Oven Scoring", "Total oven"),
        ("Oven Carrots", "Oven carrots"),
        ("Oven Carrot Cakes", "Oven carrot cakes"),
    ],
}

LINE_COLORS = ["#97AF6E", "#C68540", "#F87828", "#F6AF7D", "#728A46"]


@module.ui
def team_pit_ui():
    teams = sorted(
        [
            t
            for t in match_df["Team and Robot"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        ],
        key=lambda x: int(x),
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
            choices={
                "Auto Points": "Auto Points",
                "Teleop Points": "Teleop Points",
                "Endgame Points": "Endgame Points",
                "Total Points": "Total Points",
                "Carrots": "Carrots Scored",
                "Carrot Cakes": "Carrot Cakes Scored",
                "Pantry Scoring": "Scoring in Pantry",
                "Oven Scoring": "Scoring in Oven",
            },
            selected="Total Points",
        ),
        ui.card(output_widget("team_breakdown_graph")),
        # ui.card(output_widget("team_trend_graph")),
        ui.layout_columns(
            ui.card(
                ui.card_header("Placeholder"),
                ui.output_text("placeholder"),
            ),
        ),
    )


@module.server
def pit_overview_tab_server(input, output, session):
    @render_widget()
    def team_breakdown_graph():
        team = str(input.team_select())
        metric = str(input.y_axis_select())
        components = BREAKDOWNS.get(metric, [(metric, metric)])
        cols = [c for c, _ in components]
        labels = [l for _, l in components]
        label_map = dict(components)

        team_df = match_df[match_df["Team and Robot"].astype(str) == team].copy()
        if team_df.empty:
            return px.scatter(title=f"No match data for Team {team}")

        team_df["Match Number"] = pd.to_numeric(
            team_df["Match Number"], errors="coerce"
        )
        team_df = team_df.dropna(subset=["Match Number"]).sort_values("Match Number")

        long_df = team_df.melt(
            id_vars="Match Number",
            value_vars=cols,
            var_name="Component",
            value_name="Value",
        )
        long_df["Value"] = pd.to_numeric(long_df["Value"], errors="coerce").fillna(0)
        long_df["Component"] = long_df["Component"].map(label_map)

        fig = px.scatter(
            long_df,
            x="Match Number",
            y="Value",
            color="Component",
            category_orders={"Component": labels},
            color_discrete_sequence=LINE_COLORS,
            title=f"Team {team}: {metric} by Match",
        )
        fig.update_traces(mode="markers+lines")
        fig.update_layout(
            yaxis_title=metric,
            showlegend=len(components) > 1,
            legend_title_text="",
        )
        return fig

    # @render_widget()
    # def team_trend_graph():
    #     team = str(input.team_select())
    #     y_axis = str(input.y_axis_select())
    #
    #     team_df = match_df[match_df["Team and Robot"].astype(str) == team].copy()
    #
    #     if team_df.empty:
    #         fig = px.scatter(title=f"No match data for Team {team}")
    #         return fig
    #
    #     team_df["Match Number"] = pd.to_numeric(team_df["Match Number"], errors="coerce")
    #     team_df = team_df.dropna(subset=["Match Number"]).sort_values("Match Number")
    #
    #     team_df["Total Auto Points"] = pd.to_numeric(team_df["Total Auto Points"], errors="coerce").fillna(0)
    #     team_df["Total Teleop Points"] = pd.to_numeric(team_df["Total Teleop Points"], errors="coerce").fillna(0)
    #
    #
    #     fig = px.scatter(team_df, x="Match Number", y=y_axis,
    #                      title=f"Team {team}: {y_axis} by Match", color_discrete_sequence=["#89A45A"])
    #     fig.update_traces(mode="markers+lines")
    #     fig.update_layout(xaxis_title="Match", yaxis_title=y_axis, showlegend=False)
    #     return fig

    @render.text
    def placeholder():
        print("hello, world!")
