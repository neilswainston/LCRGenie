# LCRGenie
Ligase Chain Reaction

## Install
```bash
conda install -c conda-forge lcr_genie
```

## Run
```bash
python -m lcr_genie <input_file> <output_file> [--melting_temp TEMP]
```
where:
* **input** is the path to an .xml SBOL file containing constructs designs and sequences
* **output** is the path to the output spreadsheet
* **melting_temp** is the target melting temperature for the bridging oligos

## Example
```bash
python -m lcr_genie tests/data/input/example.xml out.xlsx --melting_temp 60.0
```
