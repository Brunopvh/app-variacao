from __future__ import annotations
import tkinter as tk
from typing import Any, Callable, Literal, Union, TypeAlias
from tkinter import (ttk, Tk, messagebox)
from app_variacao.types import BaseDict
from app_variacao.app.ui.core_types import (
    AbstractObserver, AbstractNotifyProvider, TypeMappingStylesDict,
    MessageNotification, EnumStyles, EnumMessages, MappingStyles,
)


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
# Temas e Estilos
#=================================================================#

class AppStyles(object):

    def __init__(self, window: Tk):
        self.root_window = window
        self.root_style = ttk.Style(self.root_window)
        self.PADDING_BTN = (6, 8)
        self.WIDTH_BTN = 13

        # ==============================================================#
        # Estilo para os Frames
        # ==============================================================#
        # LightFrame
        self.styleLight = ttk.Style(self.root_window)
        self.styleLight.configure(
            "LightFrame.TFrame",
            background="white",
            relief="solid",
            borderwidth=1
        )
        # CinzaFrame.TFrame
        self.styleGray = ttk.Style(self.root_window)
        self.styleGray.configure(
            "CinzaFrame.TFrame",
            background="lightgray",
            relief="solid",
            borderwidth=1
        )
        # Black.TFrame
        self.styleFrameBlack = ttk.Style(self.root_window)
        self.styleFrameBlack.theme_use("default")
        self.styleFrameBlack.configure(
            "Black.TFrame",
            background="#2C2C2C"
        )  # Cor de fundo preto
        # Estilo LightPurple.TFrame - Fundo Roxo Claro
        self.styleFrameLightPurple = ttk.Style(self.root_window)
        self.styleFrameLightPurple.theme_use("default")
        self.styleFrameLightPurple.configure(
            "LightPurple.TFrame",  # Nome do estilo alterado
            background="#9370DB"  # Roxo claro (MediumPurple)
        )
        # Estilo DarkPurple.TFrame Fundo Roxo Escuro
        self.styleFrameDarkPurple = ttk.Style(self.root_window)
        self.styleFrameDarkPurple.theme_use("default")
        self.styleFrameDarkPurple.configure(
            "DarkPurple.TFrame",
            background="#4B0082"  # Roxo escuro
        )
        # Estilo para Frame
        self.styleFrameDarkGray = ttk.Style(self.root_window)
        self.styleFrameDarkGray.theme_use("default")
        self.styleFrameDarkGray.configure(
            "DarkGray.TFrame",  # Nome do estilo alterado
            background="#2F4F4F"  # Cinza escuro (DarkSlateGray)
        )
        # DarkOrange.TFrame
        self.styleFrameDarkOrange = ttk.Style(self.root_window)
        self.styleFrameDarkOrange.theme_use("default")
        self.styleFrameDarkOrange.configure(
            "DarkOrange.TFrame",  # Nome do estilo alterado
            background="#FF8C00"  # Laranja escuro (DarkOrange)
        )
        # ==============================================================#
        # Estilo para os botões
        # ==============================================================#
        # Roxo Claro
        self.styleButtonPurpleLight = ttk.Style(self.root_window)
        self.styleButtonPurpleLight.theme_use("default")
        self.styleButtonPurpleLight.layout(
            "Custom.TButtonPurpleLight",
            self.styleButtonPurpleLight.layout("TButton")
        )
        # Define o estilo do botão roxo claro
        self.styleButtonPurpleLight.configure(
            "Custom.TButtonPurpleLight",
            foreground="white",
            background="#B388EB",  # Roxo claro
            borderwidth=1,
            focusthickness=3,
            focuscolor='none',
            anchor='center',
            padding=self.PADDING_BTN,
            width=self.WIDTH_BTN,
        )
        self.styleButtonPurpleLight.map(
            "Custom.TButtonPurpleLight",
            background=[("active", "#a070d6"), ("pressed", "#8b5fc0")]
        )
        # Verde
        self.styleButtonGreen = ttk.Style(self.root_window)
        self.styleButtonGreen.theme_use("default")
        self.styleButtonGreen.layout(
            "Custom.TButtonGreen",
            self.styleButtonGreen.layout("TButton")
        )
        # Define o estilo do botão verde
        self.styleButtonGreen.configure(
            "Custom.TButtonGreen",
            foreground="white",
            background="#5cb85c",  # Verde
            borderwidth=1,
            focusthickness=3,
            focuscolor='none',
            anchor='center',
            padding=self.PADDING_BTN,
            width=self.WIDTH_BTN,
        )
        self.styleButtonGreen.map(
            "Custom.TButtonGreen",
            background=[("active", "#4cae4c"), ("pressed", "#449d44")]
        )

        # ==============================================================#
        # Estilo para os botões - Roxo Escuro
        # ==============================================================#
        self.styleButtonPurpleDark = ttk.Style(self.root_window)
        self.styleButtonPurpleDark.theme_use("default")
        self.styleButtonPurpleDark.layout(
            "Custom.TButtonPurpleDark",
            self.styleButtonPurpleDark.layout("TButton")
        )
        # Define o estilo do botão roxo escuro
        self.styleButtonPurpleDark.configure(
            "Custom.TButtonPurpleDark",
            foreground="white",
            background="#6247AA",  # Roxo escuro
            borderwidth=1,
            focusthickness=3,
            focuscolor='none',
            anchor='center',
            padding=self.PADDING_BTN,
            width=self.WIDTH_BTN,
        )
        # Mapeamento de cores para interação
        self.styleButtonPurpleDark.map(
            "Custom.TButtonPurpleDark",
            background=[
                ("active", "#503990"),  # Tom um pouco mais escuro quando passa o mouse
                ("pressed", "#402D73")  # Tom bem mais escuro quando clica
            ]
        )

        # ==============================================================#
        # Estilo para Labels
        # ==============================================================#
        self.styleLabelPurple = ttk.Style(self.root_window)
        self.styleLabelPurple.configure(
            "LargeFont.TLabel",  # Nome do estilo
            font=("Helvetica", 14),  # Fonte maior
            background="#9370DB",  # Cor de fundo roxo claro
            foreground="white"  # Cor do texto branco
        )
        # Default
        self.styleLabelDefault = ttk.Style(self.root_window)
        self.styleLabelDefault.configure(
            "BoldLargeFont.TLabel",  # Nome do estilo
            font=("Helvetica", 14, "bold")  # Fonte maior e negrito
        )

        # ==============================================================#
        # Estilo para Barra de progresso
        # ==============================================================#
        # Verde
        self.stylePbarGreen = ttk.Style(self.root_window)
        self.stylePbarGreen.theme_use('default')
        # Define o novo estilo
        self.stylePbarGreen.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#f0f0f0',  # cor de fundo da barra
            background='#4CAF50',  # cor da barra de progresso
            thickness=6,  # espessura da barra
            bordercolor='#cccccc',  # borda
            lightcolor='#4CAF50',  # brilho da barra
            darkcolor='#4CAF50',  # sombra da barra
        )
        # Barra de progresso Roxo claro
        self.stylePbarPurpleLight = ttk.Style(self.root_window)
        self.stylePbarPurpleLight.theme_use('default')
        self.stylePbarPurpleLight.configure(
            "Thin.Horizontal.TProgressbar",
            thickness=6,  # altura fina
            troughcolor="#eeeeee",  # fundo da barra
            background="#D19FE8"  # roxo claro
            )
        # Barra de progresso Roxo escuro
        self.stylePbarPurple = ttk.Style(self.root_window)
        self.stylePbarPurple.theme_use('default')
        self.stylePbarPurple.configure(
            "Purple.Horizontal.TProgressbar",
           thickness=6,  # altura fina
           troughcolor="#eeeeee",  # fundo da barra
           background="#4B0081"
           )


