"""
Copy pixel data from original to anonymized DICOM file.
"""
import logging

log = logging.getLogger(__name__)


class PixelDataWriter:
    """Write DICOM pixel data to anonymized DICOM file."""

    def __init__(self):

    def write_pixel_data_direct_copy(self, original_dicom_file, anonymized_dicom_file):
        """Copy pixel data directly to anonymized file."""
        anonymized_dicom_file.PixelData = original_dicom_file.PixelData
        anonymized_dicom_file.is_little_endian = original_dicom_file.is_little_endian
        anonymized_dicom_file.is_implicit_VR = original_dicom_file.is_implicit_VR
        anonymized_dicom_file.file_meta = original_dicom_file.file_meta
        return anonymized_dicom_file

    #def write_pixel_data_decompress(self, original_dicom_file, anonymized_dicom_file):
    #    """Copy pixel data to anonymized file, decompress compressed data."""
    #    anonymized_dicom_file.PixelData = original_dicom_file.pixel_array.tobytes()
    #    anonymized_dicom_file.file_meta.MediaStorageSOPClassUID = (
    #        original_dicom_file.file_meta.MediaStorageSOPClassUID
    #    )
    #    anonymized_dicom_file.file_meta.ImplementationClassUID = (
    #        original_dicom_file.file_meta.ImplementationClassUID
    #    )
    #    return anonymized_dicom_file

    def write_pixel_data(self, original_dicom_file, anonymized_dicom_file):
        """Write compressed or decompressed pixel data to anonymized file depending on passage of optional --decompress arg."""
        anonymized_dicom_file = self.write_pixel_data_direct_copy(
            original_dicom_file, anonymized_dicom_file
        return anonymized_dicom_file


def main():
    pass


if __name__ == "__main__":
    main()
