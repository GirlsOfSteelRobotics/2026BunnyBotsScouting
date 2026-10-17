from shiny import App, ui
from overview_tab import overview_tab_server, overview_tab_ui
from general_match_things import general_match_server, general_match_ui
from team import pit_overview_tab_ui, pit_overview_tab_server

app_ui = ui.page_navbar(
    ui.nav_panel("A", "Page A content"),
    ui.nav_panel("Matches", general_match_ui("matches")),
    ui.nav_panel("Overview", overview_tab_ui("overview")),
    ui.nav_panel("B", "Page B content"),
    ui.nav_panel("C", "Page C content"),
    title="App with navbar",
)


def server(input, output, session):
    overview_tab_server("overview")
    general_match_server("matches")
    pit_overview_tab_server("team")


app = App(app_ui, server)
