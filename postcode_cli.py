"""A CLI application for interacting with the Postcode API."""
from postcode_functions import validate_postcode
from argparse import ArgumentParser


if __name__ == "__main__":
    validate_postcode("TW34JN")
