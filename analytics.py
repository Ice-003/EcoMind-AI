import pandas as pd
from database import get_all_history

def get_dashboard_metrics():
    """Calculates summary metrics for the dashboard."""
    df = get_all_history()
    
    if df.empty:
        return {
            'total_prompts': 0,
            'total_tokens_saved': 0,
            'total_cost_saved_usd': 0,
            'total_carbon_saved_gco2': 0,
            'average_efficiency': 0
        }
        
    return {
        'total_prompts': len(df),
        'total_tokens_saved': int(df['tokens_saved'].sum()),
        'total_cost_saved_usd': df['cost_saved'].sum(),
        'total_carbon_saved_gco2': df['carbon_saved'].sum(),
        'average_efficiency': int(df['efficiency_score'].mean())
    }

def get_trend_data():
    """Gets data grouped by date for trend charts."""
    df = get_all_history()
    if df.empty:
        return pd.DataFrame()
        
    # Convert timestamp to datetime and extract date
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
    # Group by date
    daily_stats = df.groupby('date').agg({
        'tokens_saved': 'sum',
        'cost_saved': 'sum',
        'carbon_saved': 'sum',
        'efficiency_score': 'mean',
        'id': 'count' # Number of prompts
    }).reset_index()
    
    daily_stats.rename(columns={'id': 'prompts_optimized'}, inplace=True)
    return daily_stats
