import logging
from io import StringIO
from json import loads
from subprocess import run, PIPE

from ..backend import EvalBackend

class CorAsvAnnCompareBackend(EvalBackend):

    def __init__(self, **kwargs):
        self.normalization = kwargs['normalization']
        self.metrics = kwargs['metrics']
        self.gt_level = kwargs['gt_level']

    @property
    def supported_mediatypes(self):
        return ['application/vnd.prima.page+xml', 'text/plain']

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
        result = run([
            'cor-asv-ann-compare',
            '--normalization', self.normalization,
            '--gt-level', str(self.gt_level),
            gt_file, ocr_file
        ], stdout=PIPE, encoding='utf-8', check=False)
        result_json = loads(result.stdout)
        scores = {}
        key = '%s,%s' % (gt_file, ocr_file)
        if 'WER' in self.metrics:
            scores['WER'] = result_json[key]['word-error-rate-mean']
        if 'CER' in self.metrics:
            scores['CER'] = result_json[key]['char-error-rate-mean']
        return self.make_report(gt_file, ocr_file, pageId, **scores)
