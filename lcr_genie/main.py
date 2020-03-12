'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  Zulko
@author:  neilswainston
'''
import sys

from lcr_genie import io_utils, lcr, sbol_utils


def main(args):
    '''main method.'''

    # Parse SBOL:
    part_seqs, construct_parts, construct_seqs = sbol_utils.parse(path=args[0])

    # Get bridging oligos:
    construct_oligos, oligo_seqs = \
        lcr.run(construct_parts, part_seqs, float(args[2]))

    # Write:
    io_utils.write(
        part_seqs=part_seqs,
        construct_parts=construct_parts,
        construct_seqs=construct_seqs,
        oligo_seqs=oligo_seqs,
        construct_oligos=construct_oligos,
        out_filename=args[1],
    )


if __name__ == "__main__":
    main(sys.argv[1:])
