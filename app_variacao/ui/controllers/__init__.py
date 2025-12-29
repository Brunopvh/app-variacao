from __future__ import annotations
from app_variacao.ui.models import ModelVariacao


class ControllerVariacao(object):

    def __init__(self):
        self.model = ModelVariacao()

    def get_file_disk(self, f_type) -> str | None:
        return self.model.select_file_disk(f_type)

    def get_files_disk(self, f_type) -> tuple:
        pass
