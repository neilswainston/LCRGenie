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


def write(
        part_seqs,
        construct_parts,
        construct_seqs,
        oligo_seqs,
        construct_oligos,
        out_filename='output.xlsx'):
    '''Write the result of DNA construction plan as a spreadsheet.'''
    writer = pd.ExcelWriter(out_filename)

    # construct_parts:
    parts_per_construct = [
        (name, ' + '.join(parts)) for name, parts in construct_parts.items()
    ]

    _to_spreadsheet(
        writer,
        'construct_parts',
        ['construct', 'parts'],
        parts_per_construct
    )

    # construct_sequences:
    _to_spreadsheet(
        writer,
        'construct_sequences',
        ['construct', 'sequence'],
        construct_seqs.items(),
    )

    # oligo_sequences:
    _to_spreadsheet(
        writer,
        'oligo_sequences',
        ['oligo', 'sequence'],
        sorted(oligo_seqs.items()),
    )

    # part_sequences:
    _to_spreadsheet(
        writer,
        'part_sequences',
        ['part', 'sequence'],
        sorted(part_seqs.items())
    )

    # assembly_plan:
    assembly_plan = [
        (construct,
         'lcr',
         ' + '.join(construct_parts[construct] + oligos))
        for construct, oligos in construct_oligos.items()
    ]

    _to_spreadsheet(
        writer,
        'assembly_plan',
        ['construct', 'method', 'fragments'],
        assembly_plan,
    )

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
