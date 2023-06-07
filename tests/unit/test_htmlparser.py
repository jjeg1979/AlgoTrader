"""Test HTMLParser module"""
# Standard library imports
import os
from pathlib import Path

# Third party imports
import pytest
import pandas as pd


from src.backtests.htmlparser import (
    extract_gbx_operations_information,
    extract_mt4_operations_information,
    process_backtest,
    read_html_file,
    extract_tables_from_html,
    extract_dfs_from_html_tables,
    extract_header_information,
    HEADER_KEYS,
    COLUMNS_FOR_MT4_FROM_HTML,
    COLUMNS_FOR_GBX_FROM_HTML,
    transform_mt4_to_gbx,
)

# CONSTANTS
PAYLOAD_DIR: str = r"tests/payload/backtests/"
payload: list[str] = os.listdir(PAYLOAD_DIR)
payload: list[str] = [file for file in payload if file.endswith((".html", ".htm"))]


class TestHTMLParser:
    """Test HMLTParser functions"""

    @pytest.fixture
    def result(self) -> str:
        result: str = read_html_file(Path(PAYLOAD_DIR) / payload[0])  # type: ignore
        return result

    @pytest.fixture
    def mt4_bt(self, result: str) -> list[pd.DataFrame]:
        dfs: list[pd.DataFrame] = extract_dfs_from_html_tables(
            extract_tables_from_html(result)
        )
        return dfs

    def test_read_html_file_returns_str(self, result: str):
        assert isinstance(result, str)

    def test_read_html_file_raises_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError) as ex:
            read_html_file(Path(PAYLOAD_DIR) / "no_html.htm")
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

    def test_extract_header_information(self):
        bt: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[1])
        header = extract_header_information(bt[0])
        assert isinstance(header, dict)
        assert list(header.keys()) == HEADER_KEYS
        assert header["Symbol"] == "AUDJPY"
        assert header["TF"] == "H4"

    def test_process_backtest_for_mt4_type(self):
        bt = process_backtest(Path(PAYLOAD_DIR) / payload[1])
        assert len(bt) == 2
        for part in bt:
            assert isinstance(part, pd.DataFrame)

    def test_process_backtest_for_gbx_type(self):
        bt: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[14])
        assert len(bt) == 1
        assert isinstance(bt[0], pd.DataFrame)

    def test_extract_mt4_operations_from_df(self):
        bt: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[1])
        ops: pd.DataFrame = extract_mt4_operations_information(bt[1])
        assert isinstance(bt, list)
        assert isinstance(ops, pd.DataFrame)
        expected_column_names: list[str] = list(COLUMNS_FOR_MT4_FROM_HTML.values())[1:]
        assert ops.columns.to_list() == expected_column_names  # type: ignore
        assert ops.index.name == "#"  # type: ignore

    def test_extract_gbx_operations_from_df(self):
        bt: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[14])
        gbx: pd.DataFrame = bt[0]
        ops: pd.DataFrame = extract_gbx_operations_information(gbx)
        assert isinstance(ops, pd.DataFrame)
        expected_column_names: list[str] = list(COLUMNS_FOR_GBX_FROM_HTML.values())[1:]
        assert ops.columns.to_list() == expected_column_names  # type: ignore
        assert ops.index.name == "#"  # type: ignore

    def test_transform_mt4_to_gbx(self):
        bt: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[1])
        ops: pd.DataFrame = extract_mt4_operations_information(bt[1])
        gbx: pd.DataFrame = transform_mt4_to_gbx(ops)
        expected_column_names: list[str] = list(COLUMNS_FOR_GBX_FROM_HTML.values())[1:]
        assert isinstance(gbx, pd.DataFrame)
        assert gbx.columns.to_list() == expected_column_names  # type: ignore
        assert gbx.index.name == "#"  # type: ignore

    def test_bt_from_gbx_and_from_mt4_are_compatible(self):
        mt4: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[1])
        ops_mt4: pd.DataFrame = extract_mt4_operations_information(mt4[1])
        mt4_to_gbx: pd.DataFrame = transform_mt4_to_gbx(ops_mt4)
        gbx: list[pd.DataFrame] = process_backtest(Path(PAYLOAD_DIR) / payload[14])
        ops_gbx: pd.DataFrame = extract_gbx_operations_information(gbx[0])        
        expected_column_names: list[str] = list(COLUMNS_FOR_GBX_FROM_HTML.values())[1:]
        df: pd.DataFrame = pd.concat([mt4_to_gbx, ops_gbx], axis=0)  # type: ignore
        assert df.columns.to_list() == expected_column_names  # type: ignore
        assert df.index.name == "#"  # type: ignore
