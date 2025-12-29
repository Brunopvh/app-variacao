from __future__ import annotations
from app_variacao.ui.core.base_types import CoreDict
from app_variacao.util import File, Directory, LibraryDocs, InputFiles
from tkinter import filedialog
import os.path


class AppFileDialog(object):
    """Caixa de diálogo para seleção de vários tipos de arquivos."""

    _instance_file_dialog = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_file_dialog is None:
            cls._instance_file_dialog = super(AppFileDialog, cls).__new__(cls)
        return cls._instance_file_dialog

    def __init__(self) -> None:
        self.prefs_app: dict = dict()
        self.prefs_app['initial_inputdir'] = Directory('.')

    def open_filename(self, input_type: LibraryDocs = LibraryDocs.ALL) -> str | None:
        """
            Caixa de dialogo para selecionar um arquivo
        """

        _filesTypes = [("Todos os arquivos", "*"), ]
        _title = 'Selecione um arquivo'
        if input_type == LibraryDocs.SHEET:
            _filesTypes = [("Planilhas", "*.xlsx"), ("Arquivos CSV", "*.csv *.txt *xlsx")]
            _title = 'Selecione uma planilha'
        if input_type == LibraryDocs.CSV:
            _filesTypes = [("Planilhas", "*.csv"), ("Arquivos CSV", "*.csv *.txt")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.EXCEL:
            _filesTypes = [("Arquivos Excel", "*.xlsx")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.IMAGE:
            _filesTypes = [("Arquivos de Imagem", "*.png *.jpg *.jpeg *.svg")]
            _title = 'Selecione Imagens'
        elif input_type == LibraryDocs.PDF:
            _filesTypes = [("Arquivos PDF", "*.pdf *.PDF"), ]
            _title = 'Selecione arquivos PDF'
        #
        filename: str = filedialog.askopenfilename(
            title=_title,
            initialdir=self.prefs_app['initial_inputdir'].absolute(),
            filetypes=_filesTypes,
        )

        if not filename:
            return None
        _dirname: str = os.path.dirname(filename)
        self.prefs_app['initial_inputdir'] = Directory(_dirname)
        return filename

    def open_filesname(self, input_type: LibraryDocs = LibraryDocs.ALL) -> tuple[str]:
        """
            Selecionar um ou mais arquivos
        """

        _filesTypes = [("Todos os arquivos", "*"), ]
        _title = 'Selecione um arquivo'
        if input_type == LibraryDocs.SHEET:
            _filesTypes = [("Planilas Excel CSV", "*.xlsx *.csv"), ("Arquivos CSV", "*.csv *.txt")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.EXCEL:
            _filesTypes = [("Arquivos Excel", "*.xlsx")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.IMAGE:
            _filesTypes = [("Arquivos de Imagem", "*.png *.jpg *.jpeg *.svg")]
            _title = 'Selecione Imagens'
        elif input_type == LibraryDocs.PDF:
            _filesTypes = [("Arquivos PDF", "*.pdf *.PDF"), ]
            _title = 'Selecione arquivos PDF'
        #
        files = filedialog.askopenfilenames(
            title=_title,
            initialdir=self.prefs_app['initial_inputdir'].absolute(),
            filetypes=_filesTypes,
        )

        if len(files) > 0:
            _dirname: str = os.path.abspath(os.path.dirname(files[0]))
            self.prefs_app['initial_inputdir'] = Directory(_dirname)
        return files

    def open_file_sheet(self) -> str | None:
        """
            Caixa de dialogo para selecionar um arquivo CSV/TXT/XLSX
        """
        return self.open_filename(LibraryDocs.SHEET)

    def open_files_sheet(self) -> tuple[str]:
        """
            Selecionar uma ou mais planilhas
        """
        return self.open_filesname(LibraryDocs.SHEET)

    def open_files_image(self) -> tuple[str]:
        return self.open_filesname(LibraryDocs.IMAGE)

    def open_files_pdf(self) -> tuple[str]:
        return self.open_filesname(LibraryDocs.PDF)

    def open_folder(self, action_input=True) -> str | None:
        """Selecionar uma pasta"""
        if action_input == True:
            _initial: str = self.prefs_app['initial_inputdir'].absolute()
        else:
            _initial: str = self.prefs_app['initial_outputdir'].absolute()

        _select_dir: str = filedialog.askdirectory(
            initialdir=_initial,
            title="Selecione uma pasta",
        )

        if _select_dir is None:
            return None
        _dirname = os.path.abspath(_select_dir)
        if action_input == True:
            self.prefs_app['initial_inputdir'] = Directory(_dirname)
        else:
            self.prefs_app['initial_outputdir'] = Directory(_dirname)
        return _select_dir

    def save_file(self, type_file: LibraryDocs = LibraryDocs.ALL_DOCUMENTS) -> str | None:
        """Abre uma caixa de dialogo para salvar arquivos."""
        if type_file == LibraryDocs.SHEET:
            _default = '.xlsx'
            _default_types = [("Arquivos Excel", "*.xlsx"), ("Arquivos CSV", "*.csv")]
        elif type_file == LibraryDocs.EXCEL:
            _default = '.xlsx'
            _default_types = [("Arquivos Excel", "*.xlsx")]
        elif type_file == LibraryDocs.CSV:
            _default = '.csv'
            _default_types = [("Arquivos CSV", "*.csv"), ("Arquivos de texto", "*.txt")]
        elif type_file == LibraryDocs.PDF:
            _default = '.pdf'
            _default_types = [("Arquivos PDF", "*.pdf")]
        else:
            _default = '.*'
            _default_types = [("Salvar Como", "*.*")]

        # Abre a caixa de diálogo "Salvar Como"
        dir_path = filedialog.asksaveasfilename(
            defaultextension=_default,  # Extensão padrão
            filetypes=_default_types,  # Tipos de arquivos suportados
            title="Salvar arquivo como",
            initialdir=self.prefs_app['initial_outputdir'].absolute(),
        )

        if not dir_path:
            return None
        self.prefs_app['initial_outputdir'] = Directory(dir_path)
        return dir_path


class ModelVariacao(CoreDict):

    def __init__(self, values: dict = None) -> None:
        super().__init__(values)
        self.file_dialog = AppFileDialog()

    def select_file_disk(self, f_type: LibraryDocs) -> str | None:
        return self.file_dialog.open_filename(f_type)

    def select_files_disk(self, f_type) -> tuple:
        pass

