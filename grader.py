import run
import sys
import requests
import pandas as pd

def main():
    fn_name = sys.argv[1]  # Function name to test



    if fn_name == 'get_president_terms':
        #query_parameter = sys.argv[2] # word being searched

        # Fetch expected result from a webpage (e.g., Project Gutenberg)
        expected_ans = requests.get("https://dsci.isi.edu/slides/data/presidents").json()
        actual_ans = run.get_president_terms()

        assert actual_ans == expected_ans, (
            f'ERROR: Expected answer is different than your answer. '
            f'Expected: {expected_ans}, Your answer: {actual_ans}'
        )

    elif fn_name == 'calculate_approval_changes':

        # Fetch expected result from a webpage (e.g., Wikipedia)
        expected_ans = requests.get("https://dsci.isi.edu/slides/approval_changes").json()
        actual_ans = run.calculate_approval_changes()

        assert actual_ans == expected_ans, (
            f'ERROR: Expected answer is different than your answer. '
            f'Expected: {expected_ans}, Your answer: {actual_ans}'
        )

    elif fn_name == 'generate_president_dataframe':
        

        # Fetch expected result from the Presidents Wikipedia page
        expected_ans = pd.read_json(requests.get("https://dsci.isi.edu/slides/president_df").json())
        actual_ans = run.generate_president_dataframe()

        assert actual_ans.equals(expected_ans), (
            f'ERROR: Expected answer is different than your answer. '
            f'Expected: {expected_ans}, Your answer: {actual_ans}'
        )

    else:
        assert False, "Error in testcase: Unknown function name"

    print("Success")

if __name__ == "__main__":
    main()
