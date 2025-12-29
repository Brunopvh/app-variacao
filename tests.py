#!/usr/bin/env python3
import sys
import os

TEST_FILE = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(TEST_FILE)
MODULES_DIR = os.path.join(ROOT_DIR, 'digitalized')
import app_variacao.soup_files as sp

output_dir = sp.UserFileSystem().userDownloads.concat('output', create=True)
sys.path.insert(0, MODULES_DIR)


def test():
    from app_variacao.ui.core import run_app
    from app_variacao.ui.gui import MainApp

    app = MainApp()
    run_app(app)


def main():
    test()


if __name__ == '__main__':
    main()
