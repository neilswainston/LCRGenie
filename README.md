# LCRGenie
LCRGenie

To run, call:

`python test_input.xml output.xlsx 60.0`

Alternatively, use Docker as follows:

1. From the Terminal, input `bash docker_build.sh` to build the Docker image.
2. Upon building the image, input `bash docker_run.sh` to run the built image. Parameters are specified within the `docker_run.sh` file. Specifically, these are:
    * `/test_input.xml` The input file.
    * `/output.xlsx` The output file.
    * `60.0` The target melting temperature for the bridging oligos.