class ObserverWidget(AbstractObserver):
    """
    Sujeito observador que repassa as notificações recebidas para os filhos observadores
    """

    def __init__(self):
        super().__init__()
        self._listeners: set[Callable[[MessageNotification], None]] = set()

    def __repr__(self):
        return f'{self.__class__.__name__}() Sujeito Observador'

    def add_listener(self, obs: Callable[[MessageNotification], None]) -> None:
        self._listeners.add(obs)

    def receiver_notify(self, msg: MessageNotification):
        """
        Recebe notificações dos sujeitos notificadores e repassa para a página
        """
        for obs in self._listeners:
            obs(msg)


class NotifyWidget(AbstractNotifyProvider):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'{__class__.__name__}() Sujeito Notificador'

    def send_notify(self, message: MessageNotification):
        """
        Envia a notificação para todos os sujeitos observadores, sendo a
        mensagem (MessageNotification) um subtipo de dicionário.
        """
        for _observer in self.observer_list:
            _observer.receiver_notify(message)


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
        self._app_themes: MappingStyles = MappingStyles.create_default()
        # Observador genérico para a janela
        self._window_observer = ObserverWidget()
        # Adicionar ao observador o método receiver_notify para receber notificações
        self._window_observer.add_listener(self.receiver_notify)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def get_observer(self) -> ObserverWidget:
        return self._window_observer

    def receiver_notify(self, message: MessageNotification):
        if message.get_message_type().value == EnumMessages.MSG_UPDATE_STYLE.value:
            _mapping: MappingStyles = message.get_provider()
            if _mapping.get_last_update() == "app":
                self.update_window_theme(_mapping.get_style_app())

    def initUI(self) -> None:
        pass

    def get_window_styles(self) -> AppStyles:
        return self._app_style

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
        self.configure(bg=bg_color)

    def get_themes_mapping(self) -> MappingStyles:
        return self._app_themes

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
        self.GEOMETRY: str = '400x300'
        self._page_name: str = None
        self._page_route: str = None
        self._list_frames: list[ttk.Frame] = []
        self._list_buttons: list[ttk.Button] = []
        self._list_labels: list[ttk.Label] = []

        self._page_observer: ObserverWidget = ObserverWidget()
        self._page_observer.add_listener(self.receiver_notify)
        self._page_change_notify: NotifyWidget = NotifyWidget()

        self.frame_master: ttk.Frame = ttk.Frame(self)
        self.frame_master.pack(expand=True, fill='both', padx=2, pady=2)
        self._list_frames.append(self.frame_master)

    def __repr__(self):
        return f'{__class__.__name__}() {self.get_page_name()}'

    def add_btn(self, btn: ttk.Button):
        self._list_buttons.append(btn)

    def add_label(self, label: ttk.Label):
        self._list_labels.append(label)

    def add_frame(self, frame: ttk.Frame):
        self._list_frames.append(frame)

    def init_ui_page(self):
        self.frame_master.configure(
            style=self.myapp_window.get_themes_mapping().get_style_frames().value,
        )

    def get_observer(self) -> ObserverWidget:
        return self._page_observer

    def add_listener(self, listener: AbstractObserver):
        """
            Adicionar ouvintes desta página
        """
        self._page_change_notify.add_observer(listener)

    def notify_listeners(self, message: MessageNotification):
        """
            Nofiticar ouvintes dá página.
        """
        self._page_change_notify.send_notify(message)

    def receiver_notify(self, msg: MessageNotification):
        """
            Receber notificações externas de outros objetos.
        """
        if msg.get_message_type().value == EnumMessages.MSG_UPDATE_STYLE.value:
            self.update_page_state(msg)
        else:
            print(f'DEBUG: {__class__.__name__} Nenhuma configurada para essa notificação: {msg.keys()}')

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

    def update_page_theme(self, theme: EnumStyles):
        self.configure(style=theme.value)

    def _update_page_widgets(self, app_theme: MappingStyles):
        if app_theme.get_last_update() == "buttons":
            for btn in self._list_buttons:
                btn.configure(style=app_theme.get_style_buttons().value)
        elif app_theme.get_last_update() == "frames":
            for _frame in self._list_frames:
                _frame.configure(style=app_theme.get_style_frames().value)
        elif app_theme.get_last_update() == "labels":
            for lb in self._list_labels:
                lb.configure(style=app_theme.get_style_labels().value)
        elif app_theme.get_last_update() == "app":
            #self.update_page_theme(app_theme.get_style_app())
            pass
        else:
            print(f'DEBUG: {__class__.__name__} Nenhum tema foi alterado')

    def update_page_state(self, msg: MessageNotification):
        if EnumMessages.MSG_UPDATE_STYLE.value == msg.get_message_type().value:
            self._update_page_widgets(msg.get_provider())
        elif EnumMessages.MSG_PROCESS_FINISHED.value == msg.get_message_type().value:
            print(f'{__class__.__name__} Nenhuma ação configurada para essa notificação!')
        else:
            print(
                f'{__class__.__name__} Nenhuma ação configurada para essa notificação update_page_state\n{msg}\n'
            )


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
        print(f'Página adicionada: {page.get_page_route()}')

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

    def __init__(self):
        super().__init__()
        # Garante que __init__ não será executado mais de uma vez
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self._navigator: Navigator = Navigator()
        self._base_window: BaseWindow = BaseWindow()
        self._app_observer: ObserverWidget = ObserverWidget()
        self._app_observer.add_listener(self.receiver_notify)
        self._app_change_notify: NotifyWidget = NotifyWidget()

    def receiver_notify(self, message: MessageNotification):
        pass

    def add_listener(self, listener: AbstractObserver):
        self._app_change_notify.add_observer(listener)

    def send_notify_listeners(self, message: MessageNotification):
        self._app_change_notify.send_notify(message)

    def get_styles_app(self) -> AppStyles:
        return self._base_window.get_window_styles()

    def get_styles_mapping(self) -> MappingStyles:
        return self._base_window.get_themes_mapping()

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
        page.update_page_theme(self.get_styles_mapping().get_style_frames())
        self.add_listener(page.get_observer())
        self._navigator.add_page(page)

    def go_home_page(self):
        for _key in self._navigator.get_pages().keys():
            if _key == '/home':
                self._navigator.push('/home')
                break

    def save_configs(self) -> None:
        pass

    def exit_app(self):
        self.save_configs()
        self._base_window.exit_app()


def run_app(myapp: MyApp) -> None:
    myapp.get_navigator().push('/home')
    myapp.get_window().mainloop()


__all__ = [
    'AppStyles', 'MappingStyles', 'ObserverWidget',
    'NotifyWidget', 'BaseWindow', 'BasePage', 'Navigator', 'MyApp', 'run_app',
    'show_info', 'show_alert',
]
