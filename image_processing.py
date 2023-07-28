import os
import glob
from pathlib import Path
import numpy as np
import rasterio
from matplotlib import pyplot as plt


def load_image_bands(image_folder: str, bands: list, pattern_str: str, file_ext: str = "TIF") -> dict:
    """
    Function fot loading the individual bands of a raster.
    :param image_folder:
    :param bands:
    :param pattern_str:
    :param file_ext:
    :return: dict
    """
    band_dict = {}
    path = Path(image_folder)
    for band in bands:
        file = next(path.glob(f"{pattern_str}{band}.{file_ext}"))
        dataset = rasterio.open(file)
        band_dict.update({band: dataset.read(1)})
        dataset.close()

    return band_dict


def display_rgb(bands, red_channel, green_channel, blue_channel):
    rgb = np.stack([bands[red_channel], bands[green_channel], bands[blue_channel]], axis=-1)
    rgb = rgb / rgb.max()


def stack_bands(image_path: str, image_folder: str, file_pattern: str, output_raster: str, metadata: dict, sort=True):
    os.chdir(image_path)

    files = glob.glob(f"{image_folder}/{file_pattern}")

    if sort:
        files.sort()
    else:
        files.sort(reverse=True)

    with rasterio.open(output_raster, "w", metadata) as output:
        for index, filepath in enumerate(files, start=1):
            source = rasterio.open(filepath)
            output.write(source.read(1), index)
            source.close()
        


stack_bands("C:\\Users\\orden\\Desktop\\Teledeteccion_QGIS\\ImagenesLandsat",
            "LT05_L1TP_229092_19860116_20200918_02_T1", "*_B*.TIF")
