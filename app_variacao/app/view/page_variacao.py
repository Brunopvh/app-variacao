from __future__ import annotations
from tkinter import ttk
import tkinter as tk
from app_variacao.app.ui import (
    BasePage, BaseWindow, ContainerH, EnumStyles, show_alert, show_info
)
from app_variacao.app.controllers import (
    ControllerViewVariacao
)
from app_variacao.app.view.views_widgets import DataSheetView, DataImportConfigView
from app_variacao.documents.sheet import (
    ReadSheetCsv, ReadSheetODS, ReadSheetExcel
)
import pandas as pd


class PageVariacao(BasePage):

    def __init__(self, master: BaseWindow, **kwargs):
        super().__init__(master, **kwargs)
        self.GEOMETRY = '600x350'
        self.set_page_route('/variacao')
        self.set_page_name('Váriação de leitura')
        self.controller = ControllerViewVariacao()

        #=============================================================#
        # Container 1 - Topo da janela
        # =============================================================#
        self.container1 = ContainerH(self.frame_master)
        self.add_frame(self.container1)

        # Botão para processar/ler
        self.btn_read = ttk.Button(self.container1, text="Carregar Dados", command=self.load_data_to_view)
        self.add_btn(self.btn_read)
        #self.btn_sheet_variacao = ttk.Button(
        #    self.container1, text='Selecionar Planilha',
        #    command=self.load_data_to_view, style=EnumStyles.BUTTON_PURPLE_LIGHT.value,)
        #self.add_btn(self.btn_sheet_variacao)

        # =============================================================#
        # Container 2 - Configurar a importação dos dados.
        # =============================================================#
        self.config_import: DataImportConfigView = DataImportConfigView(self.container1)
        #self.btn_sheet_variacao.configure(command=self.config_import.on_select_file)

        # =============================================================#
        # Container 3 - Exibição dos dados
        # =============================================================#
        self.container_sheet_view = ContainerH(self.frame_master)
        self.data_view: DataSheetView = DataSheetView(self.container_sheet_view)
        self.add_frame(self.data_view)
        if self.controller.sheet_variacao is not None:
            self.on_file_loaded()

    def select_sheet(self):
        pass

    def back_page(self):
        self.func_go_page('/back')

    def init_ui_page(self):
        self.container1.pack(padx=2, pady=2, fill='x')
        self.btn_read.pack(pady=10, side=tk.LEFT)
        #self.btn_sheet_variacao.pack(padx=2, pady=2, side=tk.LEFT)

        self.config_import.pack(fill='x', padx=3, pady=2)
        # O DataSheetView deve ocupar o espaço restante
        self.container_sheet_view.pack(expand=True, fill='both', padx=2, pady=2)
        self.data_view.pack(expand=True, fill='both', padx=2, pady=2)

    def load_data_to_view(self):
        config = self.config_import.get_import_config()
        if not config:
            return

        try:
            if (config['extension'] == '.csv') or (config['extension'] == '.txt'):
                df = pd.read_csv(
                    config['path'].absolute(), sep=config['sep'], encoding=config['encoding']
                )
            else:
                df = pd.read_excel(
                    config['path'].absolute(), sheet_name=config['sheet_name']
                )
            self.data_view.load_dataframe(df)
        except Exception as e:
            show_alert(f"Erro ao ler arquivo: {e}")

    def on_file_loaded(self):
        # Exemplo de como carregar os dados após selecionar o arquivo
        if self.controller.sheet_variacao is None:
            return
        if not self.controller.sheet_variacao.exists():
            return

        df: pd.DataFrame = pd.DataFrame()
        if self.controller.sheet_variacao.is_csv():
            rd = ReadSheetCsv.create_load_pandas(
                self.controller.sheet_variacao.absolute(),
                encoding='utf-8',
            )
            df = rd.get_workbook_data().get_first().to_data_frame()
        elif self.controller.sheet_variacao.is_excel():
            rd = ReadSheetExcel.create_load_pandas(self.controller.sheet_variacao.absolute())
            df = rd.get_workbook_data().get_first().to_data_frame()
        elif self.controller.sheet_variacao.is_ods():
            rd = ReadSheetODS.create_load_pandas(self.controller.sheet_variacao.absolute())
            df = rd.get_workbook_data().get_first().to_data_frame()
        else:
            return
        self.data_view.load_dataframe(df)

