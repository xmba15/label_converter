#!/usr/bin/env python
from __future__ import print_function, division, absolute_import
from label_converter.label_handler.task_loader import TASK_LOADER_DICT


def _get_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        "-t",
        type=int,
        choices=[0, 1, 2],
        help="label task. 0: 2d detection, 1: semantic segmentation, 2: instance segmentation",
    )
    parser.add_argument("--classes", "-c", type=str, help="optional object classes, separated by commas, eg: cat, dog")
    parser.add_argument(
        "--single_file",
        "-s",
        action="store_true",
        help="flag to check whether the user wants to convert a single label file or all the label files in a folder",
    )
    parser.add_argument(
        "--input_single_label",
        "-is",
        type=str,
        help="path to single input label file",
    )
    parser.add_argument(
        "--input_path",
        "-ip",
        type=str,
        help="path to multiple input label files",
    )
    parser.add_argument(
        "--input_format",
        "-if",
        type=str,
        required=True,
        choices=["yolo", "voc", "labelme"],
        help="input label format",
    )
    parser.add_argument(
        "--output_format",
        "-of",
        type=str,
        required=True,
        choices=["yolo", "voc", "labelme"],
        help="output label format",
    )
    parser.add_argument(
        "--output_path",
        "-op",
        type=str,
        default="./",
        help="path to store converted labels",
    )
    args = parser.parse_args()

    return args


def main():
    args = _get_args()
    assert args.input_format != args.output_format
    TASK_LOADER_DICT[args.task](args)


if __name__ == "__main__":
    main()
