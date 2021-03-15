import re
from pathlib import Path

from scraper import KenpomScraper

class AveragesScraper(KenpomScraper):
    def scrape(self):
        with self.browser() as browser:
            self.sign_in(browser)
            self.find_averages_data(browser)

    def find_averages_data(self, browser):
        browser.find_element_by_link_text('Florida').click()
        page_data = browser.page_source
        data = self.averages_data(page_data)
        self.write_data(data)

    def averages_data(self, data_string):
      return {
            "eff": self.data_value(data_string, "effText", 3),
            "tempo": self.data_value(data_string, "tempoText", 2),
            "efg": self.data_value(data_string, "Effective FG%:", 3),
            "turnover": self.data_value(data_string, "Turnover %:", 3),
            "reb": self.data_value(data_string, "Off. Reb. %:", 3),
            "fta_rate": self.data_value(data_string, "FTA/FGA:", 3),
            "three_point_pct": self.data_value(data_string, "3P%", 3),
            "two_point_pct": self.data_value(data_string, "2P%", 3),
            "ft_pct": self.data_value(data_string, "FT%:", 3),
            "block_pct": self.data_value(data_string, "Block%:", 3),
            "steal_pct": self.data_value(data_string, "Steal%:", 3),
            "three_pa_per_fga": self.data_value(data_string, "3PA/FGA:", 3),
            "assist_rate": self.data_value(data_string, "A/FGM:", 3),
            "three_point_dist": self.data_value(data_string, "3-Pointers:", 3),
            "two_point_dist": self.data_value(data_string, "2-Pointers:", 3),
            "ft_point_dist": self.data_value(data_string, "Free Throws:", 3),
            "sos": self.data_value(data_string, "Overall:", 2),
            "bench_minutes": self.data_value(data_string, "Bench Minutes:", 2),
            "experience": self.data_value(data_string, "Experience:", 2)
        }

    def data_value(self, data_string, element_label, td_num):
        element_pos = data_string.index(element_label)
        trimmed_string = data_string[element_pos:element_pos+600]
        average_data_str = trimmed_string.split("<td")[td_num]
        matched_data = re.search('((\+*)(-*)(\d*)\.(\d+))', average_data_str)
        if matched_data is None:
            print(f'No Data found for {element_label}')
            return None
        return matched_data[0]

    def write_data(self, data):
        base_path = Path(__file__).parent
        data_dir_path = base_path / "averages_data"
        self.write_to_file(data_dir_path, "averages_2021.json", data)

if __name__ == "__main__":
    average_scraper = AveragesScraper()
    average_scraper.scrape()
