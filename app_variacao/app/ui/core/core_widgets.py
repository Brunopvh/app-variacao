from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from tkinter import ttk


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


class ContainerH(Container):

    def __init__(
                self, master=None, *, border=None,
                borderwidth=None, class_="", cursor="",
                height=0, name=None, padding=None, relief=None,
                style="", takefocus="", width=0
            ):
        super().__init__(
                master, border=border, borderwidth=borderwidth, class_=class_,
                cursor=cursor, height=height, name=name, padding=padding,
                relief=relief, style=style, takefocus=takefocus, width=width
            )
        pass


class ContainerV(ttk.Frame):

    def __init__(
                self, master=None, *, border=None,
                borderwidth=None, class_="", cursor="",
                height=0, name=None, padding=None, relief=None,
                style="", takefocus="", width=0
            ):
        super().__init__(
                master, border=border, borderwidth=borderwidth, class_=class_,
                cursor=cursor, height=height, name=name, padding=padding,
                relief=relief, style=style, takefocus=takefocus, width=width
            )
        pass


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

    def __init__(self, container: Container):
        super().__init__()
        self._container: Container = container
        self._lb_text = ttk.Label(self._container, text='-')
        self._real_pbar: ttk.Progressbar = ttk.Progressbar(
            self._container, mode='indeterminate'
        )

    def get_real_pbar(self) -> ttk.Progressbar:
        return self._real_pbar

    def init_pbar(self, **kwargs):
        self._lb_text.pack(expand=True, fill='both')
        self._container.pack(expand=True, fill='x', padx=1, pady=1)
        self._real_pbar.pack(expand=True, fill='x', padx=1, pady=1)

    def start(self):
        self._real_pbar.start(8)

    def stop(self):
        self.add_count_value()
        self.calcule_current_progress()
        self.update_output_text()
        self._real_pbar.stop()

    def update_output_text(self):
        self._lb_text.configure(text=self.get_message_text())


class ProgressBarTkDeterminate(InterfaceProgressBar):

    def __init__(self, container: Container):
        super().__init__()
        self._container: Container = container
        self._lb_text = ttk.Label(self._container, text='-')
        self._real_pbar: ttk.Progressbar = ttk.Progressbar(
            self._container, mode='determinate', maximum=100
        )

    def get_real_pbar(self) -> ttk.Progressbar:
        return self._real_pbar

    def init_pbar(self, **kwargs):
        self._container.configure(height=35)
        # self._container.pack_propagate(False)
        #self._container.pack(fill='x', padx=2, pady=2)
        self._container.pack(side='bottom', fill='x', padx=2, pady=1)
        self._lb_text.pack(fill='x', padx=2, pady=1)
        if kwargs:
            if 'style' in kwargs:
                self._real_pbar.configure(style=kwargs['style'])
        self._real_pbar.pack(expand=True, fill='x', padx=2, pady=1)

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
