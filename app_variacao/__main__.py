"""

export VIRTUAL_ENV="/mnt/dados/var/venv/user_venv"
export UV_CACHE_DIR="/mnt/dados/uv_cache"

"""

__project__ = "app_variacao"


def main():
    print(__project__)
    from app_variacao.app import run_app, AppVariacao
    app = AppVariacao()
    run_app(app)


if __name__ == '__main__':
    main()
