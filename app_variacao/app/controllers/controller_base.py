from __future__ import annotations
from app_variacao.app.models import (
    ModelFileDialog, ModelExportJson, ModelPreferences, UserPreferences
)
from app_variacao.soup_files import (
    EnumDocFiles, File, Directory
)
from app_variacao.types.array import ArrayList, BaseDict


class ControllerVariacao(object):

    def __init__(self):
        #self.model = ModelVariacao()
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

    def get_prefs(self) -> UserPreferences:
        return self.model.get_preferences()

    def get_work_dir_app(self) -> str:
        return self.model.get_preferences()['work_dir']

    def set_work_dir_app(self, d: Directory):
        self.get_prefs()['work_dir'] = d
        self.save_config()

    def get_file_config(self) -> File:
        return self.model.file_prefs

    def save_config(self):
        self.model.save_prefs()
