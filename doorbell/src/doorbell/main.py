from doorbell.app import App
import asyncio

app = App()

# ft.app(target=main, assets_dir=ASSETS)

if __name__ == "__main__":
    asyncio.run(app.deploy())