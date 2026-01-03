from app_variacao.app.ui.core import (
    MyApp, MappingStyles, MessageNotification
)
from app_variacao.app.ui.core.core_types import EnumMessages
from app_variacao.app.view import PageVariacao, HomePage
from app_variacao.app.view.menu_bar import MenuBar
from app_variacao.app.controllers import ControllerPrefs


class AppVariacao(MyApp):

    def __init__(self):
        super().__init__()
        self.controller_prefs = ControllerPrefs()
        self.main_page = HomePage(
            self.get_window(), go_page=self.get_navigator().push
        )
        self.main_page.set_page_name('HOME')
        self.main_page.set_page_route('/home')
        self.add_page(self.main_page)

        self.add_page(
            PageVariacao(self.get_window(), go_page=self.get_navigator().push)
        )
        self.menu_bar = MenuBar(app=self)

        if 'app_styles' in self.controller_prefs.get_prefs().keys():
            final: dict = MappingStyles.format_dict(
                self.controller_prefs.get_prefs()['app_styles'],
            )
            for key, value in final.items():
                self.controller_prefs.get_prefs()[key] = value

            self.get_themes_mapping()['last_update'] = 'frames'
            msg = MessageNotification(
                message_type=EnumMessages.MSG_UPDATE_STYLE,
                provider=self.get_themes_mapping(),
            )
            self.send_notify_listeners(msg)

    def save_configs(self) -> None:
        _theme_prefs: MappingStyles = self.get_themes_mapping()
        self.controller_prefs.get_prefs()['app_styles'] = _theme_prefs.to_dict()
        self.controller_prefs.save_config()
        print(f'Salvando configurações em: {self.controller_prefs.get_file_config().absolute()}')

    def exit_app(self):
        self.save_configs()
        super().exit_app()

