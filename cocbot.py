import requests
import json
import time
import threading
import queue
import requests
import time

class RequestManager:
    def __init__(self, request_period=60):
        self.request_queue = queue.Queue()
        self.request_period = request_period  # Added for clarity

        self.worker_thread = threading.Thread(target=self.worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    # Add a request to the queue
    def add_request(self, url, header=None, func=print):
        printd("Adding request to queue")
        self.request_queue.put((url, header, func))

    def worker(self):
        printd("Starting worker")
        while True:
            if not self.request_queue.empty():
                printd("Getting request from queue")
                url, header, func = self.request_queue.get()
                success, response = self.make_request(url, header)
                if success:
                    func(response)
                else:
                    printd(response)
                self.request_queue.task_done()
            time.sleep(self.request_period)

    def make_request(self, url, header=None):
        printd(f"Sending request to {url}")
        try:
            response = requests.get(url, headers=header)
            #response.raise_for_status()  # Raise an exception if the response status code is not in the 200-299 range

            if response.status_code == 404:
                return False, f"404 {response.reason} {response.text}"

            if response.text:  # Check if the response is not empty
                try:
                    return True, response.json()
                except ValueError:
                    return False, "Response is not valid JSON"
            else:
                return False, "Empty response"

        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"

# rate limit is probably faster than 1 request per second. should be fine if you check data every hour or so. and check clan members specifically in a queue


# need to account for people that leave clan. probably just delete them. no need to keep data.

"""
Basically, we need to track activity of clan members.
We can ping the API every few minutes and see how often data changes. If data changes count them as active for 5 minutes. Add these minutes up over awhile
and see how active the players are. Sort these and kick the least active players.
Could also track "useful stats" such as donations.
Could track base activity such as cumulative spells, cumulative hero levels, cumulative troop levels.
Track capital gold contribution, capital gold looted, clan game points, clan war stars collected, elixir looted, gold looted, clan donations, multiplayer battles won, other stuff.
"""


DEBUG = True
def printd(str):
    if DEBUG: print("DEBUG: " + str)

def jsonprint(json_obj):
    print(json.dumps(json_obj, indent=2))

def format_tag(tag_string):
    return tag_string.replace("#", "%23")

def read_token():
    token_path = 'coc.token'
    try:
        with open(token_path, 'r') as file:
            # Use the 'token' variable for further processing, e.g., making API requests.
            return file.read()
    except FileNotFoundError:
        print(f"File '{token_path}' not found. Please make sure you create a file named coc.token containing your API token from developer.clashofclans.com")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

def main():

    clan_tag = "#JGJLULUG"

    printd("Initialzing request mangaer")
    manager = RequestManager(request_period=1)

    printd("Reading coc.token")
    token = read_token()
    # Include JWT in the Request Header
    headers = {"Authorization": f"Bearer {token}"}

    # This structure stores all of the data
    member_data = {}

    # Should take the output of /players/{member_tag}
    def parse_member_data(data):
        tag = data['tag']
        if tag in member_data:
            printd(f"{tag} exists in data structure")
            ## already exists
            ## need to detect any change. keep track of quite a few data points for this.
            ## could keep track of useful stats that pertain to activity such as gold looted--or other similar metrics--and add append to histogram every new change.
            ## could use this to graph and keep track of best members
            return
        ## doesn't exist. need to initialize 
        printd(f"{tag} doesnt exist in data structure")
        # need to set initial/joined time in data structure. should never change
        member_data[tag] = {
            "name": data['name'],
            "townHallLevel": data['townHallLevel'], # could do time series for this
            "expLevel": data['expLevel'], # could do time series for this
            "trophies": data['trophies'], # could do time series for this
            "warStars": data['warStars'], # could do time series for this
            "builderHallLevel": data['builderHallLevel'], # coul
            "builderBaseTrophies": data['builderBaseTrophies'],
            "clanCapitalContributions": data['clanCapitalContributions']
            ## need a function for searching through achievements. i don't think i can trust indexing by number. maybe i can?
            ## need to add times for, joined, last seen, and last queried. 
        }
        return

    # Should take the output of the /clans/{clan_tag}/members request
    def request_members(data):
        members = data['items']
        for member in members:
            # Fix member tag for API format
            member_tag = format_tag(member['tag'])
            manager.add_request(f"https://api.clashofclans.com/v1/players/{member_tag}", header=headers, func=parse_member_data)

    # Fix formatting of clan tag for API
    clan_tag = format_tag(clan_tag)
    # Add request to the request manager. Call back function should do work
    manager.add_request(f"https://api.clashofclans.com/v1/clans/{clan_tag}/members", header=headers, func=request_members) # should also use this to remove people who are no longer members
    
    while True:
        pass


    """
    members = data['items']

    member_data = {}

    for member in members:
        member_data[member['tag']] = {
            'name': member['name'],
            'role': member['role'],
            'expLevel': member['expLevel'],
            'leagueName': member['league']['name'],
            'trophies': member['trophies'],
            'builderBaseTrophies': member['builderBaseTrophies'],
            'versusTrophies': member['versusTrophies'],
            'donations': member['donations'],
            'donationsReceived': member['donationsReceived'],
            'builderBaseLeagueName': member['builderBaseLeague']['name'],
            'lastRequestTime': request_time
            # need to add firstRecord time
        }
    
    print(json.dumps(member_data, indent=2))

    #with open("member_data.json", "w") as json_file:
    #    json.dump(member_data, json_file)

    #print(members)

    #print(json.dumps(data, indent=2))
    """
    

if __name__ == "__main__":
    main()