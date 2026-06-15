import streamlit as st
from settings import get_setting

def calculate_cost_usd(tokens):
    """Calculates estimated cost in USD for a given number of tokens."""
    rate_per_1m = get_setting('cost_per_1m_tokens_usd')
    return (tokens / 1_000_000) * rate_per_1m

def usd_to_inr(usd_amount):
    """Converts USD to INR."""
    rate = get_setting('usd_to_inr_rate')
    return usd_amount * rate

def format_currency(amount, currency="USD"):
    """Formats currency beautifully."""
    if amount < 0.0001:
        return f"<{'$' if currency == 'USD' else '₹'}0.0001"
    
    if currency == "USD":
        return f"${amount:.6f}"
    else:
        return f"₹{amount:.6f}"
