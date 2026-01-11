from __future__ import annotations
import tkinter as tk
from typing import Callable
from tkinter import (ttk, Tk, messagebox)
from app_variacao.app.ui.core_types import (
    AbstractObserver, ObserverWidget, ConfigMappingStyles, NotifyWidget,
    MessageNotification, EnumStyles, EnumMessages, AppStyles
)
from app_variacao.app.controllers.controller_main_app import ControllerMainApp


def show_alert(text: str):
    messagebox.showwarning('Alerta', text)


def show_info(text: str):
    messagebox.showinfo('Info', text)


def update_theme_tk_window(new: EnumStyles, wind: tk.Tk):
    # Padrão Dark
    bg_color = "gray15"

    if new == EnumStyles.WINDOW_LIGHT:
        bg_color = "white"
    elif new == EnumStyles.WINDOW_LIGHT_PURPLE:
        bg_color = "#B388EB"  # Roxo claro (tom pastel)
    elif new == EnumStyles.WINDOW_DARK:
        pass
    else:
        return
    wind.configure(bg=bg_color)


#=================================================================#
# Base para Janelas
#=================================================================#
class BaseWindow(Tk):

    def __init__(
                self, screenName=None, baseName=None,
                className="Tk", useTk=True, sync=False, use=None
            ):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.fun_alert: Callable[[str], None] = show_alert
        self.fun_info: Callable[[str], None] = show_info
        self.geometry('500x320')
        self._app_style: AppStyles = AppStyles(self)
        # Observador genérico para a janela
        self._window_observer = ObserverWidget()
        self._window_observer.set_listener(self.receiver_notify)
        self._window_theme: EnumStyles = EnumStyles.WINDOW_DARK
        self.update_window_theme(self._window_theme)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def get_observer(self) -> ObserverWidget:
        return self._window_observer

    def receiver_notify(self, message: MessageNotification):
        if message.get_message_type().value == EnumMessages.STYLE_UPDATE.value:
            _mapping: ConfigMappingStyles = message.get_provider()
            if _mapping['last_update'] == "app":
                self.update_window_theme(_mapping['app'])

    def initUI(self) -> None:
        pass

    def get_window_styles(self) -> AppStyles:
        return self._app_style

    def get_window_theme(self) -> EnumStyles:
        return self._window_theme

    def update_window_theme(self, theme: EnumStyles) -> None:
        # Padrão Dark
        bg_color = "gray15"

        if theme == EnumStyles.WINDOW_LIGHT:
            bg_color = "white"
        elif theme == EnumStyles.WINDOW_LIGHT_PURPLE:
            bg_color = "#B388EB"  # Roxo claro (tom pastel)
        elif theme == EnumStyles.WINDOW_DARK:
            pass
        else:
            return
        self._window_theme = theme
        self.configure(bg=bg_color)

    def show_alert(self, text: str):
        self.fun_alert(text)

    def show_info(self, text: str):
        self.fun_info(text)

    def _exit_threads(self) -> None:
        pass

    def exit_app(self):
        """
        Sai do programa
        """
        self._exit_threads()
        print("Encerrando GUI.")
        self.quit()


class BasePage(ttk.Frame):

    def __init__(
                self, master: BaseWindow, *,
                go_page: Callable[[str], None] = (),
                border=None,
                borderwidth=None,
                class_="", cursor="",
                height=0, name=None, padding=None,
                relief=None, style="", takefocus="",
                width=0, **kwargs,
            ):
        super().__init__(
                    master, border=border, borderwidth=borderwidth,
                    class_=class_, cursor=cursor, height=height,
                    name=name, padding=padding, relief=relief,
                    style=style, takefocus=takefocus,
                    width=width
            )
        self.myapp_window: BaseWindow = master
        self.func_go_page: Callable[[str], None] = go_page
        self._page_style: EnumStyles = EnumStyles.FRAME_DARK_GRAY
        self.GEOMETRY: str = '400x300'
        self._page_name: str = None
        self._page_route: str = None

        # Receber notificações externas
        self._observer: ObserverWidget = ObserverWidget()
        # se inscrever no próprio observador para receber as notificações externas.
        self._observer.set_listener(self._receiver_notify)
        # Enviar notificações para outros objetos, os objetos externos que precisam
        # ser notificados devem se inscrever no objeto notificador NotifyWidget()
        self._page_change_notify: NotifyWidget = NotifyWidget()

        self._frame_master: ttk.Frame = ttk.Frame(self)
        self._frame_master.pack(expand=True, fill='both', padx=2, pady=1)


    def __repr__(self):
        return f'{__class__.__name__}() {self.get_page_name()}'

    def get_frame_master(self) -> ttk.Frame:
        return self._frame_master

    def get_page_style(self) -> EnumStyles:
        return self._page_style

    def set_page_style(self, style: EnumStyles):
        self._page_style = style
        self._frame_master.configure(style=style.value)

    def init_ui_page(self, **kwargs):
        self._frame_master.configure(
            style=self._page_style.value,
        )

    def get_notify_provider(self) -> NotifyWidget:
        return self._page_change_notify

    def get_observer(self) -> ObserverWidget:
        return self._observer

    def _receiver_notify(self, msg: MessageNotification):
        """
            Receber notificações externas de outros objetos.
        """
        if msg.get_message_type().value == EnumMessages.STYLE_UPDATE.value:
            conf_styles: ConfigMappingStyles = msg.get_provider()
            self.set_page_style(conf_styles['frames'])
        else:
            print(f'DEBUG: {__class__.__name__} Nenhuma configurada para essa notificação: {msg.keys()}')
        self.get_notify_provider().send_notify(msg)

    def set_geometry(self, geometry: str):
        self.myapp_window.geometry(geometry)

    def get_page_name(self) -> str | None:
        return self._page_name

    def set_page_name(self, name: str):
        self._page_name = name

    def get_page_route(self) -> str | None:
        return self._page_route

    def set_page_route(self, route: str):
        self._page_route = route

    def set_size_screen(self):
        self.myapp_window.geometry(self.GEOMETRY)
        self.myapp_window.title(f'{self.get_page_name().upper()}')


