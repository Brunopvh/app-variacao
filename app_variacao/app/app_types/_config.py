from __future__ import annotations
from typing import Any, Literal, Union, TypedDict
from app_variacao.util import Directory, File
from app_variacao.soup_files import JsonData, JsonConvert
from app_variacao.documents import CsvSeparator, CsvEncoding
from app_variacao.app.ui import (
    EnumStyles, ConfigMappingStyles, keyStyles, valueStyle
)

keyConfFileDialog = Literal[
    'initial_input_dir', 'initial_output_dir', 'last_input_dir', 'last_output_dir', 'last_dir',
]
keyConfApp = Literal['file_dialog', 'styles', 'sheet_csv', 'sheet_excel', 'prefs_user']
keyConfSheetCsv = Literal['extension', 'path', 'sep', 'encoding',]
keyConfSheetExcel = Literal['sheet_name', 'path', 'extension']
ExtensionSheet = Literal['.xlsx', '.ods', '.csv', '.txt']

valueConfCsv = Union[str, File, CsvEncoding, ExtensionSheet]
valueConfExcel = Union[str, File, ExtensionSheet]


#==============================================================#
# Configurações
#==============================================================#
class ConfigSheetCsv(TypedDict, total=False):

    extension: ExtensionSheet
    path: File
    sep: CsvSeparator
    encoding: CsvEncoding


class ConfigSheetExcel(TypedDict, total=False):

    path: File
    sheet_name: str
    extension: ExtensionSheet


class ConfigFileDialog(TypedDict):

    initial_input_dir: Directory
    initial_output_dir: Directory
    last_input_dir: Directory
    last_output_dir: Directory
    last_dir: Directory


class ConfigUserPrefs(TypedDict):

    app_work_dir: Directory
    sheet_variacao: File


class ConfigApp(TypedDict, total=False):
    """
    Tipos para o dicionário de configuração geral.
    """

    work_dir: ConfigUserPrefs
    file_dialog: ConfigFileDialog
    sheet_csv: ConfigSheetCsv
    sheet_excel: ConfigSheetExcel
    app_styles: dict[str, Any]


#==============================================================#
# Configurações/Criação
#==============================================================#
class InterfaceCreateConfig(object):

    _instances: dict[type, object] = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self) -> None:
        if getattr(self, "_initialized_conf", False):
            return
        self._initialized_conf = True
        self._config: dict[str, Any] | dict = dict()

    def get_name(self) -> keyConfApp:
        raise NotImplementedError()

    def set_config(self, conf: dict[str, Any]) -> None:
        self._config = conf

    def get_config(self) -> dict[str, Any]:
        return self._config

    def update_config(self, k: str, v: Any):
        """
        Atualiza o valor de uma configuração
        """
        self._config[k] = v

    def merge(self, data: dict[str, Any]) -> None:
        pass

    def create_from_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    def to_dict(self) -> dict[str, Any]:
        pass

    def to_json_string(self) -> str:
        _json_data: JsonData = JsonConvert.from_dict(self.to_dict()).to_json_data()
        return _json_data.to_string()


