from pathlib import Path
from doorbell.const import BELL_WAV, ASSETS, Size

def get_images(sub: str):
    # IMAGES = "familie"
    images_dir = ASSETS / sub
    print(f"looking for images in: {images_dir}")
    image_list = list(images_dir.glob("*.png"))
    ret = [f"{sub}/{img.name}" for img in image_list]
    return ret