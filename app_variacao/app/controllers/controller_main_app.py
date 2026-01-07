from __future__ import annotations
from app_variacao.app.app_types import ConfigMappingStyles
from app_variacao.app.controllers.controller_base import ControllerPrefs
from app_variacao.util import File


class ControllerMainApp(object):

    _instance_controller = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_controller is None:
            cls._instance_controller = super(ControllerMainApp, cls).__new__(cls)
        return cls._instance_controller

    def __init__(self):
        self._controller_prefs = ControllerPrefs()

    def get_conf_styles(self) -> ConfigMappingStyles:
        return self._controller_prefs.get_conf_styles()

    def save_configs(self) -> None:
        self._controller_prefs.save_config()

    def get_file_config(self) -> File:
        return self._controller_prefs.get_file_config()




