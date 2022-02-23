from pkg_resources import resource_string
from os.path import join
from time import time

from ocrd import Processor
from ocrd_models.ocrd_page import to_xml
from ocrd_utils import (
    getLogger,
    assert_file_grp_cardinality,
    make_file_id,
    MIME_TO_EXT,
    MIMETYPE_PAGE,
    parse_json_string_with_comments
)
from ocrd_modelfactory import page_from_file

from .runner import run_eval_backend
from .config import OcrmultievalConfig
from .report import EvalReport

OCRD_TOOL = parse_json_string_with_comments(resource_string(__name__, 'ocrd-tool.json').decode('utf8'))

class OcrMultiEvalProcessor(Processor):
    """
    Eval processor
    """

    def __init__(self, *args, **kwargs):
        kwargs['ocrd_tool'] = OCRD_TOOL['tools']['ocrd-ocrmultieval']
        kwargs['version'] = OCRD_TOOL['version']
        super(OcrMultiEvalProcessor, self).__init__(*args, **kwargs)


    def process(self):
        LOG = getLogger('ocrd-ocrmultieval')
        assert_file_grp_cardinality(self.input_file_grp, 2)
        assert_file_grp_cardinality(self.output_file_grp, 1)
        output_format = self.parameter['format']
        backend = self.parameter['backend']
        ext = '.json' if output_format == 'json' else '.csv'
        config = OcrmultievalConfig(self.parameter.get('config', None))
        for gt_file, ocr_file in self.zip_input_files():
            if not gt_file or not ocr_file:
                LOG.warning(f"Missing either GT or OCR for this page: gt={gt_file} ocr={ocr_file}")
                continue

            gt_file = self.workspace.download_file(gt_file)
            ocr_file = self.workspace.download_file(ocr_file)

            pageId = gt_file.pageId
            file_id = make_file_id(ocr_file, self.output_file_grp)
            local_filename = join(self.output_file_grp, file_id + ext)

            LOG.info("Running backend %s on %s" % (backend, pageId))
            t0 = time()
            try:
                report = run_eval_backend(config, backend, gt_file.mimetype, gt_file.url, ocr_file.mimetype, ocr_file.url, pageId)
            except ValueError:
                report = EvalReport(backend, gt_file.url, ocr_file.url, pageId)
            elapsed = time() - t0
            LOG.info("Took %s s (Result: %s)" % (elapsed, report.metrics))
            report.set('runtime', elapsed)

            self.workspace.add_file(
                ID=file_id,
                file_grp=self.output_file_grp,
                pageId=pageId,
                mimetype='appplication/json' if output_format == 'json' else 'text/csv',
                local_filename=local_filename,
                content=report.to_json if output_format == 'json' else report.to_csv)
