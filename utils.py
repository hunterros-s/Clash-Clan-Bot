import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def output(msg, title = f"[{bcolors.OKBLUE}COCBOT{bcolors.ENDC}]"):
    print(f"{title} {msg}")

def jsonprint(json_obj):
    output(json.dumps(json_obj, indent=2))

def format_tag(tag_string):
    return tag_string.replace("#", "%23")

def read_token():
    token_path = 'coc.token'
    try:
        with open(token_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File '{token_path}' not found. Please make sure you create a file named coc.token containing your API token from developer.clashofclans.com")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)