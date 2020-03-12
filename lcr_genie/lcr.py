'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=invalid-name
from synbiochem.utils import pairwise
from synbiochem.utils.seq_utils import get_seq_by_melt_temp


def run(construct_parts, part_seqs, target_tm, circular=True):
    '''Designs bridging oligos for LCR.'''
    seq_oligo = {}
    construct_oligos = {}

    for construct, part_ids in construct_parts.items():
        ordered_parts_ids = part_ids + [part_ids[0]] if circular else part_ids
        ordered_parts_seqs = [part_seqs[part] for part in ordered_parts_ids]

        oligos = [_get_oligo(pair, target_tm, seq_oligo)
                  for pair in pairwise(ordered_parts_seqs)]

        construct_oligos[construct] = oligos

    oligo_seqs = {v: k for k, v in seq_oligo.items()}

    return construct_oligos, oligo_seqs


def _get_oligo(pair, target_tm, seq_oligo):
    '''Gets a bridging oligo from a pair of Part sequences.'''
    seq = ''.join([_get_oligo_branch(pair[0], target_tm, False),
                   _get_oligo_branch(pair[1], target_tm)])

    if seq not in seq_oligo:
        seq_oligo[seq] = 'oligo_%i' % len(seq_oligo)

    return seq_oligo[seq]


def _get_oligo_branch(part_seq, target_tm, forward=True, tol=0.05):
    '''Gets bridging oligo branch from Part sequence.'''
    seq, _ = get_seq_by_melt_temp(part_seq, target_tm, forward, tol=tol)
    return seq
