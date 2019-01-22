import os

import click
import numpy as np
from PIL import Image, ImageOps


def build_mosaic(img, qr_dict, qr_size):
    """
    Function for building mosaic + inserting QR codes

    Args:
        img: PIL.Image object (raw)
        qr_dict: dictionary containing input QR codes
        qr_size: size for "inserting" QR codes

    Returns:
        out: PIL.Image object (rendered mosaic)

    """

    # convert images to grayscale
    img = img.convert('L')
    img = ImageOps.autocontrast(img)

    # images new output size
    out_size = (qr_size * img.size[0], qr_size * img.size[1])

    # cast to numpy.array for binning
    # transposition to reverse automatic transposition by conversion
    img = np.array(img)

    # binning into six bins in interval [0,256]
    levels = len(qr_dict) + 1
    digitized = levels - np.digitize(img.flatten(), np.linspace(0, 257, levels))
    digitized = digitized.reshape(img.shape)

    # create new images object (grayscale)
    out = Image.new('L', out_size)

    # insert die-pictures to represent pixels
    for x in range(0, out_size[1] - qr_size, qr_size):
        for y in range(0, out_size[0] - qr_size, qr_size):
            out.paste(qr_dict[digitized[int(x / qr_size), int(y / qr_size)]], (y, x))

    return out


@click.command()
@click.argument('image_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('qr_dir', type=click.Path(exists=True, dir_okay=True))
@click.argument('out_file', type=click.Path(exists=False, dir_okay=False))
@click.option('--qr_size', type=int, default=300,
              help="size of each qr code within mosaic")
@click.option('--im_rescale', type=float, default=0.1,
              help="factor for rescaling input images")
def qr_mosaic(image_file, qr_dir, out_file, qr_size=100, im_rescale=1.0):
    """
    Function for building mosaic images from QR codes

    Args:
        image_file: input images
        qr_dir: directory containing QR codes
        out_file: output images
        qr_size: size of QR codes within mosaid
        im_rescale: rescaling of images

    Returns:
        mosaic images based on <image_file>_mosaic.png

    """

    # open images
    img = Image.open(image_file)

    # resize images according to scaling factor provided
    scaled_img = (int(im_rescale * img.size[0]),
                  int(im_rescale * img.size[1]))
    img = img.resize(scaled_img)

    # load qr codes (input for mosaic)
    qr_files = [os.path.join(qr_dir, q) for q in os.listdir(qr_dir) if q.endswith(".png")]
    qr_dict = {num+1: Image.open(q).resize((qr_size, qr_size)) for num, q in enumerate(qr_files)}

    # build mosaic from input images
    img = build_mosaic(img, qr_dict, qr_size)

    # directory housekeeping
    out_path, _ = os.path.split(out_file)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # save
    img.save(out_file)


if __name__ == "__main__":
    qr_mosaic()
