import streamlit as st
from settings import get_setting

def calculate_energy_kwh(tokens):
    """Calculates estimated energy in kWh for a given number of tokens."""
    kwh_per_token = get_setting('kwh_per_token')
    return tokens * kwh_per_token

def calculate_carbon_gco2(tokens):
    """Calculates estimated carbon emissions in grams of CO2 for a given number of tokens."""
    kwh = calculate_energy_kwh(tokens)
    grams_per_kwh = get_setting('carbon_grams_per_kwh')
    return kwh * grams_per_kwh

def format_carbon(grams):
    """Formats carbon emissions nicely."""
    if grams < 1:
        return f"{grams * 1000:.2f} mg"
    return f"{grams:.4f} g"
