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
StyleKeys = Literal[
    "buttons", "labels", "frames", "pbar", "app", "menu_bar", "last_update"
]
StyleValues: TypeAlias = Union[EnumStyles, str]


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
class TypeMappingStylesDict(TypedDict):
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


class MappingStyles(BaseDict[StyleValues]):
    """
    Mapeia os estilos dos widgets, botões, labels, frames etc.
    """

    _instance_map_styles = None
    styles_keys: tuple[str] = (
        'buttons', 'labels', 'frames', 'pbar', 'app', 'menu_bar',
    )

    def __new__(cls, *args, **kwargs):
        if cls._instance_map_styles is None:
            cls._instance_map_styles = super(MappingStyles, cls).__new__(cls)
        return cls._instance_map_styles

    def __init__(self, values: TypeMappingStylesDict = None) -> None:
        super().__init__(values)
        # Garante que __init__ não será executado mais de uma vez
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

    def __setitem__(self, key: StyleKeys, value: StyleValues):
        if not isinstance(key, str):
            raise ValueError(
                f'{__class__.__name__} chave de estilo incorreta use str, não {type(key)}'
            )
        if (not isinstance(value, str)) and (not isinstance(value, EnumStyles)):
            raise ValueError(
                f'{__class__.__name__} valor de estilo incorreto use str|EnumStyles, não {type(value)}'
            )
        super().__setitem__(key, value)

    def __getitem__(self, key) -> StyleValues:
        return super().__getitem__(key)

    @classmethod
    def create_default(cls) -> MappingStyles:
        _values: TypeMappingStylesDict = {
                'buttons': EnumStyles.BUTTON_PURPLE_LIGHT,
                'labels': EnumStyles.LABEL_PURPLE_LIGHT,
                'frames': EnumStyles.FRAME_PURPLE_DARK,
                'pbar': EnumStyles.PBAR_PURPLE,
                'app': EnumStyles.WINDOW_DARK,
                'menu_bar': EnumStyles.TOPBAR_DARK,
                'last_update': 'frames',
            }
        return cls(_values)

    @classmethod
    def format_dict(cls, values: dict[str, Any]) -> TypeMappingStylesDict:
        """
        Formatar um dicionário para o modelo MappingStyles()
        """
        final: TypeMappingStylesDict = dict()

        for key_style, value_style in values.items():
            if key_style == 'buttons':
                if value_style == EnumStyles.BUTTON_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.BUTTON_PURPLE_LIGHT
                elif value_style == EnumStyles.BUTTON_GREEN.value:
                    final[key_style] = EnumStyles.BUTTON_GREEN
                elif value_style == EnumStyles.BUTTON_PURPLE_DARK.value:
                    final[key_style] = EnumStyles.BUTTON_PURPLE_DARK
            elif key_style == 'labels':
                if value_style == EnumStyles.LABEL_DEFAULT.value:
                    final[key_style] = EnumStyles.LABEL_DEFAULT
                elif value_style == EnumStyles.LABEL_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.LABEL_PURPLE_LIGHT
            elif key_style == 'frames':
                if value_style == EnumStyles.FRAME_DARK.value:
                    final[key_style] = EnumStyles.FRAME_DARK
                elif value_style == EnumStyles.FRAME_LIGHT.value:
                    final[key_style] = EnumStyles.FRAME_LIGHT
                elif value_style == EnumStyles.FRAME_PURPLE_DARK.value:
                    final[key_style] = EnumStyles.FRAME_PURPLE_DARK
                elif value_style == EnumStyles.FRAME_DARK_GRAY.value:
                    final[key_style] = EnumStyles.FRAME_DARK_GRAY
                elif value_style == EnumStyles.FRAME_ORANGE_DARK.value:
                    final[key_style] = EnumStyles.FRAME_ORANGE_DARK
            elif key_style == 'pbar':
                if value_style == EnumStyles.PBAR_PURPLE.value:
                    final[key_style] = EnumStyles.PBAR_PURPLE
                elif value_style == EnumStyles.PBAR_GREEN.value:
                    final[key_style] = EnumStyles.PBAR_GREEN
                elif value_style == EnumStyles.PBAR_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.PBAR_PURPLE_LIGHT
            elif key_style == 'menu_bar':
                if value_style == EnumStyles.TOPBAR_DARK.value:
                    final[key_style] = EnumStyles.TOPBAR_DARK
                elif value_style == EnumStyles.TOPBAR_LIGHT.value:
                    final[key_style] = EnumStyles.TOPBAR_LIGHT
                elif value_style == EnumStyles.TOPBAR_PURPLE_LIGHT.value:
                    final[key_style] = EnumStyles.TOPBAR_PURPLE_LIGHT
                elif value_style == EnumStyles.TOPBAR_PURPLE_DARK.value:
                    final[key_style] = EnumStyles.TOPBAR_PURPLE_DARK
        return final

    @classmethod
    def create_from_dict(cls, values: TypeStylesJsonDict) -> MappingStyles:
        final: TypeMappingStylesDict = cls.format_dict(values)
        _obj = cls()
        _obj.merge_dict(final)
        return _obj

    def merge_dict(self, new: TypeMappingStylesDict) -> None:
        for k in new.keys():
            self[k] = new[k]

    def to_dict(self) -> dict[str, str]:
        final = dict()
        for key, value_style in self.items():
            if isinstance(value_style, EnumStyles):
                final[key] = value_style.value
            else:
                final[key] = value_style
        return final

    def get_last_update(self) -> str:
        return self["last_update"]

    def set_last_update(self, value: StyleKeys):
        self["last_update"] = value

    def get_style_buttons(self) -> EnumStyles:
        return self['buttons']

    def set_style_buttons(self, style: EnumStyles) -> None:
        self['buttons'] = style
        self["last_update"] = "buttons"

    def get_style_labels(self) -> EnumStyles:
        return self['labels']

    def set_style_labels(self, style: EnumStyles) -> None:
        self['labels'] = style
        self["last_update"] = "labels"

    def get_style_frames(self) -> EnumStyles:
        return self['frames']

    def set_style_frames(self, style: EnumStyles) -> None:
        self['frames'] = style
        self["last_update"] = "frames"

    def get_style_pbar(self) -> EnumStyles:
        return self['pbar']

    def set_style_pbar(self, style: EnumStyles) -> None:
        self['pbar'] = style
        self["last_update"] = "pbar"

    def get_style_app(self) -> EnumStyles:
        return self['app']

    def set_style_app(self, style: EnumStyles) -> None:
        self['app'] = style
        self["last_update"] = "app"

    def get_style_menu_bar(self) -> EnumStyles:
        return self['menu_bar']

    def set_style_menu_bar(self, new: EnumStyles) -> None:
        self['menu_bar'] = new
        self['last_update'] = 'menu_bar'


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
    def receiver_notify(self, _obj_receiver: MessageNotification[T]):
        """Receber atualizações."""
        pass


__all__ = [
    'EnumStyles', 'EnumMessages', 'T', 'MessageNotification',
    'AbstractObserver', 'AbstractNotifyProvider', 'MappingStyles',
    'TypeMappingStylesDict', 'TypeStylesJsonDict', 'TypeMessageNotification',
    'StyleKeys', 'StyleValues',
]

