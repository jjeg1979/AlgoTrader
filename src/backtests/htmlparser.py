# Standard library imports
from typing import Optional
from pathlib import Path
from datetime import datetime
import re
from enum import StrEnum

# Third party imports
import pandas as pd
from bs4 import BeautifulSoup


# Project imports

# CONSTANTS
HTML_TABLE_TAG: str = "table"
HTML_TABLE_ROW_TAG: str = "tr"
HTML_TABLE_CELL_TAG: str = "td"
HTML_PARSER = "html.parser"
HEADER_KEYS: list[str] = [
    'Symbol',
    'TF',
    'HistBeginning',
    'HistEnding',
    'BTBeginning',
    'BTEnding',
    'EAParams',        
    ]
COLUMN_NAMES_FOR_MT4_FROM_HTML: list[str] = [
    "#",
    "Time",
    "Type",
    "Order#",
    "Volume",
    "Price",
    "SL",
    "TP",
    "Profit",
    "Balance",
]
COLUMN_NAMES_FOR_GBX_FROM_HTML: list[str] = [
    "#",
    "OpenTime",
    "Type",
    "Volume",
    "Symbol",
    "OpenPrice",
    "SL",
    "TP",
    "CloseTime",
    "ClosePrice",
    "Commission",
    "Taxes",
    "Swap",
    "Profit",
]


# ENUMERATIONS
class BTType(StrEnum):
    GBX = "GENBOX",
    MT  = "METATRADER",
    STM = "STATEMENT"
    
    def __str__(self) -> str:
        return f"{self.value}"
    
    def supported_backtest_types(self) -> list[str]:
        return [str(s) for s in BTType.__members__.values()]
    

def process_backtest(file: Path) -> list[pd.DataFrame]:
    """Performs the whole workflow for processing an htm/html
    file containing information about a backtest

    Calls other functions in this module

    Args:
        file (Path): Path to the htm/html file

    Returns:
        list[pd.DataFrame]: list with dataframes extracted
    """
    plain_text: str = read_html_file(file)  # type: ignore
    tables: list[str] = extract_tables_from_html(plain_text)
    return extract_dfs_from_html_tables(tables)
    


