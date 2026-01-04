from __future__ import annotations
from app_variacao.app.controllers.controller_base import (
    ControllerPopUpFiles, ControllerVariacao, TypeImportSheet
)
from app_variacao.app.models import ModelPreferences
from app_variacao.app.models import PreferencesImportSheet, ExtensionSheet, CsvSep
from app_variacao.documents.sheet import ReadSheetExcel, ReadSheetODS, ReadSheetCsv, WorkbookData
from app_variacao.documents.sheet.csv import CsvEncoding
from app_variacao.util import File


class ControllerViewVariacao(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self._controller_popup_files = ControllerPopUpFiles()
        self.model_prefs = ModelPreferences()

    def set_csv_separator(self, sep: CsvSep):
        self.get_prefs_import_sheet()['sep'] = sep

    def get_csv_separator(self) -> CsvSep:
        return self.get_prefs_import_sheet()['sep']

    def get_sheet_encoding(self) -> CsvEncoding:
        return self.get_prefs_import_sheet()['encoding']

    def set_sheet_encoding(self, encoding: CsvEncoding):
        self.get_prefs_import_sheet()['encoding'] = encoding

    def get_prefs_import_sheet(self) -> PreferencesImportSheet:
        return self.model_prefs.get_preferences().get_prefs_import_sheet()

    def get_path_sheet_variacao(self) -> File | None:
        if 'path' in self.get_prefs_import_sheet().keys():
            return self.get_prefs_import_sheet()['path']
        return None

    def set_path_sheet_variacao(self, p: File):
        self.get_prefs_import_sheet()['path'] = p
        self.get_prefs_import_sheet()['extension'] = p.extension().lower()

    def get_sheet_extension(self) -> str | None:
        if self.get_path_sheet_variacao() is None:
            return None
        return self.get_path_sheet_variacao().extension().lower()

    def get_sheet_names(self) -> list[str] | None:
        _extension = self.get_sheet_extension()
        _sheet_names = None
        print('Lendo Sheet Names')
        if (_extension == '.txt') or (_extension == '.csv'):
            return None
        elif _extension == '.xlsx':
            rd = ReadSheetExcel.create_load_pandas(self.get_path_sheet_variacao().absolute())
            _sheet_names = rd.get_sheet_names()
        elif _extension == '.ods':
            rd = ReadSheetODS.create_load_pandas(self.get_path_sheet_variacao().absolute())
            _sheet_names = rd.get_sheet_index().get_sheet_names()
        else:
            print('******************************************************************')
            print(_sheet_names)
            print(_extension)
            raise RuntimeError()
        return _sheet_names

    def select_sheet_variacao(self) -> None:
        """
        Abre uma caixa de diálogo para o usuário selecionar uma planilha CSV/Excel.
        """
        f: File | None = self._controller_popup_files.get_sheet()
        if f is None:
            return
        self.get_prefs_import_sheet()['path'] = f
        self.get_prefs_import_sheet()['extension'] = f.extension().lower()
        self.model_prefs.save_prefs()  # Salvar no disco após a seleção
