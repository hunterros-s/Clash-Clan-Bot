from utils import *
from requestmanager import RequestManager
import time
import json

def data_coroutine():
    global data
    data = {}

    # Read token from coc.token file
    info("Reading coc.token")
    token = read_token()

    # Format the clan tag
    info("Formatting clan tag")
    clan_tag = format_tag("#JGJLULUG")

    # Create an instance of RequestManager
    info("Creating request manager")
    m = RequestManager()

    # Set default header for requests using the token
    info("Setting default header for requests")
    m.set_header({"Authorization": f"Bearer {token}"})
    # Specify the path to JSON file
    data_file_path = 'member_data.json'

    # Try to load member_data from data_file_path
    info(f"Attempting to load member data from {data_file_path}")
    try:
        # Open the JSON file in read mode
        with open(data_file_path, 'r') as json_file:
            # Load the JSON data into a Python dictionary
            data = json.load(json_file)
            info(f"Member data loaded from {data_file_path}")
    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        info(f"File not found: {data_file_path}; member data not loaded")
        info(f"Initializing empty member data object")
        # member_data will be empty

    # Do this every five minutes:
    info("Beginning data retrieval loop")

    while True:
        # Get the clan information/member list from the COC api
        member_list_request = m.request(f"https://api.clashofclans.com/v1/clans/{clan_tag}/members")
        if member_list_request is None:
            continue
        members = member_list_request['items']

        # Loop through each member and get more specific information
        for member in members:
            time.sleep(.5)
            member_tag = format_tag(member['tag'])
            member_infomation = m.request(f"https://api.clashofclans.com/v1/players/{member_tag}")
            if member_infomation is None:
                error(f"{member_tag} is empty (?)")
                continue
            tag = member_infomation['tag']
            name = member_infomation['name']
            info(f"Checking {name} ({tag})")

            achievements_data = member_infomation.get('achievements', {})
            heroes_data = member_infomation.get('heroes', {})

            current_time = int(time.time())

            def find_by_name(name, data_list, attribute):
                for item in data_list:
                    if item.get('name') == name:
                        return item.get(attribute)
                return None

            if tag in data:
                data[tag]['name'] = member_infomation['name']
                data[tag]['lastQueried'] = current_time
                data[tag]['role'] = member_infomation['role']
                data[tag]['leagueImage'] = member_infomation.get("league", {}).get("iconUrls", {}).get("medium")

                def update_data(tag, data_key, value, current_time, historical=True):
                    if historical:
                        if data[tag][data_key][-1]['value'] != value:
                            data[tag][data_key].append({"time": current_time, "value": value})
                            data[tag]['lastSeen'] = current_time
                            info(f"{data_key} updated for {name} ({tag})")
                    else:
                        if data[tag][data_key] != value:
                            data[tag][data_key] = value
                            data[tag]['lastSeen'] = current_time
                            info(f"{data_key} updated for {name} ({tag})")

                # Cases using historical data
                update_data(tag, 'townHallLevel', member_infomation['townHallLevel'], current_time)
                update_data(tag, 'trophies', member_infomation['trophies'], current_time)
                update_data(tag, 'expLevel', member_infomation['expLevel'], current_time)
                update_data(tag, 'goldLooted', find_by_name("Gold Grab", achievements_data, 'value'), current_time)
                update_data(tag, 'elixirLooted', find_by_name("Elixir Escapade", achievements_data, 'value'), current_time)
                update_data(tag, 'darkElixirLooted', find_by_name("Heroic Heist", achievements_data, 'value'), current_time)
                update_data(tag, 'battlesWon', find_by_name("Conqueror", achievements_data, 'value'), current_time)
                update_data(tag, 'reinforcementsDonated', find_by_name("Friend in Need", achievements_data, 'value'), current_time)
                update_data(tag, 'clanGamePoints', find_by_name("Games Champion", achievements_data, 'value'), current_time)
                update_data(tag, 'warStars', member_infomation['warStars'], current_time)
                update_data(tag, 'clanCapitalContributions', member_infomation['clanCapitalContributions'], current_time)

                # Cases not using historical data
                update_data(tag, 'builderHallLevel', member_infomation['builderHallLevel'], current_time, False)
                update_data(tag, 'builderBaseTrophies', member_infomation['builderBaseTrophies'], current_time, False)
                update_data(tag, 'obstaclesRemoved', find_by_name("Nice and Tidy", achievements_data, 'value'), current_time, False)
                update_data(tag, 'kingLevel', find_by_name("Barbarian King", heroes_data, 'level'), current_time, False)
                update_data(tag, 'queenLevel', find_by_name("Archer Queen", heroes_data, 'level'), current_time, False)
                update_data(tag, 'wardenLevel', find_by_name("Grand Warden", heroes_data, 'level'), current_time, False)
            else:
                ## doesn't exist. need to initialize 
                info(f"Creating new entry for {name} ({tag}) in data structure.")
                data[tag] = {
                    # should create a more nested data structure. could have like "first seen" and "now" categories so we can see growth. if the categories are the same comparison should be easy
                    "name": member_infomation['name'],

                    "firstSeen": current_time, # this should never change after this point
                    "lastSeen": current_time,  # this should be updated anytime any metric is changed
                    "lastQueried": current_time, # this should be updated anytime the API is queried

                    "role": member_infomation['role'],
                    "leagueImage": member_infomation.get("league", {}).get("iconUrls", {}).get("medium"),

                    # everything below should be tracked for change.

                    "townHallLevel": [{"time": current_time, "value": member_infomation['townHallLevel']}],
                    "trophies": [{"time": current_time, "value": member_infomation['trophies']}],
                    "expLevel": [{"time": current_time, "value": member_infomation['expLevel']}],

                    "goldLooted": [{"time": current_time, "value": find_by_name("Gold Grab", achievements_data, 'value')}],
                    "elixirLooted": [{"time": current_time, "value": find_by_name("Elixir Escapade", achievements_data, 'value')}],
                    "darkElixirLooted": [{"time": current_time, "value": find_by_name("Heroic Heist", achievements_data, 'value')}],

                    "battlesWon": [{"time": current_time, "value": find_by_name("Conqueror", achievements_data, 'value')}],

                    "reinforcementsDonated": [{"time": current_time, "value": find_by_name("Friend in Need", achievements_data, 'value')}],
                    "clanGamePoints": [{"time": current_time, "value": find_by_name("Games Champion", achievements_data, 'value')}],
                    "warStars": [{"time" : current_time, "value" : member_infomation['warStars']}],
                    "clanCapitalContributions": [{"time": current_time, "value": member_infomation['clanCapitalContributions']}],

                    "builderHallLevel": member_infomation['builderHallLevel'],
                    "builderBaseTrophies": member_infomation['builderBaseTrophies'],
                    "obstaclesRemoved": find_by_name("Nice and Tidy", achievements_data, 'value'),
                    
                    "kingLevel": find_by_name("Barbarian King", heroes_data, 'level'),
                    "queenLevel": find_by_name("Archer Queen", heroes_data, 'level'),
                    "wardenLevel": find_by_name("Grand Warden", heroes_data, 'level'),
                }
        
        # Look for members that are no longer in the clan and remove them here.
        data_tag_list = data.keys()
        member_tag_list = [member['tag'] for member in members]
        removed_tags = [tag for tag in data_tag_list if tag not in member_tag_list]

        for tag in removed_tags:
            if tag in data:
                info(f"Removing {data[tag]['name']} ({tag}) from data structure.")
                del data[tag]

    
        info(f"Attempting to write member data to {data_file_path}")
        try:
            # Open the JSON file in write mode
            with open(data_file_path, 'w') as json_file:
                # Write the data from the dictionary to the file
                json.dump(data, json_file, indent=2)
                info(f"Member data successfully written to {data_file_path}")
        except Exception as e:
            error(f"An error occurred while saving data: {e}")

        info("Waiting 5 minutes ...")        
        time.sleep(5 * 60)