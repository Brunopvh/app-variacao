from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from tkinter import ttk
from app_variacao.app.ui.core_types import (
    ObserverWidget, NotifyWidget, MessageNotification, EnumMessages, ConfigMappingStyles
)


class Container(ttk.Frame):

    def __init__(
                self, master=None, *, border=None,
                borderwidth=None, class_="", cursor="",
                height=25, name=None, padding=None, relief=None,
                style="", takefocus="", width=0
            ):
        super().__init__(
                master, border=border, borderwidth=borderwidth, class_=class_,
                cursor=cursor, height=height, name=name, padding=padding,
                relief=relief, style=style, takefocus=takefocus, width=width
            )
        self._observer_widget: ObserverWidget = ObserverWidget()
        self._observer_widget.set_listener(self._receiver_notify)
        self._notify_provider: NotifyWidget = NotifyWidget()
        self._buttons: set[ttk.Button] = set()
        self._content_labels: set[ttk.Label] = set()
        self._tree_views: set[ttk.Treeview] = set()
        self._combos: set[ttk.Combobox] = set()
        self._progress_bar: set[ttk.Progressbar] = set()

    def add_tree_view(self, **kwargs) -> ttk.Treeview:
        tree = ttk.Treeview(self, **kwargs)
        self._tree_views.add(tree)
        return tree

    def add_pbar(self, **kwargs) -> ttk.Progressbar:
        pbar = ttk.Progressbar(self, **kwargs)
        self._progress_bar.add(pbar)
        return pbar

    def add_button(self, **kwargs) -> ttk.Button:
        '''
            VALID_TTK_OPTIONS = {
            "class_", "compound", "cursor", "image", "name",
            "padding", "state", "style", "takefocus",
            "text", "textvariable", "underline", "width", "command"
            }
        '''
        btn = ttk.Button(self, **kwargs)
        self._buttons.add(btn)
        return btn

    def remove_button(self, btn: ttk.Button) -> None:
        return self._buttons.remove(btn)

    def add_combo_box(self, **kwargs) -> ttk.Combobox:
        combo = ttk.Combobox(self, **kwargs)
        self._combos.add(combo)
        return combo

    def get_combos(self) -> set[ttk.Combobox]:
        return self._combos

    def add_label(self, **kwargs) -> ttk.Label:
        lb = ttk.Label(self, **kwargs)
        self._content_labels.add(lb)
        return lb

    def remove_label(self, lb: ttk.Label) -> None:
        return self._content_labels.remove(lb)

    def get_labels(self) -> set[ttk.Label]:
        return self._content_labels

    def get_buttons(self) -> set[ttk.Button]:
        return self._buttons

    def get_observer(self) -> ObserverWidget:
        return self._observer_widget

    def get_notify_provider(self) -> NotifyWidget:
        return self._notify_provider

    def _receiver_notify(self, message: MessageNotification):
        """
        Recebe um objeto MessageNotification() e toma uma ou mais ações
        a partir do tipo de mensagem recebida.

            Os tipos de mensagens recebidas estão na classe EnumMessages
        se a mensagem recebida for do tipo EnumMessages.STYLE_UPDATE este
        container e os filhos terão o estilo atualizados (cores/temas etc)
        conforme as configurações de estilos recebidas nas mensagens.

        O fluxo funciona com o Container() se auto atualizando e em seguida
        aplicando a atualização aos widgets filhos, frames, buttons, label etc.

        Quem envia mensagem é o próprio observador (propriedade self._observer_widget=ObserverWidget())
        ou seja, para que esse Container() se torne um observador de um sujeito NOTIFICADOR qualquer,
        basta adicionar a propriedade observador self._observer_widget=ObserverWidget() como ouvinte
        de um NOTIFICADOR qualquer, quando o notificador enviar a(s) mensagem(s) elas serão recebidas
        pela propriedade self._notify_widget=NotifyWidget() que repassará a esté Container() pois
        ele em-si não é um observador, mas possui uma propriedade observador.
        """
        if message.get_message_type() == EnumMessages.STYLE_UPDATE:
            # Atualizar o tema do container de conforme o valor de tema
            # recebido na mensagem.
            conf_styles: ConfigMappingStyles = message.get_provider()
            self.config(style=conf_styles['frames'].value)
            # Atualizar o tema dos botões
            for btn in self._buttons:
                btn.config(style=conf_styles['buttons'].value)
            # Atualizar o tema dos labels
            for lbl in self._content_labels:
                lbl.config(style=conf_styles['labels'].value)
            for tree in self._tree_views:
                tree.configure(style=conf_styles['tree_view'].value)
            for pbar in self._progress_bar:
                pbar.config(style=conf_styles['pbar'].value)
        self.get_notify_provider().send_notify(message)


