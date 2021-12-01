'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  Zulko
@author:  neilswainston
'''
import sys
from lcr_genie import io_utils, lcr, sbol_utils
from .Args import build_args_parser


def entry_point():
    '''main method.'''

    # PARSE THE COMMAN LINE PARAMETERS
    parser = build_args_parser(
        prog = 'lcr_genie',
        description='Ligase chain reaction'
    )
    args = parser.parse_args()

    # Parse SBOL:
    part_seqs, construct_parts, construct_seqs = sbol_utils.parse(path=args.input)

    # Get bridging oligos:
    construct_oligos, oligo_seqs = \
        lcr.run(construct_parts, part_seqs, float(args.melting_temp))

    # Write:
    io_utils.write(
        part_seqs=part_seqs,
        construct_parts=construct_parts,
        construct_seqs=construct_seqs,
        oligo_seqs=oligo_seqs,
        construct_oligos=construct_oligos,
        out_filename=args.output,
    )

if __name__ == '__main__':
    entry_point()
