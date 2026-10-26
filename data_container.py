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
    scouted_data["telCarrot"] = (
        scouted_data["telCarrotL1"]
        + scouted_data["telCarrotL2"]
        + scouted_data["telCarrotL3"]
    )
    scouted_data["telCarrotCake"] = (
        scouted_data["telCarrotCakeL1"]
        + scouted_data["telCarrotCakeL2"]
        + scouted_data["telCarrotCakeL3"]
    )
    scouted_data["autoCarrot"] = (
        scouted_data["autoCarrotL1"]
        + scouted_data["autoCarrotL2"]
        + scouted_data["autoCarrotL3"]
    )
    scouted_data["autoCarrotCake"] = (
        scouted_data["autoCarrotCakeL1"]
        + scouted_data["autoCarrotCakeL2"]
        + scouted_data["autoCarrotCakeL3"]
    )
    scouted_data["parkPoints"] = scouted_data["Park"] * 2
    scouted_data["Harvest Haul Carrot Points"] = scouted_data["Harvest Haul Carrots"]
    scouted_data["Harvest Haul Carrot Cake Points"] = (
        scouted_data["Harvest Haul Carrot Cakes"] * 3
    )

    team_averages = (
        scouted_data.groupby("Team and Robot").mean(numeric_only=True).reset_index()
    )

    team_averages["totalAutoOven"] = (
        team_averages["autoCarrotO"] + team_averages["autoCarrotCakeO"]
    )
    team_averages["totalAutoCarrots"] = (
        team_averages["autoCarrotL1"]
        + team_averages["autoCarrotL2"]
        + team_averages["autoCarrotL3"]
    )
    team_averages["totalAutoCarrotCakes"] = (
        team_averages["autoCarrotCakeL1"]
        + team_averages["autoCarrotCakeL2"]
        + team_averages["autoCarrotCakeL3"]
    )

    team_averages["totalTelOven"] = (
        team_averages["telCarrotO"] + team_averages["telCarrotCakeO"]
    )
    team_averages["totalTelCarrots"] = (
        team_averages["telCarrotL1"]
        + team_averages["telCarrotL2"]
        + team_averages["telCarrotL3"]
    )
    team_averages["totalTelCarrotCakes"] = (
        team_averages["telCarrotCakeL1"]
        + team_averages["telCarrotCakeL2"]
        + team_averages["telCarrotCakeL3"]
    )

    scouted_data["Total Auto"] = (
        scouted_data["autoCarrotO"] * 2
        + scouted_data["autoCarrotCakeO"] * 1
        + scouted_data["autoCarrotL1"] * 3
        + scouted_data["autoCarrotL2"] * 4
        + scouted_data["autoCarrotL3"] * 5
        + scouted_data["autoCarrotCakeL1"] * 8
        + scouted_data["autoCarrotCakeL2"] * 10
        + scouted_data["autoCarrotCakeL3"] * 12
        + scouted_data["Auto Cross Kitchen Line"] * 2
    )

    scouted_data["Total Teleop"] = (
        scouted_data["telCarrotO"] * 2
        + scouted_data["telCarrotCakeO"] * 1
        + scouted_data["telCarrotL1"] * 3
        + scouted_data["telCarrotL2"] * 4
        + scouted_data["telCarrotL3"] * 5
        + scouted_data["telCarrotCakeL1"] * 8
        + scouted_data["telCarrotCakeL2"] * 10
        + scouted_data["telCarrotCakeL3"] * 12
    )

    scouted_data["Total Points"] = (
        scouted_data["Total Auto"]
        + scouted_data["Total Teleop"]
        + scouted_data["parkPoints"]
    )

    return scouted_data


def load_match_sched():
    match_sched = pd.read_csv(SCRIPT_DIRECTORY / f"data/mock_data/match_schedule.csv")
    match_sched["Match Number"] = match_sched["Match Number"].astype(str)
    match_sched["R1"] = match_sched["R1"].astype(str)
    match_sched["R2"] = match_sched["R2"].astype(str)
    match_sched["R3"] = match_sched["R3"].astype(str)
    match_sched["B1"] = match_sched["B1"].astype(str)
    match_sched["B2"] = match_sched["B2"].astype(str)
    match_sched["B3"] = match_sched["B3"].astype(str)
    return match_sched


match_sched = load_match_sched()

# lists that I don't want to make again
match_numbers = sorted(list(load_match_sched()["Match Number"]), key=int)
team_numbers = sorted(
    match_sched["R1"].tolist()
    + match_sched["R2"].tolist()
    + match_sched["R3"].tolist()
    + match_sched["B1"].tolist()
    + match_sched["B2"].tolist()
    + match_sched["B3"].tolist(),
    key=int,
)
