import threading
import os.path
from app_variacao.ui.core import (
    BasePage, BaseWindow, MyApp, Container, ContainerH, ContainerV,
    ProgressBarTkIndeterminate, ProgressBarTkDeterminate,
    ProgressBar, EnumThemes, MappingStyles, MessageNotification
)
from app_variacao.ui.controllers import ControllerVariacao
from app_variacao.util import LibraryDocs, File
from tkinter import ttk
import tkinter as tk
from threading import Thread


class HomePage(BasePage):

    def __init__(self, master: MyApp, **kwargs):
        super().__init__(master, **kwargs)
        self.GEOMETRY = '500x250'
        self.set_page_name('Página Principal')

        self.lb1 = ttk.Label(
            self.frame_master,
            text="Página Inicial",
            style=EnumThemes.LABEL_DEFAULT,
        )

        self.btn_variacao = ttk.Button(
            self.frame_master,
            text='Variação de Leitura',
            command=lambda: self.goto('/variacao'),
            style=self.myapp_window.get_styles_mapping().get_style_buttons(),
            width=45
        )

    def goto(self, route: str):
        self.myapp_window.get_navigator().push(route)

    def init_ui_page(self):
        self.lb1.pack(padx=2, pady=2)
        self.btn_variacao.pack(padx=2, pady=2)
        self.pack(expand=True, fill='both', padx=2, pady=1)


class PageVariacao(BasePage):

    def __init__(self, master: MyApp, **kwargs):
        super().__init__(master, **kwargs)
        self.GEOMETRY = '550x200'
        self.set_page_route('/variacao')
        self.set_page_name('Váriação de leitura')
        self.container1 = ContainerH(self.frame_master)
        self._controller = ControllerVariacao()

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
        self.selected_sheet: str = self._controller.get_file_disk(LibraryDocs.CSV)
        if self.selected_sheet is not None:
            self.lb_sheet_variacao.config(
                text=f'Planilha selecionada: {os.path.basename(self.selected_sheet)}'
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


class MainApp(MyApp):

    def __init__(self):
        super().__init__()

        self.main_page = HomePage(self)
        self.main_page.set_page_name('HOME')
        self.main_page.set_page_route('/home')
        self.add_page(self.main_page)
        self.add_page(PageVariacao(self))


