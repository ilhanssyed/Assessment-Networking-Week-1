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
    mode = args.mode.lower().strip()

    if mode == "validate":
        try:
            is_valid = validate_postcode(postcode)

            if is_valid:
                print(f"{postcode} is a valid postcode.")
            else:
                print(f"{postcode} is not a valid postcode.")

        except Exception:
            print(f"{postcode} is not a valid postcode.")

    elif mode == "complete":
        try:
            results = get_postcode_completions(postcode)

            if not results:
                print(f"No matches for {postcode}.")
            else:
                for item in results[:5]:
                    print(item)

        except Exception:
            print(f"No matches for {postcode}.")

    else:
        print("Invalid mode")
