"""Test HTMLParser module"""
# Standard library imports
import os
from pathlib import Path

# Third party imports
import pytest
import pandas as pd


from src.backtests.htmlparser import (
    read_html_file, 
    extract_tables_from_html,
    extract_dfs_from_html_tables,
    extract_header_information,
)

# CONSTANTS
HEADER_KEYS: list[str] = [
    'Symbol',
    'TF',
    'HistBeginning',
    'HistEnding',
    'BTBeginning',
    'BTEnding',
    'EAParams',        
    ]

PAYLOAD_DIR: str = r'tests/payload/backtests/'
payload: list[str] = os.listdir(PAYLOAD_DIR)
payload: list[str] = [file for file in payload if file.endswith(('.html', '.htm'))]


class TestHTMLParser:
    """Test HMLTParser functions"""
    @pytest.fixture 
    def result(self) -> str:
        result: str = read_html_file(Path(PAYLOAD_DIR)/payload[0])  # type: ignore
        return result
    
    @pytest.fixture 
    def mt4_bt(self) -> list[pd.DataFrame]:
        result: str = read_html_file(Path(PAYLOAD_DIR)/payload[1])  # type: ignore
        dfs: list[pd.DataFrame] =\
            extract_dfs_from_html_tables(extract_tables_from_html(result))
        return dfs
        
    def test_read_html_file_returns_str(self, result: str):        
        assert isinstance(result, str)
        
    def test_read_html_file_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError) as ex:
            read_html_file(Path(PAYLOAD_DIR)/'no_html.htm')
        assert ex.type == FileNotFoundError        
   
    def test_extract_tables_from_html(self, result: str):
        tables = extract_tables_from_html(result)
        assert isinstance(tables, list)
        assert len(tables) > 0
        
    def test_extract_dfs_from_tables_from_html(self, result: str):
        tables = extract_tables_from_html(result)
        dfs = extract_dfs_from_html_tables(tables)
        assert isinstance(dfs, list)
        for df in dfs:
            assert isinstance(df, pd.DataFrame)
        assert len(dfs) > 0
        
    def test_extract_header_information(self, mt4_bt: list[pd.DataFrame]):
       header = extract_header_information(mt4_bt[0])
       assert isinstance(header, dict)
       assert list(header.keys()) == HEADER_KEYS
       assert header['Symbol'] == 'AUDJPY'
       assert header['TF'] == 'H4'
