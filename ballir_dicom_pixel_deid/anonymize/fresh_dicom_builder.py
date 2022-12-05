#### MARKED FOR DELETION -- Jacob



"""Build fresh DICOM file to populate with anonymized data."""

import pydicom as dcm

from ballir_dicom_anonymizer.key_handling.patient_key import PatientKey
from ballir_dicom_anonymizer.dicom_tag_handling.write_tags_from_config import (
    WriteConstant,
)

from ast import literal_eval
import logging
log = logging.getLogger(__name__)

class WriteMetaData(WriteConstant):
    """Write required meta data (for building fresh DICOM file)."""

    config_key: str = "assign_meta_data_basic"

    def __init__(self):
        super().__init__()


class FreshDicomBuilder:
    """Build empty dcm DataSet with required fields populated by default values."""

    def __init__(self):
        self.write_meta_data = WriteMetaData()
        self.psuedo_patient_key = PatientKey(output_directory="pseudo")

    def build_fresh_dicom(self, original_dicom_file) -> dcm.dataset.Dataset:
        """Build fresh DICOM meta data dataset."""
        fresh_meta_data = dcm.dataset.FileMetaDataset()
        fresh_meta_data, self.psuedo_patient_key = self.write_meta_data.write_tags(
            original_dicom_file.file_meta, fresh_meta_data, self.psuedo_patient_key
        )
        # set compression related tags in meta data
        fresh_meta_data.TransferSyntaxUID = (
            original_dicom_file.file_meta.TransferSyntaxUID
        )
        # build fresh DICOM file, populate meta data
        fresh_dicom_file = dcm.dataset.Dataset()
        fresh_dicom_file.file_meta = fresh_meta_data
        # set other required fields
        fresh_dicom_file.preamble = b"\0" * 128
        fresh_dicom_file.is_little_endian = True
        fresh_dicom_file.is_implicit_VR = True

        return fresh_dicom_file
