from __future__ import annotations
from io import BytesIO
from abc import ABC, abstractmethod
from typing import Any
import pandas as pd
from app_variacao.documents.types import SheetData, WorkbookData, IndexTables, ObjectAdapter


class ExcelLoad(ABC):

    @abstractmethod
    def hash(self) -> int:
        pass

    @abstractmethod
    def get_index_sheets(self) -> IndexTables:
        pass

    @abstractmethod
    def get_workbook_data(self, sheet_name: str = "ALL") -> WorkbookData:
        """
        Retorna todos os dados/DataFrames da planilha em formato
        chave:valor (str:SheetData)
        """
        pass

    def get_sheet_names(self) -> list[str]:
        return self.get_index_sheets().get_sheet_names()

    def get_sheet_at(self, idx: int) -> SheetData:
        idx_sheet_names: IndexTables = self.get_index_sheets()
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

    def get_index_sheets(self) -> IndexTables:
        rd: pd.ExcelFile = pd.ExcelFile(self.xlsx_file)
        names = [str(x) for x in rd.sheet_names]
        print('*********************************************')
        print(names)
        print('*********************************************')
        return IndexTables.create_from_list(names)

    def get_sheet_names(self) -> list[str]:
        rd: pd.ExcelFile = pd.ExcelFile(self.xlsx_file)
        names = [str(x) for x in rd.sheet_names]
        print('*********************************************')
        print(names)
        print('*********************************************')
        return names

    def get_workbook_data(self, sheet_name: str = "ALL") -> WorkbookData:
        if (sheet_name is None) or (sheet_name == "ALL"):
            # Ler todos os dados da planilha
            data: dict[Any, pd.DataFrame] = pd.read_excel(self.xlsx_file, sheet_name=None)
        else:
            data: dict[str, pd.DataFrame] = {
                sheet_name: pd.read_excel(self.xlsx_file, sheet_name=sheet_name)
            }

        workbook_data = WorkbookData()
        for _key in data.keys():
            workbook_data.add_sheet(
                str(_key), SheetData.create_from_data(data[_key])
            )
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

    def get_workbook_data(self, sheet_name: str = None) -> WorkbookData:
        print(f'Lendo Excel aguarde...')
        return self.__reader.get_workbook_data(sheet_name)

    def get_sheet_at(self, idx: int) -> SheetData:
        return self.__reader.get_sheet_at(idx)

    def get_sheet(self, sheet_name: str | None = None) -> SheetData:
        return self.__reader.get_sheet(sheet_name)

    def get_index_sheets(self) -> IndexTables:
        return self.__reader.get_index_sheets()

    def get_sheet_names(self) -> list[str]:
        return self.__reader.get_sheet_names()

    @classmethod
    def create_load_pandas(cls, file_excel: str | BytesIO) -> ReadSheetExcel:
        rd = ExcelLoadPandas(file_excel)
        return cls(rd)


__all__ = ['ReadSheetExcel', 'ExcelLoad']

