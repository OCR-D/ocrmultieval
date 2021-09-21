from click import command
from ocrd import Processor
from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor

from .ocrd_processor import OcrMultiEvalProcessor

@command()
@ocrd_cli_options
def cli(*args, **kwargs):
    return ocrd_cli_wrap_processor(OcrMultiEvalProcessor, *args, **kwargs)

if __name__ == "__main__":
    cli()
