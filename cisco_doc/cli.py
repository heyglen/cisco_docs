
import click

from cisco_doc.cisco_doc import Docs

CONTEXT_SETTINGS = dict(
    help_option_names=['-h'],
)

commands = click.Group('cisco_doc', context_settings=CONTEXT_SETTINGS, no_args_is_help=True)


@commands.command()
@click.pass_context
def main(ctx):
    Docs.download()