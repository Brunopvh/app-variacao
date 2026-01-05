#!/usr/bin/env python3
import sys
import os

TEST_FILE = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(TEST_FILE)
MODULES_DIR = os.path.join(ROOT_DIR, 'digitalized')

import app_variacao.soup_files as sp

output_dir = sp.UserFileSystem().get_user_downloads().concat('output', create=True)
sys.path.insert(0, MODULES_DIR)

import pandas as pd


def test():
    from app_variacao.__main__ import main as run
    from typing import Literal
    #run()

    from app_variacao.app.app_types._config import (
        ConfigApp, PrefFileDialog, PrefImportCsv, PreferencesApp
    )
    from app_variacao.app.models import ModelPreferences

    cfg = ModelPreferences()
    c = PrefFileDialog()
    print(c.get_config())
    print(cfg.get_preferences_app().get_config()['import_csv']['encoding'])
    print(c.get_config())


def main():
    test()


if __name__ == '__main__':
    main()
