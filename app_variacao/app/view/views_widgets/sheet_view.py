from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import pandas as pd
from app_variacao.app.ui import Container, ContainerV, ContainerH
from app_variacao.app.ui.core_types import EnumStyles
from app_variacao.documents.sheet.excel import ReadSheetExcel, ExcelLoad


class DataSheetView(Container):
    """
    Componente genérico para exibição de DataFrames com scroll horizontal e vertical.
    Hereda de Container (ttk.Frame).
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Layout principal usando grid para as barras de rolagem
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 1. Criação do Treeview
        # 'show="headings"' esconde a primeira coluna vazia padrão do Tkinter
        self.tree = ttk.Treeview(self, show="headings", selectmode="browse")

        # 2. Configuração dos Scrollbars
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Posicionamento via Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

    def load_dataframe(self, df: pd.DataFrame):
        """
        Limpa os dados atuais e carrega um novo DataFrame no componente.
        """
        # Limpar dados existentes
        self.tree.delete(*self.tree.get_children())

        # Configurar colunas
        columns = list(df.columns)
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            # Ajuste automático de largura inicial (opcional)
            self.tree.column(col, width=100, minwidth=50, stretch=True)

        # Inserir linhas
        for _, row in df.iterrows():
            # Converte todos os valores para string para exibição segura
            values = [str(v) for v in row.values]
            self.tree.insert("", "end", values=values)

    def clear(self):
        """Remove todos os itens da visualização"""
        for item in self.tree.get_children():
            self.tree.delete(item)
