#!/usr/bin/env python3
from __future__ import annotations
from typing import Callable, Any
from app_variacao.soup_files import File, EnumDocFiles
from app_variacao.app.controllers import ControllerPopUpFiles, ControllerAppConfig, EnumPrefs
from app_variacao.ui.core.core_widgets import (
    ObserverWidget, NotifyWidget, MyApp, EnumThemes, AppStyles
)
import tkinter as tk


class MenuBar(object):

    def __init__(self, *, app: MyApp):
        super().__init__()
        self.version = '1.0'
        self.myapp = app
        self._controller_conf = ControllerAppConfig()

        # -------------------------------------------------------------#
        # Criar a barra superior
        # -------------------------------------------------------------#
        # Iniciar a barra com tema dark
        bg_color = "gray15"
        fg_color = "white"
        active_bg_color = "gray30"
        active_fg_color = "white"

        self.menu_bar: tk.Menu = tk.Menu(self.myapp.get_window())
        self.menu_bar.config(
            bg=bg_color,
            fg=fg_color,
            activebackground=active_bg_color,
            activeforeground=active_fg_color
        )
        self.myapp.get_window().config(menu=self.menu_bar)

        # -------------------------------------------------------------#
        # Criar o menu Arquivo
        # -------------------------------------------------------------#
        self.menu_file: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.menu_file)
        self.index_menu_exit = self.add_item_menu(
            name='Sair',
            tooltip='Sair do programa',
            cmd=self.myapp.exit_app,
            submenu=self.menu_file,
        )
        self.menu_file.config(background='red')

        # -------------------------------------------------------------#
        # Menu Configurações
        # -------------------------------------------------------------#
        self.menu_config: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Configurações", menu=self.menu_config)

        # Arquivo de configurações
        file_conf: str = self._controller_conf.get_file_config().absolute()

        self.index_config_file = self.add_item_menu(
            tooltip=self._controller_conf.get_file_config().absolute(),
            name='Arquivo de configuração: ',
            cmd=(),
            submenu=self.menu_config,
        )
        # Pasta de trabalho
        self.index_work_dir: int = self.add_item_menu(
            tooltip=self._controller_conf.get_work_dir_app(),
            name='Pasta de trabalho: ',
            cmd=lambda: self.change_work_dir(),
            submenu=self.menu_config,
        )

        # -------------------------------------------------------------#
        # Menu Estilo
        # -------------------------------------------------------------#
        self.style_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tema", menu=self.style_menu)
        self.init_menu_style()

        # -------------------------------------------------------------#
        # Menu sobre
        # -------------------------------------------------------------#
        self.menu_about_bar: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sobre", menu=self.menu_about_bar)
        self.menu_about_bar.add_command(label=f'Versão: {self.version}')

        self.indexAutor = self.add_item_menu(
            cmd=(),
            submenu=self.menu_about_bar,
            tooltip='autor',
            name='Autor'
        )

    def add_item_menu(
                self, *,
                name: str,
                tooltip: str,
                cmd: Callable[[], Any],
                submenu: tk.Menu
            ) -> int:
        """
            Adiciona um item ao menu com um tooltip.

            :param name: Nome do item no menu.
            :param tooltip: Texto do tooltip exibido no menu.
            :param cmd: Função a ser chamada ao clicar no item.
            :param submenu: Um item do menu, Arquivo, Sobre, etc.
            :return: Índice do item adicionado no menu.
        """
        submenu.add_command(label=f"{name} ({tooltip})", command=cmd)
        return submenu.index(tk.END)

    def init_menu_style(self):
        # Submenu para temas da barra
        self.bar_theme_menu: tk.Menu = tk.Menu(self.style_menu, tearoff=0)

        self.bar_theme_menu.add_command(
            label="Tema Claro",
            command=lambda: self.set_theme_menu_bar(EnumThemes.LIGHT)
        )
        self.bar_theme_menu.add_command(
            label="Tema Escuro",
            command=lambda: self.set_theme_menu_bar(EnumThemes.DARK)
        )
        self.bar_theme_menu.add_command(
            label="Tema Roxo Claro",
            command=lambda: self.set_theme_menu_bar(EnumThemes.LIGHT_PURPLE)
        )

        # -------------------------------------------------------------#
        # Submenu para temas do app
        # -------------------------------------------------------------#
        self.bar_theme_app = tk.Menu(self.style_menu, tearoff=0)
        self.bar_theme_app.add_command(
            label="Tema Claro",
            command=lambda: self.set_theme_app(EnumThemes.LIGHT),
        )
        self.bar_theme_app.add_command(
            label="Tema Escuro",
            command=lambda: self.set_theme_app(EnumThemes.DARK),
        )
        self.bar_theme_app.add_command(
            label="Roxo Escuro",
            command=lambda: self.set_theme_app(EnumThemes.DARK_PURPLE),
        )
        self.bar_theme_app.add_command(
            label="Roxo Claro",
            command=lambda: self.set_theme_app(EnumThemes.LIGHT_PURPLE),
        )

        # Submenu para temas dos botões
        self.bar_theme_buttons = tk.Menu(self.style_menu, tearoff=0)
        self.bar_theme_buttons.add_command(
            label="Botões verdes",
            command=lambda: self.set_theme_buttons(EnumThemes.BUTTON_GREEN),
        )
        self.bar_theme_buttons.add_command(
            label="Botões Roxo claro",
            command=lambda: self.set_theme_buttons(EnumThemes.BUTTON_PURPLE_LIGHT),
        )

        # Adicionar os submenus à barra de menu principal
        self.style_menu.add_cascade(label="Tema do App", menu=self.bar_theme_app)
        self.style_menu.add_cascade(label="Tema da barra", menu=self.bar_theme_menu)
        self.style_menu.add_cascade(label="Tema dos botões", menu=self.bar_theme_buttons)

    def set_theme_menu_bar(self, new: EnumThemes):
        bg_color = "gray15"
        fg_color = "white"
        active_bg_color = "gray30"
        active_fg_color = "white"

        if new == EnumThemes.LIGHT:
            bg_color = "white"
            fg_color = "black"
            active_bg_color = "lightgray"
            active_fg_color = "black"
        elif new == EnumThemes.LIGHT_PURPLE:
            # barra com tema roxo claro
            bg_color = "#B388EB"  # Roxo claro (tom pastel)
            fg_color = "white"  # Texto branco para contraste
            active_bg_color = "#a070d6"  # Roxo um pouco mais escuro para hover
            active_fg_color = "white"  # Texto branco também no hover

        self.menu_bar.config(
            bg=bg_color,
            fg=fg_color,
            activebackground=active_bg_color,
            activeforeground=active_fg_color
        )

    def set_theme_app(self, new: EnumThemes):
        self.myapp.appTheme = new

    def set_theme_buttons(self, new: EnumThemes):
        self.myapp.buttonsTheme = new

    def change_work_dir(self):
        _popup = ControllerPopUpFiles()
        _work_dir = _popup.select_folder()
        if _work_dir is None:
            return

        self._controller_conf.set_work_dir_app(_work_dir)
        self.menu_config.entryconfig(
            self.index_work_dir,
            label=f'Pasta de trabalho: {_work_dir.absolute()}'
        )

    def update_menu_bar(self):
        """Atualizar as opções do Menu"""
        self.menu_config.entryconfig(
            self.index_menu_exit,
            label=f'Arquivo: {self._controller_conf.get_file_config().absolute()}'
        )

    def update_state(self):
        self.update_menu_bar()

    def receiver_notify(self, notify_provider = None):
        """
            Receber notificações quando as preferências
            do app_ui forem atualizadas.
        """
        self.update_state()
