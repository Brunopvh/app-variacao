from __future__ import annotations
from enum import StrEnum
import json
from typing import Any
from app_variacao.types.array import ArrayList, BaseDict
from app_variacao.util import (
    File, Directory, EnumDocFiles, ContentFiles, UserFileSystem, UserAppDir
)
from app_variacao.soup_files import JsonConvert, JsonData
from tkinter import filedialog
import os.path

_app_dir = UserAppDir('app-variacao')


class EnumPrefs(StrEnum):

    PREFS_FILE_DIALOG = 'prefs.filedialog'
    PREFS_USER = 'prefs.user'
    ALL = 'ALL'


class PreferencesFileDialog(BaseDict):

    default_keys = [
        'initial_input_dir',
        'initial_output_dir',
    ]
    _instance_prefs = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(PreferencesFileDialog, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self, values: dict = None, *, user_fs: UserFileSystem = UserFileSystem()) -> None:
        super().__init__(values)
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        self._user_fs: UserFileSystem = user_fs
        if not 'initial_input_dir' in self.keys():
            self['initial_input_dir'] = self._user_fs.get_user_downloads()
        if not 'initial_output_dir' in self.keys():
            self['initial_output_dir'] = self._user_fs.get_user_downloads()
        if not 'last_dir' in self.keys():
            self['last_dir'] = self._user_fs.get_user_downloads()

    def get_initial_output_dir(self) -> Directory:
        return self['initial_output_dir']

    def set_initial_output_dir(self, new: Directory) -> None:
        self['initial_output_dir'] = new

    def get_initial_input_dir(self) -> Directory:
        return self['initial_input_dir']

    def set_initial_input_dir(self, new: Directory) -> None:
        self['initial_input_dir'] = new

    def update_values(self, values: dict[str, Any]) -> None:
        for _k in values.keys():
            if _k == "initial_input_dir":
                if isinstance(values[_k], Directory):
                    self.set_initial_input_dir(values[_k])
            elif _k == "initial_output_dir":
                if isinstance(values[_k], Directory):
                    self.set_initial_output_dir(values[_k])

    @classmethod
    def create_from_json(cls, file_json: File) -> PreferencesFileDialog:
        _data = JsonConvert.from_file(file_json)
        return cls(_data.to_json_data().to_dict())


