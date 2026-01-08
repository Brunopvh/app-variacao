from __future__ import annotations
from tkinter import ttk
import tkinter as tk
from app_variacao.app.ui import (
    BasePage, BaseWindow, ContainerH, EnumStyles, show_alert, show_info,
    ProgressBar, InterfaceProgressBar,
)
from app_variacao.app.controllers import ControllerViewVariacao
from app_variacao.app.app_types import ConfigSheetCsv, ConfigSheetExcel
from app_variacao.app.view.views_widgets import DataSheetView, DataImportConfigView
from app_variacao.documents import (
    ReadSheetCsv, ReadSheetODS, ReadSheetExcel, WorkbookData
)
import threading
import pandas as pd
from time import sleep


class PageVariacao(BasePage):

    def __init__(self, master: BaseWindow, **kwargs):
        super().__init__(master, **kwargs)
        self.GEOMETRY = '720x420'
        self.set_page_route('/variacao')
        self.set_page_name('Váriação de leitura')
        self.controller = ControllerViewVariacao()

        #=============================================================#
        # Container 1 - Topo da janela
        # =============================================================#
        self.container_pbar = ContainerH(self.frame_master)
        self.pbar = ProgressBar.create_pbar_tk(self.container_pbar, mode="indeterminate")

        self.container1 = ContainerH(self.frame_master)
        self.add_listener(self.container1.get_observer())

        # Botão para processar/ler
        self.btn_read = ttk.Button(
            self.container1,
            text="Carregar Dados",
            command=self.load_data_to_view
        )
        #self.add_btn(self.btn_read)

        # =============================================================#
        # Container 2 - Configurar a importação dos dados.
        # =============================================================#
        self.container_import: DataImportConfigView = DataImportConfigView(self.container1)
        self.add_listener(self.container_import.get_observer())

        # =============================================================#
        # Container 3 - Exibição dos dados
        # =============================================================#
        self.container_sheet_view = ContainerH(self.frame_master)
        self.data_view: DataSheetView = DataSheetView(self.container_sheet_view)

    def back_page(self):
        self.func_go_page('/back')

    def init_ui_page(self):
        self.pbar.init_pbar()
        self.container1.pack(padx=2, pady=2, fill='x')
        self.btn_read.pack(pady=10, side=tk.LEFT)

        self.container_import.pack(fill='x', padx=3, pady=2)
        # O DataSheetView deve ocupar o espaço restante
        self.container_sheet_view.pack(expand=True, fill='both', padx=2, pady=2)
        self.data_view.pack(expand=True, fill='both', padx=2, pady=2)

    def load_data_to_view(self):
        _th = threading.Thread(target=self._execute_load_data)
        _th.start()

    def _execute_load_data(self):
        config: ConfigSheetExcel | ConfigSheetCsv = self.container_import.get_import_config()
        if config is None:
            show_info('Selecione uma planilha para prosseguir!')
            return

        self.pbar.set_prefix_text(f'Lendo dados {config["path"].basename()}')
        self.pbar.set_end_value(1)
        self.pbar.start()
        self.controller.read_thread_data_frame(config)
        while True:
            sleep(1)
            if not self.controller.isLoading:
                break
        self.pbar.set_output_text('Carregando visualização')
        self.pbar.set_prefix_text('aguarde')

        self.pbar.update_output_text()
        self.data_view.load_dataframe(self.controller.loaded_data)
        self.pbar.stop()

    def old_load_data_to_view(self):
        """
        Ler o DataFrame da planilha selecionada e enviar ao DataSheetView()
        """
        config: ConfigSheetExcel | ConfigSheetCsv = self.container_import.get_import_config()
        if config is None:
            show_info('Selecione uma planilha para prosseguir!')
            return

        try:
            df: pd.DataFrame
            if (config['extension'] == '.csv') or (config['extension'] == '.txt'):
                rd = ReadSheetCsv.create_load_pandas(
                    config['path'].absolute(), delimiter=config['sep'], encoding=config['encoding']
                )
                df = rd.get_workbook_data().get_first().to_data_frame()
            elif config['extension'] == '.xlsx':
                rd = ReadSheetExcel.create_load_pandas(config['path'].absolute())
                df = rd.get_workbook_data(config['sheet_name']).get_first().to_data_frame()
            elif config['extension'] == '.ods':
                rd = ReadSheetODS.create_load_pandas(config['path'].absolute())
                df = rd.get_workbook_data().get_sheet(config['sheet_name']).to_data_frame()
            self.data_view.load_dataframe(df)
        except Exception as e:
            print('==================================================')
            print(e)
            show_alert(f"Erro ao ler arquivo: {e}")

