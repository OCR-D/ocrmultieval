from ..backend import EvalBackend

from qurator.dinglehopper.ocr_files import extract
from qurator.dinglehopper.word_error_rate import word_error_rate_n, words_normalized
from qurator.dinglehopper.character_error_rate import character_error_rate_n

class DinglehopperEvalBackend(EvalBackend):

    def __init__(self, **kwargs):
        self.textequiv_level = kwargs['textequiv_level']

    @property
    def supported_mediatypes(self):
        return ['application/vnd.prima.page+xml', 'application/page+alto']

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
        gt_text = extract(gt_file, textequiv_level=self.textequiv_level)
        ocr_text = extract(ocr_file, textequiv_level=self.textequiv_level)

        cer, n_characters = character_error_rate_n(gt_text, ocr_text)
        wer, n_words = word_error_rate_n(gt_text, ocr_text)

        return self.make_report(gt_file, ocr_file, pageId, CER=cer, WER=wer)
