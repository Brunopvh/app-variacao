from __future__ import annotations
import json
from typing import Any, TypedDict, Literal, Union
from app_variacao.documents.sheet.csv import CsvEncoding
from app_variacao.types.array import ArrayList, BaseDict
from app_variacao.soup_files import JsonConvert
from app_variacao.app.ui import MappingStyles, TypeMappingStylesDict
from app_variacao.util import File, Directory, EnumDocFiles, UserAppDir
from tkinter import filedialog
import os.path

_app_dir = UserAppDir('app-variacao')

KeyFileDialog = Literal[
    'initial_input_dir', 'initial_output_dir', 'last_input_dir', 'last_output_dir', 'last_dir',
]


#==============================================================#
# Configurações para o pop-up filedialog
#==============================================================#
class TypeConfFileDialog(TypedDict):

    initial_input_dir: Directory
    initial_output_dir: Directory
    last_input_dir: Directory
    last_output_dir: Directory
    last_dir: Directory


class PreferencesFileDialog(BaseDict):

    _instance_prefs = None  # Singleton
    keys_file_dialog: tuple = (
        'initial_output_dir', 'initial_input_dir', 'last_dir', 'last_input_dir', 'last_output_dir'
    )

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(PreferencesFileDialog, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self, values: TypeConfFileDialog = None) -> None:
        super().__init__(values)
        if hasattr(self, '_initialized_prefs') and self._initialized_prefs:
            return
        self._initialized_prefs = True

    def to_dict(self) -> dict[str, str]:
        output: dict[str, str] = dict()
        key: KeyFileDialog
        value: Directory
        for key, value in self.items():
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

    def merge(self, data: TypeConfFileDialog) -> None:
        for key, value in data.items():
            self[key] = value

    @classmethod
    def format_dict(cls, data: dict[str, str]) -> TypeConfFileDialog:
        final: TypeConfFileDialog = dict()
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
        return final

    @classmethod
    def create_default(cls) -> PreferencesFileDialog:
        data: TypeConfFileDialog = {
            'initial_input_dir': _app_dir.userFileSystem.get_user_downloads(),
            'initial_output_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_input_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_output_dir': _app_dir.userFileSystem.get_user_downloads(),
            'last_dir': _app_dir.userFileSystem.get_user_downloads(),
        }
        return cls(data)


#==============================================================#
# Configurações para importação de planilhas
#==============================================================#

ExtensionSheet = Literal['.xlsx', '.ods', '.csv', '.txt']
CsvSep = Literal[',', ';', '\t', '|', '_']
KeyCsvImport = Literal['extension', 'path', 'sep', 'encoding']


class TypeImportSheet(TypedDict, total=False):

    extension: ExtensionSheet
    path: File
    sep: CsvSep
    encoding: CsvEncoding


class PreferencesImportSheet(BaseDict):

    _instance_prefs = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(PreferencesImportSheet, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self, values: TypeImportSheet = None) -> None:
        super().__init__(values)
        if hasattr(self, '_initialized_prefs') and self._initialized_prefs:
            return
        self._initialized_prefs = True
        self['extension'] = '.csv'
        self['sep'] = ";"
        self['encoding'] = 'utf-8'

    @classmethod
    def format_dict(cls, data: dict[str, Any]) -> TypeImportSheet:
        final: TypeImportSheet = dict()
        key: KeyCsvImport
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
        return final

    def merge(self, data: TypeImportSheet) -> None:
        for key, value in data.items():
            self[key] = value

    def to_dict(self) -> dict[str, str]:
        final = dict()
        for key, value in self.items():
            if key == 'path':
                final[key] = value.absolute()
            else:
                final[key] = value
        return final


#==============================================================#
# Configurações gerais do APP
#==============================================================#
KeyUserConfig = Literal['prefs_file_dialog', 'app_styles', 'work_dir', 'sheet_variacao']


class TypeConfApp(TypedDict, total=False):
    """
    Tipos para o dicionário de configuração geral.
    """

    prefs_file_dialog: PreferencesFileDialog
    app_styles: MappingStyles
    work_dir: Directory
    sheet_variacao: TypeImportSheet


