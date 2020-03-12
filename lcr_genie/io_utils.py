'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  Zulko
@author:  neilswainston
'''
# pylint: disable=abstract-class-instantiated
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import pandas as pd

FILEPATH = 'output.xlsx'


def write(
    quotes,
    primer_seqs,
    fragment_quotes,
    errors,
    part_seqs,
    construct_parts,
    construct_seqs,
    target='output.xlsx',
):
    '''Write the result of DNA construction plan computations as a spreadsheet.

    Parameters
    ----------

    quotes, primer_seqs, fragments_quotes, errors
      Output of ``compute_all_construct_quotes()`` (see docs of this method)

    part_seqs, construct_parts, construct_seqs
      Output of ``get_assembly_plan_from_sbol()`` (cf that method's doc)

    target
      Path to the output file
    '''

    # WRITE THE CONSTRUCTS PARTS SPREADSHEET

    writer = pd.ExcelWriter(target)

    parts_per_construct = [
        (name, ' + '.join(parts)) for name, parts in construct_parts.items()
    ]

    _to_spreadsheet(
        writer,
        'construct_parts',
        ['construct', 'parts'],
        parts_per_construct
    )

    # WRITE THE CONSTRUCT SEQUENCES SPREADSHEET

    _to_spreadsheet(
        writer,
        'construct_seqs',
        ['construct', 'sequence'],
        construct_seqs.items(),
    )

    # WRITE THE PRIMERS SEQUENCES SPREADSHEET

    _to_spreadsheet(
        writer,
        'primer_seqs',
        ['primer', 'sequence'],
        sorted(primer_seqs.items()),
    )

    # WRITE THE PARTS SEQUENCES SPREADSHEET

    _to_spreadsheet(
        writer,
        'part_seqs',
        ['part', 'sequence'],
        sorted(part_seqs.items())
    )

    # WRITE THE PCR_EXTENSIONS SPREADSHEET

    fragments_list = [
        (
            fragment,
            quote.metadata['subject'],
            ' + '.join(_quote_components_ids(quote)),
            quote.seq,
        )
        for fragment, quote in fragment_quotes.items()
    ]

    _to_spreadsheet(
        writer,
        'fragment_extensions',
        ['fragment_id', 'part', 'primers', 'fragment_sequence'],
        fragments_list,
    )

    # WRITE THE ASSEMBLY PLAN SPREADSHEET

    assembly_plan = [
        (construct,
         quote.source.name,
         ' + '.join(_quote_components_ids(quote)))
        for construct, quote in quotes.items()
    ]

    _to_spreadsheet(
        writer,
        'assembly_plan',
        ['construct', 'method', 'fragments'],
        assembly_plan,
    )

    # WRITE THE ERRORED CONSTRUCTS SPREADSHEET
    _to_spreadsheet(
        writer,
        'errors',
        ['construct', 'error'],
        list(errors.items()))

    writer.close()


def _to_spreadsheet(writer, sheet_name, column_names, lst):
    '''Writes the provided list as a sheet of an Excel spreadsheet.'''
    records = [dict(zip(column_names, row)) for row in lst]

    df = pd.DataFrame.from_records(
        records,
        index=column_names[0],
        columns=column_names
    )

    df.to_excel(writer, sheet_name=sheet_name)


def _quote_components_ids(quote):
    '''Return the list of ids of all fragments or primers in a quote.'''
    return [
        _subquote_to_id(subquote)
        for subquote in quote.assembly_plan.values()
    ]


def _subquote_to_id(subquote):
    'Return the ID of either the quote or the re-used seq'
    if subquote.source.operation_type == 'library':
        return subquote.metadata['part_name']

    return subquote.id
