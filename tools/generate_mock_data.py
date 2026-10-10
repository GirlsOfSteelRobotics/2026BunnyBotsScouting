from tools.mock_data_utils import IntValue, BooleanValue, EnumValue
from typing import Optional
from data_container import SCOUTED_COLUMNS
import random
import pandas as pd


class TeamConfig:
    # This list should be in the same order and column count as SCOUTED_COLUMNS
    def __init__(
        self,
        starting_position: Optional[EnumValue] = None,
        no_show: Optional[BooleanValue] = None,
        autoCarrotO: Optional[IntValue] = None,
        autoCarrotCakeO: Optional[IntValue] = None,
        autoCarrotL1: Optional[IntValue] = None,
        autoCarrotL2: Optional[IntValue] = None,
        autoCarrotL3: Optional[IntValue] = None,
        autoCarrotCakeL1: Optional[IntValue] = None,
        autoCarrotCakeL2: Optional[IntValue] = None,
        autoCarrotCakeL3: Optional[IntValue] = None,
        telCarrotO: Optional[IntValue] = None,
        telCarrotCakeO: Optional[IntValue] = None,
        telCarrotL1: Optional[IntValue] = None,
        telCarrotL2: Optional[IntValue] = None,
        telCarrotL3: Optional[IntValue] = None,
        telCarrotCakeL1: Optional[IntValue] = None,
        telCarrotCakeL2: Optional[IntValue] = None,
        telCarrotCakeL3: Optional[IntValue] = None,
        auto_cross_kitchen_line: Optional[BooleanValue] = None,
        auto_robot_stuck_or_astop_in_auto: Optional[BooleanValue] = None,
        harvest_haul_carrots: Optional[IntValue] = None,
        harvest_haul_carrots_cake: Optional[IntValue] = None,
        defended_by_opponent: Optional[BooleanValue] = None,
        opposing_zone_actions: Optional[EnumValue] = None,
        park: Optional[BooleanValue] = None,
        mechanical_issue: Optional[BooleanValue] = None,
        died: Optional[BooleanValue] = None,
        tipped_or_fell_over: Optional[BooleanValue] = None,
        scoring_effectiveness: Optional[IntValue] = None,
        defense_skill: Optional[IntValue] = None,
        yellow_red_card: Optional[EnumValue] = None,
    ):
        self.fields = [
            starting_position or EnumValue(["Alliance Pantry","Alliance Oven/Ramp","Middle Driver Station","Other"],[30,30,30,10]),
            no_show or BooleanValue(0.95),
            autoCarrotO or IntValue(0, 5),
            autoCarrotCakeO or IntValue(0, 2),
            autoCarrotL1 or IntValue(0, 5),
            autoCarrotL2 or IntValue(0, 5),
            autoCarrotL3 or IntValue(0, 5),
            autoCarrotCakeL1 or IntValue(0, 2),
            autoCarrotCakeL2 or IntValue(0, 2),
            autoCarrotCakeL3 or IntValue(0, 2),
            telCarrotO or IntValue(0, 30),
            telCarrotCakeO or IntValue(0, 20),
            telCarrotL1 or IntValue(0, 30),
            telCarrotL2 or IntValue(0, 30),
            telCarrotL3 or IntValue(0, 30),
            telCarrotCakeL1 or IntValue(0, 20),
            telCarrotCakeL2 or IntValue(0, 20),
            telCarrotCakeL3 or IntValue(0, 20),
            auto_cross_kitchen_line or BooleanValue(0.95),
            auto_robot_stuck_or_astop_in_auto or BooleanValue(0.95),
            harvest_haul_carrots or IntValue(0, 3),
            harvest_haul_carrots_cake or IntValue(0, 1),
            defended_by_opponent or BooleanValue(0.05),
            opposing_zone_actions or EnumValue(["Collecting","Defense"],[50,50]),
            park or BooleanValue(0.05),
            mechanical_issue or BooleanValue(0.5),
            died or BooleanValue(0.95),
            tipped_or_fell_over or BooleanValue(0.95),
            scoring_effectiveness or IntValue(0,5),
            defense_skill or IntValue(0,5),
            yellow_red_card or EnumValue(["No Card","Yellow Card","Red Card"],[85,10,5]),
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
