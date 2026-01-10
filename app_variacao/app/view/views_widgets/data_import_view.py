from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from app_variacao.app.ui import Container, ContainerV, ContainerH, show_alert
from app_variacao.app.controllers import ControllerViewVariacao
from app_variacao.app.app_types import ConfigSheetCsv, ConfigSheetExcel
from app_variacao.documents.sheet import CsvSeparator, CsvEncoding, CsvMapping
from app_variacao.util import File
from typing import TypedDict


class CsvMappingSeparator(TypedDict, total=True):

    virgula: CsvSeparator
    ponto_virgula: CsvSeparator
    pipe: CsvSeparator
    tab: CsvSeparator
    esp: CsvSeparator
    under: CsvSeparator


class CsvMappingEncoding(TypedDict, total=True):

    utf_8: CsvEncoding
    latin: CsvEncoding
    iso: CsvEncoding
    cp1252: CsvEncoding


class DataImportConfigView(Container):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller_view = ControllerViewVariacao()
        if 'sheet_variacao' in  self.controller_view._controller_prefs.get_user_prefs().keys():
            self.controller_view._controller_prefs.get_user_prefs().pop('sheet_variacao')

        self.csv_mapping_separator: CsvMappingSeparator = {
            'tab': "\t",
            'esp': ' ',
            'pipe': '|',
            'ponto_virgula': ';',
            'virgula': ',',
            'under': '_',

        }
        self.csv_mapping_encoding: CsvMappingEncoding = {
            'utf_8': 'utf-8',
            'cp1252': 'cp1252',
            'iso': 'iso-8859-1',
            'latin': 'latin1',
        }

        # Estrutura interna fixa
        self.main_container = ContainerV(self)
        self.main_container.pack(fill='both', expand=True, padx=1, pady=1)
        self.add_listener(self.main_container.get_observer())

        # Seleção de Arquivo
        self.container_select_file = ContainerH(self.main_container)
        self.container_select_file.pack(fill='x', pady=1)

        self.btn_select_sheet = ttk.Button(
            self.container_select_file, text='Selecionar Planilha', command=self.on_select_file
        )
        self.btn_select_sheet.pack(side=tk.LEFT, padx=1, pady=1)

        # Containers de Opções
        self.options_container = ContainerV(self.container_select_file)
        self.options_container.pack(fill='x', pady=1, side=tk.LEFT)

        self.container_csv = ContainerV(self.main_container)
        self.container_excel = ContainerV(self.options_container)

        self.lbl_file_path = ttk.Label(self.container_select_file, text="Nenhum arquivo selecionado", wraplength=400)
        self.lbl_file_path.pack(side=tk.LEFT, padx=2)

        # Variáveis
        _default_sep = list(self.csv_mapping_separator.keys())[0]
        _default_enc = list(self.csv_mapping_encoding.keys())[0]
        self.var_sep = tk.StringVar(value=_default_sep)
        self.var_encoding = tk.StringVar(value=_default_enc)
        self.var_sheet_name = tk.StringVar()

        # Importação de CSV
        self._lb_conf_csv = ttk.Label(
            self.container_csv, text="Configurações de CSV: ", font=('', 10, 'bold')
        )
        self._container_separator = ContainerH(self.container_csv)
        self.add_listener(self._container_separator.get_observer())
        self._lb_csv_sep = ttk.Label(self._container_separator, text="Separador: ")
        self._combo_sep = ttk.Combobox(
            self._container_separator,
            textvariable=self.var_sep,
            values=list(self.csv_mapping_separator.keys()),
            state='readonly'
        )

        # Linha Encoding
        self.row_enc = ContainerH(self.container_csv)
        self._combo_csv_encoding = ttk.Combobox(
            self.row_enc,
            textvariable=self.var_encoding,
            values=list(self.csv_mapping_encoding.keys())
        )
        self._lb_encoding = ttk.Label(self.row_enc, text="Encoding: ")

        # Excel
        self._lb_sheet_name = ttk.Label(
            self.container_excel, text="Selecione a Aba (Sheet): ", font=('', 10, 'bold')
        )
        self.row_sheet = ContainerH(self.container_excel)
        self.comb_sheet_names = ttk.Combobox(
            self.row_sheet, textvariable=self.var_sheet_name, state="readonly"
        )
        self.add_listener(self.row_sheet.get_observer())

        # Inicializa as UIs internas
        self._setup_csv_ui()
        self._setup_excel_ui()

    def _setup_csv_ui(self):
        self._lb_conf_csv.pack(anchor='w', side=tk.LEFT, padx=1, pady=1)
        self._container_separator.pack(fill='x', pady=1, padx=1, side=tk.LEFT)
        self._lb_csv_sep.pack(side='left', pady=1, padx=1)
        self._combo_sep.pack(side='left', padx=2, pady=1)
        self.row_enc.pack(fill='x', pady=1, sid=tk.LEFT)
        self._lb_encoding.pack(side='left')
        self._combo_csv_encoding.pack(side='left', padx=2, pady=1)

    def _setup_excel_ui(self):
        self._lb_sheet_name.pack(anchor='w', side=tk.LEFT)
        self.row_sheet.pack(fill='x', pady=1)
        self.comb_sheet_names.pack(side='left', fill='x', expand=True, padx=2, pady=1)

    def on_select_file(self):
        self.controller_view.select_sheet_variacao()
        self.update_options_ui()

    def update_options_ui(self):
        path: File = self.controller_view.get_path_sheet_variacao()
        if path is None:
            return
        if not path.exists():
            return

        self.lbl_file_path.config(text=path.basename())
        # Oculta ambos antes de decidir qual mostrar
        self.container_csv.pack_forget()
        self.container_excel.pack_forget()

        if path.is_csv():
            self.container_csv.pack(fill='x', pady=1, padx=2)
        elif path.is_excel() or path.is_ods():
            # ATUALIZA OS VALORES DO COMBOBOX ANTES DE MOSTRAR
            sheets = self.controller_view.get_sheet_names()
            self.comb_sheet_names['values'] = sheets
            if sheets:
                self.var_sheet_name.set(sheets[0])
            self.container_excel.pack(fill='x', pady=1, padx=2)

    def get_import_config(self) -> ConfigSheetCsv | ConfigSheetExcel | None:
        path = self.controller_view.get_path_sheet_variacao()
        if path is None:
            return None
        if not path.exists():
            return None

        if path.is_csv():
            # self.var_sep.get().replace("\\t", "\t")
            self.controller_view.get_conf_sheet_csv()['sep'] = self.csv_mapping_separator[self.var_sep.get()]
            self.controller_view.get_conf_sheet_csv()['encoding'] = self.csv_mapping_encoding[self.var_encoding.get()]
            return self.controller_view.get_conf_sheet_csv()
        else:
            self.controller_view.get_conf_sheet_excel()['sheet_name'] = self.var_sheet_name.get()
            return self.controller_view.get_conf_sheet_excel()


