#!/usr/bin/env python
import label_converter.label_handler.detection_2d as detection_2d
from label_converter.types import LabelTask


__all__ = ["TASK_LOADER_DICT"]


TASK_LOADER_DICT = {LabelTask.DETECTION_2D: detection_2d.main}
