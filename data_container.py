import pathlib
import pandas as pd

EVENT_KEY = "mock_data"

SCOUTED_COLUMNS = [
    "Scouter Initials",
    "Match Number",
    "Team and Robot",
    "Starting Position",
    "No Show",
    "Pantry Carrot Scoring",
    "Pantry Carrot Cake Scoring",
    "Oven Carrot Scoring",
    "Oven Carrot Cake Scoring",
    "Cross Kitchen Line",
    "Robot Stuck or Astop in Auto?",
    "Pantry Carrot Scoring",
    "Pantry Carrot Cake Scoring",
    "Oven Carrot Scoring",
    "Oven Carrot Cake Scoring",
    "Defended by opponent?",
    "Opposing Zone Actions",
    "Park",
    "Harvest Haul Carrots",
    "Harvest Haul Carrot Cakes",
    "Mechanical Issue?",
    "Died?",
    "Tipped/Fell Over",
    "Scoring Effectiveness",
    "Defense Skill",
    "Yellow/Red Card",
    "Comments",
]

SCRIPT_DIRECTORY = pathlib.Path(__file__).resolve().parent

def load_scouted_data():
    scouted_data = pd.read_csv(SCRIPT_DIRECTORY / f'data/{EVENT_KEY}/scouted_data.tsv', sep='\t')

    return scouted_data
    