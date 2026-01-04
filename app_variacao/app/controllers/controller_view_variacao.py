from __future__ import annotations
from app_variacao.app.controllers.controller_base import (
    ControllerPopUpFiles, ControllerPrefs, ControllerVariacao,
    TypeImportSheet
)
from app_variacao.util import File


class ControllerViewVariacao(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self._controller_popup_files = ControllerPopUpFiles()
        self._controller_prefs = ControllerPrefs()

    def get_prefs_import_sheet(self) -> TypeImportSheet:
        return self._controller_prefs.get_prefs_import_sheet()

    def get_path_sheet_variacao(self) -> File | None:
        if 'path' in self._controller_prefs.get_prefs_import_sheet().keys():
            return self._controller_prefs.get_prefs_import_sheet()['path']
        return None

    def select_sheet_variacao(self) -> None:
        """
        Abre uma caixa de diálogo para o usuário selecionar uma planilha CSV/Excel.
        """
        f: File | None = self._controller_popup_files.get_sheet()
        if f is None:
            return
        self.get_prefs_import_sheet()['path'] = f
        self._controller_prefs.save_config()  # Salvar no disco após a seleção
