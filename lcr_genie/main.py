'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  Zulko
@author:  neilswainston
'''
import sys

from lcr_genie import io_utils, sbol_utils


def main(args):
    '''main method.'''

    # Parse SBOL:
    part_seqs, construct_parts, construct_seqs = sbol_utils.parse(path=args[0])

    # Get bridging oligos:
    quotes, primer_seqs, fragment_quotes, errors = {}, {}, {}, {}

    # Write:
    io_utils.write(
        quotes=quotes,
        primer_seqs=primer_seqs,
        part_seqs=part_seqs,
        fragment_quotes=fragment_quotes,
        construct_parts=construct_parts,
        construct_seqs=construct_seqs,
        errors=errors,
        target=args[1],
    )


if __name__ == "__main__":
    main(sys.argv[1:])
