from tkinter.ttk import Button


class BaseView(object):

    def __init__(self, parent=None):
        self._parent = parent

    def get_button(self, name: str) -> Button:
        pass