class Row(object):

    def __init__(self, container_master: Container):
        self._container_master = container_master
        self._containers: set[Container] = set()
        self._row_notify_provider: NotifyWidget = NotifyWidget()
        self._row_notify_provider.add_observer(self._container_master.get_observer())
        self._observer: ObserverWidget = ObserverWidget()
        self._observer.set_listener(self._receiver_notify)
        self.values_pack: dict[str, Any] = {
            'side': 'left',
            'padx': 1,
            'pady': 1,
            'fill': 'x',
        }

    def _receiver_notify(self, message: MessageNotification) -> None:
        self.get_notify_provider().send_notify(message)

    def get_observer(self) -> ObserverWidget:
        return self._observer

    def get_notify_provider(self) -> NotifyWidget:
        return self._row_notify_provider

    def add_container(self, **kwargs) -> Container:
        container = Container(self._container_master, **kwargs)
        self._containers.add(container)
        return container

    def add_button(self, **kwargs) -> ttk.Button:
        return self._container_master.add_button(**kwargs)

    def add_label(self, **kwargs) -> ttk.Label:
        return self._container_master.add_label(**kwargs)

    def get_container_master(self) -> Container:
        return self._container_master

    def pack_forget(self) -> None:
        self._container_master.pack_forget()

    def pack(self):

        self._container_master.pack(
            side=self.values_pack['side'], pady=self.values_pack['pady'],
            padx=self.values_pack['padx'], fill=self.values_pack['fill'],
        )
        for _container in self._containers:
            _container.pack(
                side=self.values_pack['side'], pady=self.values_pack['pady'],
                padx=self.values_pack['padx'], fill=self.values_pack['fill'],
            )

        for combo in self._container_master.get_combos():
            combo.pack(
                side=self.values_pack['side'], pady=self.values_pack['pady'],
                padx=self.values_pack['padx'], fill=self.values_pack['fill'],
            )

        for btn in self._container_master.get_buttons():
            btn.pack(
                side=self.values_pack['side'], pady=self.values_pack['pady'],
                padx=self.values_pack['padx'], fill=self.values_pack['fill'],
            )

        for lb in self._container_master.get_labels():
            lb.pack(
                side=self.values_pack['side'], pady=self.values_pack['pady'],
                padx=self.values_pack['padx'], fill=self.values_pack['fill'],
            )


class Column(Row):

    def __init__(self, container_master: Container):
        super().__init__(container_master)
        self.values_pack['side'] = 'bottom'


class InterfaceProgressBar(ABC):

    def __init__(self):
        self._current_percent: float = 0.0  # 0 -> 100
        self._initial_value: int = 0
        self._end_value: int = 0
        self._prefix_text: str = '-'
        self._output_text: str = 'Aguarde...'
        self._running: bool = False

    @abstractmethod
    def start(self):
        """Inicia a barra de progresso (pode ser vazio dependendo da implementação)"""
        pass

    @abstractmethod
    def stop(self):
        """Para a barra de progresso (pode ser vazio dependendo da implementação)"""
        pass

    @abstractmethod
    def update_output_text(self):
        pass

    @abstractmethod
    def init_pbar(self, **kwargs):
        pass

    @abstractmethod
    def get_real_pbar(self) -> Any:
        pass

    def is_running(self) -> bool:
        return self._running

    def set_running(self, running: bool):
        self._running = running

    def get_prefix_text(self) -> str:
        return self._prefix_text

    def set_prefix_text(self, text: str) -> None:
        self._prefix_text = text

    def add_count_value(self) -> None:
        if self._initial_value < self._end_value:
            self._initial_value += 1

    def calcule_current_progress(self) -> None:
        if self._current_percent < 0:
            self._current_percent = 0.0
            return
        if self._initial_value >= self._end_value:
            self._current_percent = 100.0
            self._initial_value = self._end_value
        if self._end_value < 0:
            print(f'DEBUG: {__class__.__name__} Erro ... defina um valor final diferente de 0')
            return
        self._current_percent = (self._initial_value / self._end_value) * 100
        self.set_output_text(
            f"{self._current_percent:.2f}% [{self._initial_value}/{self._end_value}]:"
        )

    def set_output_text(self, text: str):
        self._output_text = text

    def get_output_text(self):
        return self._output_text

    def get_message_text(self) -> str:
        return f"{self.get_output_text()} {self.get_prefix_text()}"

    def set_current_percent(self, prog: float):
        self._current_percent = prog

    def get_current_percent(self) -> float:
        return self._current_percent

    def set_initial_value(self, prog: int):
        self._initial_value = prog

    def get_initial_value(self) -> int:
        return self._initial_value

    def set_end_value(self, prog: int):
        self._end_value = prog

    def get_end_value(self) -> int:
        return self._end_value


