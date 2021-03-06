import argparse
import os
import pickle
import shutil
from typing import List

from PIL import Image
from omrdatasettools.downloaders.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader
from omrdatasettools.downloaders.FornesMusicSymbolsDatasetDownloader import FornesMusicSymbolsDatasetDownloader
from omrdatasettools.downloaders.HomusDatasetDownloader import HomusDatasetDownloader
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader
from omrdatasettools.downloaders.OpenOmrDatasetDownloader import OpenOmrDatasetDownloader
from omrdatasettools.downloaders.PrintedMusicSymbolsDatasetDownloader import PrintedMusicSymbolsDatasetDownloader
from omrdatasettools.downloaders.RebeloMusicSymbolDataset1Downloader import RebeloMusicSymbolDataset1Downloader
from omrdatasettools.downloaders.RebeloMusicSymbolDataset2Downloader import RebeloMusicSymbolDataset2Downloader
from omrdatasettools.image_generators.AudiverisOmrImageGenerator import AudiverisOmrImageGenerator
from omrdatasettools.image_generators.HomusImageGenerator import HomusImageGenerator

from datasets.AudiverisOmrImageExtractor import AudiverisOmrImageExtractor
from datasets.DatasetSplitter import DatasetSplitter
from datasets.FornesMusicSymbolsImagePreparer import FornesMusicSymbolsImagePreparer
from datasets.ImageResizer import ImageResizer
from datasets.MuscimaPlusPlusImageGenerator2 import MuscimaPlusPlusImageGenerator2
from datasets.OpenOmrImagePreparer import OpenOmrImagePreparer


