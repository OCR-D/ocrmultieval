from .report import EvalReport

class EvalBackend():

    @property
    def supported_mediatypes(self):
        raise NotImplementedError("Must override supported_mediatypes")

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
        raise NotImplementedError("Must override compare_files")

    def make_report(self, gt_file, ocr_file, pageId, **kwargs):
        report = EvalReport(self.__class__.__name__, gt_file, ocr_file, pageId)
        for k, v in kwargs.items():
            report.set(k, v)
        return report
