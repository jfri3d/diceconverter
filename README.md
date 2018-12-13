# Building QR mosaic

This work is based on https://github.com/almaan/diceconverter but adapted for QR codes and splitting the resulting *massive* image.

## Workflow

This requires an input json file with QR data/configs. The mosaic is built as follows:

- run `qr_creator.py` with an input json file
    - an example is as follows:
    
            {
               "<name>":{
                  "data":"<url or string>",
                  "color":"black"
               },
               "<another_name>":{
                  "data":"<url or string>",
                  "color":"red"
               }
            }

- run `qr_mosaic.py` to create the mosaic with created QR codes (i.e. images)

- run `image_splitter.py` to create printable image "chunks" (i.e. tiled mosaic image)