def read_html_file(file: Path) -> Optional[str]:
    """Reads a backtest file in html format

    Valid for MT4/MT5, Genbox and Account Statements

    Args:
        file (Path): Path to the htm/html file

    Raises:
        FileNotFoundError: Raised when the file is not found

    Returns:
        Optional[str]: _description_
    """
    try:        
        with open(file, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError

def extract_tables_from_html(html_content: str) -> list[str]:
    """Extract tables contained in html file


    Args:
        html_content (str): text string with html content

    Returns:
        list[str]: list with html tables as text
    """
    soup = BeautifulSoup(html_content, HTML_PARSER)
    tables = soup.find_all(HTML_TABLE_TAG)
    return tables

def extract_dfs_from_html_tables(tables: list[str]) -> \
    list[pd.DataFrame]:
    """Extract DataFrames from HTML Tables
    
    Args:
        tables (list[str]): list with tablas in text format
        
    Returns:
        list[pd.DataFrame]: list with dataframes extracted
    
    """   
    extracted_tables: list[pd.DataFrame] = []
    for table in tables:
        rows: list[str] = table.find_all(HTML_TABLE_ROW_TAG)  # type: ignore
        table_data: list[pd.DataFrame] = []
        for row in rows:  # type: ignore
            cells: list[str] = row.find_all(HTML_TABLE_CELL_TAG)  # type: ignore
            row_data: list[str] = [cell.text.strip() for cell in cells]  # type: ignore
            table_data.append(row_data)  # type: ignore
        df = pd.DataFrame(table_data)
        extracted_tables.append(df)  
    return extracted_tables

def parse_dates_and_times_from_string(text: str) -> list[str]:
    """Parses dates and times from a text string.

    Format for substrings: YYYY.MM.DD (HH:MM)

    Args:
        text (str): string with several times and dates

    Returns:
        list[str]: list with the dates and times in text format
    """
     # Pattern for date and time
    pattern_dt: str = r'\d{4}\.\d{2}\.\d{2}(?: \d{2}:\d{2})?'
    dates_in_table: list[str] = re.findall(pattern_dt, text)
    return dates_in_table

def parse_timeframe_from_string(text: str) -> str:
    """Captures the timeframe from a string and returns it without 
    parenthesis.

    
    Args:
        text (str): String with timeframe to be extracted

    Returns:
        str: Text with only the TF
    """
    # Pattern for TF
    pattern_tf: str = r'\(([A-Z0-9]{2})\)'
    timeframe: str = re.findall(pattern_tf, text)[0]
    return timeframe


def convert_to_datetime(str_date: str) -> datetime:
    """Convert to datetime a date in string format
   
    Args:
        str_date (str): date in string format

    Returns:
        datetime: time and date as datetime object
    """
    if len(str_date) > 10:
        format_str: str = "%Y.%m.%d %H:%M"
    else:
        format_str: str = "%Y.%m.%d"
    return datetime.strptime(str_date, format_str)
    

def parse_ea_parameters(text: str) -> dict[str, str]:
    """Gathers the EA parameters from the header

    Header must come from an MT4/5 backtest file.

    Args:
        text (str): Text string with CSV parameters 

    Returns:
        dict[str, str]: 'Param_name': 'Param_value'
    """
    elems: list[str] = text.split(';')
    # Remove empty strings
    elems = [elem for elem in elems if elem != '']
    params: dict[str, str] = {}    
    for elem in elems:
        key, value = elem.split('=')
        params[key.strip()] = value.strip()
        
    return params
        

def extract_header_information(table: pd.DataFrame) -> dict[str, str | dict[str, str]]:
    """Parses and stores data from header in a dictionary
    

    Args:
        table (pd.DataFrame): DataFrame with header information

    Returns:
        dict[str, str | dict[str, str]]: Formatted header information
    """
    data_col: list[str] = table.iloc[:,1]  # type: ignore
    
    dates_in_table: list[str] = parse_dates_and_times_from_string(data_col[1])
    dates_as_dt: list[datetime] = [convert_to_datetime(date) for date in dates_in_table]
    timeframe: str = parse_timeframe_from_string(data_col[1])
    
    ea_params: dict[str, str] = parse_ea_parameters(data_col[3])
    
    header: dict[str, str | datetime | dict[str, str]] = {
        'Symbol': data_col[0].split(' ')[0],
        'TF': timeframe,
        'HistBeginning': dates_as_dt[0],
        'HistEnding': dates_as_dt[1],
        'BTBeginning': dates_as_dt[2],
        'BTEnding': dates_as_dt[3],
        'EAParams': ea_params,        
    }
    return header  # type: ignore
    
    
def extract_mt4_operations_information(table: pd.DataFrame,) -> pd.DataFrame:
    """Proceses the df with MT4 operations so it is easier to deal with.

    - Removes unnecessary columns.
    - Set column names as COLUMN_NAMES_FROM_HTML list
    - Sets the index

    Args:
        table (pd.DataFrame): DataFrame with raw operations

    Returns:
        pd.DataFrame: DataFrame with the operations processed
    """
    # Remove first two columns    
    df: pd.DataFrame = table.iloc[1:, :]
    # Set column names
    df.columns = COLUMN_NAMES_FOR_MT4_FROM_HTML
    index_col = COLUMN_NAMES_FOR_MT4_FROM_HTML[0]
    df.set_index(index_col, inplace=True, drop=True)  # type: ignore        
    return df

def extract_gbx_operations_information(table: pd.DataFrame) -> pd.DataFrame:
    """Proceses the df with GBX operations so it is easier to deal with.

    - Removes unnecessary columns.
    - Set column names as COLUMN_NAMES_FROM_HTML list
    - Sets the index

    Args:
        table (pd.DataFrame): DataFrame with raw operations
        initial_balance (Decimal): Initial balance

    Returns:
        pd.DataFrame: DataFrame with the operations processed
    """
    # Remove first two columns
    df: pd.DataFrame = table.iloc[4:, :]
    # Set column names
    df.columns = COLUMN_NAMES_FOR_GBX_FROM_HTML    
    # GBX Needs a little bit more processing
    odd_idx: list[int] = df[df['#'] == ''].index.to_list()  # type: ignore
    df_red: pd.DataFrame = df.drop(odd_idx)
    df_red = df_red.drop("#", axis=1)
    df_red = df_red.reset_index(drop=True)
    df_red.index.name = "#"
    # Remove last rows without operations information
    flag: str = df_red['Type'].unique()[0]   # type: ignore
    last_idx: int = int(df_red[df_red['Type']==flag].index.values[-1]) + 1 # type: ignore
    df_red = df_red.drop(range(last_idx, df_red.shape[0]))  # type: ignore        
    return df_red

def transform_mt4_to_gbx(bt: pd.DataFrame) -> pd.DataFrame:
    """Given a DataFrame with operations processed, this function
    further processes the operations and provides an homogeneous format

.
    Args:
        bt (pd.DataFrame): Operations as extracted from HTML backtest

    Returns:
        pd.DataFrame: DataFrame ops homogenized
    """
    ORDER_COL: str = "Order#"
    TIME_COL: str = "Time"
    SL_COL: str = "SL"
    TP_COL: str = "TP"
    PRICE_COL: str = "Price"
    VOL_COL: str = "Volume"
    PROFIT_COL: str = "Profit"
    #BALANCE_COL: str = "Balance"
    ORDER_TYPE: str = "Type"
    # format_dt: str = "%Y.%m.%d %H:"
    ops: list[str] = bt[ORDER_COL].unique().tolist()  # type: ignore
    operations = []
    for op in ops:        
        df: pd.DataFrame = bt[bt[ORDER_COL] == op]  # type: ignore
        open_time: str = df[TIME_COL][0]
        open_price: str = df[PRICE_COL][0]
        order_type: str = df[ORDER_TYPE][0]
        close_time: str = df[TIME_COL][-1]
        close_price: str = df[PRICE_COL][-1]
        stop_loss: str = df[SL_COL][0]
        take_profit: str = df[TP_COL][0]
        volume: str = df[VOL_COL][0]
        profit: str = df[PROFIT_COL][-1]
        #balance: str = df[BALANCE_COL][-1]
        # TODO: Consider modifications of SL and TP (modified in Type)
        operations.append([
            op,
            open_time,
            order_type,
            volume,
            open_price,            
            stop_loss,
            take_profit,
            close_time,
            close_price,
            "0", # Commision
            "0", # Taxes
            "0", # Swap
            profit,
        ])
    
    bt_df: pd.DataFrame = pd.DataFrame(data=operations)
    bt_df.columns = COLUMN_NAMES_FOR_GBX_FROM_HTML
    breakpoint()
    return bt_df
        
    
