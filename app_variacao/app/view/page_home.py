from app_variacao.app.ui.core import (
    BasePage, BaseWindow, EnumStyles
)
from tkinter import ttk
from typing import Any, Callable


class HomePage(BasePage):

    def __init__(
                self, master: BaseWindow, *,
                go_page: Callable[[str], None] = (),
                border=None, borderwidth=None, class_="",
                cursor="", height=0, name=None, padding=None,
                relief=None, style="", takefocus="", width=0,
                **kwargs,
            ):
        super().__init__(
                master, go_page=go_page, border=border,
                borderwidth=borderwidth, class_=class_,
                cursor=cursor, height=height, name=name,
                padding=padding, relief=relief, style=style,
                takefocus=takefocus, width=width, **kwargs
            )

        self.GEOMETRY = '500x250'
        self.set_page_name('Página Principal')

        self.lb1 = ttk.Label(
            self.frame_master,
            text="Página Inicial",
            style=EnumStyles.LABEL_DEFAULT.value,
        )
        self.add_label(self.lb1)

        self.btn_variacao = ttk.Button(
            self.frame_master,
            text='Variação de Leitura',
            command=lambda: self.func_go_page('/variacao'),
            width=45,
            style=EnumStyles.BUTTON_PURPLE_LIGHT.value
        )
        self.add_btn(self.btn_variacao)

    def init_ui_page(self):
        self.lb1.pack(padx=2, pady=2)
        self.btn_variacao.pack(padx=2, pady=2)
        self.pack(expand=True, fill='both', padx=2, pady=1)
