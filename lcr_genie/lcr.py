'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
from Bio.SeqUtils.MeltingTemp import Tm_NN


NA = 'NA'
K = 'K'
TRIS = 'TRIS'
MG = 'MG'
DNTP = 'DNTP'

__DEFAULT_REAG_CONC = {NA: 0.05, K: 0, TRIS: 0, MG: 0.01, DNTP: 0}


def run(construct_parts, part_seqs, target_tm, circular=True):
    '''Designs bridging oligos for LCR.'''
    seq_oligo = {}
    construct_oligos = {}

    for construct, part_ids in construct_parts.items():
        ordered_parts_ids = part_ids + [part_ids[0]] if circular else part_ids
        ordered_parts_seqs = [part_seqs[part] for part in ordered_parts_ids]

        oligos = [_get_oligo(pair, target_tm, seq_oligo)
                  for pair in _pairwise(ordered_parts_seqs)]

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
    seq, _ = _get_seq_by_melt_temp(part_seq, target_tm, forward, tol=tol)
    return seq


def _get_melting_temp(dna1, dna2=None, reag_concs=None, strict=True):
    '''Calculates melting temperarure of DNA sequence against its
    complement, or against second DNA sequence using Nearest-Neighbour
    method.'''
    assert len(dna1) > 1

    reagent_concs = __DEFAULT_REAG_CONC

    if reag_concs is not None:
        reagent_concs.update(reag_concs)

    reagent_conc = {k: v * 1000 for k, v in reagent_concs.items()}
    dnac1 = 30

    return Tm_NN(dna1, check=True, strict=strict, c_seq=dna2, shift=0,
                 Na=reagent_conc[NA], K=reagent_conc[K],
                 Tris=reagent_conc[TRIS], Mg=reagent_conc[MG],
                 dNTPs=reagent_conc[DNTP],
                 dnac1=dnac1, dnac2=dnac1, selfcomp=dna2 is None,
                 saltcorr=7)


def _get_seq_by_melt_temp(seq, target_melt_temp, forward=True,
                          terminii=None,
                          reagent_concs=None,
                          tol=0.025):
    '''Returns a subsequence close to desired melting temperature.'''
    if terminii is None:
        terminii = ['A', 'C', 'G', 'T']
    else:
        terminii = [term.upper() for term in terminii]

    best_delta_tm = float('inf')
    best_subseq = ''
    best_melt_temp = float('NaN')
    in_tol = False

    for i in range(3, len(seq)):
        subseq = seq[:(i + 1)] if forward else seq[-(i + 1):]
        melt_temp = _get_melting_temp(subseq, None, reagent_concs)

        if subseq[-1 if forward else 0].upper() in terminii:
            delta_tm = abs(melt_temp - target_melt_temp)

            if delta_tm / target_melt_temp < tol:
                in_tol = True

                if delta_tm < best_delta_tm:
                    best_delta_tm = delta_tm
                    best_subseq = subseq
                    best_melt_temp = melt_temp
            elif in_tol:
                break

    if in_tol:
        return best_subseq, best_melt_temp

    raise ValueError('Unable to get sequence of required melting temperature')


def _pairwise(iterable):
    '''s -> (s0,s1), (s1,s2), (s2, s3), ...'''
    return [(iterable[i], iterable[i + 1]) for i in range(len(iterable) - 1)]
