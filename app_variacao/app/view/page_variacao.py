from __future__ import annotations
from tkinter import ttk
import tkinter as tk
from app_variacao.app.ui import (
    BasePage, BaseWindow, Container, EnumStyles, show_alert, show_info,
    ProgressBar
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

        self.container_body = Container(self._frame_master)
        self.container_import_and_load = Container(self.container_body)
        self.get_notify_provider().add_observer(self.container_import_and_load.get_observer())

        # =============================================================#
        # Container 2 - Carregamento de dados
        # =============================================================#
        self.container_body_load = Container(
            self.container_import_and_load, style=EnumStyles.FRAME_DARK.value,
        )
        # Botão para processar/ler
        self.btn_read = self.container_body_load.add_button(
            text="Carregar Dados",
            command=self.load_data_to_view,
            style=EnumStyles.BUTTON_GREEN.value,
        )
        # Combo para o tipo de planilha
        self.var_view_sheet = tk.StringVar(value='variação')
        self.combo_view = self.container_body_load.add_combo_box(
            textvariable=self.var_view_sheet,
            values=['variação', 'colaboradores'],
            width=8,
        )

        # =============================================================#
        # Container 3 - Importação de dados
        # =============================================================#
        self.container_body_import: DataImportConfigView = DataImportConfigView(self.container_import_and_load)
        self.get_notify_provider().add_observer(self.container_body_import.get_observer())

        # =============================================================#
        # Container 4 - Exibição dos dados
        # =============================================================#
        self.container_body_tables = Container(self.container_body)

        # Variação de leitura
        self.container_variacao = Container(self.container_body_tables)
        self._lbl_title = self.container_variacao.add_label(text='Planilha Variação')
        self.data_view: DataSheetView = DataSheetView(self.container_variacao)
        self.get_notify_provider().add_observer(self.data_view.get_observer())

        # Colaboradores
        self.container_colaboradores = Container(self.container_body_tables)
        self._lbl_title_colaboradores = self.container_colaboradores.add_label(text='Colaboradores')
        self.data_view_colaboradores: DataSheetView = DataSheetView(self.container_colaboradores)
        self.get_notify_provider().add_observer(self.data_view_colaboradores.get_observer())

    def back_page(self):
        self.func_go_page('/back')

    def init_ui_page(self, **kwargs):
        self._frame_master.pack(fill='both', expand=True)
        self.container_pbar.pack(fill='x', padx=2, pady=1)
        self.pbar.init_pbar(kwargs={'style': EnumStyles.PBAR_PURPLE.value})
        self.container_body.pack(padx=2, pady=1, fill='both', expand=True)

        self.container_import_and_load.pack(padx=2, pady=2, fill='x',)
        self.container_body_load.pack(padx=2, pady=1, fill='x', side='left')
        self.btn_read.pack(padx=1, pady=1, fill='x',)
        self.combo_view.pack(padx=1, pady=1, fill='x',)

        self.container_body_import.pack(fill='x', padx=2, pady=1)

        self.container_body_tables.pack(pady=1, padx=2, fill='both', expand=True)
        # DataSheetView - Variação
        self.container_variacao.pack(expand=True, fill='both', padx=2, pady=1)
        self._lbl_title.pack(fill='x', padx=2, pady=1)
        self.data_view.pack(expand=True, fill='both', padx=2, pady=1)
        # DataSheetView - Colaboradores
        self.container_colaboradores.pack(expand=True, fill='both', padx=2, pady=1)
        self._lbl_title_colaboradores.pack(fill='x', padx=2, pady=1)
        self.data_view_colaboradores.pack(expand=True, fill='both', padx=2, pady=1)

    def load_data_to_view(self):
        _th = threading.Thread(target=self._execute_load_data)
        _th.start()

    def _execute_load_data(self):
        config: ConfigSheetExcel | ConfigSheetCsv = self.container_body_import.get_import_config()
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
        self.pbar.set_prefix_text('Aguarde')

        self.pbar.update_output_text()
        if self.var_view_sheet.get() == 'variação':
            self.data_view.load_dataframe(self.controller.loaded_data)
        elif self.var_view_sheet.get() == 'colaboradores':
            self.data_view_colaboradores.load_dataframe(self.controller.loaded_data)
        self.pbar.set_prefix_text('OK')
        self.pbar.stop()

