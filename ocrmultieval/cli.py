from csv import DictReader, DictWriter
from click import command, option, argument, group, pass_context, pass_obj, Choice, Path as ClickPath

from .runner import BACKENDS, run_eval_backend, load_config

@group()
@option('-C', '--config', help="Configuration file, overrides default")
@pass_context
def cli(ctx, config):
    ctx_obj = load_config(config)

@cli.command('compare')
@argument('backend', type=Choice(BACKENDS.keys()))
@option('--gt-mediatype')
@argument('gt_file', type=ClickPath())
@option('--ocr-mediatype')
@argument('ocr_file', type=ClickPath())
@option('--format', type=Choice(['csv', 'json']), default='json')
@pass_obj
def compare(config, backend, gt_mediatype, gt_file, ocr_mediatype, ocr_file, format):
    config = load_config(config)
    report = run_eval_backend(config, backend, gt_mediatype, gt_file, ocr_mediatype, ocr_file)
    print(getattr(report, 'to_%s' % format))

@cli.command('import-layouteval')
@option('--add-to-workspace/--no-add-to-workspace', help="Whether to register with workspace", default=True)
@argument('output_folder')
@argument('prima_csv_files', nargs=-1)
@pass_obj
def import_layouteval(config, output_folder, prima_csv_files):
    for prima_csv_file in prima_csv_files:
        print(prima_csv_file)


if __name__ == "__main__":
    cli()
