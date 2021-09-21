from pkg_resources import resource_filename
from subprocess import run, PIPE

from ...backend import EvalBackend

OCREVALUIATION_JAR = resource_filename(__name__, 'ocrevalUAtion-1.3.4-jar-with-dependencies.jar')

class OcrevalUAtionEvalBackend(EvalBackend):

    @property
    def supported_mediatypes(self):
        return [
            'text/plain',
            'application/vnd.prima.page+xml',
            'application/page+alto'
        ]

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file):
        cmd = ['java', '-cp', OCREVALUIATION_JAR, 'eu.digitisation.Main']
        cmd += ['-gt', gt_file]
        cmd += ['-ocr', ocr_file]
        cmd += ['-o', '/dev/stdout']
        result = run(cmd, stdout=PIPE, encoding='utf-8')

        report = self.make_report(gt_file, ocr_file)
        for line in result.stdout.split('\n'):
            line = line.strip()
            if '<td>WER</td>' in line:
                report.set('WER', float(line[16:-6].replace(',', '.')) / 100)
            elif '<td>CER</td>' in line:
                report.set('CER', float(line[16:-6].replace(',', '.')) / 100)
            elif '<td>WER (order independent)</td>' in line:
                report.set('BOW', float(line[36:-6].replace(',', '.')) / 100)
        return report
