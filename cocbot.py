import requests
import json
import time
import threading
import queue
import requests
import time

token_path = 'coc.token'

clan_tag = "%23JGJLULUG"

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

    # Force the top process in the queue to run
    def force_process_top(self):
        if not self.request_queue.empty():
            printd("Forcing the top process in the queue")
            url, header, func = self.request_queue.get()
            response = self.make_request(url, header)
            func(response)
            self.request_queue.task_done()

    def worker(self):
        printd("Starting worker")
        while True:
            if not self.request_queue.empty():
                printd("Getting request from queue")
                url, header, func = self.request_queue.get()
                response = self.make_request(url, header)
                func(response)
                self.request_queue.task_done()
            time.sleep(self.request_period)

    def make_request(self, url, header=None):
        printd("Making request")
        try:
            response = requests.get(url, headers=header)
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"

# rate limit is probably faster than 1 request per second. should be fine if you check data every hour or so. and check clan members specifically in a queue


# need to account for people that leave clan. probably just delete them. no need to keep data.

"""
{
    'tag': '#PCYCQU2V', 
    'name': 'mohadplayz', 
    'role': 'member', 
    'expLevel': 103, 
    'league': {
        'id': 29000009, 
        'name': 'Gold League I', 
        'iconUrls': {
            'small': 'https://api-assets.clashofclans.com/leagues/72/CorhMY9ZmQvqXTZ4VYVuUgPNGSHsO0cEXEL5WYRmB2Y.png', 
            'tiny': 'https://api-assets.clashofclans.com/leagues/36/CorhMY9ZmQvqXTZ4VYVuUgPNGSHsO0cEXEL5WYRmB2Y.png', 
            'medium': 'https://api-assets.clashofclans.com/leagues/288/CorhMY9ZmQvqXTZ4VYVuUgPNGSHsO0cEXEL5WYRmB2Y.png'
            }
        }, 
    'trophies': 1772, 
    'builderBaseTrophies': 2140, 
    'versusTrophies': 2140, 
    'clanRank': 42, 
    'previousClanRank': 41, 
    'donations': 0, 
    'donationsReceived': 0, 
    'playerHouse': {
        'elements': [
            {
                'type': 'ground', 
                'id': 82000002
            }, {
                'type': 'walls', 
                'id': 82000049
            }, {
                'type': 'roof', 
                'id': 82000010
            }, {
                'type': 'decoration', 
                'id': 82000061
        }]}, 
    'builderBaseLeague': {
        'id': 44000020, 
        'name': 'Brass League III'
    }}
"""
DEBUG = True
def printd(str):
    if DEBUG: print("DEBUG: " + str)

def main():
    printd("Initialzing request mangaer")
    manager = RequestManager(request_period=60)

    printd("Reading coc.token")
    try:
        with open(token_path, 'r') as file:
            # Use the 'token' variable for further processing, e.g., making API requests.
            token = file.read()
    except FileNotFoundError:
        print(f"File '{token_path}' not found. Please make sure you create a file named coc.token containing your API token from developer.clashofclans.com")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    # Include JWT in the Request Header
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-type':'application/json'
    }
    manager.add_request(f"https://api.clashofclans.com/v1/clans/{clan_tag}/members", headers)
    manager.force_process_top()


    """
    # Make the API request
    api_url = f"https://api.clashofclans.com/v1/clans/{clan_tag}/members"
    response = requests.get(api_url, headers=headers)
    request_time = int(time.time())

    # Handle the API Response
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        exit(1)

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