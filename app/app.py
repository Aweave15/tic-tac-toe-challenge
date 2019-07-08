from core.app_config import create_app


if __name__ == '__main__':
    app = create_app(testing=True)
    # for dev purposes, use WSGI server for non-dev server
    app.run(host='0.0.0.0')
