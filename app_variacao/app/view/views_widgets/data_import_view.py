from __future__ import annotations
import tkinter as tk
from app_variacao.app.ui import Container
from app_variacao.app.ui.core_widgets import Row
from app_variacao.app.controllers import ControllerViewVariacao
from app_variacao.app.app_types import ConfigSheetCsv, ConfigSheetExcel
from app_variacao.documents.sheet import CsvSeparator, CsvEncoding
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

        # Container Principal.
        self.main_container = Container(self)
        self.main_container.pack(fill='both', expand=True, padx=1, pady=1)
        self.get_notify_provider().add_observer(self.main_container.get_observer())

        # Seleção de Arquivo
        self.container_select_file = Container(self.main_container)
        self.container_select_file.pack(fill='x', padx=2, pady=1)
        self.get_notify_provider().add_observer(self.container_select_file.get_observer())
        self.btn_select_sheet = self.container_select_file.add_button(
            text='Selecionar Planilha',
            command=self.on_select_file,
            padding=(13, 5),
            width=16
        )
        self.btn_select_sheet.pack(fill='x', padx=2, pady=1, side='left')
        self.lbl_file_path = self.container_select_file.add_label(
            text="Nenhum arquivo selecionado", wraplength=400
        )
        self.lbl_file_path.pack(fill='x', padx=2, pady=1)

        #==========================================================#
        # Containers de Opções
        #==========================================================#
        self.options_container: Container = Container(self.main_container)
        self.options_container.pack(fill='x', expand=True, padx=2, pady=1)
        self.get_notify_provider().add_observer(self.options_container.get_observer())

        # Opções CSV/Excel
        self.row_options_csv = Row(Container(self.options_container))
        self.row_excel = Row(Container(self.options_container))
        self.get_notify_provider().add_observer(self.row_options_csv.get_observer())
        self.get_notify_provider().add_observer(self.row_excel.get_observer())

        # Variáveis
        _default_sep = list(self.csv_mapping_separator.keys())[0]
        _default_enc = list(self.csv_mapping_encoding.keys())[0]
        self.var_sep = tk.StringVar(value=_default_sep)
        self.var_encoding = tk.StringVar(value=_default_enc)
        self.var_sheet_name = tk.StringVar()

        # Importação de CSV
        self._lb_conf_csv = self.row_options_csv.add_label(
            text="Configurações de CSV: ", font=('', 10, 'bold')
        )
        self._lb_csv_sep = self.row_options_csv.add_label(text="Separador: ")
        self._combo_sep = self.row_options_csv.get_container_master().add_combo_box(
            textvariable=self.var_sep, width=8,
            values=list(self.csv_mapping_separator.keys()),
            state='readonly'
        )
        # Widgets Encoding
        self._combo_csv_encoding = self.row_options_csv.get_container_master().add_combo_box(
            textvariable=self.var_encoding, width=8, state='readonly',
            values=list(self.csv_mapping_encoding.keys())
        )
        self._lb_encoding = self.row_options_csv.add_label(text="Encoding: ")

        # ==========================================================#
        # Opções Excel
        # ==========================================================#
        self._lb_excel_sheet_name = self.row_excel.add_label(
            text="Selecione a Aba (Sheet): ", font=('', 10, 'bold')
        )
        self._comb_sheet_names = self.row_excel.get_container_master().add_combo_box(
            textvariable=self.var_sheet_name, state="readonly"
        )

    def _setup_csv_ui(self):
        self.row_options_csv.get_container_master().pack(side='left', padx=1, pady=1, fill='x')
        self._lb_conf_csv.pack(side='left', padx=1, pady=1, fill='x')
        self._lb_csv_sep.pack(side='left', padx=1, pady=1, fill='x')
        self._combo_sep.pack(side='left', padx=1, pady=1, fill='x')
        self._lb_encoding.pack(side='left', padx=1, pady=1, fill='x')
        self._combo_csv_encoding.pack(side='left', padx=1, pady=1, fill='x')

    def _setup_excel_ui(self):
        self.row_excel.get_container_master().pack(side='left', padx=1, pady=1, fill='x')
        self._lb_excel_sheet_name.pack(side='left', padx=1, pady=1, fill='x')
        self._comb_sheet_names.pack(side='left', padx=1, pady=1, fill='x')

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
        self.row_options_csv.pack_forget()
        self.row_excel.pack_forget()

        if path.is_csv():
            self._setup_csv_ui()
        elif path.is_excel() or path.is_ods():
            # ATUALIZA OS VALORES DO COMBOBOX ANTES DE MOSTRAR
            sheets = self.controller_view.get_sheet_names()
            self._comb_sheet_names['values'] = sheets
            if sheets:
                self.var_sheet_name.set(sheets[0])
            self._setup_excel_ui()

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


