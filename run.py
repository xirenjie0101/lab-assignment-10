import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_president_terms():

    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")

    presidents_terms = {}

    for row in rows[1:]:  
        cols = row.find_all("td")
        if len(cols) > 0:
            # Extract president name (1st column), party (4th column), and terms served (2nd column)
            name = cols[0].text.strip()
            party = cols[3].text.strip() if len(cols) > 3 else "Unknown"
            term = cols[1].text.strip()

            term_count = len(re.findall(r"\d{4}", term))
            presidents_terms[name] = [party, term_count]

    with open("presidents_terms.json", "w") as json_file:
        json.dump(presidents_terms, json_file, indent=4)

    return presidents_terms


def calculate_approval_changes():

    response = requests.get(url)
    data = response.json()

    approval_changes = {}

    for president, ratings in data.items():
        if "start" in ratings and "end" in ratings:
            start = ratings["start"]
            end = ratings["end"]
            if start is not None and end is not None:
                approval_changes[president] = end - start

    with open("approval_changes.json", "w") as json_file:
        json.dump(approval_changes, json_file, indent=4)

    return approval_changes


def generate_president_dataframe():

    with open("presidents_terms.json", "r") as json_file:
        presidents_terms = json.load(json_file)

    with open("approval_changes.json", "r") as json_file:
        approval_changes = json.load(json_file)

    data = []
    for president, info in presidents_terms.items():
        party, terms = info
        approval_change = approval_changes.get(president, None)
        data.append([president, party, terms, approval_change])

    df = pd.DataFrame(data, columns=["President", "Party", "Terms", "Approval Change"])

    print(df)
    return df
