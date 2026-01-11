#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Generic, TypeVar, TypeAlias, Union, Literal, TypedDict, Callable
from app_variacao.documents.types import BaseDict
from tkinter import Tk
from tkinter import ttk


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

        # ==============================================================#
        # Estilo para Treeview
        # ==============================================================#

        # ===================== Roxo ===================== #
        self.styleTreePurple = ttk.Style(self.root_window)
        self.styleTreePurple.theme_use("default")
        self.styleTreePurple.configure(
            "Purple.Treeview",
            background="#E6D9F2",
            fieldbackground="#E6D9F2",
            foreground="#2E003E",
            rowheight=24,
            borderwidth=0
        )
        self.styleTreePurple.map(
            "Purple.Treeview",
            background=[("selected", "#6247AA")],
            foreground=[("selected", "white")]
        )

        self.styleTreePurple.configure(
            "Purple.Treeview.Heading",
            background="#4B0082",
            foreground="white",
            relief="flat",
            font=("Helvetica", 10, "bold")
        )

        # ===================== Roxo Claro ===================== #
        self.styleTreePurpleLight = ttk.Style(self.root_window)
        self.styleTreePurpleLight.theme_use("default")
        self.styleTreePurpleLight.configure(
            "PurpleLight.Treeview",
            background="#F2ECFA",
            fieldbackground="#F2ECFA",
            foreground="#3A1F5C",
            rowheight=24
        )
        self.styleTreePurpleLight.map(
            "PurpleLight.Treeview",
            background=[("selected", "#B388EB")],
            foreground=[("selected", "white")]
        )

        self.styleTreePurpleLight.configure(
            "PurpleLight.Treeview.Heading",
            background="#9370DB",
            foreground="white",
            font=("Helvetica", 10, "bold")
        )

        # ===================== Dark ===================== #
        self.styleTreeDark = ttk.Style(self.root_window)
        self.styleTreeDark.theme_use("default")
        self.styleTreeDark.configure(
            "Dark.Treeview",
            background="#2C2C2C",
            fieldbackground="#2C2C2C",
            foreground="#EAEAEA",
            rowheight=18
        )
        self.styleTreeDark.map(
            "Dark.Treeview",
            background=[("selected", "#444444")],
            foreground=[("selected", "white")]
        )

        self.styleTreeDark.configure(
            "Dark.Treeview.Heading",
            background="#1F1F1F",
            foreground="white",
            font=("Helvetica", 10, "bold")
        )

        # ===================== Verde ===================== #
        self.styleTreeGreen = ttk.Style(self.root_window)
        self.styleTreeGreen.theme_use("default")
        self.styleTreeGreen.configure(
            "Green.Treeview",
            background="#E6F4EA",
            fieldbackground="#E6F4EA",
            foreground="#1E4620",
            rowheight=18
        )
        self.styleTreeGreen.map(
            "Green.Treeview",
            background=[("selected", "#5CB85C")],
            foreground=[("selected", "white")]
        )

        self.styleTreeGreen.configure(
            "Green.Treeview.Heading",
            background="#4CAF50",
            foreground="white",
            font=("Helvetica", 10, "bold")
        )


class EnumStyles(Enum):

    # Temas da janela principal
    WINDOW_DARK = 'DARK'
    WINDOW_LIGHT = 'LIGHT'
    WINDOW_LIGHT_PURPLE = 'LIGHT_PURPLE'

    # Temas da janela principal
    TOPBAR_DARK = 'TOP_BAR_DARK'
    TOPBAR_LIGHT = 'TOP_BAR_LIGHT'
    TOPBAR_PURPLE_LIGHT = 'TOP_BAR_PURPLE_LIGHT'
    TOPBAR_PURPLE_DARK = 'TOP_BAR_PURPLE_DARK'

    # Tema dos Frames
    FRAME_DARK = 'Black.TFrame'  # OK
    FRAME_DARK_GRAY = 'DarkGray.TFrame'
    FRAME_LIGHT = 'LightFrame.TFrame'  # OK
    FRAME_PURPLE_DARK = 'DarkPurple.TFrame'  # OK
    FRAME_PURPLE_LIGHT = 'LightPurple.TFrame'  # OK
    FRAME_GRAY = 'CinzaFrame.TFrame'  # OK
    FRAME_ORANGE_DARK = 'DarkOrange.TFrame'

    # Tama dos botões
    BUTTON_PURPLE_LIGHT = 'Custom.TButtonPurpleLight'  # OK
    BUTTON_GREEN = 'Custom.TButtonGreen'  # OK
    BUTTON_PURPLE_DARK = 'Custom.TButtonPurpleDark'

    # Tema da barra de progresso
    PBAR_GREEN = "Custom.Horizontal.TProgressbar"
    PBAR_PURPLE_LIGHT = "Thin.Horizontal.TProgressbar"
    PBAR_PURPLE = "Purple.Horizontal.TProgressbar"

    # Temas Para Labels
    LABEL_PURPLE_LIGHT = "LargeFont.TLabel"
    LABEL_DEFAULT = "BoldLargeFont.TLabel"  # Custom.TLabel

    TREE_VIEW_PURPLE = "Purple.Treeview.Heading"
    TREE_VIEW_PURPLE_LIGHT = "PurpleLight.Treeview.Heading"
    TREE_VIEW_DARK = "Dark.Treeview"
    TREE_VIEW_GREEN = "Green.Treeview.Heading"


