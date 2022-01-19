'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  Zulko
@author:  neilswainston
'''
from collections import OrderedDict
import sbol2 as sbol

_SO_PLASMID = 'http://identifiers.org/so/SO:0000155'

def id_sort(i: iter):
    """Sort a collection of SBOL objects and/or URIs by identity URI"""
    return sorted(i, key=lambda x: x.identity if isinstance(x, sbol.Identified) else x)


def parse(sbol_doc=None, path=None):
    '''Parse SBOL and extract an assembly plan.

    Parameters
    ----------

    sbol_doc
      A PySBOL Document() containing the designs and parts seqs.
      A path to a SBOL .xml file can be provided instead.

    path
      A path to a SBOL .xml file

    Returns
    -------

    (parts_seqs, parts_per_construct, constructs_seqs)
      Assembly plan data:
      - parts_seqs is of the form ``{part_id: 'ATTTGTGTGC...'}``,
      - parts_per_constructs is of the form ``{construct_id: [part_id_1,...]}``
      - constructs_seqs is of the form ``{construct_id: 'ATGCCC...'}``.
    '''
    if path is not None:
        sbol_doc = sbol.Document()
        sbol_doc.read(path)

    parts_seqs = {
        comp_def.displayId: comp_def.sequence.elements.upper()
        for comp_def in sbol_doc.componentDefinitions
        if comp_def.sequence
    }

    parts_per_construct = [
        (comp_def.displayId, [sbol_doc.getComponentDefinition(
            comp.definition).displayId
            for comp in id_sort(comp_def.components)])
        for comp_def in sbol_doc.componentDefinitions
        if _SO_PLASMID in comp_def.roles
    ]

    constructs_seqs = [
        (construct_name, ''.join([parts_seqs[part] for part in id_sort(parts)]))
        for construct_name, parts in parts_per_construct
    ]

    return parts_seqs, \
        OrderedDict(parts_per_construct), \
        OrderedDict(constructs_seqs)
