from __future__ import annotations
from app_variacao.app.models import (
    ModelFileDialog, ModelExportJson, ModelPreferences
)
from app_variacao.app.app_types import (
    ConfigFileDialog, ConfigSheetCsv, ConfigSheetExcel, ConfigMappingStyles, ConfigUserPrefs,
)
from app_variacao.soup_files import EnumDocFiles, File, Directory
from app_variacao.documents.types import ArrayList, BaseDict


class ControllerVariacao(object):

    def __init__(self):
        pass


class ControllerIoJson(ControllerVariacao):

    _instance_controller = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_controller is None:
            cls._instance_controller = super(ControllerIoJson, cls).__new__(cls)
        return cls._instance_controller

    def __init__(self, file_json: File):
        super().__init__()
        self.model = ModelExportJson(file_json=file_json)
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

    def set_file_json(self, f: File):
        self.model.set_file_json(f)

    def get_file_json(self) -> File:
        return self.model.get_file_json()

    def save_data_json(self, data: dict):
        self.model.save_data(data)

    def read_file_json(self) -> BaseDict | None:
        return self.model.read_file_json()


class ControllerPrefs(ControllerVariacao):

    _instance_controller = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_controller is None:
            cls._instance_controller = super(ControllerPrefs, cls).__new__(cls)
        return cls._instance_controller

    def __init__(self):
        super().__init__()
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.model: ModelPreferences = ModelPreferences()

    def get_user_prefs(self) -> ConfigUserPrefs:
        return self.model.get_config_user()

    def get_conf_sheet_csv(self) -> ConfigSheetCsv:
        return self.model.get_conf_sheet_csv()

    def get_conf_sheet_excel(self) -> ConfigSheetExcel:
        return self.model.get_config_sheet_excel()

    def get_conf_file_dialog(self) -> ConfigFileDialog:
        return self.model.get_conf_file_dialog()

    def get_conf_styles(self) -> ConfigMappingStyles:
        return self.model.get_conf_style()

    def get_work_dir_app(self) -> Directory:
        return self.model.get_config_user()['app_work_dir']

    def get_file_config(self) -> File:
        return self.model.file_prefs

    def save_config(self):
        self.model.save_prefs()


class ControllerPopUpFiles(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self.model = ModelFileDialog()

    def select_folder(self) -> Directory:
        return self.model.select_folder()

    def get_files_excel(self) -> ArrayList[File]:
        return self.model.select_files_disk(EnumDocFiles.EXCEL)

    def get_file_excel(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.EXCEL)

    def get_file_csv(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.CSV)

    def get_sheet(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.SHEET)
