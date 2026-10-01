from tools.mock_data_utils import IntValue, BooleanValue, EnumValue
from typing import Optional
from data_container import SCOUTED_COLUMNS
import random
import pandas as pd


class TeamConfig:
    # This list should be in the same order and column count as SCOUTED_COLUMNS
    def __init__(
        self,
        no_show: Optional[BooleanValue] = None,
        auto_pantry_carrots: Optional[IntValue] = None,
        auto_oven_carrots: Optional[IntValue] = None,
        tele_pantry_carrots: Optional[IntValue] = None,
        auto_pantry_carrot_cake: Optional[IntValue] = None,
        auto_oven_carrot_cake: Optional[IntValue] = None,
        auto_cross_kitchen_line: Optional[BooleanValue] = None,
        auto_robot_stuck_or_astop_in_auto: Optional[BooleanValue] = None,
        tele_pantry_carrots_cake: Optional[IntValue] = None,
        tele_oven_carrots_cake: Optional[IntValue] = None,
        tele_oven_carrots: Optional[IntValue] = None,
        harvest_haul_carrots: Optional[IntValue] = None,
        harvest_haul_carrots_cake: Optional[IntValue] = None,
    ):
        self.fields = [
            no_show or BooleanValue(0.95),
            auto_pantry_carrots or IntValue(0,2),
            auto_pantry_carrot_cake or IntValue(0, 2),
            auto_oven_carrots or IntValue(0,10),
            auto_oven_carrot_cake or IntValue(0, 1),
            auto_cross_kitchen_line or BooleanValue(0.05),
            auto_robot_stuck_or_astop_in_auto or BooleanValue (0.96),
            tele_pantry_carrots or IntValue(0, 25),
            tele_pantry_carrots_cake or IntValue(0,7),
            tele_oven_carrots or IntValue(0, 30),
            tele_oven_carrots_cake or IntValue(0,10),
            harvest_haul_carrots or IntValue(0,2),
            harvest_haul_carrots_cake or IntValue (0,1),
        ]

    def generate_data(self):
        data = []

        for field in self.fields:
            data.append(field.get_value())

        return data


def populate_from_previous_event():
    teams = set()
    matches = []

    match_schedule = pd.read_csv("data/mock_data/match_schedule.csv")

    for _, row in match_schedule.iterrows():
        match_number = int(row["Match Number"])
        red_teams = [int(row["R1"]), int(row["R2"]), int(row["R3"])]
        blue_teams = [int(row["B1"]), int(row["B2"]), int(row["B3"])]
        teams.update(red_teams + blue_teams)

        matches.append([match_number] + red_teams + blue_teams)

    teams = sorted(teams)

    team_configs = {}

    for team in teams:
        team_configs[team] = TeamConfig()

    return team_configs, teams, matches


def main():
    random.seed(3504)

    team_configs, team_numbers, matches = populate_from_previous_event()

    scouted_data = []
    scouted_data.append(SCOUTED_COLUMNS)

    match_schedule = []
    match_schedule.append(["Match Number", "R1", "R2", "R3", "B1", "B2", "B3"])

    num_scouted_matches = 28
    for i, match_data in enumerate(matches):
        match_number = match_data[0]
        teams = match_data[1:]

        match_schedule.append(match_data)

        if i < num_scouted_matches:
            for team in teams:
                scouted_data.append(
                    ["abc", match_number, team, *team_configs[team].generate_data()]
                )

    with open("data/mock_data/scouted_data.tsv", "w") as f:
        for row in scouted_data:
            f.write("\t".join(str(x) for x in row))
            f.write("\n")

    with open("data/mock_data/match_schedule.csv", "w") as f:
        for row in match_schedule:
            f.write(",".join(str(x) for x in row))
            f.write("\n")


if __name__ == "__main__":
    # python3 -m tools.generate_mock_data
    main()
