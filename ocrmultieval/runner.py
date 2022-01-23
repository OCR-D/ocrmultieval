from pathlib import Path
from pkg_resources import resource_filename

from ocrd_utils import EXT_TO_MIME
from yaml import safe_load, safe_dump

from .backends.dinglehopper import DinglehopperEvalBackend
from .backends.ocrevalUAtion import OcrevalUAtionEvalBackend
from .backends.PrimaTextEval import PrimaTextEvalBackend
from .backends.CorAsvAnnEval import CorAsvAnnEvalBackend
from .backends.OcrdSegmentEvaluate import OcrdSegmentEvaluateBackend

BACKENDS = {
    'dinglehopper': DinglehopperEvalBackend,
    'ocrevalUAtion': OcrevalUAtionEvalBackend,
    'PrimaTextEval': PrimaTextEvalBackend,
    'CorAsvAnnEval': CorAsvAnnEvalBackend,
    'OcrdSegmentEvaluate': OcrdSegmentEvaluateBackend,
}

def guess_mediatype(fname, option_):
    try:
        return EXT_TO_MIME[Path(fname).suffix]
    except KeyError:
        raise ValueError("Cannot guess mimetype from extension '%s' for '%s'. Set %s explicitly" % (Path(fname).suffix, fname, option_))


def run_eval_backend(config, backend, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
    evaluator_config = config['backends_config'][backend] if backend in config['backends_config'] else {}
    evaluator = BACKENDS[backend](**evaluator_config)

    if not evaluator.is_installed():
        print('Backend %s requires installation:' % backend)
        print(evaluator.is_installed.__doc__)
        return

    gt_mediatype = gt_mediatype if gt_mediatype else guess_mediatype(gt_file, '--gt-mediatype')
    if gt_mediatype not in evaluator.supported_mediatypes:
        raise ValueError('--gt-mediatype %s not supported by %s backend, must be one of %s' % (gt_mediatype, backend, evaluator.supported_mediatypes))

    ocr_mediatype = ocr_mediatype if ocr_mediatype else guess_mediatype(ocr_file, '--ocr-mediatype')
    if ocr_mediatype not in evaluator.supported_mediatypes:
        raise ValueError('--ocr-mediatype %s not supported by %s backend, must be one of %s' % (ocr_mediatype, backend, evaluator.supported_mediatypes))

    return evaluator.compare_files(gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId)

def load_config(config):
    with open(config if config else resource_filename(__name__, 'default_config.yml'), 'r') as f:
        return safe_load(f)

