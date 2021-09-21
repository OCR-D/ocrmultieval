import logging
from io import StringIO

from ..backend import EvalBackend

from ocrd_cor_asv_ann.lib.seq2seq import Sequence2Sequence

class CorAsvAnnEvalBackend(EvalBackend):

    def __init__(self, **kwargs):
        pass
        # self.fast = kwargs['fast']

    @property
    def supported_mediatypes(self):
        return ['application/vnd.prima.page+xml', 'application/page+alto']

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file):
        pass
        # TODO
        # log_stream = StringIO()
        # logging.basicConfig(stream=log_stream, level=logging.INFO)

        # s2s = Sequence2Sequence(logger=logging.getLogger(__name__), progbars=True)
        # s2s.load_config(load_model)
        # s2s.configure()
        # s2s.load_weights(load_model)
        # s2s.rejection_threshold = rejection
        
        # s2s.evaluate(data, fast, normalization, gt_level, confusion, histogram)

        # # return {'cer': cer, 'wer': wer, 'words_total': n_words, 'chars_total': n_characters}

