"""CUSTOM ERROR CLASSES."""


class UnsupportedFileError(Exception):
    """Raised when DICOM file is of unsupported type."""

    pass


class UnreadableFileError(UnsupportedFileError):
    """Raised when pydicom cannot read provided file."""

    pass


class DicomDirError(UnsupportedFileError):
    """Raised when target file is DICOMDIR."""

    pass


class MissingPixelDataError(UnsupportedFileError):
    """Raised when target file is missing pixel data."""

    pass


class ReportDetectedError(UnsupportedFileError):
    """Raised when target file is detected as a possible report."""

    pass


class EssentialTagMissingError(Exception):
    """Raised when original DICOM file is missing tag used in anonymization."""

    pass


class MissingStudyDateTimeError(EssentialTagMissingError):
    """Raised when DICOM file is missing StudyDateTime tag."""

    pass


class MissingStudyDateError(EssentialTagMissingError):
    """Raised when DICOM file is missing StudyDate tag."""

    pass


class MissingStudyTimeError(EssentialTagMissingError):
    """Raised when DICOM file is missing StudyTime tag."""

    pass
