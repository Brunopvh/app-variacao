from __future__ import annotations
from tkinter import ttk
import pandas as pd
from app_variacao.app.ui import Container


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
        #self.tree_view = ttk.Treeview(self, show="headings", selectmode="browse")
        self.tree_view = self.add_tree_view(show="headings", selectmode="browse")

        # 2. Configuração dos Scrollbars
        self.scrow_bar_v = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
        self.scrow_bar_h = ttk.Scrollbar(self, orient="horizontal", command=self.tree_view.xview)
        self.tree_view.configure(yscrollcommand=self.scrow_bar_v.set, xscrollcommand=self.scrow_bar_h.set)

        # Posicionamento via Grid
        self.tree_view.grid(row=0, column=0, sticky="nsew")
        self.scrow_bar_v.grid(row=0, column=1, sticky="ns")
        self.scrow_bar_h.grid(row=1, column=0, sticky="ew")

    def load_dataframe(self, df: pd.DataFrame):
        """
        Exibe os dados do DataFrame() em uma tabela ttk.Treeview() do tk
        """
        # Limpar dados existentes
        self.tree_view.configure(columns=(), displaycolumns=())
        self.tree_view.delete(*self.tree_view.get_children())

        # Configurar colunas
        df = df.astype("str")
        columns: list[str] = df.columns.tolist()
        self.tree_view["columns"] = columns
        self.tree_view["displaycolumns"] = columns

        for col in columns:
            self.tree_view.heading(col, text=col, anchor="w")
            # Ajuste automático de largura inicial (opcional)
            self.tree_view.column(col, width=130, minwidth=80, stretch=True, anchor="center")

        # Inserir linhas
        self.tree_view.configure(displaycolumns=())
        iter_rows_data = df.itertuples(index=False, name=None)
        for row in iter_rows_data:
            self.tree_view.insert("", "end", values=row)
        self.tree_view.configure(displaycolumns=columns)

    def clear(self):
        """Remove todos os itens da visualização"""
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
