from app_variacao.ui.core import (
    BasePage, MyApp, ContainerH, EnumThemes
)
from .page_variacao import PageVariacao
from tkinter import ttk


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
