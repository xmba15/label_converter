#!/usr/bin/env python
from enum import Enum, IntEnum


__all__ = ["LabelTask"]


class LabelTask(IntEnum):
    DETECTION_2D = 0
    SEMANTIC_SEGMENTATION = 1
    INSTANCE_SEGMENTATION = 2


class Detection2DLabelFormat(Enum):
    YOLO = 0
    VOC = 1
    LABELME = 2


DETECTION2D_LABEL_FILE_FORMAT_DICT = {
    Detection2DLabelFormat.YOLO: "txt",
    Detection2DLabelFormat.VOC: "xml",
    Detection2DLabelFormat.LABELME: "json",
}
