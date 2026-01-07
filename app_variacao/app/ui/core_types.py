#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Generic, TypeVar, TypeAlias, Union, Literal, TypedDict
from app_variacao.documents.types import BaseDict


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


class EnumMessages(Enum):

    MSG_UPDATE_STYLE = 'update_style'
    MSG_PROCESS_FINISHED = 'process_finished'


T = TypeVar('T')
keyStyles = Literal["buttons", "labels", "frames", "pbar", "app", "menu_bar", "last_update"]
valueStyle: TypeAlias = Union[EnumStyles, str]


class CoreDict(dict[str, T], Generic[T]):

    def __init__(self, values: dict = None) -> None:
        if values is None:
            super().__init__({})
        else:
            super().__init__(values)

    def __repr__(self):
        return f'{self.__class__.__name__}()\n{super().__repr__()}\n'

    def get_first(self) -> T:
        _k = self.keys()[0]
        return self[_k]

    def set_first(self, value: T) -> None:
        self[self.keys()[0]] = value

    def get_last(self) -> T:
        return self[self.keys()[-1]]

    def set_last(self, value: T) -> None:
        self[self.keys()[-1]] = value

    def keys(self) -> list[str]:
        return list(super().keys())


#=================================================================#
# Dicionário com tipos de estilos
#=================================================================#
class ConfigMappingStyles(TypedDict):
    buttons: EnumStyles
    labels: EnumStyles
    frames: EnumStyles
    pbar: EnumStyles
    app: EnumStyles
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


class MessageNotification(CoreDict):

    def __init__(self, values: dict[str, T] = None, *, provider: Any, message_type: EnumMessages) -> None:
        super().__init__(values)
        self['provider'] = provider
        self['message_type'] = message_type

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

    def get_first(self) -> T:
        _k = self.keys()[0]
        return self[_k]

    def set_first(self, value: T) -> None:
        self[self.keys()[0]] = value

    def get_last(self) -> T:
        return self[self.keys()[-1]]

    def set_last(self, value: T) -> None:
        self[self.keys()[-1]] = value

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


__all__ = [
    'EnumStyles', 'EnumMessages', 'T', 'MessageNotification',
    'AbstractObserver', 'AbstractNotifyProvider', 'ConfigMappingStyles',
    'TypeStylesJsonDict', 'TypeMessageNotification', 'valueStyle', 'keyStyles'
]

