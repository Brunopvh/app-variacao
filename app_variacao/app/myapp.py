from app_variacao.app.ui.core import MyApp
from app_variacao.app.view import PageVariacao, HomePage
from app_variacao.app.view.menu_bar import MenuBar


class AppVariacao(MyApp):

    def __init__(self):
        super().__init__()

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

    def save_configs(self) -> None:
        pass


