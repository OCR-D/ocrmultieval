from pkg_resources import resource_filename
from subprocess import run, PIPE
from distutils.spawn import find_executable as which

from ..backend import EvalBackend

class IsriOcrevalBackend(EvalBackend):

    def __init__(self, **kwargs):
        self.metrics = kwargs['metrics']

    @property
    def supported_mediatypes(self):
        return ['text/plain']

    def is_installed(self):
        """
        IsriOcrevalBackend requires the tools accuracy and wordacc to be installed.

        See https://github.com/eddieantonio/ocreval for instructions
        """
        return which('accuracy') and which('wordacc')

    def _run_ocreval(self, gt_file, ocr_file, scores, metric):
        key = 'chars' if metric == 'CER' else 'words'
        cmd = 'accuracy' if metric == 'CER' else 'wordacc'
        result = run([cmd, gt_file, ocr_file], stdout=PIPE, encoding='utf-8', check=False)
        lines = [x.strip() for x in result.stdout.splitlines()]
        scores['%s_total' % key] = int(lines[2].split(' ')[0])
        scores['%s_wrong' % key] = int(lines[3].split(' ')[0])
        scores[metric] = scores['%s_wrong' % key] / max(scores['%s_total' % key], 1)
        return scores


    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
        scores = {}
        if 'CER' in self.metrics:
            self._run_ocreval(gt_file, ocr_file, scores, 'CER')
        if 'WER' in self.metrics:
            self._run_ocreval(gt_file, ocr_file, scores, 'WER')
        return self.make_report(gt_file, ocr_file, pageId, **scores)

