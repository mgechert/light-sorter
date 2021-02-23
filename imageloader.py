import adafruit_imageload
from displayio import Bitmap, Palette
from io import BytesIO

# Modified version of adafruit_imageload.load to accept raw bytes (loaded from URL, e.g.)
# https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad/blob/master/adafruit_imageload/bmp/indexed.py


def load_from_bytes(raw_image_bytes, *, bitmap=None, palette=None):
    """Modified version of adafruit_imageload.load
    Loads a bmp image from raw bytes instead of from a file. Intended to
    allow loading an image from a URL.
    Returns tuple of bitmap object and palette object.
    :param object bitmap: Type to store bitmap data. Must have API similar to `displayio.Bitmap`.

    :param object palette: Type to store the palette. Must have API similar to
      `displayio.Palette`
    :param append_bw: Appends white 0xffffff and black 0x000000 to the palette  
      """

    if not bitmap:
        bitmap = Bitmap
    if not palette:
        palette = Palette

    image_bytes = BytesIO(raw_image_bytes)
    image_bytes.seek(10)
    data_start = int.from_bytes(image_bytes.read(4), "little")
    image_bytes.seek(0x12)  # Width of the bitmap in pixels
    width = int.from_bytes(image_bytes.read(4), "little")
    try:
        height = int.from_bytes(image_bytes.read(4), "little")
    except OverflowError as error:
        raise NotImplementedError(
            "Negative height BMP files are not supported on builds without longint"
        ) from error
    image_bytes.seek(0x1C)  # Number of bits per pixel
    color_depth = int.from_bytes(image_bytes.read(2), "little")
    image_bytes.seek(0x1E)  # Compression type
    compression = int.from_bytes(image_bytes.read(2), "little")
    image_bytes.seek(0x2E)  # Number of colors in the color palette
    colors = int.from_bytes(image_bytes.read(4), "little")

    # GIMP writes a bad compression byte; try just overriding it with 0x00
    if compression == 3:
        print('WARNING: unsupported compression; trying without')
        compression = 0

    if colors == 0 and color_depth >= 16:
        raise NotImplementedError("True color BMP unsupported")

    if compression > 2:
        raise NotImplementedError("bitmask compression unsupported")

    if colors == 0:
        colors = 2 ** color_depth
    from adafruit_imageload.bmp import indexed

    return indexed.load(
        image_bytes,
        width,
        height,
        data_start,
        colors,
        color_depth,
        compression,
        bitmap=bitmap,
        palette=palette,
    )
