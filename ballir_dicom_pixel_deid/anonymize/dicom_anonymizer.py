"""
Tool to build blank-slate DICOM files, populate with required meta-data, and populate with randomized fields and pixel data from original DICOM file.
"""

import pydicom as dcm

from ballir_dicom_anonymizer.pixel_handling.pixel_data_writer import PixelDataWriter
from ballir_dicom_anonymizer.error_handling import (
    DicomDirError,
    MissingPixelDataError,
    ReportDetectedError,
)

import logging

log = logging.getLogger(__name__)


class DicomAnonymizer:
    """Builds fresh DICOM file and populates with anonymized data."""

    def __init__(self, output_directory: str):
        self.pixel_data_writer = PixelDataWriter()

    def check_valid_dicom(self, original_dicom_file):
        """Raise error if file type or DICOM contents are unsupported."""
        if type(original_dicom_file) == dcm.dicomdir.DicomDir:
            raise DicomDirError("DicomDirError")
        if not hasattr(original_dicom_file, "PixelData") and not hasattr(
            original_dicom_file, "pixel_array"
        ):
            raise MissingPixelDataError("MissingPixelDataError")
        if (
            "SeriesDescription" in original_dicom_file
            and "report" in original_dicom_file.SeriesDescription.lower()
        ):
            raise ReportDetectedError("ReportDetectedError")

    def read_dicom_file(self, dicom_file_path) -> dcm.dataset.Dataset:
        """Read DICOM-style files with pydicom library."""
        original_dicom_file = dcm.dcmread(dicom_file_path)
        self.check_valid_dicom(original_dicom_file)
        return original_dicom_file

    def anonymize(self, dicom_file_path) -> dcm.dataset.Dataset:
        """Build fresh DICOM file, populate with anonymized data and pixel data."""
        original_dicom_file = self.read_dicom_file(dicom_file_path)
        anonymized_dicom_file = original_dicom_file
        if hasattr(original_dicom_file, "PixelData") or hasattr(original_dicom_file, "pixel_array"):
            anonymized_dicom_file = self.pixel_data_writer.write_pixel_data(
            	original_dicom_file, anonymized_dicom_file
            )
        return anonymized_dicom_file


def main():
    pass


if __name__ == "__main__":
    main()