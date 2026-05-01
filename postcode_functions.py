"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=3)
    ...


def validate_postcode(postcode: str) -> bool:

    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    formatted_postcode = postcode.upper().strip()

    cache = load_cache()

    if postcode in cache and "valid" in cache[postcode]:
        return cache[postcode]["valid"]

    url = f"https://api.postcodes.io/postcodes/{formatted_postcode}/validate"

    response = req.get(url)
    if response.status_code >= 500:
        raise req.RequestException(f"Unable to access API.")

    response.raise_for_status()
    result = response.json().get("result", False)

    data = response.json()
    cache.setdefault(postcode, {})
    cache[postcode]["valid"] = result
    save_cache(cache)

    return data.get("result", False)


def get_postcode_for_location(lat: float, long: float) -> str:

    if not isinstance(lat, float):
        raise TypeError("Function expects two floats.")

    if not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    url = f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"

    response = req.get(url)
    if response.status_code >= 500:
        raise req.RequestException(f"Unable to access API.")

    response.raise_for_status()

    data = response.json()
    value = data.get("result")
    if value is None:
        raise ValueError("No relevant postcode found.")
    else:
        return value[0].get("postcode")


def get_postcode_completions(postcode_start: str) -> list[str]:
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    url = f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"

    response = req.get(url)

    cache = load_cache()

    if postcode_start in cache and "completions" in cache[postcode_start]:
        return cache[postcode_start]["completions"]

    if response.status_code >= 500:
        raise req.RequestException("Unable to access API.")

    response.raise_for_status()

    data = response.json()

    value = data.get("result", [])

    cache.setdefault(postcode_start, {})
    cache[postcode_start]["valid"] = value
    save_cache(cache)

    return value[:5]


def get_postcodes_details(postcodes: list[str]) -> dict:
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for p in postcodes:
        if not isinstance(p, str):
            raise TypeError("Function expects a list of strings.")

    url = "https://api.postcodes.io/postcodes"

    response = req.post(url, json={"postcodes": postcodes})

    if response.status_code >= 500:
        raise req.RequestException("Unable to access API.")

    response.raise_for_status()

    return response.json().get("result", [])