class TrainingDatasetProvider:
    """
    Class that provides the datasets used for training a convolutional neural network in the appropriate way.
    It deletes the existing directory, handles the downloading, creating, resizing and splitting of the
    requested datasets for a subsequent training.
    """

    def __init__(self, dataset_directory: str) -> None:
        self.dataset_directory = dataset_directory
        self.image_dataset_directory = os.path.join(dataset_directory, "images")

    def recreate_and_prepare_datasets_for_training(self, datasets: List[str], width: int, height: int,
                                                   use_fixed_canvas: bool,
                                                   stroke_thicknesses_for_generated_symbols: List[int],
                                                   staff_line_spacing: int,
                                                   staff_line_vertical_offsets: List[int],
                                                   random_position_on_canvas: bool) -> None:
        """
        Deletes the dataset_directory and recreates the requested datasets into that folder.
        Some datasets just need to be downloaded and extracted (e.g. PrintedMusicSymbolsDataset),
        whereas other datasets require more extensive generation operations, e.g. Homus dataset.
        """
        self.__delete_dataset_directory()
        self.__download_and_extract_datasets(datasets, width, height, use_fixed_canvas, staff_line_spacing,
                                             staff_line_vertical_offsets, stroke_thicknesses_for_generated_symbols,
                                             random_position_on_canvas)

    def resize_all_images_to_fixed_size(self, width, height):
        print("Resizing all images with the LANCZOS interpolation to {0}x{1}px (width x height).".format(width, height))
        image_resizer = ImageResizer()
        image_resizer.resize_all_images(self.image_dataset_directory, width, height, Image.LANCZOS)

    def split_dataset_into_training_validation_and_test_set(self):
        dataset_splitter = DatasetSplitter(self.image_dataset_directory, self.image_dataset_directory)
        dataset_splitter.delete_split_directories()
        dataset_splitter.split_images_into_training_validation_and_test_set()

    def __delete_dataset_directory(self):
        print("Deleting dataset directory {0}".format(self.dataset_directory))
        if os.path.exists(self.dataset_directory):
            shutil.rmtree(self.dataset_directory)

    def __download_and_extract_datasets(self, datasets, width, height, use_fixed_canvas, staff_line_spacing,
                                        staff_line_vertical_offsets, stroke_thicknesses_for_generated_symbols,
                                        random_position_on_canvas: bool):
        if 'homus' in datasets:
            raw_dataset_directory = os.path.join(self.dataset_directory, "homus_raw")
            dataset_downloader = HomusDatasetDownloader(raw_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
            generated_image_width = width
            generated_image_height = height
            if not use_fixed_canvas:
                # If we are not using a fixed canvas, remove those arguments to
                # allow symbols being drawn at their original shapes
                generated_image_width, generated_image_height = None, None
            bounding_boxes = HomusImageGenerator.create_images(raw_dataset_directory, self.image_dataset_directory,
                                                               stroke_thicknesses_for_generated_symbols,
                                                               generated_image_width,
                                                               generated_image_height, staff_line_spacing,
                                                               staff_line_vertical_offsets,
                                                               random_position_on_canvas)

            bounding_boxes_cache = os.path.join(self.dataset_directory, "bounding_boxes.txt")
            with open(bounding_boxes_cache, "wb") as cache:
                pickle.dump(bounding_boxes, cache)
        if 'rebelo1' in datasets:
            dataset_downloader = RebeloMusicSymbolDataset1Downloader(self.image_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
        if 'rebelo2' in datasets:
            dataset_downloader = RebeloMusicSymbolDataset2Downloader(self.image_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
        if 'printed' in datasets:
            dataset_downloader = PrintedMusicSymbolsDatasetDownloader(self.image_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
        if 'fornes' in datasets:
            raw_dataset_directory = os.path.join(self.dataset_directory, "fornes_raw")
            dataset_downloader = FornesMusicSymbolsDatasetDownloader(raw_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
            image_preparer = FornesMusicSymbolsImagePreparer()
            image_preparer.prepare_dataset(raw_dataset_directory, self.image_dataset_directory)
        if 'audiveris' in datasets:
            raw_dataset_directory = os.path.join(self.dataset_directory, "audiveris_omr_raw")
            intermediate_image_directory = os.path.join(self.dataset_directory, "audiveris_omr_images")
            dataset_downloader = AudiverisOmrDatasetDownloader(raw_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
            image_generator = AudiverisOmrImageGenerator()
            image_generator.extract_symbols(raw_dataset_directory, intermediate_image_directory)
            image_preparer = AudiverisOmrImageExtractor()
            image_preparer.prepare_dataset(intermediate_image_directory, self.image_dataset_directory)
        if 'muscima_pp' in datasets:
            raw_dataset_directory = os.path.join(self.dataset_directory, "muscima_pp_raw")
            dataset_downloader = MuscimaPlusPlusDatasetDownloader(raw_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
            image_generator = MuscimaPlusPlusImageGenerator2()
            image_generator.extract_symbols_for_training(raw_dataset_directory, self.image_dataset_directory)
        if 'openomr' in datasets:
            raw_dataset_directory = os.path.join(self.dataset_directory, "open_omr_raw")
            dataset_downloader = OpenOmrDatasetDownloader(raw_dataset_directory)
            dataset_downloader.download_and_extract_dataset()
            image_preparer = OpenOmrImagePreparer()
            image_preparer.prepare_dataset(raw_dataset_directory, self.image_dataset_directory)

    @staticmethod
    def add_arguments_for_training_dataset_provider(parser: argparse.ArgumentParser):
        parser.add_argument("--width", default=96, type=int, help="Width of the input-images for the network in pixel")
        parser.add_argument("--height", default=96, type=int,
                            help="Height of the input-images for the network in pixel")
        parser.add_argument("--datasets", dest="datasets", default="homus",
                            help="Specifies which datasets are used for the training. One or multiple datasets of the "
                                 "following are possible: homus, rebelo1, rebelo2, printed, audiveris, muscima_pp, "
                                 "fornes or openomr. "
                                 "Multiple values are connected by a separating comma, i.e. 'homus,rebelo1'")
        HomusImageGenerator.add_arguments_for_homus_image_generator(parser)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_directory", type=str, default="../data",
                        help="The directory, where the dataset should be created in")
    TrainingDatasetProvider.add_arguments_for_training_dataset_provider(parser)
    flags, unparsed = parser.parse_known_args()

    offsets = []
    if flags.offsets != "":
        offsets = [int(o) for o in flags.offsets.split(',')]
    stroke_thicknesses_for_generated_symbols = [int(s) for s in flags.stroke_thicknesses.split(',')]

    if flags.datasets == "":
        raise Exception("No dataset selected. Specify the dataset for the training via the --dataset parameter")
    datasets = flags.datasets.split(',')

    training_dataset_provider = TrainingDatasetProvider(flags.dataset_directory)
    training_dataset_provider.recreate_and_prepare_datasets_for_training(
        datasets=datasets, width=flags.width,
        height=flags.height,
        use_fixed_canvas=flags.use_fixed_canvas,
        stroke_thicknesses_for_generated_symbols=stroke_thicknesses_for_generated_symbols,
        staff_line_spacing=flags.staff_line_spacing,
        staff_line_vertical_offsets=offsets,
        random_position_on_canvas=False)
