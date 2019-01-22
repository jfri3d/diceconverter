import os

# RUN SETTINGS
DOCKER_RUN = "docker run --rm -v /Users:/Users -w $(pwd) pysnake:latest"

# PARAMS
GIPHY_RETURNS = 10  # number of gifs to return from giphy API call
IM_RESCALE = 0.05  # factor for rescaling input image
QR_SIZE = 100  # number of pixels for each "embedded" QR within the mosaic

# DIRECTORY SETTINGS
PWD = os.getcwd()
MSG_PASSING_DIR = os.path.join(PWD, "msg_passing")
CONFIG_DIR = os.path.join(PWD, "configs")
QR_DIR = os.path.join(PWD, "qr")
IMAGES_DIR = os.path.join(PWD, "images")
OUT_DIR = os.path.join(PWD, "mosaic")

#####################
##### WORKFLOW ######
#####################

# # SINGLE
# # ======
# IMAGES = ["Josh"]
# SEARCHES = ["happy"]

# # MULTIPLE
# # ========
# IMAGES = ["Josh"]
# SEARCHES = ["happy", "sad", "funny", "silly", "angry", "happy_birthday", "snake"]

# ALL
# ===
IMAGES = [f.split('.')[0] for f in os.listdir(IMAGES_DIR) if f.endswith('.png')]
SEARCHES = ["happy", "sad", "funny", "silly", "angry", "happy_birthday", "snake"]

rule all:
    input:
        expand(os.path.join(OUT_DIR, "{search}_{images}.png"), search=SEARCHES, images=IMAGES)

rule qr_mosaic:
    input:
        expand(os.path.join(IMAGES_DIR, "{{images}}.png")),
        expand(os.path.join(QR_DIR, "{{search}}"))
    output:
        expand(os.path.join(OUT_DIR, "{{search}}_{{images}}.png"))
    priority: 0
    threads: 1
    shell:
        "{DOCKER_RUN} python3 -m tools.qr_mosaic {input[0]} {input[1]} {output[0]} "
        "--qr_size {QR_SIZE} --im_rescale {IM_RESCALE}"

rule qr_creator:
    input:
        expand(os.path.join(CONFIG_DIR, "{{search}}.json"))
    output:
        directory(expand(os.path.join(QR_DIR, "{{search}}"))),
    priority: 0
    threads: 1
    shell:
        "{DOCKER_RUN} python3 -m tools.qr_creator {input[0]} {output[0]}"

rule get_giphy:
    output:
        expand(os.path.join(CONFIG_DIR, "{{search}}.json"))
    priority: 0
    threads: 1
    shell:
        "{DOCKER_RUN} python3 -m tools.giphy_grabber {wildcards.search} {output[0]} --max_returns {GIPHY_RETURNS}"
