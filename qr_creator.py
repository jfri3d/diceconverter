import json
import os

import click
import qrcode


@click.command()
@click.argument('input_data', type=click.Path(exists=True, dir_okay=False))
@click.argument('out_dir', type=click.Path(exists=False, dir_okay=True))
def qr_creator(input_data, out_dir):
    """
    Simple function to split input GeoJSON into multiple files based on specific key (and possible filtering)

    Args:
        input_data: input json file with structure as <out_file>:{"data":<data>, "color":<color>}
        out_dir: output directory for saving qr codes as *.png files

    Returns:
        *.png files based on input_data and out_dir

    """

    # directory housekeeping
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # load json input data
    with open(input_data, 'r') as fp:
        base = json.load(fp)

    # iterate through base
    for key in base:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )

        # add data
        qr.add_data(base[key]["data"])

        # save QR code
        col = base[key]["color"]
        img = qr.make_image(fill_color=col, back_color="white")
        img.save(os.path.join(out_dir, '{}.png'.format(key)))


if __name__ == "__main__":
    qr_creator()
