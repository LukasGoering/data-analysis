from nba_api.stats.static import teams
import matplotlib.pyplot as plt
import pandas as pd

## File Destinations
save_path = 'webscraper/data_webscraping/Golden_State.pkl'

# Merge a list of dictionaries into a single dictionary
# where each key corresponds to a list of values from the dictionaries
def one_dict(list_dict):
    # Initialize the set of keys with the keys from the first dictionary
    keys = list_dict[0].keys()
    # Initialize the output dictionary with empty lists for each key
    out_dict={key:[] for key in keys}
    # Iterate though each given dictionary
    for dict in list_dict:
        # Iterate through each key-value pair in the dictionary
        for key, value in dict.items():
            # Append the value to the corresponding list in the output dictionary
            out_dict[key].append(value)
    return out_dict

# Use the NBA API to get the list of NBA teams
nba_teams = teams.get_teams()

# Merge the list of dictionaries into a single dictionary
dict_nba_teams = one_dict(nba_teams)

# Create a DataFrame from the merged dictionary
df_teams = pd.DataFrame(dict_nba_teams)
#print(df_teams.head())

# Extract the information of a team using the nickname
df_warriors = df_teams[df_teams['nickname']=='Warriors']
#print(df_warriors)

# Extract the ID of the warriors:
id_warriors = df_warriors[['id']].values[0][0] #.values: Konvertiert den DataFrame in ein NumPy-Array. Dadurch wird der Zugriff auf die Daten als Array möglich.
#print(id_warriors)

# The function "League Game Finder " will make an API call, it's in the module stats.endpoints.
from nba_api.stats.endpoints import leaguegamefinder
# Create an instance of the LeagueGameFinder class with the team ID
# This will make an API call to get the game data for the team
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id_warriors)
# Get the data from the API call as a JSON object
gamefinder.get_json()
# Get the data from the API call as a DataFrame
games = gamefinder.get_data_frames()[0]
#print(games.head())


import requests

url = "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/PY0101EN/Chapter%205/Labs/Golden_State.pkl"

def download(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)

download(url, save_path)

file_name = save_path
games = pd.read_pickle(file_name)
print(games.head())
