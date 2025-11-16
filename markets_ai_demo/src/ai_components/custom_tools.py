# src/ai_components/custom_tools.py
# Custom tools for Snowflake Intelligence Agents - Frost Markets Intelligence Demo

from snowflake.snowpark import Session
from config import DemoConfig


def create_all_custom_tools(session: Session) -> None:
    """Create all custom tools (Python stored procedures) for agents"""
    
    print("\n🔧 Creating Custom Tools...")
    
    print("   📊 Creating CALCULATE_PORTFOLIO_VAR stored procedure...")
    create_var_calculation_tool(session)
    
    print("✅ All custom tools created successfully\n")


def create_var_calculation_tool(session: Session) -> None:
    """
    Create CALCULATE_PORTFOLIO_VAR stored procedure for Market Risk Agent.
    Implements historical simulation VaR calculation.
    """
    
    # Create the stored procedure
    create_procedure_sql = """
CREATE OR REPLACE PROCEDURE AI.CALCULATE_PORTFOLIO_VAR(
    TICKERS ARRAY,
    SHOCK_PERCENTAGE FLOAT
)
RETURNS TABLE(
    VAR_99 FLOAT,
    VAR_95 FLOAT,
    STRESSED_VAR_99 FLOAT,
    STRESSED_VAR_95 FLOAT,
    TOTAL_PORTFOLIO_VALUE FLOAT,
    METHODOLOGY VARCHAR
)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.10'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy')
HANDLER = 'calculate_var'
COMMENT = 'Calculate portfolio Value-at-Risk using historical simulation with optional stress scenario'
AS
$$
import pandas as pd
import numpy as np
from snowflake.snowpark import Session

def calculate_var(session: Session, tickers: list, shock_percentage: float):
    \"\"\"
    Calculate portfolio VaR using historical simulation.
    
    Args:
        session: Snowpark session
        tickers: List of tickers in the portfolio
        shock_percentage: Price shock to apply for stress testing (e.g., -15 for 15% drop)
    
    Returns:
        DataFrame with VaR calculations
    \"\"\"
    
    # Convert tickers array to Python list if needed
    if not isinstance(tickers, list):
        tickers = list(tickers)
    
    # Get current positions for specified tickers
    ticker_list = "', '".join(tickers)
    positions_query = \"\"\"
        SELECT TICKER, MARKET_VALUE, QUANTITY
        FROM CURATED.FACT_FIRM_POSITION
        WHERE AS_OF_DATE = (SELECT MAX(AS_OF_DATE) FROM CURATED.FACT_FIRM_POSITION)
        AND TICKER IN ({})
    \"\"\".format(ticker_list)
    
    positions_df = session.sql(positions_query).to_pandas()
    
    if positions_df.empty:
        # No positions found - return zero values
        return pd.DataFrame([{{
            'VAR_99': 0.0,
            'VAR_95': 0.0,
            'STRESSED_VAR_99': 0.0,
            'STRESSED_VAR_95': 0.0,
            'TOTAL_PORTFOLIO_VALUE': 0.0,
            'METHODOLOGY': 'Historical Simulation (No positions found)'
        }}])
    
    total_portfolio_value = positions_df['MARKET_VALUE'].sum()
    
    # Get 60 days of historical returns for VaR calculation
    historical_returns_query = \"\"\"
        WITH price_data AS (
            SELECT 
                TICKER,
                PRICE_DATE,
                CLOSE,
                LAG(CLOSE, 1) OVER (PARTITION BY TICKER ORDER BY PRICE_DATE) AS PREV_CLOSE
            FROM CURATED.FACT_STOCK_PRICE_DAILY
            WHERE TICKER IN ({})
            AND PRICE_DATE >= DATEADD(day, -70, CURRENT_DATE())
            ORDER BY TICKER, PRICE_DATE DESC
        )
        SELECT 
            TICKER,
            PRICE_DATE,
            (CLOSE - PREV_CLOSE) / PREV_CLOSE AS DAILY_RETURN
        FROM price_data
        WHERE PREV_CLOSE IS NOT NULL
        LIMIT 60
    \"\"\".format(ticker_list)
    
    returns_df = session.sql(historical_returns_query).to_pandas()
    
    if returns_df.empty:
        # No historical data - use simplified estimation
        var_99 = total_portfolio_value * 0.03  # 3% rule of thumb
        var_95 = total_portfolio_value * 0.02  # 2% rule of thumb
        stressed_var_99 = total_portfolio_value * abs(shock_percentage / 100) * 1.5
        stressed_var_95 = total_portfolio_value * abs(shock_percentage / 100) * 1.2
        
        return pd.DataFrame([{{
            'VAR_99': round(var_99, 2),
            'VAR_95': round(var_95, 2),
            'STRESSED_VAR_99': round(stressed_var_99, 2),
            'STRESSED_VAR_95': round(stressed_var_95, 2),
            'TOTAL_PORTFOLIO_VALUE': round(total_portfolio_value, 2),
            'METHODOLOGY': 'Simplified Estimation (Limited historical data)'
        }}])
    
    # Pivot returns data to get ticker columns
    returns_pivot = returns_df.pivot(index='PRICE_DATE', columns='TICKER', values='DAILY_RETURN').fillna(0)
    
    # Calculate portfolio daily returns
    portfolio_weights = {}
    for _, row in positions_df.iterrows():
        ticker = row['TICKER']
        weight = row['MARKET_VALUE'] / total_portfolio_value
        portfolio_weights[ticker] = weight
    
    portfolio_returns = []
    for date, row in returns_pivot.iterrows():
        daily_portfolio_return = sum([
            row.get(ticker, 0) * portfolio_weights.get(ticker, 0)
            for ticker in portfolio_weights.keys()
        ])
        portfolio_returns.append(daily_portfolio_return)
    
    # Calculate VaR as percentiles of historical portfolio returns distribution
    portfolio_returns_array = np.array(portfolio_returns)
    var_99_pct = np.percentile(portfolio_returns_array, 1)  # 1st percentile for 99% VaR
    var_95_pct = np.percentile(portfolio_returns_array, 5)  # 5th percentile for 95% VaR
    
    var_99 = abs(var_99_pct * total_portfolio_value)
    var_95 = abs(var_95_pct * total_portfolio_value)
    
    # Calculate stressed VaR with shock applied
    # Apply shock to all returns and recalculate VaR
    shock_factor = 1 + (shock_percentage / 100)
    stressed_returns = portfolio_returns_array * shock_factor
    
    stressed_var_99_pct = np.percentile(stressed_returns, 1)
    stressed_var_95_pct = np.percentile(stressed_returns, 5)
    
    stressed_var_99 = abs(stressed_var_99_pct * total_portfolio_value)
    stressed_var_95 = abs(stressed_var_95_pct * total_portfolio_value)
    
    return pd.DataFrame([{{
        'VAR_99': round(var_99, 2),
        'VAR_95': round(var_95, 2),
        'STRESSED_VAR_99': round(stressed_var_99, 2),
        'STRESSED_VAR_95': round(stressed_var_95, 2),
        'TOTAL_PORTFOLIO_VALUE': round(total_portfolio_value, 2),
        'METHODOLOGY': 'Historical Simulation (60-day window)'
    }}])
$$
"""
    try:
        session.sql(create_procedure_sql).collect()
        print("   ✅ CALCULATE_PORTFOLIO_VAR stored procedure created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create CALCULATE_PORTFOLIO_VAR: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(create_procedure_sql)
        raise


if __name__ == "__main__":
    print("ℹ️  Custom tools are created automatically via SQL during setup.")
    print("   Run: python setup.py --mode=full")
    print("\n   Custom tools created:")
    print("   - CALCULATE_PORTFOLIO_VAR")