class UserPreferences(BaseDict):
    """
    Preferências do APP
    """

    _instance_prefs = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(UserPreferences, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self, values: TypeConfApp = None) -> None:
        super().__init__(values)
        if hasattr(self, '_initialized_prefs') and self._initialized_prefs:
            return
        self._initialized_prefs = True
        self['prefs_file_dialog'] = PreferencesFileDialog.create_default()
        self['app_styles'] = MappingStyles.create_default()
        self['work_dir'] = _app_dir.workspaceDirApp
        self['sheet_variacao'] = PreferencesImportSheet()

    def __repr__(self):
        return f"{self.__class__.__name__}()\n{self.values()}"

    def get_pref_file_dialog(self) -> PreferencesFileDialog:
        return self['prefs_file_dialog']

    def get_app_styles(self) -> MappingStyles:
        return self['app_styles']

    def to_dict(self) -> dict[str, Any]:
        data = {}
        k: KeyUserConfig
        v: Any
        for k, v in self.items():
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

    def merge_dict(self, merge: TypeConfApp) -> None:
        k: KeyUserConfig
        for k, v in merge.items():
            if k == 'app_styles':
                self['app_styles'] = v
            elif k == 'prefs_file_dialog':
                self['prefs_file_dialog'] = v
            elif k == 'sheet_variacao':
                self['sheet_variacao'] = v
            else:
                self[k] = v

    @classmethod
    def format_dict(cls, data: dict[str, Any]) -> TypeConfApp:
        final: TypeConfApp = dict()
        key: KeyUserConfig
        for key, value_conf in data.items():
            # Verificar se é uma configuração de filedialog
            if key == 'prefs_file_dialog':
                prefs_file_dialog = PreferencesFileDialog.create_default()
                data_file_dialog: TypeConfFileDialog = PreferencesFileDialog.format_dict(value_conf)
                prefs_file_dialog.merge(data_file_dialog)
                final['prefs_file_dialog'] = prefs_file_dialog
            # Verificar se é uma configuração de estilo
            elif key == 'app_styles':
                fmt_data_styles: TypeMappingStylesDict = MappingStyles.format_dict(value_conf)
                mapping_styles: MappingStyles = MappingStyles.create_default()
                mapping_styles.merge_dict(fmt_data_styles)
                final['app_styles'] = mapping_styles
            elif key == 'work_dir':
                if isinstance(value_conf, str):
                    final['work_dir'] = Directory(value_conf)
                elif isinstance(value_conf, Directory):
                    final['work_dir'] = value_conf
            elif key == 'sheet_variacao':
                fmt_conf = PreferencesImportSheet.format_dict(value_conf)
                pref_import = PreferencesImportSheet()
                pref_import.merge(fmt_conf)
                final['sheet_variacao'] = pref_import
        return final


class ModelPreferences(object):

    _instance_prefs = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(ModelPreferences, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self) -> None:
        super().__init__()
        if hasattr(self, '_initialized_prefs') and self._initialized_prefs:
            return
        self._initialized_prefs = True
        self.file_prefs: File = _app_dir.config_dir_app().join_file('prefs-variacao.json')
        self._user_prefs: UserPreferences = None

    def get_preferences(self) -> UserPreferences:
        if self._user_prefs is None:
            self._create_prefs()
        return self._user_prefs

    def save_prefs(self):
        output = JsonConvert.from_dict(self.get_preferences().to_dict())
        output.to_json_data().to_file(self.file_prefs)

    def load_file_prefs(self) -> dict[str, Any]:
        """
        Ler as configurações do APP a partir de um arquivo JSON no disco.
        """
        if not self.file_prefs.exists():
            raise FileNotFoundError(f'{__class__.__name__}(): Arquivo não encontrado {self.file_prefs}')
        values_file = JsonConvert.from_file(self.file_prefs)
        return values_file.to_json_data().to_dict()

    def _create_prefs(self) -> None:
        self._user_prefs = UserPreferences()
        if self.file_prefs.exists():
            # Criar preferências a partir do arquivo de configuração
            content_file_config: dict[str, Any] = self.load_file_prefs()
            self._user_prefs.merge_dict(
                UserPreferences.format_dict(content_file_config)
            )


