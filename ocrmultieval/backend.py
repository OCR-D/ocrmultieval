from .report import EvalReport

class EvalBackend():
    """
    Base class for evaluation backends
    """

    @property
    def supported_mediatypes(self):
        """
        List of supported media types as input for this evaluator
        """
        raise NotImplementedError("Must override supported_mediatypes")

    def is_installed(self):
        """
        Whether any external dependencies of this evaluator are met
        """
        return True

    def compare_files(self, gt_mediatype, gt_file, ocr_mediatype, ocr_file, pageId):
        """
        Run the evaluation
        """
        raise NotImplementedError("Must override compare_files")

    def make_report(self, gt_file, ocr_file, pageId, **kwargs):
        """
        Generate a report from the results with every kwarg one measure to record
        """
        report = EvalReport(self.__class__.__name__, gt_file, ocr_file, pageId)
        for k, v in kwargs.items():
            report.set(k, v)
        return report
