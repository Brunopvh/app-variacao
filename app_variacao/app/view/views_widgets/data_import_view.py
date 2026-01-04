from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import pandas as pd
from app_variacao.app.ui import Container, ContainerV, ContainerH
from app_variacao.app.controllers import ControllerViewVariacao


class DataImportConfigView(Container):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller_view = ControllerViewVariacao()

        # Estrutura interna
        self.main_container = ContainerV(self)
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Seção de Seleção de Arquivo ---
        self.container_file = ContainerH(self.main_container)
        self.container_file.pack(fill='x', pady=5)
        self.btn_select_sheet = ttk.Button(
            self.container_file, text='Selecionar Planilha', command=self.on_select_file
        )
        self.btn_select_sheet.pack(fill='x', pady=1, padx=1, side=tk.LEFT)
        self.lbl_file_path = ttk.Label(self.container_file, text="Nenhum arquivo selecionado", wraplength=400)
        self.lbl_file_path.pack(side='left', padx=2, pady=1)
        if self.controller_view.get_path_sheet_variacao() is not None:
            if self.controller_view.get_path_sheet_variacao().exists():
                self.lbl_file_path.config(
                    text=self.controller_view.get_path_sheet_variacao().basename()
                )

        # --- Container Dinâmico para Opções ---
        self.options_container = ContainerV(self.main_container)
        self.options_container.pack(fill='both', expand=True, pady=10)
        # Variáveis de Configuração
        self.var_sep = tk.StringVar(value=";")
        self.var_encoding = tk.StringVar(value="utf-8")
        self.var_sheet_name = tk.StringVar()

    def on_select_file(self):
        # Chama o seu controller existente
        self.controller_view.select_sheet_variacao()
        if self.controller_view.get_path_sheet_variacao() is not None:
            if self.controller_view.get_path_sheet_variacao().exists():
                self.lbl_file_path.config(text=self.controller_view.get_path_sheet_variacao().basename())
                self._update_options_ui()

    def _update_options_ui(self):
        """Limpa as opções anteriores e desenha as novas baseadas na extensão"""
        for widget in self.options_container.winfo_children():
            widget.destroy()

        if self.controller_view.get_path_sheet_variacao().is_csv():
            self._build_csv_options()
        elif (self.controller_view.get_path_sheet_variacao().is_excel() or
              self.controller_view.get_path_sheet_variacao().is_ods()):
            self._build_excel_options()

    def _build_csv_options(self):
        ttk.Label(
            self.options_container, text="Configurações de CSV", font=('', 10, 'bold')
        ).pack(anchor='w')

        # Separador
        row_sep = ContainerH(self.options_container)
        row_sep.pack(fill='x', pady=2)
        ttk.Label(row_sep, text="Separador:").pack(side='left', padx=5)
        comb_sep = ttk.Combobox(row_sep, textvariable=self.var_sep, values=[";", ",", "\\t", "|", "-"])
        comb_sep.pack(side='left')
        # Encoding
        row_enc = ContainerH(self.options_container)
        row_enc.pack(fill='x', pady=2)
        ttk.Label(row_enc, text="Encoding:").pack(side='left', padx=5)
        comb_enc = ttk.Combobox(
            row_enc, textvariable=self.var_encoding, values=["utf-8", "latin1", "iso-8859-1", "cp1252"]
        )
        comb_enc.pack(side='left')

    def _build_excel_options(self):
        ttk.Label(
            self.options_container, text="Selecione a Aba (Sheet):", font=('', 10, 'bold')
        ).pack(anchor='w', side=tk.LEFT, pady=1, padx=2)

        try:
            # Obtém apenas os nomes das abas sem ler o conteúdo (rápido)
            xl = pd.ExcelFile(self.controller_view.get_path_sheet_variacao().absolute())
            sheets = xl.sheet_names

            # Criar um container horizontal para o label e o combobox
            container_row_sheet = ContainerH(self.options_container)
            container_row_sheet.pack(fill='x', pady=2, side=tk.LEFT)
            ttk.Label(container_row_sheet, text="Planilha:").pack(side='left', padx=5)

            # Combobox para as abas
            comb_sheets = ttk.Combobox(
                container_row_sheet,
                textvariable=self.var_sheet_name,
                values=sheets,
                state="readonly"  # Impede o usuário de digitar algo que não existe
            )
            comb_sheets.pack(side='left', fill='x', expand=True, padx=3, pady=1)
            if sheets:
                self.var_sheet_name.set(sheets[0])
        except Exception as e:
            ttk.Label(self.options_container, text=f"Erro ao ler abas: {e}", foreground='red').pack()

    def get_import_config(self) -> dict:
        """Retorna o dicionário final para o processamento"""
        if self.controller_view.get_path_sheet_variacao() is None:
            return {}

        data = {
            "path": self.controller_view.get_path_sheet_variacao(),
            "extension": self.controller_view.get_path_sheet_variacao().extension().lower()
        }

        if (data["extension"] == ".csv") or (data["extension"] == ".txt"):
            data.update({
                "sep": self.var_sep.get().replace("\\t", "\t"),
                "encoding": self.var_encoding.get()
            })
        else:
            data.update({
                "sheet_name": self.var_sheet_name.get()
            })
        return data

