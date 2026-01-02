from __future__ import annotations
from tkinter import ttk
import tkinter as tk
from app_variacao.soup_files import File
from app_variacao.app.ui.core import (
    BasePage, MyApp, ContainerH,
)
from app_variacao.app.controllers import ControllerPopUpFiles


class PageVariacao(BasePage):

    def __init__(self, master: MyApp, **kwargs):
        super().__init__(master, **kwargs)
        self.GEOMETRY = '600x350'
        self.set_page_route('/variacao')
        self.set_page_name('Váriação de leitura')
        self.container1 = ContainerH(self.frame_master)
        self._controller = ControllerPopUpFiles()

        self.btn_sheet_variacao = ttk.Button(
            self.container1,
            text='Selecionar\nPlanilha',
            command=self.select_sheet,
            style=self.myapp_window.get_styles_mapping().get_style_buttons(),
            #width=25
        )
        self.lb_sheet_variacao = ttk.Label(
            self.container1,
            text='Nenhuma planilha selecionada!'
        )

        self.container2 = ContainerH(self.frame_master)
        self.btn_back_page = ttk.Button(
            self.container2,
            command=self.back_page,
            text='Voltar',
        )
        self.selected_sheet: str = None

    def select_sheet(self):
        self.selected_sheet: File = self._controller.get_file_excel()
        if self.selected_sheet is not None:
            self.lb_sheet_variacao.config(
                text=f'Planilha selecionada: {self.selected_sheet.basename()}'
            )

    def back_page(self):
        self.myapp_window.get_navigator().pop()

    def init_ui_page(self):
        self.container1.pack(padx=2, pady=1, expand=True, fill='x')
        self.btn_sheet_variacao.pack(padx=2, pady=2, side=tk.LEFT)
        self.lb_sheet_variacao.pack(padx=2, pady=2, expand=True, fill='x')

        self.container2.pack(padx=2, pady=1)
        self.btn_back_page.pack(padx=2, pady=1)
        self.pack(expand=True, fill='both', padx=2, pady=1)