class PreferencesUser(BaseDict):

    _instance_prefs = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(PreferencesUser, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True


class AppFileDialog(object):
    """Caixa de diálogo para seleção de vários tipos de arquivos."""

    _instance_file_dialog = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_file_dialog is None:
            cls._instance_file_dialog = super(AppFileDialog, cls).__new__(cls)
        return cls._instance_file_dialog

    def __init__(self, prefs: PreferencesFileDialog = None) -> None:
        self.prefs = prefs
        if self.prefs is None:
            self.prefs = PreferencesFileDialog()
        self.title_pop_up_files: str = 'Selecione um arquivo'
        self.pop_up_text_filetypes: list[tuple[str, str]] = [("Todos os arquivos", "*"), ]
        self.default_extension = '.*'

    def _config_pop_up_open_filename(self, file_ext_type: EnumDocFiles) -> None:
        """
            Caixa de dialogo para selecionar um arquivo
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
        print(
            f'{__class__.__name__} valores ... {file_ext_type} | {self.title_pop_up_files} | {self.title_pop_up_files} | {self.pop_up_text_filetypes}')
        filename: str = filedialog.askopenfilename(
            title=self.title_pop_up_files,
            initialdir=self.prefs.get_initial_input_dir().absolute(),
            filetypes=self.pop_up_text_filetypes,
        )
        if not filename:
            return None
        _dir_name = os.path.dirname(filename)
        self.prefs.set_initial_input_dir(Directory(_dir_name))
        return filename

    def open_files_name(self, file_ext_type: EnumDocFiles = EnumDocFiles.ALL) -> tuple:
        """
            Selecionar um ou mais arquivos
        """
        self._config_pop_up_open_filename(file_ext_type)
        files = filedialog.askopenfilenames(
            title=self.title_pop_up_files,
            initialdir=self.prefs.get_initial_input_dir().absolute(),
            filetypes=self.pop_up_text_filetypes,
        )
        if (files == "") or (len(files) < 0):
            return tuple()
        _dir_name = os.path.abspath(os.path.dirname(files[0]))
        self.prefs.set_initial_input_dir(Directory(_dir_name))
        return files

    def open_file_sheet(self) -> str | None:
        """
            Caixa de dialogo para selecionar um arquivo CSV/TXT/XLSX/ODS
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
            _initial: str = self.prefs.get_initial_input_dir().absolute()
        else:
            _initial: str = self.prefs.get_initial_output_dir().absolute()

        _select_dir: str = filedialog.askdirectory(
            initialdir=_initial,
            title="Selecione uma pasta",
        )
        if _select_dir is None:
            return None

        _parent_dir = os.path.abspath(_select_dir)
        if action_input:
            self.prefs.set_initial_input_dir(Directory(_parent_dir))
        else:
            self.prefs.set_initial_output_dir(Directory(_parent_dir))
        return _select_dir

    def save_file(self, type_file: EnumDocFiles = EnumDocFiles.ALL_DOCUMENTS) -> File | None:
        """Abre uma caixa de diálogo para salvar arquivos."""
        self._config_pop_up_save_filename(type_file)
        # Abre a caixa de diálogo "Salvar Como"
        dir_path = filedialog.asksaveasfilename(
            defaultextension=self.default_extension,
            filetypes=self.pop_up_text_filetypes,  # Tipos de arquivos suportados
            title=self.title_pop_up_files,
            initialdir=self.prefs.get_initial_output_dir().absolute(),
        )

        if not dir_path:
            return None
        self.prefs.set_initial_output_dir(Directory(dir_path))
        return File(dir_path)


class ModelVariacao(BaseDict):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        self.__file_config: File | None = None


class ModelPopUpFiles(BaseDict):

    def __init__(self, values: dict = None, *, prefs_file_dialog: dict[str, str] = None) -> None:
        super().__init__(values)
        if prefs_file_dialog is None:
            prefs_file_dialog = {}
        self._file_dialog = AppFileDialog(
            PreferencesFileDialog(prefs_file_dialog)
        )

    def get_prefs_file_dialog(self) -> PreferencesFileDialog:
        return self._file_dialog.prefs

    def select_file_disk(self, f_type: EnumDocFiles) -> File | None:
        _f = self._file_dialog.open_filename(f_type)
        return None if _f is None else File(_f)

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


class ModelExportJson(ModelVariacao):

    def __init__(self, values: dict = None, *, file_json: File) -> None:
        super().__init__(values)
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


class ModelAppConfig(ModelVariacao):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        self._dir_config = _app_dir.config_dir_app()
        self._dir_config.mkdir()
        self._export_json = ModelExportJson(
            file_json=self._dir_config.join_file('app-variacao.json')
        )

    def get_file_config(self) -> File:
        return self._export_json.get_file_json()

    def load_all_prefs(self) -> BaseDict:
        try:
            _data: BaseDict = self._export_json.read_file_json()
        except Exception as err:
            print(f'{__class__.__name__} Erro: {err}')
            return BaseDict()
        else:
            return _data

    def save_all_prefs(self, data: dict[str, dict]) -> None:
        try:
            _app_dir.config_dir_app().mkdir()
            all_prefs = self.load_all_prefs()
            if all_prefs is None:
                return None
        except Exception as err:
            print(f'{__class__.__name__} Erro: {err}')
        else:
            for _k in data.keys():
                if _k == EnumPrefs.PREFS_FILE_DIALOG.value:
                    all_prefs[_k] = data[_k]
                elif _k == EnumPrefs.PREFS_USER.value:
                    all_prefs[_k] = data[_k]
            self._export_json.save_data(all_prefs)

    def load_prefs_user(self) -> PreferencesUser:
        prefs = PreferencesUser()
        prefs['work_dir'] = _app_dir.workspaceDirApp.absolute()
        all_prefs = self.load_all_prefs()
        if EnumPrefs.PREFS_USER.value in all_prefs.keys():
            for _k in all_prefs[EnumPrefs.PREFS_USER.value].keys():
                prefs[_k] = all_prefs[EnumPrefs.PREFS_USER.value][_k]
        return prefs

    def save_prefs_user(self, prefs: dict):
        _new = dict()
        _new[EnumPrefs.PREFS_USER.value] = prefs
        self.save_all_prefs(_new)

    def load_prefs_file_dialog(self) -> PreferencesFileDialog:
        """
        Ler os dados do arquivo de configuração Json e obter as configurações
        para diálogo de arquivos.
        """
        _data: dict = self.load_all_prefs()
        _prefs = PreferencesFileDialog()
        if _data is None:
            return _prefs
        if not EnumPrefs.PREFS_FILE_DIALOG.value in _data.keys():
            return _prefs

        for _k in _data[EnumPrefs.PREFS_FILE_DIALOG.value].keys():
            if _k == EnumPrefs.PREFS_FILE_DIALOG.value:
                _prefs[_k] = _data[_k]
        return _prefs

    def save_prefs_file_dialog(self, prefs: dict) -> None:
        _new = dict()
        _new[EnumPrefs.PREFS_FILE_DIALOG.value] = prefs
        self.save_all_prefs(_new)
