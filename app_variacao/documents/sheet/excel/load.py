from __future__ import annotations
from io import BytesIO
from abc import ABC, abstractmethod
from typing import Any
import pandas as pd
from app_variacao.documents.sheet.types import SheetData, WorkbookData, SheetIndexNames
from app_variacao.types.core import ObjectAdapter


class ExcelLoad(ABC):

    @abstractmethod
    def hash(self) -> int:
        pass

    @abstractmethod
    def get_sheet_index(self) -> SheetIndexNames:
        pass

    @abstractmethod
    def get_workbook_data(self) -> WorkbookData:
        pass

    def get_sheet_at(self, idx: int) -> SheetData:
        idx_sheet_names: SheetIndexNames = self.get_sheet_index()
        name = idx_sheet_names[idx]
        return self.get_workbook_data()[name]

    def get_sheet(self, sheet_name: str | None) -> SheetData:
        if sheet_name is not None:
            return self.get_workbook_data()[sheet_name]
        return self.get_sheet_at(0)


class ExcelLoadPandas(ExcelLoad):

    def __init__(self, xlsx_file):
        self.xlsx_file: str | BytesIO = xlsx_file
        self.__hash: int = hash(xlsx_file)

    def hash(self) -> int:
        return self.__hash

    def get_sheet_index(self) -> SheetIndexNames:
        rd: pd.ExcelFile = pd.ExcelFile(self.xlsx_file)
        names = [str(x) for x in rd.sheet_names]
        return SheetIndexNames.create_from_list(names)

    def get_workbook_data(self) -> WorkbookData:
        data: dict[Any, pd.DataFrame] = pd.read_excel(self.xlsx_file, sheet_name=None)
        workbook_data = WorkbookData()
        for _key in data.keys():
            df: pd.DataFrame = data[_key]
            workbook_data.add_sheet(str(_key), SheetData.create_from_data(df))
        return workbook_data

    def get_sheet_at(self, idx: int) -> SheetData:
        return super().get_sheet_at(idx)

    def get_sheet(self, sheet_name: str | None) -> SheetData:
        return super().get_sheet(sheet_name)


class ReadSheetExcel(ObjectAdapter):

    def __init__(self, reader: ExcelLoad):
        super().__init__()
        self.__reader: ExcelLoad = reader

    def get_implementation(self) -> ExcelLoad:
        return self.__reader

    def hash(self) -> int:
        return self.get_implementation().hash()

    def get_workbook_data(self) -> WorkbookData:
        return self.__reader.get_workbook_data()

    def get_sheet_at(self, idx: int) -> SheetData:
        return self.__reader.get_sheet_at(idx)

    def get_sheet(self, sheet_name: str | None = None) -> SheetData:
        return self.__reader.get_sheet(sheet_name)

    def get_sheet_index(self) -> SheetIndexNames:
        return self.__reader.get_sheet_index()

    @classmethod
    def create_load_pandas(cls, file_excel: str | BytesIO) -> ReadSheetExcel:
        rd = ExcelLoadPandas(file_excel)
        return cls(rd)


__all__ = ['ReadSheetExcel', 'ExcelLoad']