class EnumMessages(Enum):

    STYLE_UPDATE = 'update_style'
    PROCESS_FINISHED = 'process_finished'


T = TypeVar('T')
keyStyles = Literal["buttons", "labels", "frames", "pbar", "app", "menu_bar", "last_update"]
valueStyle: TypeAlias = Union[EnumStyles, str]


#=================================================================#
# Dicionário com tipos de estilos
#=================================================================#
class ConfigMappingStyles(TypedDict):
    buttons: EnumStyles
    labels: EnumStyles
    frames: EnumStyles
    pbar: EnumStyles
    app: EnumStyles
    tree_view: EnumStyles
    menu_bar: EnumStyles
    last_update: str


class TypeStylesJsonDict(TypedDict, total=False):
    buttons: str
    labels: str
    frames: str
    pbar: str
    app: str
    menu_bar: str
    last_update: str


#=================================================================#
# Dicionário com tipos de mensagens enviadas pelos observadores/notificadores
#=================================================================#
class TypeMessageNotification(TypedDict, total=False):
    provider: Any
    message_type: EnumMessages
    body: dict[str, Any]


class MessageNotification(BaseDict):

    def __init__(self, values: dict[str, T] = None, *, provider: Any, message_type: EnumMessages) -> None:
        super().__init__(values)
        self['provider'] = provider
        self['message_type'] = message_type
        self['body'] = {}

    def __repr__(self):
        return f'{self.__class__.__name__}()\n{self.values()}'

    def get_message_type(self) -> EnumMessages:
        return self['message_type']

    def set_message_type(self, n: EnumMessages) -> None:
        self['message_type'] = n

    def get_provider(self) -> Any:
        return self['provider']

    def set_provider(self, p: Any) -> None:
        self['provider'] = p

    def keys(self) -> list[str]:
        return list(super().keys())


# Sujeito notificador
class AbstractNotifyProvider(ABC):
    def __init__(self):
        self.observer_list: set[AbstractObserver] = set()

    def add_observer(self, observer: AbstractObserver):
        self.observer_list.add(observer)

    def remove_observer(self, observer: AbstractObserver):
        if len(self.observer_list) < 1:
            return
        self.observer_list.remove(observer)

    def clear(self):
        self.observer_list.clear()

    @abstractmethod
    def send_notify(self, msg: MessageNotification):
        pass


# Sujeito Observador
class AbstractObserver(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def receiver_notify(self, _obj_receiver: MessageNotification):
        """Receber atualizações."""
        pass


class ObserverWidget(AbstractObserver):
    """
    Sujeito observador que repassa as notificações recebidas para os filhos observadores
    """

    def __init__(self):
        super().__init__()
        self._listener: Callable[[MessageNotification], None] = None

    def __repr__(self):
        return f'{self.__class__.__name__}() Sujeito Observador'

    def set_listener(self, func_observer: Callable[[MessageNotification], None]) -> None:
        self._listener = func_observer

    def receiver_notify(self, msg: MessageNotification):
        """
        Recebe notificações dos sujeitos notificadores e repassa para a página
        """
        if self._listener is not None:
            self._listener(msg)


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


__all__ = [
    'EnumStyles', 'EnumMessages', 'T', 'MessageNotification',
    'AbstractObserver', 'AbstractNotifyProvider', 'ConfigMappingStyles',
    'TypeStylesJsonDict', 'TypeMessageNotification', 'valueStyle', 'keyStyles',
    'NotifyWidget', 'ObserverWidget', 'AppStyles',
]

