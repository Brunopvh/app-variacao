from __future__ import annotations
from io import BytesIO
from abc import ABC, abstractmethod
import pandas as pd
from typing import Any
from app_variacao.documents.erros import *
from app_variacao.documents.sheet.types import (
    SheetData, SheetIndexNames, WorkbookData
)
from app_variacao.types.core import ObjectAdapter


#===========================================================#
# CLASSES BASE E ADAPTADORES (ODS)
#===========================================================#

class ODSLoad(ABC):
    """
    Classe abstrata base para carregadores de planilhas ODS.
    """

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


# --------------------------------------------------------------------------------
# 1. IMPLEMENTAÇÃO COM PANDAS
# --------------------------------------------------------------------------------
class ODSLoadPandas(ODSLoad):
    """Carregador ODS utilizando a biblioteca Pandas."""

    def __init__(self, ods_file: str | BytesIO):
        self.ods_file: str | BytesIO = ods_file
        self.__sheet_names: list[str] | None = None

    def hash(self) -> int:
        return hash(self.ods_file)

    def get_sheet_index(self) -> SheetIndexNames:
        # Pandas suporta ODS via pd.ExcelFile ou pd.read_excel
        if self.__sheet_names is None:
            try:
                rd: pd.ExcelFile = pd.ExcelFile(self.ods_file, "odf")
                self.__sheet_names = [str(x) for x in rd.sheet_names]
            except Exception as e:
                # O pandas falha se o backend (odfpy, por exemplo) não estiver instalado
                raise LoadWorkbookError(
                    f'{__class__.__name__} ODSLoadPandas (odfpy): {e}'
                )
        return SheetIndexNames.create_from_list(self.__sheet_names)

    def get_workbook_data(self) -> WorkbookData:
        try:
            # Se sheet_name=None
            # carrega todas as abas em um dicionário de DataFrames
            data: dict[Any, pd.DataFrame] = pd.read_excel(
                self.ods_file, sheet_name=None, engine='odf'
            )
        except Exception as e:
            raise LoadWorkbookError(f'{__class__.__name__}: {e}')

        workbook_data = WorkbookData()
        for sheet_name, df in data.items():
            # Limpeza opcional de nomes de abas e conversão para SheetData
            workbook_data.add_sheet(str(sheet_name), SheetData.create_from_data(df))
        return workbook_data


# --------------------------------------------------------------------------------
# CLASSE PRINCIPAL DE LEITURA (FACTORY)
# --------------------------------------------------------------------------------

class ReadSheetODS(ObjectAdapter):

    def __init__(self, reader: ODSLoad):
        super().__init__()
        self.__reader: ODSLoad = reader

    def get_implementation(self) -> ODSLoad:
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
    def create_load_pandas(cls, ods_file: str | BytesIO) -> ReadSheetODS:
        rd = ODSLoadPandas(ods_file)
        return cls(rd)
