import urllib3, requests, json
from requests.auth import HTTPBasicAuth
from pprint import pprint
import os 
import argparse
import sys
import json
import logging

def get_options(argv):
    parser = argparse.ArgumentParser()
    # store the file name
    parser.add_argument('-a', action='store', help='Auth URL', required=True)
    parser.add_argument('-u', action='store', help='User', required=True)
    parser.add_argument('-p', action='store', help='Password', required=True)
    parser.add_argument('-l', action='store', help='logging level', default='INFO')
    options = parser.parse_args(argv)
    return options

def main():
    options = get_options(sys.argv[1:])
    authUrl = options.a
    user = options.u
    password = options.p
    # set the logging level 
    loglevel = options.l
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify -l DEBUG or -l debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
       raise ValueError('Invalid log level: %s' % loglevel.upper())
    logging.basicConfig(level=numeric_level)

    logging.info("Authenticating.")
    response = requests.get(authUrl, auth=HTTPBasicAuth(user, password), verify=False)

    print('Bearer Token:')
    print(response.json()['accessToken'])

if __name__ == "__main__":
    main()
