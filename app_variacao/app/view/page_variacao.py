from __future__ import annotations
from tkinter import ttk
import tkinter as tk
from app_variacao.app.ui import (
    BasePage, BaseWindow, Container, EnumStyles, show_alert, show_info,
    ProgressBar, InterfaceProgressBar,
)
from app_variacao.app.controllers import ControllerViewVariacao
from app_variacao.app.app_types import ConfigSheetCsv, ConfigSheetExcel
from app_variacao.app.view.views_widgets import DataSheetView, DataImportConfigView
import threading
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
        self.container_pbar = Container(self._frame_master)
        self.get_notify_provider().add_observer(self.container_pbar.get_observer())
        self.pbar = ProgressBar.create_pbar_tk(self.container_pbar, mode="indeterminate")

        self.container_buttons = Container(self._frame_master)
        self.get_notify_provider().add_observer(self.container_buttons.get_observer())
        # Botão para processar/ler
        self.btn_read = self.container_buttons.add_button(
            text="Carregar Dados",
            command=self.load_data_to_view
        )

        # =============================================================#
        # Container 2 - Configurar a importação dos dados.
        # =============================================================#
        self.container_import: DataImportConfigView = DataImportConfigView(self.container_buttons)
        self.get_notify_provider().add_observer(self.container_import.get_observer())

        # =============================================================#
        # Container 3 - Exibição dos dados
        # =============================================================#
        self.container_sheet_view = Container(self._frame_master)
        self.data_view: DataSheetView = DataSheetView(self.container_sheet_view)
        self.get_notify_provider().add_observer(self.data_view.get_observer())

    def back_page(self):
        self.func_go_page('/back')

    def init_ui_page(self, **kwargs):
        self.container_pbar.pack(fill='x', padx=2, pady=1)
        self.pbar.init_pbar(
            kwargs={'style': EnumStyles.PBAR_GREEN}
        )
        self.container_buttons.pack(padx=2, pady=2, fill='x')
        self.btn_read.pack(pady=10, side=tk.LEFT)

        self.container_import.pack(fill='x', padx=3, pady=2)
        # O DataSheetView deve ocupar o espaço restante
        self.container_sheet_view.pack(expand=True, fill='both', padx=2, pady=2)
        self.data_view.pack(expand=True, fill='both', padx=4, pady=3)

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