class AppFileDialog(object):
    """Caixa de diálogo para seleção de vários tipos de arquivos."""

    _instance_file_dialog = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_file_dialog is None:
            cls._instance_file_dialog = super(AppFileDialog, cls).__new__(cls)
        return cls._instance_file_dialog

    def __init__(self) -> None:
        self.prefs: TypeConfFileDialog = ModelPreferences().get_preferences().get_pref_file_dialog()
        self.title_pop_up_files: str = 'Selecione um arquivo'
        self.pop_up_text_filetypes: list[tuple[str, str]] = [("Todos os arquivos", "*"), ]
        self.default_extension = '.*'

    def _config_pop_up_open_filename(self, file_ext_type: EnumDocFiles) -> None:
        """
            Caixa de diálogo para selecionar um arquivo
        """
        self.title_pop_up_files = 'Selecione um arquivo'
        if file_ext_type == EnumDocFiles.CSV:
            self.pop_up_text_filetypes = [("Planilhas", "*.csv"), ("Arquivos CSV", "*.csv *.txt")]
            self.title_pop_up_files = 'Selecione uma planilha CSV'
        elif file_ext_type == EnumDocFiles.EXCEL:
            self.pop_up_text_filetypes = [("Arquivos Excel", "*.xlsx")]
            self.title_pop_up_files = 'Selecione uma planilha Excel'
        elif file_ext_type == EnumDocFiles.ODS:
            self.pop_up_text_filetypes = [("Arquivos ODS", "*.ods")]
            self.title_pop_up_files = 'Selecione uma planilha ODS'
        elif file_ext_type == EnumDocFiles.SHEET:
            self.pop_up_text_filetypes = [
                ("Planilhas Excel", "*.xlsx"),
                ("Planilhas ODS", "*.ods"),
                ("Planilhas CSV", "*.csv *.txt"),
            ]
            self.title_pop_up_files = 'Selecione uma Planilha'
        elif file_ext_type == EnumDocFiles.IMAGE:
            self.pop_up_text_filetypes = [("Arquivos de Imagem", "*.png *.jpg *.jpeg *.svg")]
            self.title_pop_up_files = 'Selecione Imagens'
        elif file_ext_type == EnumDocFiles.PDF:
            self.pop_up_text_filetypes = [("Arquivos PDF", "*.pdf *.PDF"), ]
            self.title_pop_up_files = 'Selecione arquivos PDF'
        else:
            self.title_pop_up_files = 'Selecione um arquivo'
            self.pop_up_text_filetypes = [("Todos os tipos de arquivos", ".*"), ]

    def _config_pop_up_save_filename(self, type_file: EnumDocFiles = EnumDocFiles.ALL_DOCUMENTS) -> str | None:
        """Abre uma caixa de diálogo para salvar arquivos."""
        self.title_pop_up_files = "Salvar arquivo como"
        if type_file == EnumDocFiles.SHEET:
            self.default_extension = '.xlsx'
            self.pop_up_text_filetypes = [("Arquivos Excel", "*.xlsx"), ("Arquivos CSV", "*.csv")]
        elif type_file == EnumDocFiles.EXCEL:
            self.default_extension = '.xlsx'
            self.pop_up_text_filetypes = [("Arquivos Excel", "*.xlsx")]
        elif type_file == EnumDocFiles.CSV:
            self.default_extension = '.csv'
            self.pop_up_text_filetypes = [("Arquivos CSV", "*.csv"), ("Arquivos de texto", "*.txt")]
        elif type_file == EnumDocFiles.ODS:
            self.default_extension = '.ods'
            self.pop_up_text_filetypes = [("Arquivos ODS", "*.ods"),]
        elif type_file == EnumDocFiles.PDF:
            self.default_extension = '.pdf'
            self.pop_up_text_filetypes = [("Arquivos PDF", "*.pdf")]
        else:
            self.default_extension = '.*'
            self.pop_up_text_filetypes = [("Salvar Como", "*.*")]

    def open_filename(self, file_ext_type: EnumDocFiles = EnumDocFiles.ALL) -> str | None:
        """
            Caixa de diálogo para selecionar um arquivo
        """
        self._config_pop_up_open_filename(file_ext_type)
        print(f'{__class__.__name__}  | {file_ext_type}')
        filename: str = filedialog.askopenfilename(
            title=self.title_pop_up_files,
            initialdir=self.prefs["initial_input_dir"].absolute(),
            filetypes=self.pop_up_text_filetypes,
        )
        if not filename:
            return None
        _dir_name = os.path.dirname(filename)
        self.prefs['initial_input_dir'] = Directory(_dir_name)
        return filename

    def open_files_name(self, file_ext_type: EnumDocFiles = EnumDocFiles.ALL) -> tuple:
        """
            Selecionar um ou mais arquivos
        """
        self._config_pop_up_open_filename(file_ext_type)
        files = filedialog.askopenfilenames(
            title=self.title_pop_up_files,
            initialdir=self.prefs['initial_input_dir'].absolute(),
            filetypes=self.pop_up_text_filetypes,
        )
        if (files == "") or (len(files) < 0):
            return tuple()
        _dir_name = os.path.abspath(os.path.dirname(files[0]))
        self.prefs['initial_input_dir'] = Directory(_dir_name)
        return files

    def open_file_sheet(self) -> str | None:
        """
            Caixa de diálogo para selecionar um arquivo CSV/TXT/XLSX/ODS
        """
        return self.open_filename(EnumDocFiles.SHEET)

    def open_files_sheet(self) -> tuple[str]:
        """
            Selecionar uma ou mais planilhas
        """
        return self.open_files_name(EnumDocFiles.SHEET)

    def open_files_image(self) -> tuple[str]:
        return self.open_files_name(EnumDocFiles.IMAGE)

    def open_files_pdf(self) -> tuple[str]:
        return self.open_files_name(EnumDocFiles.PDF)

    def open_folder(self, action_input=True) -> str | None:
        """Selecionar uma pasta"""
        if action_input:
            _initial: str = self.prefs['initial_input_dir'].absolute()
        else:
            _initial: str = self.prefs['initial_output_dir'].absolute()

        _select_dir: str = filedialog.askdirectory(
            initialdir=_initial,
            title="Selecione uma pasta",
        )
        if _select_dir is None:
            return None

        _parent_dir = os.path.abspath(_select_dir)
        if action_input:
            self.prefs['initial_input_dir'] = Directory(_parent_dir)
        else:
            self.prefs['initial_output_dir'] = Directory(_parent_dir)
        return _select_dir

    def save_file(self, type_file: EnumDocFiles = EnumDocFiles.ALL_DOCUMENTS) -> File | None:
        """Abre uma caixa de diálogo para salvar arquivos."""
        self._config_pop_up_save_filename(type_file)
        # Abre a caixa de diálogo "Salvar Como"
        dir_path = filedialog.asksaveasfilename(
            defaultextension=self.default_extension,
            filetypes=self.pop_up_text_filetypes,  # Tipos de arquivos suportados
            title=self.title_pop_up_files,
            initialdir=self.prefs['initial_output_dir'].absolute(),
        )

        if not dir_path:
            return None
        self.prefs['initial_output_dir'] = Directory(dir_path)
        return File(dir_path)


