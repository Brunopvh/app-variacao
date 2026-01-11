from app_variacao.app.ui import BasePage, BaseWindow, EnumStyles, Container
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
        self._main_frame = Container(self._frame_master)
        self.get_notify_provider().add_observer(self._main_frame.get_observer())

        self.lb1 = self._main_frame.add_label(
            text="Página Inicial",
            style=EnumStyles.LABEL_DEFAULT.value,
        )

        self.btn_variacao = self._main_frame.add_button(
            text='Variação de Leitura',
            command=lambda: self.func_go_page('/variacao'),
            width=45,
            style=EnumStyles.BUTTON_PURPLE_LIGHT.value
        )

    def init_ui_page(self, **kwargs):
        self.pack(expand=True, fill='both', padx=2, pady=1)
        self._frame_master.pack(fill='both', padx=2, pady=1, expand=True)
        self._main_frame.pack(fill='both', padx=2, pady=1, expand=True)
        self.lb1.pack(padx=2, pady=2)
        self.btn_variacao.pack(padx=2, pady=1)

