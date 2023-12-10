#!/usr/bin/env python3

from requestmanager import RequestManager
from utils import *

def main():
    # Read token from coc.token file
    output("Reading coc.token")
    token = read_token()

    # Format the clan tag
    output("Formatting clan tag")
    clan_tag = format_tag("#JGJLULUG")

    # Create an instance of RequestManager
    output("Creating request manager")
    m = RequestManager()

    # Set default header for requests using the token
    output("Setting default header for requests")
    m.set_header({"Authorization": f"Bearer {token}"})


    members = m.request(f"https://api.clashofclans.com/v1/clans/{clan_tag}/members")
    jsonprint(members)

    # create a TCP server where you can request the database shit from memory. save the stuff into a json every 5 minutes



if __name__ == '__main__':
    main()