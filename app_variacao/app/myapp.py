from app_variacao.app.ui import (
    MyApp, MessageNotification, EnumMessages, MappingStyles
)
from app_variacao.app.view import PageVariacao, HomePage, MenuBar
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

        # Alterar os temas dos widgets conforme as configurações.
        map_styles = self.controller_prefs.get_user_prefs().get_app_styles()
        msg = MessageNotification(
            message_type=EnumMessages.MSG_UPDATE_STYLE,
            provider=map_styles,
        )
        for key_style in MappingStyles.styles_keys:
            map_styles.set_last_update(key_style)
            self.send_notify_listeners(msg)

    def save_configs(self) -> None:
        self.controller_prefs.save_config()
        print(f'Salvando configurações em: {self.controller_prefs.get_file_config().absolute()}')

    def exit_app(self):
        self.save_configs()
        super().exit_app()

