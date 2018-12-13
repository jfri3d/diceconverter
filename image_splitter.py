import os

import click
import gdal


@click.command()
@click.argument('image_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('out_dir', type=click.Path(exists=False, dir_okay=True))
@click.option('--tx', type=int, default=7500,
              help="size of each chunk")
@click.option('--ty', type=int, default=10500,
              help="size of each chunk")
def image_splitter(image_file, out_dir, tx=25000, ty=25000):
    """
    Function for splitting an input raster into "chunks"

    Args:
        image_file: input image
        out_dir: directory for saving chunked image
        tx: size of chunks (in pixels)
        ty: size of chunks (in pixels)

    Returns:
        chunked image based on tx, ty

    """

    # directory housekeeping
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # load image
    ds = gdal.Open(image_file)

    # get size (for identifying number of "chunks" to create)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    # out image
    _, namer = os.path.split(image_file)
    namer, ext = os.path.splitext(namer)

    # create "chunks" of image
    for i in range(0, xsize, tx):
        for j in range(0, ysize, ty):
            print(i, j)
            out_img = os.path.join(out_dir, namer)
            src_str = "gdal_translate -of JPEG -ot Byte -srcwin {}, {}, {}, {} {} {}"
            out_img = "{}_{}_{}.tif".format(out_img, i, j)
            fmt_str = src_str.format(i, j, tx, ty, image_file, out_img)
            os.system(fmt_str)


if __name__ == "__main__":
    image_splitter()
