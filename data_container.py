import pathlib
import pandas as pd

EVENT_KEY = "mock_data"

SCOUTED_COLUMNS = [
    "Scouter Initials",
    "Match Number",
    "Team and Robot",
    "Starting Position",
    "No Show",
    "autoCarrotO",
    "autoCarrotCakeO",
    "autoCarrotL1",
    "autoCarrotL2",
    "autoCarrotL3",
    "autoCarrotCakeL1",
    "autoCarrotCakeL2",
    "autoCarrotCakeL3",
    "telCarrotO",
    "telCarrotCakeO",
    "telCarrotL1",
    "telCarrotL2",
    "telCarrotL3",
    "telCarrotCakeL1",
    "telCarrotCakeL2",
    "telCarrotCakeL3",
    "Auto Cross Kitchen Line",
    "Auto Robot Stuck or Astop in Auto?",
    "Harvest Haul Carrots",
    "Harvest Haul Carrot Cakes",
    "Defended by opponent?",
    "Opposing Zone Actions",
    "Park",
    "Mechanical Issue?",
    "Died?",
    "Tipped/Fell Over",
    "Scoring Effectiveness",
    "Defense Skill",
    "Yellow/Red Card",
    # "Comments",
]

SCRIPT_DIRECTORY = pathlib.Path(__file__).resolve().parent


def load_scouted_data():
    scouted_data = pd.read_csv(
        SCRIPT_DIRECTORY / f"data/{EVENT_KEY}/scouted_data.tsv", sep="\t"
    )
    scouted_data["Team and Robot"] = scouted_data["Team and Robot"].astype(str)
    scouted_data["telCarrot"] = scouted_data["telCarrotL1"] + scouted_data["telCarrotL2"] + scouted_data["telCarrotL3"]
    scouted_data["telCarrotCake"] = scouted_data["telCarrotCakeL1"] + scouted_data["telCarrotCakeL2"] + scouted_data[
        "telCarrotCakeL3"]
    scouted_data["autoCarrot"] = scouted_data["autoCarrotL1"] + scouted_data["autoCarrotL2"] + scouted_data[
        "autoCarrotL3"]
    scouted_data["autoCarrotCake"] = scouted_data["autoCarrotCakeL1"] + scouted_data["autoCarrotCakeL2"] + scouted_data[
        "autoCarrotCakeL3"]
    scouted_data["parkPoints"] = scouted_data["Park"]*2
    scouted_data["Harvest Haul Carrot Points"] = scouted_data["Harvest Haul Carrots"]
    scouted_data["Harvest Haul Carrot Cake Points"] = scouted_data["Harvest Haul Carrot Cakes"]*3


    return scouted_data
