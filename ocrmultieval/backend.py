from .report import EvalReport

class EvalBackend():

    @property
    def supported_mediatypes(self):
        raise NotImplementedError("Must override supported_mediatypes")

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file):
        raise NotImplementedError("Must override compare_files")

    def make_report(self, gt_file, ocr_file, **kwargs):
        report = EvalReport(self.__class__.__name__, gt_file, ocr_file)
        for k, v in kwargs.items():
            report.set(k, v)
        return report
