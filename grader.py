import run
import sys
import requests
from bs4 import BeautifulSoup



def main():
    fn_name = sys.argv[1]  # Function name to test



    if fn_name == 'get_frequency':
        query_parameter = sys.argv[2] # word being searched

        # Fetch expected result from a webpage (e.g., Project Gutenberg)
        expected_ans = requests.get(f"https://dsci.isi.edu/slides/alice?word={query_parameter}").json()
        actual_ans = run.get_frequency(query_parameter)

        assert actual_ans == expected_ans, (
            f'ERROR: Expected answer is different than your answer. '
            f'Expected: {expected_ans}, Your answer: {actual_ans}'
        )

    elif fn_name == 'count_links_on_page':

        # Fetch expected result from a webpage (e.g., Wikipedia)
        expected_ans = requests.get(f"https://dsci.isi.edu/slides/links").json()
        actual_ans = run.count_links_on_page()

        assert actual_ans == expected_ans, (
            f'ERROR: Expected answer is different than your answer. '
            f'Expected: {expected_ans}, Your answer: {actual_ans}'
        )

    elif fn_name == 'count_presidents_by_party_and_year':
        year = int(sys.argv[2])  # The year to filter presidents by

        # Fetch expected result from the Presidents Wikipedia page
        expected_ans = requests.get(f"https://dsci.isi.edu/slides/party_count?year={year}").json()
        actual_ans = run.count_presidents_by_party_and_year(year)

        assert actual_ans == expected_ans, (
            f'ERROR: Expected answer is different than your answer. '
            f'Expected: {expected_ans}, Your answer: {actual_ans}'
        )

    else:
        assert False, "Error in testcase: Unknown function name"


if __name__ == "__main__":
    main()