class PrefsConfUser(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()

    def get_config(self) -> ConfigUserPrefs:
        return self._config

    def get_name(self) -> keyConfApp:
        return 'prefs_user'

    def merge(self, data: ConfigUserPrefs) -> None:
        for k, v in data.items():
            self._config[k] = v

    def to_dict(self) -> dict[str, Any]:
        final: dict[str, Any] = dict()
        for k, v in self._config.items():
            if hasattr(v, 'absolute'):
                final[k] = v.absolute()
        return final

    def create_from_dict(self, data: dict[str, Any]) -> ConfigUserPrefs:
        final: ConfigUserPrefs = ConfigUserPrefs()
        for k, value in data.items():
            if k == 'app_work_dir':
                if isinstance(value, Directory):
                    final[k] = value
                else:
                    final[k] = Directory(value)
            elif k == 'sheet_variacao':
                if isinstance(value, File):
                    final[k] = value
                else:
                    final[k] = File(data[k])
        self.merge(final)
        return final


class PrefStyles(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()

    def get_name(self) -> keyConfApp:
        return 'styles'

    def get_config(self) -> ConfigMappingStyles:
        return self._config

    def set_config(self, cfg: ConfigMappingStyles):
        self._config = cfg

    def merge(self, data: ConfigMappingStyles) -> None:
        for k, _value in data.items():
            self._config[k] = _value

    def to_dict(self) -> dict[str, str]:
        final = dict()
        key: keyStyles
        value_style: valueStyle
        for key, value_style in self._config.items():
            if isinstance(value_style, EnumStyles):
                final[key] = value_style.value
            else:
                final[key] = value_style
        return final

    def create_from_dict(self, data: dict[str, Any]) -> ConfigMappingStyles:
        final: ConfigMappingStyles = dict()
        key_style: keyStyles
        value_style: valueStyle
        for key_style, value_style in data.items():
            if key_style == 'buttons':
                if value_style == EnumStyles.BUTTON_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.BUTTON_PURPLE_LIGHT
                elif value_style == EnumStyles.BUTTON_GREEN.value:
                    final[key_style] = EnumStyles.BUTTON_GREEN
                elif value_style == EnumStyles.BUTTON_PURPLE_DARK.value:
                    final[key_style] = EnumStyles.BUTTON_PURPLE_DARK
            elif key_style == 'labels':
                if value_style == EnumStyles.LABEL_DEFAULT.value:
                    final[key_style] = EnumStyles.LABEL_DEFAULT
                elif value_style == EnumStyles.LABEL_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.LABEL_PURPLE_LIGHT
            elif key_style == 'frames':
                if value_style == EnumStyles.FRAME_DARK.value:
                    final[key_style] = EnumStyles.FRAME_DARK
                elif value_style == EnumStyles.FRAME_LIGHT.value:
                    final[key_style] = EnumStyles.FRAME_LIGHT
                elif value_style == EnumStyles.FRAME_PURPLE_DARK.value:
                    final[key_style] = EnumStyles.FRAME_PURPLE_DARK
                elif value_style == EnumStyles.FRAME_DARK_GRAY.value:
                    final[key_style] = EnumStyles.FRAME_DARK_GRAY
                elif value_style == EnumStyles.FRAME_ORANGE_DARK.value:
                    final[key_style] = EnumStyles.FRAME_ORANGE_DARK
            elif key_style == 'pbar':
                if value_style == EnumStyles.PBAR_PURPLE.value:
                    final[key_style] = EnumStyles.PBAR_PURPLE
                elif value_style == EnumStyles.PBAR_GREEN.value:
                    final[key_style] = EnumStyles.PBAR_GREEN
                elif value_style == EnumStyles.PBAR_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.PBAR_PURPLE_LIGHT
            elif key_style == 'menu_bar':
                if value_style == EnumStyles.TOPBAR_DARK.value:
                    final[key_style] = EnumStyles.TOPBAR_DARK
                elif value_style == EnumStyles.TOPBAR_LIGHT.value:
                    final[key_style] = EnumStyles.TOPBAR_LIGHT
                elif value_style == EnumStyles.TOPBAR_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.TOPBAR_PURPLE_LIGHT
                elif value_style == EnumStyles.TOPBAR_PURPLE_DARK.value:
                    final[key_style] = EnumStyles.TOPBAR_PURPLE_DARK
        self.merge(final)
        return final


class PrefFileDialog(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()
        self._config: ConfigFileDialog = ConfigFileDialog()

    def get_name(self) -> keyConfApp:
        return 'file_dialog'

    def get_config(self) -> ConfigFileDialog:
        return self._config

    def set_config(self, conf: ConfigFileDialog) -> None:
        self._config = conf

    def update_config(self, k: keyConfFileDialog, v: Directory | Any):
        self._config[k] = v

    def to_dict(self) -> dict[str, Any]:
        output: dict[str, str] = dict()
        key: keyConfFileDialog
        value: Directory
        for key, value in self.get_config().items():
            if key == 'initial_input_dir':
                output[key] = value.absolute()
            elif key == 'initial_output_dir':
                output[key] = value.absolute()
            elif key == 'last_input_dir':
                output[key] = value.absolute()
            elif key == 'last_output_dir':
                output[key] = value.absolute()
            elif key == 'last_dir':
                output[key] = value.absolute()
        return output

    def merge(self, data: ConfigFileDialog) -> None:
        for key, value in data.items():
            self._config[key] = value

    def create_from_dict(self, data: dict[str, Any]) -> ConfigFileDialog:
        final: ConfigFileDialog = dict()
        key: keyConfFileDialog
        value: str
        for key, value in data.items():
            if key == 'initial_input_dir':
                final[key] = Directory(value)
            elif key == 'initial_output_dir':
                final[key] = Directory(value)
            elif key == 'last_input_dir':
                final[key] = Directory(value)
            elif key == 'last_output_dir':
                final[key] = Directory(value)
            elif key == 'last_dir':
                final[key] = Directory(value)
        self.set_config(final)
        return final


#==============================================================#
# Configurações para importação de planilhas
#==============================================================#
class PrefSheetCsv(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()

        self._config['extension'] = '.csv'
        self._config['sep'] = ";"
        self._config['encoding'] = 'utf-8'

    def get_name(self) -> keyConfApp:
        return 'sheet_csv'

    def get_config(self) -> ConfigSheetCsv:
        return self._config

    def update_config(
            self, k: keyConfSheetCsv, v: CsvSeparator | CsvEncoding | File | ExtensionSheet
        ) -> None:
        self._config[k] = v

    def create_from_dict(self, data: dict[str, Any]) -> ConfigSheetCsv:
        final: ConfigSheetCsv = dict()
        key: keyConfSheetCsv
        value: str
        for key, value in data.items():
            if key == 'extension':
                final[key] = value
            elif key == 'sep':
                final[key] = value
            elif key == 'encoding':
                final[key] = value
            elif key == 'path':
                final[key] = File(value)
        self.set_config(final)
        return final

    def merge(self, data: ConfigSheetCsv) -> None:
        for key, value in data.items():
            self._config[key] = value

    def to_dict(self) -> dict[str, Any]:
        final = dict()
        for key, value in self.get_config().items():
            if key == 'path':
                final[key] = value.absolute()
            else:
                final[key] = value
        return final


class PrefSheetExcel(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()
        self._config: ConfigSheetExcel = dict()

    def get_name(self) -> keyConfApp:
        return 'sheet_excel'

    def get_config(self) -> ConfigSheetExcel:
        return self._config

    def set_config(self, conf: ConfigSheetExcel) -> None:
        self._config = conf

    def update_config(self, k: keyConfSheetExcel, v: valueConfExcel):
        self._config[k] = v

    def create_from_dict(self, data: dict[str, Any]) -> ConfigSheetExcel:
        final: ConfigSheetExcel = dict()
        key: keyConfSheetExcel
        value: valueConfExcel
        for key, value in data.items():
            if key == 'extension':
                final[key] = value
            elif key == 'sheet_name':
                final[key] = value
            elif key == 'path':
                if isinstance(value, str):
                    final[key] = File(value)
                elif isinstance(value, File):
                    final[key] = value
        self.set_config(final)
        return final

    def merge(self, data: ConfigSheetExcel) -> None:
        key: keyConfSheetExcel
        value: valueConfExcel
        for key, value in data.items():
            self._config[key] = value

    def to_dict(self) -> dict[str, Any]:
        final = dict()
        for key, value in self.get_config().items():
            if key == 'path':
                final[key] = value.absolute()
            else:
                final[key] = value
        return final

