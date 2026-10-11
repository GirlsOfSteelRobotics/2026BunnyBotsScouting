from shiny import App, ui
from general_match_things import general_match_ui
from team import team_pit_trend_ui

app_ui = ui.page_navbar(
    ui.nav_panel("A", "Page A content"),
    ui.nav_panel("Matches", general_match_ui("matches")),
    ui.nav_panel("Team", team_pit_trend_ui("team")),
    title="App with navbar",
)


def server(input, output, session):
    pass


app = App(app_ui, server)