class ModelFileDialog(BaseDict):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        self._file_dialog = AppFileDialog()

    def get_prefs(self) -> PreferencesFileDialog:
        return self._file_dialog.prefs

    def select_file_disk(self, f_type: EnumDocFiles) -> File | None:
        _f: str = self._file_dialog.open_filename(f_type)
        if _f is None:
            return None
        return File(_f)

    def select_files_disk(self, f_type: EnumDocFiles) -> ArrayList[File]:
        _files = self._file_dialog.open_files_name(f_type)
        arr = ArrayList()
        for _file in _files:
            if (_file is not None) and (_file != ""):
                if os.path.isfile(_file):
                    arr.append(File(_file))
        return arr

    def select_folder(self) -> Directory | None:
        _folder = self._file_dialog.open_folder()
        return None if _folder is None else Directory(_folder)


class ModelExportJson(object):

    def __init__(self, file_json: File) -> None:
        super().__init__()
        self.__file_json = file_json

    def get_file_json(self) -> File:
        return self.__file_json

    def set_file_json(self, f: File):
        self.__file_json = f

    def read_file_json(self) -> BaseDict | None:
        try:
            _data = JsonConvert.from_file(self.get_file_json())
        except Exception as err:
            print(f'{__class__.__name__} Erro: {err}')
            return None
        else:
            return BaseDict(_data.to_json_data().to_dict())

    def save_data(self, data: dict) -> None:
        """
        Salva um arquivo JSON no disco
        """
        try:
            conv = JsonConvert.from_dict(data)
            conv.to_json_data().to_file(self.get_file_json())
        except json.decoder.JSONDecodeError:
            print(f'{__class__.__name__} Falha: ao tentar converter JSON {self}')
        except Exception as err:
            print(f'{__class__.__name__} Falha: {err}')


__all__ = [
    'KeyUserConfig', 'KeyFileDialog', 'TypeConfFileDialog', 'PreferencesFileDialog',
    'ExtensionSheet', 'CsvSep', 'TypeImportSheet', 'PreferencesImportSheet', 'TypeConfApp',
    'UserPreferences', 'ModelPreferences', 'ModelFileDialog', 'ModelExportJson'
]
