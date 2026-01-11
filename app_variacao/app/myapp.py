from app_variacao.app.ui import (
    MyApp, MessageNotification, EnumMessages, ConfigMappingStyles
)
from app_variacao.app.view import PageVariacao, HomePage, MenuBar
from app_variacao.app.controllers.controller_main_app import ControllerMainApp


class AppVariacao(MyApp):

    def __init__(self, controller: ControllerMainApp):
        super().__init__(controller)

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
        map_styles: ConfigMappingStyles = self._controller.get_conf_styles()
        msg = MessageNotification(
            message_type=EnumMessages.STYLE_UPDATE,
            provider=map_styles,
        )
        self.send_notify_listeners(msg)

    def exit_app(self):
        self.save_configs()
        super().exit_app()

