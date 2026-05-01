"""A CLI application for interacting with the Postcode API."""
from postcode_functions import validate_postcode, get_postcodes_details, get_postcode_completions, get_postcode_for_location
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Postcode Checker",
        description="Takes in a postcode and returns the information",
        epilog="Contact S1gma L8bs for help")

    parser.add_argument("--mode", "-m", required=True,
                        help="Enter validate or complete")
    parser.add_argument("postcode", help="Enter a postcode")

    args = parser.parse_args()

    postcode = args.postcode.upper().strip()
