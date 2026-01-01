from __future__ import annotations
from typing import Any
from app_variacao.types.array import ArrayList
from app_variacao.ui.core.core_types import CoreDict
from app_variacao.util import (
    File, Directory, EnumDocFiles, ContentFiles, UserFileSystem
)
from app_variacao.soup_files import JsonConvert, JsonData
from tkinter import filedialog
import os.path


class PreferencesFileDialog(CoreDict):

    default_keys = [
        'initial_input_dir',
        'initial_output_dir',
    ]

    def __init__(self, values: dict = None, *, user_fs: UserFileSystem = UserFileSystem()) -> None:
        super().__init__(values)
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


class ModelVariacao(CoreDict):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)


class ModelPopUpFiles(CoreDict):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        self._file_dialog = AppFileDialog()

    def select_file_disk(self, f_type: EnumDocFiles) -> File | None:
        print(f'{__class__.__name__} chamando ... {f_type}')
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
