from doorbell.app import App

app = App()
# app.serve()

# app = ft.app(target=main, assets_dir=ASSETS, export_asgi_app=True)
# uvicorn.run(app, host="0.0.0.0", port=COMMON.port, log_level="debug")
if __name__ == "__main__":
    app.serve()