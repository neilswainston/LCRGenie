import os
import pandas
from lcr_genie import io_utils, lcr, sbol_utils

this_directory = os.path.dirname(os.path.realpath(__file__))

def get_sheet_length(filepath, sheet_name):
    return len(pandas.read_excel(filepath, sheet_name=sheet_name))

def test_lcr_genie(tmpdir):
    input_path = os.path.join(
        this_directory,
        'data',
        'input',
        'example.xml'
    )
    output_path = os.path.join(str(tmpdir), "example.xlsx")

    # Parse SBOL:
    part_seqs, construct_parts, construct_seqs = sbol_utils.parse(path=input_path)
    # Get bridging oligos:
    construct_oligos, oligo_seqs = \
        lcr.run(construct_parts, part_seqs, 60.0)
    # Write:
    io_utils.write(
        part_seqs=part_seqs,
        construct_parts=construct_parts,
        construct_seqs=construct_seqs,
        oligo_seqs=oligo_seqs,
        construct_oligos=construct_oligos,
        out_filename=output_path,
    )

    expected = dict(oligo_sequences=15, part_sequences=94)
    for sheet_name, expected_size in expected.items():
        assert get_sheet_length(output_path, sheet_name) == expected_size
