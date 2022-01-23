import sys

from click import command, option, argument, group, pass_context, pass_obj, Choice, Path as ClickPath

from .runner import BACKENDS, run_eval_backend, load_config

@group()
@option('-C', '--config', help="Configuration file, overrides default")
@pass_context
def cli(ctx, config):
    ctx.obj = load_config(config)

@cli.command('compare')
@argument('backend', type=Choice(BACKENDS.keys()))
@option('--gt-mediatype')
@argument('gt_file', type=ClickPath())
@option('--ocr-mediatype')
@argument('ocr_file', type=ClickPath())
@option('--format', type=Choice(['csv', 'json']), default='json')
@option('--pageId', '-g', help="pageId to uniquely identify pages in a work", default='P0000')
@pass_obj
def compare(config, backend, gt_mediatype, gt_file, ocr_mediatype, ocr_file, format, pageid):
    report = run_eval_backend(config, backend, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageid)
    if not report:
        sys.exit(1)
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
    cli() # pylint: disable=no-value-for-parameter
