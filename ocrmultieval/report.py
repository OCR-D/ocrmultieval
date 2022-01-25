from json import dumps
from csv import DictWriter
from io import StringIO

from yaml import safe_dump

from .constants import FIELDNAMES

class EvalReport():

    def __init__(self, backend, gt_file, ocr_file, pageId):
        self.backend = backend
        self.gt_file = gt_file
        self.ocr_file = ocr_file
        self.pageId = pageId
        self.metrics = {}

    def set(self, metric, value):
        self.metrics[metric] = value

    @property
    def to_obj(self):
        return {
            'backend': self.backend,
            'gt_file': self.gt_file,
            'ocr_file': self.ocr_file,
            'pageId': self.pageId,
            **self.metrics
        }

    @property
    def to_json(self):
        return dumps(self.to_obj)

    @property
    def to_yaml(self):
        return safe_dump(self.to_obj)

    @property
    def to_csv(self):
        f = StringIO()
        fieldnames = FIELDNAMES
        for metric in self.metrics:
            if metric not in fieldnames:
                fieldnames.append(metric)
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(self.to_obj)
        return f.getvalue()

    @property
    def to_xml(self):
        ret = ''
        for k, v in self.to_obj.items():
            ret += '    <%s>%s</%s>\n' % (k, v, k)
        return '<eval>\n%s</eval>' % ret


