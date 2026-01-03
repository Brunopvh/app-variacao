from __future__ import annotations
from enum import StrEnum
import json
from typing import Any
from app_variacao.types.array import ArrayList, BaseDict
from app_variacao.util import (
    File, Directory, EnumDocFiles, UserAppDir
)
from app_variacao.soup_files import JsonConvert
from tkinter import filedialog
import os.path

_app_dir = UserAppDir('app-variacao')


class UserPreferences(BaseDict):

    _instance_prefs = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_prefs is None:
            cls._instance_prefs = super(UserPreferences, cls).__new__(cls)
        return cls._instance_prefs

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        if hasattr(self, '_initialized_prefs') and self._initialized_prefs:
            return
        self._initialized_prefs = True

    def __repr__(self):
        return f"{self.__class__.__name__}()\n{self.values()}"

    def get_initial_output_dir(self) -> Directory:
        return self['initial_output_dir']

    def set_initial_output_dir(self, new: Directory) -> None:
        if not isinstance(new, Directory):
            raise TypeError('initial_output_dir must be a Directory')
        self['initial_output_dir'] = new

    def get_initial_input_dir(self) -> Directory:
        return self['initial_input_dir']

    def set_initial_input_dir(self, new: Directory) -> None:
        if not isinstance(new, Directory):
            raise TypeError('initial_input_dir must be a Directory')
        self['initial_input_dir'] = new

    def to_dict(self) -> dict[str, Any]:
        data = {}
        for k, v in self.items():
            if hasattr(v, 'absolute'):
                data[k] = v.absolute()
            else:
                data[k] = v
        return data


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
        self.__prefs = None

    def get_preferences(self) -> UserPreferences:
        if self.__prefs is None:
            self.__prefs = self.create_prefs()
        return self.__prefs

    def save_prefs(self):
        try:
            _data = JsonConvert.from_dict(self.get_preferences().to_dict())
            _data.to_json_data().to_file(self.file_prefs)
        except Exception as e:
            print(f'DEBUG: {__class__.__name__} {e}')

    def load_prefs(self) -> dict[str, Any]:
        try:
            return JsonConvert.from_file(self.file_prefs).to_json_data().to_dict()
        except Exception as e:
            print(f'{__class__.__name__} load_prefs error: {e}')
            return dict()

    def create_prefs(self) -> UserPreferences:
        _default_prefs = self.load_prefs()
        if len(_default_prefs) == 0:
            _default_prefs['initial_input_dir'] = _app_dir.userFileSystem.get_user_downloads()
            _default_prefs['initial_output_dir'] = _app_dir.userFileSystem.get_user_downloads()
            _default_prefs['work_dir'] = _app_dir.workspaceDirApp
            _default_prefs['last_dir'] = _app_dir.userFileSystem.get_user_downloads()
        else:
            dir_keys = ['initial_input_dir', 'initial_output_dir', 'last_dir', 'work_dir']
            for k, v in _default_prefs.items():
                if k in dir_keys:
                    dir_obj = Directory(v)
                    if k == 'initial_input_dir':
                        _default_prefs[k] = dir_obj
                    elif k == 'initial_output_dir':
                        _default_prefs[k] = dir_obj
                    else:
                        _default_prefs[k] = dir_obj
                else:
                    _default_prefs[k] = v
        return UserPreferences(_default_prefs)


class AppFileDialog(object):
    """Caixa de diálogo para seleção de vários tipos de arquivos."""

    _instance_file_dialog = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_file_dialog is None:
            cls._instance_file_dialog = super(AppFileDialog, cls).__new__(cls)
        return cls._instance_file_dialog

    def __init__(self) -> None:
        self.prefs: UserPreferences = ModelPreferences().get_preferences()
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


class ModelFileDialog(BaseDict):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        self._file_dialog = AppFileDialog()

    def get_prefs(self) -> UserPreferences:
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

