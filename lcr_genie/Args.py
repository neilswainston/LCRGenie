from argparse  import ArgumentParser
from ._version import __version__

DEFAULT_MELTING_TEMP = 60.0

def build_args_parser(
    prog: str,
    description: str = '',
    epilog: str = ''
) -> ArgumentParser:

    parser = ArgumentParser(
        prog = prog,
        description = description,
        epilog = epilog
    )

    # Build Parser
    parser = add_arguments(parser)

    return parser

def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        'input',
        type=str,
        help='Path to an .xml SBOL file containing constructs designs and sequences'
    )
    parser.add_argument(
        'output',
        type=str,
        help='Path to the output spreadsheet'
    )
    parser.add_argument(
        '--melting_temp',
        type=float,
        default=DEFAULT_MELTING_TEMP,
        help=f'The target melting temperature for the bridging oligos (default {DEFAULT_MELTING_TEMP})'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help='show the version number and exit'
    )
    return parser
