from __future__ import annotations
from app_variacao.app.controllers.controller_base import (
    ControllerPopUpFiles, ControllerPrefs, ControllerVariacao, UserPreferences,
)
from app_variacao.util import File, Directory


class ControllerViewVariacao(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self._controller_popup_files = ControllerPopUpFiles()
        self._controller_prefs = ControllerPrefs()
        self.sheet_variacao: File | None = None
        self.start()

    def start(self):
        if 'sheet_variacao' in self._controller_prefs.get_prefs().keys():
            self.sheet_variacao = File(self._controller_prefs.get_prefs()['sheet_variacao'])

    def select_sheet_variacao(self) -> None:
        f: File | None = self._controller_popup_files.get_sheet()
        if f is not None:
            self.sheet_variacao = f
            self._controller_prefs.get_prefs()['sheet_variacao'] = f.absolute()
            self._controller_prefs.save_config()
