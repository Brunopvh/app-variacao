from __future__ import annotations
from typing import Any, Union, Literal
from app_variacao.app.app_types import (
    ConfigImportCsv, ConfigImportExcel, ConfigApp, ConfigFileDialog,
    KeyFileDialog, KeyConfUser, ExtensionSheet, InterfaceCreateConfig,
    PrefImportCsv, PrefFileDialog, PreferencesApp, KeyConfImportCsv,
)
from app_variacao.app.ui import MappingStyles
from app_variacao.soup_files import (
    UserAppDir, Directory, File, ExtensionFiles, EnumDocFiles,
    JsonConvert, JsonData
)

_app_dir = UserAppDir('app-variacao')
_app_dir.config_dir_app().mkdir()


class ModelPreferences(object):

    _instance_model = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_model is None:
            cls._instance_model = super(ModelPreferences, cls).__new__(cls)
        return cls._instance_model

    def __init__(self) -> None:
        super().__init__()
        if hasattr(self, '_initialized_model') and self._initialized_model:
            return
        self._initialized_model = True
        self.file_prefs: File = _app_dir.config_dir_app().join_file('prefs-variacao.json')
        self._prefs_app: PreferencesApp = None
        self._pref_file_dialog = PrefFileDialog()
        self._pref_import_csv = PrefImportCsv()
        self._pref_styles = MappingStyles().create_default()

    def get_preferences_app(self) -> PreferencesApp:
        if self._prefs_app is None:
            #self._create_prefs()
            self.__create_default_prefs()
        return self._prefs_app

    def set_preferences_app(self, p: PreferencesApp):
        self._prefs_app = p

    def save_prefs(self):
        try:
            output = JsonConvert.from_dict(self.get_preferences_app().to_dict())
            output.to_json_data().to_file(self.file_prefs)
        except Exception as e:
            print(f"{__class__.__name__} {e}")

    def _load_file_prefs(self) -> dict[str, Any]:
        """
        Ler as configurações do APP a partir de um arquivo JSON no disco.
        """
        if not self.file_prefs.exists():
            raise FileNotFoundError(f'{__class__.__name__}(): Arquivo não encontrado {self.file_prefs}')
        values_file = JsonConvert.from_file(self.file_prefs)
        return values_file.to_json_data().to_dict()

    def __create_default_prefs(self):

        cfg_csv: ConfigImportCsv = {'encoding': 'utf-8', 'extension': '.csv', 'sep': ' '}
        cfg_dialog: ConfigFileDialog = {
            'initial_output_dir': _app_dir.userFileSystem.get_user_downloads(),
            'initial_input_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_input_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_output_dir': _app_dir.userFileSystem.get_user_downloads(),
        }

        self._prefs_app = PreferencesApp()
        self._prefs_app.get_config()['import_csv'] = cfg_csv
        self._prefs_app.get_config()['file_dialog'] = cfg_dialog
        self._prefs_app.get_config()['work_dir'] = _app_dir.workspaceDirApp
        self._prefs_app.get_config()['import_excel'] = ConfigImportExcel()
        self._prefs_app.get_config()['app_styles'] = self._pref_styles

        self._pref_file_dialog.merge(self._prefs_app.get_config()['file_dialog'])
        self._pref_import_csv.merge(self._prefs_app.get_config()['import_csv'])

    def _create_prefs(self) -> None:
        self.__create_default_prefs()
        if self.file_prefs.exists():
            # Criar preferências a partir do arquivo de configuração
            content_file_config: dict[str, Any] = self._load_file_prefs()
            self._prefs_app.create_from_dict(content_file_config)

