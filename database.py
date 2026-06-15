import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "ecomind.db"

def init_db():
    """Initializes the SQLite database with the required tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompt_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            original_prompt TEXT,
            optimized_prompt TEXT,
            optimization_mode TEXT,
            original_tokens INTEGER,
            optimized_tokens INTEGER,
            tokens_saved INTEGER,
            original_cost REAL,
            optimized_cost REAL,
            cost_saved REAL,
            original_carbon REAL,
            optimized_carbon REAL,
            carbon_saved REAL,
            efficiency_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_optimization_result(data):
    """Saves an optimization result to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prompt_history (
            original_prompt, optimized_prompt, optimization_mode,
            original_tokens, optimized_tokens, tokens_saved,
            original_cost, optimized_cost, cost_saved,
            original_carbon, optimized_carbon, carbon_saved,
            efficiency_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['original_prompt'], data['optimized_prompt'], data['optimization_mode'],
        data['original_tokens'], data['optimized_tokens'], data['tokens_saved'],
        data['original_cost'], data['optimized_cost'], data['cost_saved'],
        data['original_carbon'], data['optimized_carbon'], data['carbon_saved'],
        data['efficiency_score']
    ))
    conn.commit()
    conn.close()

def get_all_history():
    """Retrieves all prompt history as a Pandas DataFrame."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM prompt_history ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def clear_history():
    """Deletes all records from the prompt history."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prompt_history")
    conn.commit()
    conn.close()

def delete_record(record_id):
    """Deletes a specific record by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prompt_history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
