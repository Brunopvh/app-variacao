from __future__ import annotations
from typing import Callable, Any, Optional
from app_variacao.app.controllers import ControllerPopUpFiles, ControllerPrefs
from app_variacao.app.ui.base_view import BaseView
from app_variacao.app.ui.core.core_types import EnumStyles, MessageNotification, EnumMessages
from app_variacao.app.ui.core.core_pages import MyApp
import tkinter as tk


def add_item_menu(name: str, submenu: tk.Menu, *, tooltip: str = None, cmd: Callable[[], Any] = ()) -> int:
    """
        Adiciona um elemento em um submenu com um tooltip.

        :param name: Nome do item no menu.
        :param tooltip: Texto do tooltip exibido no menu.
        :param cmd: Função a ser chamada ao clicar no item.
        :param submenu: Um item do menu, Arquivo, Sobre, etc.
        :return: Índice do item adicionado no menu.
    """
    _txt = name
    if tooltip is not None:
        _txt = f"{name} [{tooltip}]"
    submenu.add_command(label=_txt, command=cmd)
    return submenu.index(tk.END)


class MenuBar(BaseView):

    def __init__(self, *, app: MyApp):
        super().__init__()
        self.version = '1.0'
        self.myapp = app
        self._controller_conf = ControllerPrefs()
        self._add_item_menu: Callable[
            [str, tk.Menu, Optional[str], Optional[Callable]], int
        ] = add_item_menu

        # -------------------------------------------------------------#
        # Criar a barra superior
        # -------------------------------------------------------------#
        # Criar a barra superior principal
        self.master_menu_bar: tk.Menu = tk.Menu(self.myapp.get_window())
        self.myapp.get_window().config(menu=self.master_menu_bar)

        # -------------------------------------------------------------#
        # Criar o menu Arquivo
        # -------------------------------------------------------------#
        self.menu_file: tk.Menu = tk.Menu(self.master_menu_bar, tearoff=0)
        self.master_menu_bar.add_cascade(label="Arquivo", menu=self.menu_file)
        # Pasta de trabalho
        self.index_menu_back_page: int = self.add_item_menu(
            name='Voltar',
            submenu=self.menu_file,
            cmd=lambda: self.myapp.get_navigator().pop(),
        )
        self.index_menu_exit = self.add_item_menu(
            name='Sair',
            submenu=self.menu_file,
            tooltip='Sair do programa',
            cmd=self.myapp.exit_app,
        )
        self.menu_file.config(background='gray')

        # -------------------------------------------------------------#
        # Menu Configurações
        # -------------------------------------------------------------#
        self.menu_config: tk.Menu = tk.Menu(self.master_menu_bar, tearoff=0)
        self.master_menu_bar.add_cascade(label="Configurações", menu=self.menu_config)

        # Arquivo de configurações obtido do disco a partir da controller.
        self.index_config_file = self.add_item_menu(
            name='Arquivo de configuração: ',
            submenu=self.menu_config,
            tooltip=self._controller_conf.get_file_config().absolute(),
            cmd=(),
        )

        # Pasta de trabalho
        self.index_work_dir: int = self.add_item_menu(
            name='Pasta de trabalho: ',
            submenu=self.menu_config,
            tooltip=self._controller_conf.get_work_dir_app(),
            cmd=lambda: self.change_work_dir(),
        )

        # -------------------------------------------------------------#
        # Menu Estilo (Alterar os temas/estilos do app)
        # -------------------------------------------------------------#
        # Menu Estilo
        self.style_menu = tk.Menu(self.master_menu_bar, tearoff=0)
        self.master_menu_bar.add_cascade(label="Tema", menu=self.style_menu)

        # Iniciar o tema
        self.set_theme_menu_bar(
            self._controller_conf.get_prefs().get_app_styles().get_style_menu_bar()
        )

        # Submenu para alterar o estilo da barra/menu.
        self.menu_option_style_top_bar: tk.Menu = tk.Menu(self.style_menu, tearoff=0)
        # Sub sessão para o tema claro.
        self.menu_option_style_top_bar.add_command(
            label="Tema Claro",
            command=lambda: self.set_theme_menu_bar(EnumStyles.TOPBAR_LIGHT)
        )
        # Sub sessão para o tema escuro.
        self.menu_option_style_top_bar.add_command(
            label="Tema Escuro",
            command=lambda: self.set_theme_menu_bar(EnumStyles.TOPBAR_DARK)
        )
        # Sub sessão para o tema roxo claro.
        self.menu_option_style_top_bar.add_command(
            label="Tema Roxo Claro",
            command=lambda: self.set_theme_menu_bar(EnumStyles.TOPBAR_PURPLE_LIGHT)
        )
        # Sub sessão para o tema roxo escuro.
        self.menu_option_style_top_bar.add_command(
            label="Tema Roxo escuro",
            command=lambda: self.set_theme_menu_bar(EnumStyles.TOPBAR_PURPLE_DARK)
        )

        # -------------------------------------------------------------#
        # Submenu para temas do app
        # -------------------------------------------------------------#
        self.menu_option_style_app = tk.Menu(self.style_menu, tearoff=0)
        self.menu_option_style_app.add_command(
            label="Tema Escuro",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_DARK),
        )
        self.menu_option_style_app.add_command(
            label="Tema Cinza Escuro",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_DARK_GRAY),
        )
        self.menu_option_style_app.add_command(
            label="Tema Cinza",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_GRAY),
        )
        self.menu_option_style_app.add_command(
            label="Tema Claro",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_LIGHT),
        )
        self.menu_option_style_app.add_command(
            label="Roxo Escuro",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_PURPLE_DARK),
        )
        self.menu_option_style_app.add_command(
            label="Roxo Claro",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_PURPLE_LIGHT),
        )
        self.menu_option_style_app.add_command(
            label="Laranja",
            command=lambda: self.update_theme_frames(EnumStyles.FRAME_ORANGE_DARK),
        )

        # -------------------------------------------------------------#
        # Submenu para temas dos botões
        # -------------------------------------------------------------#
        self.menu_option_style_buttons = tk.Menu(self.style_menu, tearoff=0)
        self.menu_option_style_buttons.add_command(
            label="Botões verdes",
            command=lambda: self.set_theme_buttons(EnumStyles.BUTTON_GREEN),
        )
        self.menu_option_style_buttons.add_command(
            label="Botões Roxo claro",
            command=lambda: self.set_theme_buttons(EnumStyles.BUTTON_PURPLE_LIGHT),
        )
        self.menu_option_style_buttons.add_command(
            label="Botões Roxo escuro",
            command=lambda: self.set_theme_buttons(EnumStyles.BUTTON_PURPLE_DARK),
        )

        # Adicionar os submenus à barra de menu principal
        self.style_menu.add_cascade(label="Tema do App", menu=self.menu_option_style_app)
        self.style_menu.add_cascade(label="Tema da barra", menu=self.menu_option_style_top_bar)
        self.style_menu.add_cascade(label="Tema dos botões", menu=self.menu_option_style_buttons)

        # -------------------------------------------------------------#
        # Menu sobre (Versão do app etc)
        # -------------------------------------------------------------#
        self.menu_bar_about: tk.Menu = tk.Menu(self.master_menu_bar, tearoff=0)
        self.master_menu_bar.add_cascade(label="Sobre", menu=self.menu_bar_about)
        self.menu_bar_about.add_command(label=f'Versão: {self.version}')

        self.idx_pos_autor: int = self.add_item_menu(
            name='Autor',
            submenu=self.menu_bar_about,
            tooltip='autor',
        )

        self._message_top_bar = MessageNotification(
            provider=self.myapp.get_styles_mapping(),
            message_type=EnumMessages.MSG_UPDATE_STYLE,
        )

    def add_item_menu(
                self,
                name: str,
                submenu: tk.Menu, *,
                tooltip: str = None,
                cmd: Callable[[], Any] = (),
            ) -> int:
        """
            Adiciona um item ao menu com um tooltip.

            :param name: Nome do elemento no menu.
            :param tooltip: Texto do tooltip exibido no menu.
            :param cmd: Função a ser chamada ao clicar no item.
            :param submenu: Um item do menu, Arquivo, Sobre, etc.
            :return: Índice do item adicionado no menu.
        """
        return self._add_item_menu(
            name, submenu, tooltip=tooltip, cmd=cmd
        )

    def set_theme_menu_bar(self, new: EnumStyles):
        """
        Alterar o tema da barra superior
        """
        if new == EnumStyles.TOPBAR_LIGHT:
            bg_color = "white"
            fg_color = "black"
            active_bg_color = "lightgray"
            active_fg_color = "black"
        elif new == EnumStyles.TOPBAR_PURPLE_LIGHT:
            # barra com tema roxo claro
            bg_color = "#B388EB"  # Roxo claro (tom pastel)
            fg_color = "white"  # Texto branco para contraste
            active_bg_color = "#a070d6"  # Roxo um pouco mais escuro para hover
            active_fg_color = "white"  # Texto branco também no hover
        elif new == EnumStyles.TOPBAR_PURPLE_DARK:
            # barra com tema roxo escuro
            bg_color = "#6247AA"  # Roxo escuro profundo
            fg_color = "white"  # Texto branco para alto contraste
            active_bg_color = "#503990"  # Tom mais fechado para o hover
            active_fg_color = "white"
        elif new == EnumStyles.TOPBAR_DARK:
            bg_color = "gray15"
            fg_color = "white"
            active_bg_color = "gray30"
            active_fg_color = "white"
        else:
            print(f'{__class__.__name__} Tema não alterado | {print(new)} |')
            return

        self.myapp.get_styles_mapping().set_style_menu_bar(new)
        self.master_menu_bar.config(
            bg=bg_color,
            fg=fg_color,
            activebackground=active_bg_color,
            activeforeground=active_fg_color
        )

    def update_theme_frames(self, new: EnumStyles):
        self.myapp.get_styles_mapping().set_style_frames(new)
        self.myapp.send_notify_listeners(self._message_top_bar)

    def set_theme_buttons(self, new: EnumStyles):
        self.myapp.get_styles_mapping().set_style_buttons(new)
        self.myapp.send_notify_listeners(self._message_top_bar)

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
