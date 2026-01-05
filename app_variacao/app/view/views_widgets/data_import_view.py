from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import pandas as pd
from app_variacao.app.ui import Container, ContainerV, ContainerH, show_alert
from app_variacao.app.controllers import ControllerViewVariacao
from app_variacao.app.models import ConfigImportCsv, PrefImportCsv
from app_variacao.util import File


class DataImportConfigView(Container):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller_view = ControllerViewVariacao()

        # Estrutura interna fixa
        self.main_container = ContainerV(self)
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Seção de Seleção de Arquivo ---
        self.container_file = ContainerH(self.main_container)
        self.container_file.pack(fill='x', pady=5)

        self.btn_select_sheet = ttk.Button(
            self.container_file, text='Selecionar Planilha', command=self.on_select_file
        )
        self.btn_select_sheet.pack(side=tk.LEFT, padx=1, pady=1)

        self.lbl_file_path = ttk.Label(self.container_file, text="Nenhum arquivo selecionado", wraplength=400)
        self.lbl_file_path.pack(side=tk.LEFT, padx=5)

        # --- Containers de Opções (Criados uma única vez) ---
        self.options_container = ContainerV(self.main_container)
        self.options_container.pack(fill='x', pady=5)

        self.container_csv = ContainerV(self.options_container)
        self.container_excel = ContainerV(self.options_container)

        # Variáveis
        self.var_sep = tk.StringVar(value=";")
        self.var_encoding = tk.StringVar(value="utf-8")
        self.var_sheet_name = tk.StringVar()

        # Inicializa as UIs internas (elas começam "escondidas")
        self._setup_csv_ui()
        self._setup_excel_ui()

    def _setup_csv_ui(self):
        ttk.Label(self.container_csv, text="Configurações de CSV", font=('', 10, 'bold')).pack(anchor='w')

        # Linha Separador
        row_sep = ContainerH(self.container_csv)
        row_sep.pack(fill='x', pady=2)
        ttk.Label(row_sep, text="Separador: ").pack(side='left')
        ttk.Combobox(row_sep, textvariable=self.var_sep, values=[";", ",", "\\t", "|", "-"]).pack(side='left', padx=5)

        # Linha Encoding
        row_enc = ContainerH(self.container_csv)
        row_enc.pack(fill='x', pady=2)
        ttk.Label(row_enc, text="Encoding: ").pack(side='left')
        ttk.Combobox(row_enc, textvariable=self.var_encoding, values=["utf-8", "latin1", "cp1252"]
                     ).pack(side='left', padx=5)

    def _setup_excel_ui(self):
        ttk.Label(
            self.container_excel, text="Selecione a Aba (Sheet):", font=('', 10, 'bold')
        ).pack(anchor='w')

        row_sheet = ContainerH(self.container_excel)
        row_sheet.pack(fill='x', pady=5)
        ttk.Label(row_sheet, text="Planilha: ").pack(side='left')

        self.comb_sheet_names = ttk.Combobox(
            row_sheet, textvariable=self.var_sheet_name, state="readonly"
        )
        self.comb_sheet_names.pack(side='left', fill='x', expand=True, padx=5)

    def on_select_file(self):
        self.controller_view.select_sheet_variacao()
        self.update_options_ui()

    def update_options_ui(self):
        path: File = self.controller_view.get_path_sheet_variacao()
        if not path or not path.exists():
            return

        self.lbl_file_path.config(text=path.basename())
        # Oculta ambos antes de decidir qual mostrar
        self.container_csv.pack_forget()
        self.container_excel.pack_forget()

        if path.is_csv():
            self.container_csv.pack(fill='x', pady=5)
        elif path.is_excel() or path.is_ods():
            # ATUALIZA OS VALORES DO COMBOBOX ANTES DE MOSTRAR
            sheets = self.controller_view.get_sheet_names()
            self.comb_sheet_names['values'] = sheets
            if sheets:
                self.var_sheet_name.set(sheets[0])
            self.container_excel.pack(fill='x', pady=5)

    def get_import_config(self) -> dict | None:
        path = self.controller_view.get_path_sheet_variacao()
        if not path: return None

        config = {"path": path, "extension": path.extension().lower()}

        if path.is_csv():
            config.update({
                "sep": self.var_sep.get().replace("\\t", "\t"),
                "encoding": self.var_encoding.get()
            })
        else:
            config.update({"sheet_name": self.var_sheet_name.get()})
        return config

