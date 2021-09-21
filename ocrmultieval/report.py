from json import dumps
from csv import DictWriter
from io import StringIO

from .constants import FIELDNAMES

class EvalReport():

    def __init__(self, backend, gt_file, ocr_file):
        self.backend = backend
        self.gt_file = gt_file
        self.ocr_file = ocr_file
        self.measures = {}

    def set(self, measure, value):
        self.measures[measure] = value

    @property
    def to_obj(self):
        return {
            'backend': self.backend,
            'gt_file': self.gt_file,
            'ocr_file': self.ocr_file,
            **self.measures
        }

    @property
    def to_json(self):
        return dumps(self.to_obj)

    @property
    def to_csv(self):
        f = StringIO()
        writer = DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerow(self.to_obj)
        return f.getvalue()


