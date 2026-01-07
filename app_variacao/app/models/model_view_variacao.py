from __future__ import annotations
import pandas as pd
import threading
from app_variacao.documents.sheet import ReadSheetExcel, ReadSheetODS, ReadSheetCsv
from app_variacao.app.app_types import ConfigSheetCsv, ConfigSheetExcel, ConfigUserPrefs
from app_variacao.app.models.base_model import ModelPreferences


class ModelViewVariacao:

    def __init__(self):
        self.isLoading = False
        self.model_prefs = ModelPreferences()
        self.df: pd.DataFrame = pd.DataFrame()

    def read_data_frame(self, config: ConfigSheetExcel | ConfigSheetCsv) -> None:
        self.isLoading = True
        if not 'path' in config.keys():
            self.isLoading = False
            return
        if not config["path"].exists():
            self.isLoading = False
            return

        try:

            if (config['extension'] == '.csv') or (config['extension'] == '.txt'):
                rd = ReadSheetCsv.create_load_pandas(
                    config['path'].absolute(), delimiter=config['sep'], encoding=config['encoding']
                )
                self.df = rd.get_workbook_data().get_first().to_data_frame()
            elif config['extension'] == '.xlsx':
                rd = ReadSheetExcel.create_load_pandas(config['path'].absolute())
                self.df = rd.get_workbook_data(config['sheet_name']).get_first().to_data_frame()
            elif config['extension'] == '.ods':
                raise NotImplementedError()
        except Exception as e:
            print('==================================================')
            print(e)
        self.isLoading = False
