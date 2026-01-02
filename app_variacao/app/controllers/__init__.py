from __future__ import annotations
from app_variacao.app.models import (
    ModelPopUpFiles, ModelVariacao, ModelExportJson, ModelAppConfig, EnumPrefs,
    PreferencesFileDialog, PreferencesUser
)
from app_variacao.soup_files import (
    EnumDocFiles, File, JsonConvert, JsonData, Directory
)
from app_variacao.types.array import ArrayList, BaseDict


class ControllerVariacao(object):

    def __init__(self):
        self.model = ModelVariacao()


class ControllerPopUpFiles(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self.model = ModelPopUpFiles()

    def select_folder(self) -> Directory:
        return self.model.select_folder()

    def get_files_excel(self) -> ArrayList[File]:
        return self.model.select_files_disk(EnumDocFiles.EXCEL)

    def get_file_excel(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.EXCEL)

    def get_file_csv(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.CSV)


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


class ControllerAppConfig(ControllerVariacao):

    _instance_controller = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_controller is None:
            cls._instance_controller = super(ControllerAppConfig, cls).__new__(cls)
        return cls._instance_controller

    def __init__(self):
        super().__init__()
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.model = ModelAppConfig()
        self._config_app: dict = {}

    def get_prefs_file_dialog(self) -> PreferencesFileDialog:
        return self.model.load_prefs_file_dialog()

    def get_prefs_user(self) -> PreferencesUser:
        return self.model.load_prefs_user()

    def get_work_dir_app(self) -> str:
        return self.model.load_prefs_user()['work_dir']

    def set_work_dir_app(self, d: Directory):
        _prefs = self.model.load_prefs_user()
        _prefs['work_dir'] = d.absolute()
        self.model.save_prefs_user(_prefs)

    def get_file_config(self) -> File:
        return self.model.get_file_config()

    def load_disk_pref(self, pref: EnumPrefs) -> BaseDict | None:
        if pref == EnumPrefs.PREFS_FILE_DIALOG:
            return self.model.load_prefs_file_dialog()
        else:
            return BaseDict()

    def save_config(self, name_pref: EnumPrefs, values_prefs: dict):
        if name_pref == EnumPrefs.PREFS_FILE_DIALOG:
            self.model.save_prefs_file_dialog(values_prefs)
        elif name_pref == EnumPrefs.ALL:
            self.model.save_all_prefs(values_prefs)




