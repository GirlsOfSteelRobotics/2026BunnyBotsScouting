import pathlib
import pandas as pd

EVENT_KEY = "mock_data"

SCOUTED_COLUMNS = [
    "scout",
    "number",
    "robot",
    "teamNumber",
    "autoPantry",
    "autoOven",
    "autoCakes",
    "L1C," "L2C," "L3C," "CO",
    "L1CC",
    "L2CC",
    "L3CC",
    "CCO",
    "CH",
    "CCH",
    "IK",
    "INZ",
    "ID",
    "noShow",
    "startPos",
    "defenseStrat",
    "defenseEff",
    "scoringEff",
    "driverRating",
    "died",
]

SCRIPT_DIRECTORY = pathlib.Path(__file__).resolve().parent


def load_scouted_data():
    scouted_data = pd.read_csv(
        SCRIPT_DIRECTORY / f"data/{EVENT_KEY}/scouted_data.tsv", sep="\t"
    )
    scouted_data["Team and Robot"] = scouted_data["Team and Robot"].astype(str)

    scouted_data["telCarrot"] = (
        scouted_data["L1C"] + scouted_data["L2C"] + scouted_data["L3C"]
    )
    scouted_data["telCarrotCake"] = (
        scouted_data["L1CC"] + scouted_data["L2CC"] + scouted_data["L3CC"]
    )

    scouted_data["parkPoints"] = scouted_data["Park"] * 2
    scouted_data["Harvest Haul Carrot Points"] = scouted_data["CH"]
    scouted_data["Harvest Haul Carrot Cake Points"] = scouted_data["CCH"] * 3

    scouted_data["Endgame Points"] = (
        scouted_data["parkPoints"]
        + scouted_data["Harvest Haul Carrot Points"]
        + scouted_data["Harvest Haul Carrot Cake Points"]
    )

    scouted_data["telOven"] = scouted_data["CO"] + scouted_data["CCO"]

    scouted_data["Oven Scoring"] = scouted_data["autoOven"] + scouted_data["telOven"]

    scouted_data["teleopPantry"] = (
        scouted_data["telCarrot"] + scouted_data["telCarrotCake"]
    )

    scouted_data["Pantry Scoring"] = (
        scouted_data["autoPantry"] + scouted_data["teleopPantry"]
    )

    scouted_data["Carrots Scored"] = (
        scouted_data["autoPantry"]
        + scouted_data["autoOven"]
        + scouted_data["telCarrot"]
        + scouted_data["CO"]
        + scouted_data["CH"]
    )

    scouted_data["Carrot Cakes Scored"] = (
        +scouted_data["telCarrotCake"] + scouted_data["CCO"] + scouted_data["CCH"]
    )

    scouted_data["Auto Points"] = (
        scouted_data["autoOven"] * 2
        + scouted_data["autoPantry"] * 4
        + scouted_data["Auto Taxi"] * 2
    )

    scouted_data["Teleop Points"] = (
        scouted_data["CO"] * 2
        + scouted_data["CCO"] * 1
        + scouted_data["L1C"] * 3
        + scouted_data["L2C"] * 4
        + scouted_data["L3C"] * 5
        + scouted_data["L1CC"] * 8
        + scouted_data["L2CC"] * 10
        + scouted_data["L3CC"] * 12
    )

    scouted_data["Auto and Endgame Points"] = (
        scouted_data["Auto Points"] + scouted_data["Endgame Points"]
    )

    scouted_data["Total Points"] = (
        scouted_data["Auto Points"]
        + scouted_data["Teleop Points"]
        + scouted_data["Endgame Points"]
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

# variables that i dont want to make again
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
scouted_data = load_scouted_data()