class Navigator(object):

    _instance_navigator = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_navigator is None:
            cls._instance_navigator = super(Navigator, cls).__new__(cls)
        return cls._instance_navigator

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        self._app_pages: dict[str, BasePage] = dict()
        self.current_page: BasePage = None  # Página atualmente exibida
        self.history_pages: list[str] = list()  # Pilha para armazenar o histórico de navegação

    def get_pages_route(self) -> list[str]:
        return list(self._app_pages.keys())

    def add_page(self, page: BasePage):
        if page.get_page_route() is None:
            raise ValueError(f'Defina uma rota para página: {page}')
        if page.get_page_route() in self.get_pages_route():
            return
        self._app_pages[page.get_page_route()] = page

    def get_pages(self) -> dict[str, BasePage]:
        return self._app_pages

    def push(self, page_route: str):
        """
        Exibe a página especificada.

        :param page_route: Rota da página a ser exibida.
        """
        if page_route == '/back':
            self.pop()
            return
        if not (page_route in self.get_pages_route()):
            messagebox.showwarning(
                "Aviso", f'Página não encontrada: {page_route}'
            )
            return

        # Esconde a página atual, se houver
        if self.current_page is not None:
            self.history_pages.append(self.current_page.get_page_route())  # Salvar no histórico
            self.current_page.pack_forget()

        # Mostra a nova página
        self.current_page = self._app_pages[page_route]
        self.current_page.set_size_screen()
        self.current_page.init_ui_page()
        self.current_page.pack(expand=True, fill='both', padx=3, pady=3)

    def pop(self):
        """
        Retorna à página anterior no histórico de navegação.
        """
        if len(self.history_pages) == 0:
            messagebox.showwarning(
                "Aviso", "Não há páginas anteriores no histórico para retornar."
            )
            return

        # Esconde a página atual
        if self.current_page is not None:
            self.current_page.pack_forget()

        # Recupera a página anterior do histórico
        previous_page_route: str = self.history_pages.pop()
        self.current_page = self._app_pages[previous_page_route]
        self.current_page.init_ui_page()
        self.current_page.set_size_screen()
        self.current_page.pack(expand=True, fill='both', padx=2, pady=2)


class MyApp(object):
    """
        Controlador de páginas
    """
    _instance_controller = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_controller is None:
            cls._instance_controller = super(MyApp, cls).__new__(cls)
        return cls._instance_controller

    def __init__(self, controller: ControllerMainApp):
        super().__init__()
        # Garante que __init__ não será executado mais de uma vez
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self._controller: ControllerMainApp = controller
        self._navigator: Navigator = Navigator()
        self._base_window: BaseWindow = BaseWindow()
        self._app_observer: ObserverWidget = ObserverWidget()
        self._app_observer.set_listener(self.receiver_notify)
        self._app_change_notify: NotifyWidget = NotifyWidget()

    def get_notify_provider(self) -> NotifyWidget:
        return self._app_change_notify

    def receiver_notify(self, message: MessageNotification):
        pass

    def add_listener(self, listener: AbstractObserver):
        self._app_change_notify.add_observer(listener)

    def send_notify_listeners(self, message: MessageNotification):
        print(f'{__class__.__name__} Repassando notificação: {message.keys()}')
        self._app_change_notify.send_notify(message)

    def get_styles_app(self) -> AppStyles:
        return self._base_window.get_window_styles()

    def get_styles_mapping(self) -> ConfigMappingStyles:
        return self._controller.get_conf_styles()

    def get_navigator(self) -> Navigator:
        return self._navigator

    def get_pages(self) -> dict[str, BasePage]:
        return self._navigator.get_pages()

    def get_window(self) -> BaseWindow:
        return self._base_window

    def add_page(self, page: BasePage):
        """
        Adiciona uma página ao navegador de páginas
        """
        self.add_listener(page.get_observer())
        self._navigator.add_page(page)

    def go_home_page(self):
        for _key in self._navigator.get_pages().keys():
            if _key == '/home':
                self._navigator.push('/home')
                break

    def save_configs(self) -> None:
        print(f'Salvando configurações em: {self._controller.get_file_config().absolute()}')
        self._controller.save_configs()

    def exit_app(self):
        self.save_configs()
        self._base_window.exit_app()


def run_app(myapp: MyApp) -> None:
    myapp.get_navigator().push('/home')
    myapp.get_window().mainloop()


__all__ = [
    'AppStyles', 'ObserverWidget', 'NotifyWidget', 'BaseWindow', 'BasePage',
    'Navigator', 'MyApp', 'run_app', 'show_info', 'show_alert',
]
