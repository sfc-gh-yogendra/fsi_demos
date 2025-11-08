"""
Snowpark Helper Functions for Server-Side Data Generation

Provides reusable patterns for generating data using Snowpark DataFrame operations
that execute on Snowflake servers, eliminating local computation and data transfer.
"""

from typing import List, Optional
from snowflake.snowpark import Session, Column
from snowflake.snowpark.functions import (
    col, lit, concat, uniform, random, current_date, current_timestamp,
    dateadd, lpad, when, array_construct, iff
)
import snowflake.snowpark.functions as F
from snowflake.snowpark import Window


def random_choice_from_list(items: List[str], seed_col: Optional[Column] = None) -> Column:
    """
    Select a random item from a list using CASE WHEN for compatibility.
    
    Args:
        items: List of strings to choose from
        seed_col: Optional column to use as random seed (default: F.random())
    
    Returns:
        Column expression that selects random item from list
    """
    if seed_col is None:
        seed_col = F.random()
    
    # Use CASE WHEN approach to avoid array type inference issues
    index = F.uniform(0, len(items) - 1, seed_col).cast("int")
    
    result = None
    for i, item in enumerate(items):
        condition = (index == i)
        if result is None:
            result = F.when(condition, F.lit(item))
        else:
            result = result.when(condition, F.lit(item))
    
    return result.otherwise(F.lit(items[0]))


def random_date_in_past(min_days: int, max_days: int, seed_col: Optional[Column] = None) -> Column:
    """
    Generate a random date in the past within specified range.
    
    Args:
        min_days: Minimum days in the past
        max_days: Maximum days in the past
        seed_col: Optional column to use as random seed
    
    Returns:
        Column expression for random past date
    """
    if seed_col is None:
        seed_col = F.random()
    
    days_back = F.uniform(min_days, max_days, seed_col)
    return F.dateadd("day", -days_back, F.current_date())


def random_date_in_future(min_days: int, max_days: int, seed_col: Optional[Column] = None) -> Column:
    """
    Generate a random date in the future within specified range.
    
    Args:
        min_days: Minimum days in the future
        max_days: Maximum days in the future
        seed_col: Optional column to use as random seed
    
    Returns:
        Column expression for random future date
    """
    if seed_col is None:
        seed_col = F.random()
    
    days_forward = F.uniform(min_days, max_days, seed_col)
    return F.dateadd("day", days_forward, F.current_date())


def random_amount(min_amount: float, max_amount: float, decimals: int = 2, 
                  seed_col: Optional[Column] = None) -> Column:
    """
    Generate a random monetary amount.
    
    Args:
        min_amount: Minimum amount
        max_amount: Maximum amount
        decimals: Number of decimal places
        seed_col: Optional column to use as random seed
    
    Returns:
        Column expression for random amount
    """
    if seed_col is None:
        seed_col = F.random()
    
    return F.uniform(min_amount, max_amount, seed_col).cast(f"DECIMAL(18,{decimals})")


def generate_id_from_prefix(prefix: str, seq_col: Column, padding: int = 6) -> Column:
    """
    Generate an ID by combining a prefix with a zero-padded sequence number.
    
    Args:
        prefix: ID prefix string
        seq_col: Column containing sequence numbers
        padding: Number of digits to pad to
    
    Returns:
        Column expression for generated ID
    """
    return F.concat(
        F.lit(prefix),
        F.lpad(seq_col.cast("string"), padding, "0")
    )


def weighted_random_choice(choices: List[tuple], seed_col: Optional[Column] = None) -> Column:
    """
    Select a random choice based on weights.
    
    Args:
        choices: List of (value, weight) tuples
        seed_col: Optional column to use as random seed
    
    Returns:
        Column expression for weighted random selection
    """
    if seed_col is None:
        seed_col = F.random()
    
    total_weight = sum(weight for _, weight in choices)
    rand_value = F.uniform(0, total_weight, seed_col)
    
    cumulative = 0
    result = None
    for value, weight in choices:
        cumulative += weight
        if result is None:
            result = F.when(rand_value < cumulative, F.lit(value))
        else:
            result = result.when(rand_value < cumulative, F.lit(value))
    
    return result.otherwise(F.lit(choices[-1][0]))


def add_row_number_column(df, column_name: str = "ROW_NUM", 
                          partition_by: Optional[List[str]] = None,
                          order_by: Optional[List[str]] = None) -> "DataFrame":
    """
    Add a row number column to a DataFrame.
    
    Args:
        df: Input DataFrame
        column_name: Name for the row number column
        partition_by: Optional list of columns to partition by
        order_by: Optional list of columns to order by (default: random)
    
    Returns:
        DataFrame with row number column added
    """
    if order_by is None:
        order_by = [F.random()]
    else:
        order_by = [F.col(c) if isinstance(c, str) else c for c in order_by]
    
    window_spec = Window.order_by(*order_by)
    if partition_by:
        window_spec = Window.partition_by(*[F.col(c) for c in partition_by]).order_by(*order_by)
    
    return df.with_column(column_name, F.row_number().over(window_spec))


def sample_n_from_table(session: Session, table_name: str, n: int, 
                        filter_expr: Optional[Column] = None) -> "DataFrame":
    """
    Sample n rows from a table efficiently.
    
    Args:
        session: Snowpark session
        table_name: Fully qualified table name
        n: Number of rows to sample
        filter_expr: Optional filter expression
    
    Returns:
        DataFrame with n sampled rows
    """
    df = session.table(table_name)
    if filter_expr is not None:
        df = df.filter(filter_expr)
    
    # Use SAMPLE for efficiency if sampling ratio is reasonable
    total_rows = df.count()
    if total_rows > n * 10:  # If we have 10x more rows than needed, use SAMPLE
        sample_ratio = (n * 1.2) / total_rows  # Over-sample by 20% for safety
        df = df.sample(fraction=sample_ratio)
    
    # Add row number and filter to exact count
    df = add_row_number_column(df, "SAMPLE_ROW_NUM")
    return df.filter(F.col("SAMPLE_ROW_NUM") <= n).drop("SAMPLE_ROW_NUM")


def cross_join_with_generator(df, generator_rowcount: int, 
                               seq_column_name: str = "SEQ") -> "DataFrame":
    """
    Cross join a DataFrame with a generator to create multiple rows per input row.
    
    Args:
        df: Input DataFrame
        generator_rowcount: Number of rows to generate per input row
        seq_column_name: Name for the sequence column from generator
    
    Returns:
        DataFrame with generator rows crossed with input
    """
    from snowflake.snowpark import Session
    
    # Get session from DataFrame
    session = df._session
    
    # Create generator DataFrame
    generator_df = session.generator(
        F.col(seq_column_name).cast("int"),
        rowcount=generator_rowcount
    )
    
    # Cross join
    return df.cross_join(generator_df)

