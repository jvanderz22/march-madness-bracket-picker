import re
from pathlib import Path
import json

from scraper import KenpomScraper

base_path = Path(__file__).parent.parent.parent
tournament_file_dir = base_path / "data/tournament_data"


class TeamDataScraper(KenpomScraper):
    def __init__(self):
        super().__init__()
        tournament_file = "ncaa_mens_2021_bracket.json"
        tournament_file_data = open(tournament_file_dir / tournament_file, "r")
        tournament_data = json.load(tournament_file_data)
        self.teams = [team_data["team"] for team_data in tournament_data["bracket"]]

    def scrape(self):
        with self.browser() as browser:
            self.sign_in(browser)
            self.find_teams_data(browser)

    def find_teams_data(self, browser):
        teams_data = {}
        for team in self.teams:
            teams_data[team] = self.get_team_data(browser, team)
        self.write_data(teams_data)

    def navigate_home(self, browser):
        browser.get(self.home_address)

    def navigate_to_team(self, browser, team):
        team_link = browser.find_element_by_link_text(team)
        if team_link is None:
            print("Could not find team link")
            return False
        team_link.click()
        return True

    def get_team_data(self, browser, team):
        self.navigate_home(browser)
        navigated_to_team = self.navigate_to_team(browser, team)
        if navigated_to_team is False:
            print(f"Could not get data for team {team}")
            return
        page_data = browser.page_source
        return self.team_data(page_data)

    def data_value(self, data_string, element_label, td_num):
        element_pos = data_string.index(element_label)
        trimmed_string = data_string[element_pos : element_pos + 600]
        average_data_str = trimmed_string.split("<td")[td_num]
        matched_data = re.search("((\+*)(-*)(\d*)\.(\d+))", average_data_str)
        if matched_data is None:
            print(f"No Data found for {element_label}")
            return None
        return matched_data[0]

    def team_data(self, data_string):
        return {
            "off_eff": self.match_value(data_string, "RankAdjOE"),
            "off_eff_rank": self.match_rank(data_string, "RankAdjOE"),
            "def_eff": self.match_value(data_string, "RankAdjDE"),
            "def_eff_rank": self.match_rank(data_string, "RankAdjDE"),
            "tempo": self.match_value(data_string, "RankAdjTempo"),
            "off_efg": self.match_value(data_string, "RankeFG_Pct"),
            "off_efg_rank": self.match_rank(data_string, "RankeFG_Pct"),
            "def_efg": self.match_value(data_string, "RankDeFG_Pct"),
            "def_efg_rank": self.match_rank(data_string, "RankDeFG_Pct"),
            "off_turnover": self.match_value(data_string, "RankTO_Pct"),
            "off_turnover_rank": self.match_rank(data_string, "RankTO_Pct"),
            "def_turnover": self.match_value(data_string, "RankDTO_Pct"),
            "def_turnover_rank": self.match_rank(data_string, "RankDTO_Pct"),
            "off_reb": self.match_value(data_string, "RankOR_Pct"),
            "off_reb_rank": self.match_rank(data_string, "RankOR_Pct"),
            "def_reb": self.match_value(data_string, "RankDOR_Pct"),
            "def_reb_rank": self.match_rank(data_string, "RankDOR_Pct"),
            "off_fta_rate": self.match_value(data_string, "RankFT_Rate"),
            "off_fta_rate_rank": self.match_rank(data_string, "RankFT_Rate"),
            "def_fta_rate": self.match_value(data_string, "RankDFT_Rate"),
            "def_fta_rate_rank": self.match_rank(data_string, "RankDFT_Rate"),
            "off_three_point_pct": self.match_value(data_string, "RankFG3Pct"),
            "off_three_point_pct_rank": self.match_rank(data_string, "RankFG3Pct"),
            "def_three_point_pct": self.match_value(data_string, "RankFG3Pct&od=d"),
            "def_three_point_pct_rank": self.match_rank(data_string, "RankFG3Pct&od=d"),
            "off_two_point_pct": self.match_value(data_string, "RankFG2Pct"),
            "off_two_point_pct_rank": self.match_rank(data_string, "RankFG2Pct"),
            "def_two_point_pct": self.match_value(data_string, "RankFG2Pct&od=d"),
            "def_two_point_pct_rank": self.match_rank(data_string, "RankFG2Pct&od=d"),
            "off_ft_pct": self.match_value(data_string, "RankFTPct"),
            "off_ft_pct_rank": self.match_rank(data_string, "RankFTPct"),
            "def_ft_pct": self.match_value(data_string, "RankFTPct&od=d"),
            "def_ft_pct_rank": self.match_rank(data_string, "RankFTPct&od=d"),
            "off_block_pct": self.match_value(data_string, "RankBlockPct"),
            "off_block_pct_rank": self.match_rank(data_string, "RankBlockPct"),
            "def_block_pct": self.match_value(data_string, "RankBlockPct&od=d"),
            "def_block_pct_rank": self.match_rank(data_string, "RankBlockPct&od=d"),
            "off_steal_pct": self.match_value(data_string, "RankStlRate"),
            "off_steal_pct_rank": self.match_rank(data_string, "RankStlRate"),
            "def_steal_pct": self.match_value(data_string, "RankStlRate&od=d"),
            "def_steal_pct_rank": self.match_rank(data_string, "RankStlRate&od=d"),
            "off_3pa_per_fga": self.match_value(data_string, "RankF3GRate"),
            "off_3pa_per_fga_rank": self.match_rank(data_string, "RankF3GRate"),
            "def_3pa_per_fga": self.match_value(data_string, "RankF3GRate&od=d"),
            "def_3pa_per_fga_rank": self.match_rank(data_string, "RankF3GRate&od=d"),
            "off_assist_rate": self.match_value(data_string, "RankARate"),
            "off_assist_rate_rank": self.match_rank(data_string, "RankARate"),
            "def_assist_rate": self.match_value(data_string, "RankARate&od=d"),
            "def_assist_rate_rank": self.match_rank(data_string, "RankARate&od=d"),
            "off_3_point_dist": self.match_value(data_string, "RankOff_3"),
            "off_3_point_dist_rank": self.match_rank(data_string, "RankOff_3"),
            "def_3_point_dist": self.match_value(data_string, "RankDef_3"),
            "def_3_point_dist_rank": self.match_rank(data_string, "RankDef_3"),
            "off_2_point_dist": self.match_value(data_string, "RankOff_2"),
            "off_2_point_dist_rank": self.match_rank(data_string, "RankOff_2"),
            "def_2_point_dist": self.match_value(data_string, "RankDef_2"),
            "def_2_point_dist_rank": self.match_rank(data_string, "RankDef_2"),
            "off_ft_point_dist": self.match_value(data_string, "RankOff_1"),
            "off_ft_point_dist_rank": self.match_rank(data_string, "RankOff_1"),
            "def_ft_point_dist": self.match_value(data_string, "RankDef_1"),
            "def_ft_point_dist_rank": self.match_rank(data_string, "RankDef_1"),
            "sos": self.find_value_in_html(data_string, "RankSOSPythag"),
            "sos_rank": self.match_rank_in_html(data_string, "RankSOSPythag"),
            "bench_minutes": self.find_value_in_html(data_string, "BenchRank"),
            "bench_minutes_rank": self.match_rank_in_html(data_string, "BenchRank"),
            "experience": self.find_value_in_html(data_string, "ExpRank"),
            "experience_rank": self.match_rank_in_html(data_string, "ExpRank"),
        }

    def match_value(self, data_string, match_string):
        whole_season_data_string = data_string.split("function tableStart()")[-1]
        regex_str = f"={match_string}.*?seed"
        try:
            matched_data = re.search(regex_str, whole_season_data_string)[0]
            value = re.search(">(\d+\.*\d*)<", matched_data)[1]
            return value
        except:
            import pdb

            pdb.set_trace()

    def match_rank(self, data_string, match_string):
        whole_season_data_string = data_string.split("function tableStart()")[-1]
        regex_str = f'={match_string}.*?seed\\\\">\d*'
        matched_data = re.search(regex_str, whole_season_data_string)[0]
        rank = re.search("seed\D*(\d+)", matched_data)[1]
        return rank

    def match_rank_in_html(self, data_string, match_string):
        data_pos = data_string.index(match_string)
        search_string = data_string[data_pos : data_pos + 50]
        rank = re.search("seed\D*(\d+)", search_string)[1]
        return rank

    def find_value_in_html(self, data_string, match_string):
        data_pos = data_string.index(match_string)
        search_string = data_string[data_pos : data_pos + 20]
        value = re.search("((\+*)(-*)(\d*)\.(\d+))", search_string)[1]
        return value

    def write_data(self, data):
        base_path = Path(__file__).parent
        data_dir_path = base_path / "teams_data"
        self.write_to_file(data_dir_path, "teams_2021.json", data)


if __name__ == "__main__":
    team_data_scraper = TeamDataScraper()
    team_data_scraper.scrape()
