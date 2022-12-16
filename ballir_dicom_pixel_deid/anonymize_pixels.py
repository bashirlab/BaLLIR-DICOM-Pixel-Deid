"""Anonymize all DICOM-type files in target directory."""

import argparse
import os
import time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # Hide Tensorflow info messages (warnings and errors should still show)
import keras_ocr

from glob import glob
from natsort import natsorted
import pydicom as dcm
from tqdm import tqdm
import tensorflow as tf

#from ballir_dicom_pixel_deid.anonymize.dicom_anonymizer import DicomAnonymizer
#from ballir_dicom_pixel_deid.error_handling import UnsupportedFileError
from dicom_anonymizer import DicomAnonymizer
from error_handling import UnsupportedFileError

import logging

log = logging.getLogger(__name__)


def return_dicom_paths(input_directory: str) -> list:
    """Perform recursive search for DICOM files."""
    print(f"Finding DICOM files in {os.path.basename(input_directory)}...")
    all_dicom_file_paths: list = glob(
        os.path.join(input_directory, "**/*"), recursive=True
    )
    all_dicom_file_paths = natsorted(
        [file for file in all_dicom_file_paths if not os.path.isdir(file)]
    )
    return all_dicom_file_paths


def parse_dicoms(input_directory: str):
    """Parses dicom files in input directory to sort by modality and identify/drop secondary captures"""
    MR_list = []
    CT_list = []
    XR_list = []
    US_list = []
    not_sorted = []

    all_dicom_file_paths = return_dicom_paths(input_directory)

    for dicom_file_path in tqdm(
        all_dicom_file_paths,
        position=0,
        leave=True,
        desc=f"Sorting DICOM files in {os.path.basename(input_directory)}...",
    ):
        dcm_temp = dcm.dcmread(dicom_file_path, stop_before_pixels=True)

        # Check/get modality tag
        if "Modality" in dcm_temp:
            modality = dcm_temp.Modality
        else:
            not_sorted.append(dicom_file_path)
            continue

        # Check/get secondary captures
        if "ImageType" in dcm_temp:
            secondary_cap = "SECONDARY" in dcm_temp.ImageType
        else:
            not_sorted.append(dicom_file_path)
            continue
        
        if secondary_cap:
            not_sorted.append(dicom_file_path)
            continue

        # Sort by modality
        if modality == "US":
            US_list.append(dicom_file_path)
        elif modality == "CT":
            CT_list.append(dicom_file_path)
        elif modality == "MR":
            MR_list.append(dicom_file_path)
        elif (modality == "CR") | (modality == "DX"):
            XR_list.append(dicom_file_path)
        else:
            not_sorted.append(dicom_file_path)

    return US_list, CT_list, MR_list, XR_list, not_sorted
            


def return_anonymized_write_path(
    output_directory: str, dicom_file_path: str, input_directory: str
) -> str:

    """Build write path for anonymized DICOM file from Series and SOPInstance."""

    anonymized_write_dir = dicom_file_path.replace(input_directory, output_directory)

    return anonymized_write_dir


def write_anonymized_dicom_file(
    anonymized_dicom_file: dcm.dataset.Dataset,
    output_directory: str,
    dicom_file_path: str,
    input_directory: str,
) -> str:
    """Save anonymized file to write path with pydicom save_as()."""
    anonymized_write_path = return_anonymized_write_path(
        output_directory, dicom_file_path, input_directory
    )
    anonymized_dicom_file.save_as(anonymized_write_path, write_like_original=False)
    return anonymized_write_path


def anonymize_dicom_files(
    input_directory: str, output_directory: str
):
    """Anonymize all supported files in target directory."""
    start = time.time()

    modalities = ["US","CT","MR","XR"]
    US_list, CT_list, MR_list, XR_list, not_sorted = parse_dicoms(input_directory)
    image_dict = {'US':US_list, 'CT':CT_list, 'MR':MR_list, 'XR':XR_list}

    dicom_anonymizer = DicomAnonymizer()

    for modality in modalities:
        found_dicoms = image_dict[modality]
        if len(found_dicoms) == 0:
            continue

        #if modality == "US":
            #model = ''
        #detector = keras_ocr.detection.Detector()
        #detector.model.load_weights('detector_2022-05-12T09:58:08.272889.h5')
        #pipeline = keras_ocr.pipeline.Pipeline(detector=detector)

        for dicom_file_path in tqdm(
            found_dicoms,
            position=0,
            leave=True,
            desc=f"Anonymizing {modality} DICOM files in {os.path.basename(input_directory)}...",
        ):
            log.info(f"processing {dicom_file_path}...")
            try:
                anonymized_dicom_file = dicom_anonymizer.anonymize(dicom_file_path)
                anonymized_write_path = write_anonymized_dicom_file(
                    anonymized_dicom_file, output_directory, dicom_file_path, input_directory
                )
            except UnsupportedFileError as e:
                log.exception(e)

    elapsed_time = time.time() - start
    log.info(f"Anonymization completed in {elapsed_time} seconds")
    print(f"Anonymization completed in {elapsed_time} seconds")


def main():
    """Parse arguments and execute anonymization script."""
    # parse args
    parser = argparse.ArgumentParser(description="DICOM anonymizer parser.")
    parser.add_argument("input_directory", type=str, help="Directory to anonymize.")
    parser.add_argument(
        "-output_directory", type=str, help="Destination for anonymized DICOM files."
    )
    args = parser.parse_args()

    # build output directory
    if not args.output_directory:
        args.output_directory = f"{args.input_directory}_PIXEL-DEID"
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    print(args.input_directory)
    print(args.output_directory)

    # set up log config
    """
    logging.basicConfig(
        filename=os.path.join(
            args.output_directory,
            f"{os.path.basename(args.input_directory)}_PIXEL-DEID.log",
        ),
        encoding="utf-8",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    """

    # anonymize DICOM files
    anonymize_dicom_files(
        args.input_directory, args.output_directory
    )


if __name__ == "__main__":
    main()
