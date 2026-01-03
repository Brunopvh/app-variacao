from __future__ import annotations
from tkinter import ttk
import tkinter as tk
from app_variacao.soup_files import File
from app_variacao.app.ui.core import (
    BasePage, BaseWindow, ContainerH, EnumStyles
)
from app_variacao.app.controllers import (
    ControllerViewVariacao
)


class PageVariacao(BasePage):

    def __init__(self, master: BaseWindow, **kwargs):
        super().__init__(master, **kwargs)
        self.GEOMETRY = '600x350'
        self.set_page_route('/variacao')
        self.set_page_name('Váriação de leitura')
        self.container1 = ContainerH(self.frame_master)
        self.add_frame(self.container1)
        self._controller = ControllerViewVariacao()

        self.btn_sheet_variacao = ttk.Button(
            self.container1,
            text='Selecionar\nPlanilha',
            command=self.select_sheet,
            style=EnumStyles.BUTTON_PURPLE_LIGHT.value,
            #width=25
        )
        self.add_btn(self.btn_sheet_variacao)

        self.lb_sheet_variacao = ttk.Label(
            self.container1,
            text='Nenhuma planilha selecionada!'
        )
        self.add_label(self.lb_sheet_variacao)

        self.container2 = ContainerH(self.frame_master)

        self.btn_back_page = ttk.Button(
            self.container2,
            command=self.back_page,
            text='Voltar',
        )
        self.add_btn(self.btn_back_page)

    def select_sheet(self):
        print(self._controller._controller_prefs.get_prefs())
        self._controller.select_sheet_variacao()
        if self._controller.sheet_variacao is not None:
            self.lb_sheet_variacao.config(
                text=f'Planilha selecionada: {self._controller.sheet_variacao.basename()}'
            )

    def back_page(self):
        self.func_go_page('/back')

    def init_ui_page(self):
        self.container1.pack(padx=2, pady=1, expand=True, fill='x')
        self.btn_sheet_variacao.pack(padx=2, pady=2, side=tk.LEFT)
        self.lb_sheet_variacao.pack(padx=2, pady=2, expand=True, fill='x')

        self.container2.pack(padx=2, pady=1)
        self.btn_back_page.pack(padx=2, pady=1)
        self.pack(expand=True, fill='both', padx=2, pady=1)