class ProgressBarTkIndeterminate(InterfaceProgressBar):

    def __init__(self, container: Container, mode='indeterminate'):
        super().__init__()
        self._container: Container = container
        self._lb_text = ttk.Label(self._container, text='-')
        self._real_pbar: ttk.Progressbar = self._container.add_pbar(mode=mode)

    def get_real_pbar(self) -> ttk.Progressbar:
        return self._real_pbar

    def init_pbar(self, **kwargs):
        self._lb_text.pack(fill='both', pady=2, padx=1)
        self._container.pack(fill='x', padx=2, pady=1)
        self._real_pbar.pack(fill='x', padx=2, pady=1)

        if kwargs:
            if 'style' in kwargs.get("kwargs").keys():
                self._real_pbar.configure(style=kwargs.get("kwargs")["style"])
        self._real_pbar.pack(fill='x', padx=2, pady=1)

    def start(self):
        self._real_pbar.start(8)

    def stop(self):
        self.add_count_value()
        self.calcule_current_progress()
        self.update_output_text()
        self._real_pbar.stop()

    def update_output_text(self):
        self._lb_text.configure(text=self.get_message_text())


class ProgressBarTkDeterminate(ProgressBarTkIndeterminate):

    def __init__(self, container: Container, mode='indeterminate'):
        super().__init__(container, mode)

        self._real_pbar: ttk.Progressbar = ttk.Progressbar(
            self._container, mode='determinate', maximum=100
        )

    def get_real_pbar(self) -> ttk.Progressbar:
        return self._real_pbar

    def start(self):
        self.set_running(True)
        self._real_pbar['value'] = 0

    def stop(self):
        self.add_count_value()
        self.calcule_current_progress()
        self.update_output_text()
        self._real_pbar.stop()
        self.set_running(False)

    def update_output_text(self):
        self._lb_text.configure(text=self.get_message_text())
        self._real_pbar['value'] = self.get_current_percent()
        # FORÇA o Tkinter a redesenhar a interface imediatamente
        self._container.update_idletasks()


class ProgressBar(object):

    def __init__(self, pbar: InterfaceProgressBar):
        super().__init__()
        self.interface_pbar: InterfaceProgressBar = pbar

    def get_real_pbar(self) -> Any:
        self.interface_pbar.get_real_pbar()

    def init_pbar(self, **kwargs):
        self.interface_pbar.init_pbar(**kwargs)

    def get_message_text(self) -> str:
        return self.interface_pbar.get_message_text()

    def update_output_text(self):
        self.interface_pbar.update_output_text()

    def update(self, value_progress: int = None, output_text: str = None):
        _increment = True if value_progress is None else False
        if value_progress is not None:
            self.set_initial_value(value_progress)
        if output_text is not None:
            self.set_output_text(output_text)
        if _increment:
            self.add_count_value()
        self.calcule_current_progress()
        self.update_output_text()

    def start(self):
        self.interface_pbar.start()

    def stop(self):
        self.interface_pbar.stop()

    def is_running(self) -> bool:
        return self.interface_pbar.is_running()

    def set_running(self, running: bool):
        self.interface_pbar.set_running(running)

    def get_prefix_text(self) -> str:
        return self.interface_pbar.get_prefix_text()

    def set_prefix_text(self, text: str) -> None:
        self.interface_pbar.set_prefix_text(text)

    def add_count_value(self) -> None:
        self.interface_pbar.add_count_value()

    def calcule_current_progress(self) -> None:
        self.interface_pbar.calcule_current_progress()

    def set_output_text(self, text: str):
        self.interface_pbar.set_output_text(text)

    def get_output_text(self):
        return self.interface_pbar.get_output_text()

    def set_current_percent(self, prog: float):
        self.interface_pbar.set_current_percent(prog)

    def get_current_percent(self) -> float:
        return self.interface_pbar.get_current_percent()

    def set_initial_value(self, prog: int):
        self.interface_pbar.set_initial_value(prog)

    def get_initial_value(self) -> int:
        return self.interface_pbar.get_initial_value()

    def set_end_value(self, prog: int):
        self.interface_pbar.set_end_value(prog)

    def get_end_value(self) -> int:
        return self.interface_pbar.get_end_value()

    @classmethod
    def create_pbar_tk(cls, container: Container, *, mode: str = 'determinate'):
        return cls(
            ProgressBarTkDeterminate(container) if mode == 'determinate' else ProgressBarTkIndeterminate(container)
        )


__all__ = [
    'Container', 'InterfaceProgressBar',
    'ProgressBar', 'Row'
]
