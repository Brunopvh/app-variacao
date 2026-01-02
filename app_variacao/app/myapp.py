from app_variacao.ui.core import MyApp
from app_variacao.app.pages import PageVariacao, HomePage
from app_variacao.app.menu_bar import MenuBar
from tkinter import ttk
from app_variacao.app.controllers import ControllerAppConfig


class AppVariacao(MyApp):

    def __init__(self):
        super().__init__()

        self.main_page = HomePage(self)
        self.main_page.set_page_name('HOME')
        self.main_page.set_page_route('/home')
        self.add_page(self.main_page)
        self.add_page(PageVariacao(self))

        self.menu_bar = MenuBar(app=self)

    def save_configs(self) -> None:
        pass


