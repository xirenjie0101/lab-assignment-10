import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

#
#

def get_president_terms():
    """
    Scrapes the Wikipedia page for U.S. Presidents and constructs a dictionary
    with each president's name as the key, and a list with their political party and
    number of terms served as the values. Saves the result in JSON format.
    
    :return: None (data saved in presidents_terms.json)
    """
    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    presidents_dict = {}

    # Find the main table that contains the list of U.S. Presidents
    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")[1:]  # Skip header row

    for row in rows:
        columns = row.find_all("td")
     
        
        if len(columns) < 5:
            continue

        # Extract name, party, and term start/end dates
        name = columns[1].text.strip()
        name = re.sub(r"\(.*?\)|\[.*?\]", "", name).strip()  # Remove parentheses and footnotes
    
        
        # Extract party name and clean footnote markers
        party = columns[4].text.strip()
        party = re.sub(r"\[.*?\]", "", party)
     
        
        term_data = columns[2].text.strip()

        # Extract term start and end years
        term_years = re.findall(r'\d{4}', term_data)
        if len(term_years) == 2:
            start_year, end_year = map(int, term_years)
            terms_served = round((end_year - start_year) / 4)  # Approximate each term as 4 years
        else:
            terms_served = 1  # Default to 1 term if end year is unavailable

        presidents_dict[name] = [party, terms_served]
    
    return presidents_dict



def calculate_approval_changes():
    """
    Fetches JSON data from an API endpoint, calculates the difference
    in approval ratings between the start and end of each president's term,
    and saves the result as a JSON file.
    
    :return: None (data saved in approval_changes.json)
    """
    url = "https://dsci.isi.edu/slides/data/presidents"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    approval_changes = {}

    for president in data['presidents']:
        name = president['name']
        start_approval = president['approval_ratings'].get('start')
        end_approval = president['approval_ratings'].get('end')

        if start_approval is not None and end_approval is not None:
            approval_changes[name] = end_approval - start_approval

    return approval_changes



def generate_president_dataframe():
    """
    Reads data from JSON files created in the previous functions, consolidates
    the information into a pandas DataFrame, and displays the result.
    
    :return: DataFrame containing the presidents, their party, terms, and approval changes
    """
    # Load the JSON data files
    with open("presidents_terms.json", "r") as f:
        presidents_terms = json.load(f)
    
    with open("approval_changes.json", "r") as f:
        approval_changes = json.load(f)
    
    # Prepare DataFrame columns
    names = []
    parties = []
    terms = []
    approval_change = []

    for name, (party, term_count) in presidents_terms.items():
        names.append(name)
        parties.append(party)
        terms.append(term_count)
        approval_change.append(approval_changes.get(name, None))  # None if no approval change data

    # Create the DataFrame
    df = pd.DataFrame({
        "President": names,
        "Party": parties,
        "Terms": terms,
        "Approval Change": approval_change
    })
    

    return df
