"""

export VIRTUAL_ENV="/mnt/dados/var/venv/user_venv"
export UV_CACHE_DIR="/mnt/dados/uv_cache"

"""

__project__ = "app_variacao"


def main():
    print(__project__)
    from app_variacao.app.controllers.controller_main_app import ControllerMainApp
    from app_variacao.app import run_app, AppVariacao

    controller_main_app = ControllerMainApp()
    app = AppVariacao(controller_main_app)
    run_app(app)


if __name__ == '__main__':
    main()
