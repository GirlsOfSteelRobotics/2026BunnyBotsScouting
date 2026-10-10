from shiny import App, ui
from general_match_things import general_match_ui, general_match_server

app_ui = ui.page_navbar(
    ui.nav_panel("A", "Page A content"),
    ui.nav_panel("Matches", general_match_ui("matches")),
    ui.nav_panel("C", "Page C content"),
    title="App with navbar",
)


def server(input, output, session):
    pass
    general_match_server("matches")


app = App(app_ui, server)
