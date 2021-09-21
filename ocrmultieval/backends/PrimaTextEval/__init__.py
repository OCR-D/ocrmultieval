from pkg_resources import resource_filename
from csv import DictReader
from pathlib import Path
from subprocess import run, PIPE

from ...backend import EvalBackend

class PrimaTextEvalBackend(EvalBackend):

    def __init__(self, **kwargs):
        # TODO re-enable this before publication
        # if 'distdir' not in kwargs:
        #     raise ValueError("Due to licensing restrictions, PRImA TextEval cannot be bundled with ocrmultieval. Please download TextEval_1.5.zip, unpack it, and set the PrimaTextEval.distdir config property to this folder path")
        # self.distdir = kwargs['distdir']
        self.distdir = resource_filename(__name__, 'dist')
        self.methods = kwargs['methods']

    @property
    def supported_mediatypes(self):
        return ['text/plain', 'application/vnd.prima.page+xml', 'application/page+alto']

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file):
        # java -jar PrimaText.jar -gt-text input\gt.txt -gt-enc UTF-8 -res-text input\res.txt -res-enc UTF-8 -method BagOfWords,CharacterAccuracy,WordAccuracy,WordStatistics -toLower ENGLISH -csv-headers -csv-addinp>output.csv
        cmd = ['java', '-jar', str(Path(self.distdir, 'PrimaText.jar')), 'eu.digitisation.Main']
        cmd += ['-gt-text', gt_file]
        cmd += ['-res-text', ocr_file]
        cmd += ['-csv-headers']
        cmd += ['-method', ','.join(self.methods)]
        result = run(cmd, stdout=PIPE, encoding='utf-8')

        result_out = result.stdout
        if not result_out:
            print("Error processing. Check the log")
            return self.make_report(gt_file, ocr_file)
        row = list(DictReader(result_out.split('\n')))[0]

        report = self.make_report(gt_file, ocr_file)
        if 'CharacterAccuracy' in self.methods:
            report.set('CER', 1 - float(row['characterAccuracy']))
        if 'WordAccuracy' in self.methods:
            report.set('WER', 1 - float(row['wordAccuracy']))
        if 'BagOfWords' in self.methods:
            report.set('BOW', 1 - float(row['wordCountSuccessRate']))
        if 'FlexCharAccuracy' in self.methods:
            report.set('FCER', 1 - float(row['flexCharacterAccuracy']))
        return report
