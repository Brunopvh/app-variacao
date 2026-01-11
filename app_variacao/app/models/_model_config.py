from __future__ import annotations
from typing import Any, Union, Literal
from app_variacao.app.app_types import (
    ConfigApp, ConfigFileDialog, ConfigSheetCsv, ConfigSheetExcel, ConfigMappingStyles,
    PrefStyles, PrefSheetExcel, PrefFileDialog, PrefSheetCsv, CsvEncoding, CsvSeparator,
    valueStyle, valueConfCsv, keyStyles, keyConfSheetCsv, keyConfFileDialog, keyConfApp, keyConfSheetExcel,
    InterfaceCreateConfig, PrefsConfUser, ConfigUserPrefs,
)
from app_variacao.app.ui import EnumStyles
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
        self._pref_style: PrefStyles = PrefStyles()
        self._pref_file_dialog: PrefFileDialog = PrefFileDialog()
        self._pref_sheet_csv: PrefSheetCsv = PrefSheetCsv()
        self._pref_sheet_excel: PrefSheetExcel = PrefSheetExcel()
        self._pref_user: PrefsConfUser = PrefsConfUser()
        self._prefs_all: dict[keyConfApp, InterfaceCreateConfig] = dict()
        self._init_prefs()

    def _load_file_prefs(self) -> dict[str, Any]:
        """
        Ler as configurações do APP a partir de um arquivo JSON no disco.
        """
        if not self.file_prefs.exists():
            raise FileNotFoundError(f'{__class__.__name__}(): Arquivo não encontrado {self.file_prefs}')
        values_file = JsonConvert.from_file(self.file_prefs)
        return values_file.to_json_data().to_dict()

    def __create_default_prefs(self):

        cfg_csv: ConfigSheetCsv = {'encoding': 'utf-8', 'extension': '.csv', 'sep': ' '}
        cfg_excel: ConfigSheetExcel = dict()
        cfg_user: ConfigUserPrefs = {'app_work_dir': _app_dir.workspaceDirApp}

        cfg_dialog: ConfigFileDialog = {
            'initial_output_dir': _app_dir.userFileSystem.get_user_downloads(),
            'initial_input_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_input_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_output_dir': _app_dir.userFileSystem.get_user_downloads(),
        }

        cfg_style: ConfigMappingStyles = {
                'buttons': EnumStyles.BUTTON_PURPLE_LIGHT,
                'labels': EnumStyles.LABEL_PURPLE_LIGHT,
                'frames': EnumStyles.FRAME_PURPLE_DARK,
                'pbar': EnumStyles.PBAR_PURPLE,
                'app': EnumStyles.WINDOW_DARK,
                'menu_bar': EnumStyles.TOPBAR_DARK,
                'last_update': 'frames',
                'tree_view': EnumStyles.TREE_VIEW_DARK,
            }

        self._pref_sheet_csv.merge(cfg_csv)
        self._pref_sheet_excel.merge(cfg_excel)
        self._pref_file_dialog.merge(cfg_dialog)
        self._pref_style.merge(cfg_style)
        self._pref_user.merge(cfg_user)

        self._prefs_all[self._pref_sheet_csv.get_name()] = self._pref_sheet_csv
        self._prefs_all[self._pref_sheet_excel.get_name()] = self._pref_sheet_excel
        self._prefs_all[self._pref_file_dialog.get_name()] = self._pref_file_dialog
        self._prefs_all[self._pref_style.get_name()] = self._pref_style
        self._prefs_all[self._pref_user.get_name()] = self._pref_user

    def __create_prefs_from_file(self) -> None:
        content_file: dict[keyConfApp, dict[str, Any]] = self._load_file_prefs()
        key: keyConfApp
        for key, value in content_file.items():
            self._prefs_all[key].create_from_dict(value)

    def _init_prefs(self) -> None:
        self.__create_default_prefs()
        if self.file_prefs.exists():
            # Criar preferências a partir do arquivo de configuração
            self.__create_prefs_from_file()

    def to_dict(self) -> dict[str, dict[str, Any]]:
        final: dict[keyConfApp, dict[str, Any]] = dict()
        for k, v in self._prefs_all.items():
            final[k] = v.to_dict()
        return final

    def save_prefs(self):
        try:
            output = JsonConvert.from_dict(self.to_dict())
            output.to_json_data().to_file(self.file_prefs)
        except Exception as e:
            print(f"{__class__.__name__} {e}")

    def get_conf_from_name(self, name: keyConfApp) -> InterfaceCreateConfig:
        return self._prefs_all[name]

    def get_conf_style(self) -> ConfigMappingStyles:
        return self._prefs_all['styles'].get_config()

    def set_conf_style(self, style: ConfigMappingStyles):
        self._prefs_all['styles'].set_config(style)

    def get_conf_file_dialog(self) -> ConfigFileDialog:
        return self._prefs_all['file_dialog'].get_config()

    def set_conf_file_dialog(self, file_dialog: ConfigFileDialog):
        self._prefs_all['file_dialog'].set_config(file_dialog)

    def get_conf_sheet_csv(self) -> ConfigSheetCsv:
        return self._prefs_all['sheet_csv'].get_config()

    def set_config_sheet_csv(self, conf: ConfigSheetCsv):
        self._prefs_all['sheet_csv'].set_config(conf)

    def get_config_sheet_excel(self) -> ConfigSheetExcel:
        return self._prefs_all['sheet_excel'].get_config()

    def set_config_sheet_excel(self, conf: ConfigSheetExcel):
        self._prefs_all['sheet_excel'].set_config(conf)

    def get_config_user(self) -> ConfigUserPrefs:
        return self._prefs_all['prefs_user'].get_config()

    def set_config_user(self, conf: ConfigUserPrefs):
        self._prefs_all['prefs_user'].set_config(conf)

