from __future__ import annotations
from typing import Any, Literal, Union, TypedDict
from app_variacao.util import Directory, File
from app_variacao.soup_files import EnumDocFiles, ExtensionFiles
from app_variacao.documents import CsvSeparator, CsvMapping, CsvEncoding, create_csv_mapping

KeyFileDialog = Literal[
    'initial_input_dir', 'initial_output_dir', 'last_input_dir', 'last_output_dir', 'last_dir',
]
KeyConfUser = Literal['file_dialog', 'app_styles', 'work_dir', 'import_csv', 'import_excel']
KeyConfImportCsv = Literal['extension', 'path', 'sep', 'encoding', 'sheet_name']
ExtensionSheet = Literal['.xlsx', '.ods', '.csv', '.txt']


#==============================================================#
# Configurações
#==============================================================#
class ConfigImportCsv(TypedDict, total=False):

    extension: ExtensionSheet
    path: File
    sep: CsvSeparator
    encoding: CsvEncoding


class ConfigImportExcel(TypedDict, total=False):

    path: File
    sheet_name: str
    extension: ExtensionSheet


class ConfigFileDialog(TypedDict):

    initial_input_dir: Directory
    initial_output_dir: Directory
    last_input_dir: Directory
    last_output_dir: Directory
    last_dir: Directory


class ConfigApp(TypedDict, total=False):
    """
    Tipos para o dicionário de configuração geral.
    """

    work_dir: Directory
    file_dialog: ConfigFileDialog
    import_csv: ConfigImportCsv
    import_excel: ConfigImportExcel


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
        self._config: dict[str, Any] = dict()

    def set_config(self, conf: dict[str, Any]) -> None:
        self._config = conf

    def get_config(self) -> dict[str, Any]:
        return self._config

    def update_config(self, k: str, v: Any):
        self._config[k] = v

    def merge(self, data: dict[str, Any]) -> None:
        pass

    def create_from_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    def to_dict(self) -> dict[str, Any]:
        pass

    def to_json_string(self) -> str:
        pass


class PrefFileDialog(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()

    def get_config(self) -> ConfigFileDialog:
        return self._config

    def set_config(self, conf: ConfigFileDialog) -> None:
        self._config = conf

    def to_dict(self) -> dict[str, Any]:
        output: dict[str, str] = dict()
        key: KeyFileDialog
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
        key: KeyFileDialog
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
class PrefImportCsv(InterfaceCreateConfig):

    def __init__(self) -> None:
        super().__init__()

        self._config['extension'] = '.csv'
        self._config['sep'] = ";"
        self._config['encoding'] = 'utf-8'

    def create_from_dict(self, data: dict[str, Any]) -> ConfigImportCsv:
        final: ConfigImportCsv = dict()
        key: KeyConfImportCsv
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

    def merge(self, data: ConfigImportCsv) -> None:
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


#==============================================================#
# Configurações gerais do APP
#==============================================================#
class PreferencesApp(InterfaceCreateConfig):
    """
    Preferências do APP
    """

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}()\n{self.get_config().values()}"

    def get_config(self) -> ConfigApp:
        return self._config

    def set_config(self, conf: ConfigApp) -> None:
        self._config = conf

    def to_dict(self) -> dict[str, Any]:
        data = {}
        k: KeyConfUser
        v: Any
        for k, v in self.get_config().items():
            # métodos absolute() devem ser salvos como strings.
            if hasattr(v, 'absolute'):
                data[k] = v.absolute()
            elif k == 'app_styles':
                data[k] = v.to_dict()
            elif k == 'prefs_file_dialog':
                data[k] = v.to_dict()
            elif k == 'sheet_variacao':
                data[k] = v.to_dict()
            else:
                data[k] = v
        return data

    def merge(self, data: ConfigApp) -> None:
        k: KeyConfUser
        for k, v in data.items():
            if k == 'app_styles':
                self._config['app_styles'] = v
            elif k == 'file_dialog':
                self._config['file_dialog'] = v
            elif k == 'import_csv':
                self._config['import_csv'] = v
            elif k == 'import_excel':
                pass
            else:
                self._config[k] = v

    def create_from_dict(self, data: dict[str, Any]) -> ConfigApp:
        key: KeyConfUser
        for key, value_conf in data.items():
            # Verificar se é uma configuração de filedialog
            if key == 'file_dialog':
                prefs_file_dialog = PrefFileDialog().create_from_dict(value_conf)
                self.update_config('file_dialog', prefs_file_dialog)
            # Verificar se é uma configuração de estilo
            elif key == 'app_styles':
                pass
            elif key == 'work_dir':
                if isinstance(value_conf, str):
                    self.update_config('work_dir', Directory(value_conf))
                elif isinstance(value_conf, Directory):
                    self.update_config('work_dir', value_conf)
            elif key == 'import_csv':
                fmt_conf = PrefImportCsv().create_from_dict(value_conf)
                self.update_config('import_csv', fmt_conf)
            elif key == 'import_excel':
                pass
        return self.get_config()
