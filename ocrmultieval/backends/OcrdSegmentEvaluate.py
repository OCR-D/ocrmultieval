from ..backend import EvalBackend

from ocrd_models.ocrd_page import parse
from ocrd_segment.evaluate import evaluate_files

class OcrdSegmentEvaluateBackend(EvalBackend):

    def __init__(self, **kwargs):
        self.level = kwargs['level']
        self.typed = kwargs['typed']
        self.metrics = kwargs['metrics']
        self.selected = kwargs['selected']

    @property
    def supported_mediatypes(self):
        return ['application/vnd.prima.page+xml']

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
        pcgts = parse(ocr_file)
        bin_file = None
        for alt_img in pcgts.get_Page().get_AlternativeImage():
            if 'binarized' in alt_img.comments:
                bin_file = alt_img.filename
                break
        stats = evaluate_files([gt_file], [ocr_file], [bin_file], self.level, self.typed, self.selected)
        scores = {}
        for metric in self.metrics:
            scores[metric] = stats['scores'][metric]

        return self.make_report(gt_file, ocr_file, pageId, **scores)
