import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_president_terms():
    """
    Scrapes the Wikipedia page for U.S. Presidents and constructs a dictionary
    with each president's name as the key, and a list with their political party and
    number of terms served as the values. Saves the result in JSON format.

    :return: Dictionary containing presidents' terms data
    """
    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")

    presidents_terms = {}

    for row in rows[1:]:  # Skip the header row
        cols = row.find_all("td")
        if len(cols) > 0:
            # Extract president name (1st column), party (4th column), and terms served (2nd column)
            name = cols[0].text.strip()
            party = cols[3].text.strip() if len(cols) > 3 else "Unknown"
            term = cols[1].text.strip()

            # Clean up term to count terms served
            term_count = len(re.findall(r"\d{4}", term))
            presidents_terms[name] = [party, term_count]

    # Save to JSON
    with open("presidents_terms.json", "w") as json_file:
        json.dump(presidents_terms, json_file, indent=4)

    return presidents_terms


def calculate_approval_changes():
    """
    Fetches JSON data from an API endpoint, calculates the difference
    in approval ratings between the start and end of each president's term,
    and saves the result as a JSON file.

    :return: Dictionary containing presidents' approval rating changes
    """
    url = "https://dsci.isi.edu/slides/data/presidents"
    response = requests.get(url)
    data = response.json()

    approval_changes = {}

    for president, ratings in data.items():
        if "start" in ratings and "end" in ratings:
            start = ratings["start"]
            end = ratings["end"]
            if start is not None and end is not None:
                approval_changes[president] = end - start

    # Save to JSON
    with open("approval_changes.json", "w") as json_file:
        json.dump(approval_changes, json_file, indent=4)

    return approval_changes


def generate_president_dataframe():
    """
    Reads data from JSON files created in the previous functions, consolidates
    the information into a pandas DataFrame, and displays the result.

    :return: DataFrame containing the presidents, their party, terms, and approval changes
    """
    # Load data from JSON files
    with open("presidents_terms.json", "r") as json_file:
        presidents_terms = json.load(json_file)

    with open("approval_changes.json", "r") as json_file:
        approval_changes = json.load(json_file)

    # Consolidate data into a DataFrame
    data = []
    for president, info in presidents_terms.items():
        party, terms = info
        approval_change = approval_changes.get(president, None)
        data.append([president, party, terms, approval_change])

    df = pd.DataFrame(data, columns=["President", "Party", "Terms", "Approval Change"])

    # Display the DataFrame
    print(df)
    return df


if __name__ == "__main__":
    # Execute the functions
    get_president_terms()
    calculate_approval_changes()
    generate_president_dataframe()
