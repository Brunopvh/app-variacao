from __future__ import annotations
from app_variacao.app.models import ModelPopUpFiles, ModelVariacao
from app_variacao.soup_files import EnumDocFiles, File
from app_variacao.types.array import ArrayList


class ControllerVariacao(object):

    def __init__(self):
        self.model = ModelVariacao()


class ControllerPopUpFiles(ControllerVariacao):

    def __init__(self):
        super().__init__()
        self.model = ModelPopUpFiles()

    def get_files_excel(self) -> ArrayList[File]:
        return self.model.select_files_disk(EnumDocFiles.EXCEL)

    def get_file_excel(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.EXCEL)

    def get_file_csv(self) -> File | None:
        return self.model.select_file_disk(EnumDocFiles.CSV)





