from pathlib import Path
from doorbell.app import App
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve


current_dir=Path().absolute()
print(current_dir)
assets = current_dir / "doorbell" / "assets"
print(assets)
t = App(assets=assets)
app = t.serve()

config = Config.from_toml(current_dir/ "hyper.toml")
# config
asyncio.run(serve(app, config))