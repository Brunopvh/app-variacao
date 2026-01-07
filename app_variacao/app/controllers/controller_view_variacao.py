from __future__ import annotations
from app_variacao.app.app_types import ConfigSheetCsv, ConfigSheetExcel
from app_variacao.documents import CsvSeparator
from app_variacao.app.controllers.controller_base import (
    ControllerPopUpFiles, ControllerVariacao, ControllerPrefs
)
from app_variacao.documents import ReadSheetExcel, ReadSheetODS, CsvEncoding
from app_variacao.app.models.model_view_variacao import ModelViewVariacao
from app_variacao.util import File
import threading
import pandas as pd


class ControllerViewVariacao(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self._controller_popup_files = ControllerPopUpFiles()
        self._controller_prefs = ControllerPrefs()
        self.model = ModelViewVariacao()

    @property
    def isLoading(self) -> bool:
        return self.model.isLoading

    @property
    def loaded_data(self) -> pd.DataFrame:
        return self.model.df

    def read_thread_data_frame(self, config: ConfigSheetExcel | ConfigSheetCsv) -> None:
        data_thread = threading.Thread(target=self.model.read_data_frame, args=(config,))
        data_thread.start()

    def set_csv_separator(self, sep: CsvSeparator):
        self._controller_prefs.get_conf_sheet_csv()['sep'] = sep

    def get_csv_separator(self) -> CsvSeparator:
        return self._controller_prefs.get_conf_sheet_csv()['sep']

    def get_csv_encoding(self) -> CsvEncoding:
        return self._controller_prefs.get_conf_sheet_csv()['encoding']

    def set_csv_encoding(self, encoding: CsvEncoding):
        self._controller_prefs.get_conf_sheet_csv()['encoding'] = encoding

    def get_conf_sheet_csv(self) -> ConfigSheetCsv:
        return self._controller_prefs.get_conf_sheet_csv()

    def get_conf_sheet_excel(self) -> ConfigSheetExcel:
        return self._controller_prefs.get_conf_sheet_excel()

    def get_path_sheet_variacao(self) -> File | None:
        if 'sheet_variacao' in self._controller_prefs.get_user_prefs().keys():
            return self._controller_prefs.get_user_prefs()['sheet_variacao']
        return None

    def get_sheet_names(self) -> list[str] | None:
        if self.get_path_sheet_variacao() is None:
            return None

        _sheet_names = list()
        if self._controller_prefs.get_conf_sheet_excel()['extension'] == '.xlsx':
            rd = ReadSheetExcel.create_load_pandas(self.get_path_sheet_variacao().absolute())
            _sheet_names = rd.get_sheet_names()
        elif self._controller_prefs.get_conf_sheet_excel()['extension'] == '.ods':
            rd = ReadSheetODS.create_load_pandas(self.get_path_sheet_variacao().absolute())
            _sheet_names = rd.get_sheet_index().get_sheet_names()
        else:
            raise RuntimeError()
        return _sheet_names

    def select_sheet_variacao(self) -> None:
        """
        Abre uma caixa de diálogo para o usuário selecionar uma planilha CSV/Excel.
        """
        f: File | None = self._controller_popup_files.get_sheet()
        if f is None:
            return

        _extension = f.extension().lower()
        self._controller_prefs.get_user_prefs()['sheet_variacao'] = f
        if (_extension == '.csv') or (_extension == '.txt'):
            self._controller_prefs.get_conf_sheet_csv()['extension'] = _extension
            self._controller_prefs.get_conf_sheet_csv()['path'] = f
        elif (_extension == '.xlsx') or (_extension == '.ods'):
            self._controller_prefs.get_conf_sheet_excel()['path'] = f
            self._controller_prefs.get_conf_sheet_excel()['extension'] = _extension
        self._controller_prefs.save_config()  # Salvar no disco após a seleção

