#!/usr/bin/env python
import json
import os
from label_converter.types import Detection2DLabelFormat, DETECTION2D_LABEL_FILE_FORMAT_DICT
from label_converter.utils import get_all_files_with_format_from_path


__all__ = ["Detection2DLabelHandler"]


class Detection2DLabelHandler(object):
    @staticmethod
    def load_label(label_path, label_format):
        assert os.path.join(label_path)

        if label_format == Detection2DLabelFormat.VOC:
            load_label_method = _load_voc
        elif label_format == Detection2DLabelFormat.LABELME:
            load_label_method = _load_label_me
        else:
            raise Exception("not supported label format: {}".format(label_format))

        return load_label_method(label_path)

    @staticmethod
    def save_label(label_format, image_path, image_height, image_width, labels, bbox_list, output_path, *args):
        assert len(bbox_list) == len(labels)

        if label_format == Detection2DLabelFormat.YOLO:
            save_label_method = _save_yolo
        elif label_format == Detection2DLabelFormat.VOC:
            save_label_method = _save_voc
        elif label_format == Detection2DLabelFormat.LABELME:
            save_label_method = _save_label_me
        else:
            raise Exception("not supported label format: {}".format(label_format))

        save_label_method(image_path, image_height, image_width, labels, bbox_list, output_path, *args)


def _save_yolo(image_path, image_height, image_width, labels, bbox_list, output_path, *args):
    assert image_height > 0 and image_width > 0

    classes = args[0]
    write_content = ""

    for label, (xmin, ymin, xmax, ymax) in zip(labels, bbox_list):
        assert label in classes
        label_id = classes.index(label)
        width = xmax - xmin
        height = ymax - ymin
        xcenter = (xmin + xmax) / 2
        ycenter = (ymin + ymax) / 2
        normalized_xcenter = xcenter / image_width
        normalized_ycenter = ycenter / image_height
        normalized_width = width / image_width
        normalized_height = height / image_height

        if len(write_content) != 0:
            write_content += "\n"

        write_content += "{} {} {} {} {}".format(
            label_id, normalized_xcenter, normalized_ycenter, normalized_width, normalized_height
        )

    assert len(write_content) > 0

    with open(output_path, "w") as output_file:
        output_file.write(write_content)


def _load_voc(xml_path):
    import xml.etree.ElementTree as ET

    with open(xml_path) as f:
        tree = ET.parse(f)
        root = tree.getroot()

    image_path = root.find("filename").text
    image_height = int(root.find("size").find("height").text)
    image_width = int(root.find("size").find("width").text)

    labels = []
    bbox_list = []

    for obj in root.iter("object"):
        labels.append(obj.find("name").text)
        xmlbox = obj.find("bndbox")
        bbox_list.append(
            [
                float(xmlbox.find("xmin").text),
                float(xmlbox.find("ymin").text),
                float(xmlbox.find("xmax").text),
                float(xmlbox.find("ymax").text),
            ]
        )

    return image_path, image_height, image_width, labels, bbox_list


def _create_voc(image_path, image_height, image_width, labels, bbox_list):
    from lxml.etree import Element, SubElement, tostring

    node_root = Element("annotation")
    node_folder = SubElement(node_root, "folder")
    node_folder.text = ""

    node_filename = SubElement(node_root, "filename")
    node_filename.text = image_path

    node_size = SubElement(node_root, "size")
    node_width = SubElement(node_size, "width")
    node_width.text = str(image_width)
    node_height = SubElement(node_size, "height")
    node_height.text = str(image_height)

    node_depth = SubElement(node_size, "depth")
    node_depth.text = ""

    node_segmented = SubElement(node_root, "depth")
    node_segmented.text = "0"

    for label, (xmin, ymin, xmax, ymax) in zip(labels, bbox_list):
        node_object = SubElement(node_root, "object")
        node_name = SubElement(node_object, "name")
        node_name.text = label

        node_occluded = SubElement(node_object, "occluded")
        node_occluded.text = "0"
        node_bndbox = SubElement(node_object, "bndbox")
        node_xmin = SubElement(node_bndbox, "xmin")
        node_xmin.text = str(xmin)
        node_ymin = SubElement(node_bndbox, "ymin")
        node_ymin.text = str(ymin)
        node_xmax = SubElement(node_bndbox, "xmax")
        node_xmax.text = str(xmax)
        node_ymax = SubElement(node_bndbox, "ymax")
        node_ymax.text = str(ymax)

    return tostring(node_root, pretty_print=True)


def _save_voc(image_path, image_height, image_width, labels, bbox_list, output_path, *args):
    with open(output_path, "wb") as output_file:
        output_file.write(_create_voc(image_path, image_height, image_width, labels, bbox_list))


def _load_label_me(json_path):
    json_dict = {}
    with open(json_path) as json_file:
        json_dict = json.load(json_file)
    assert len(json_dict) != 0

    image_path = json_dict["imagePath"]
    image_width = json_dict["imageWidth"]
    image_height = json_dict["imageHeight"]

    labels = []
    bbox_list = []
    for obj in json_dict["shapes"]:
        labels.append(obj["label"])
        [xmin, ymin], [xmax, ymax] = obj["points"]
        bbox_list.append([xmin, ymin, xmax, ymax])

    return image_path, image_width, image_height, labels, bbox_list


def _create_label_me_json_dict(image_path, image_height, image_width, labels, bbox_list):
    json_dict = {}
    json_dict["imagePath"] = image_path
    json_dict["imageHeight"] = image_height
    json_dict["imageWidth"] = image_width
    json_dict["shapes"] = []
    json_dict["imageData"] = None

    for bbox, label in zip(bbox_list, labels):
        xmin, ymin, xmax, ymax = bbox

        cur_shape = {}
        cur_shape["label"] = label
        cur_shape["shape_type"] = "rectangle"
        cur_shape["points"] = [[xmin, ymin], [xmax, ymax]]
        cur_shape["group_id"] = None
        cur_shape["flags"] = {}
        json_dict["shapes"].append(cur_shape)

    return json_dict


def _save_label_me(image_path, image_height, image_width, labels, bbox_list, output_path, *args):
    with open(output_path, "w") as output_file:
        json.dump(_create_label_me_json_dict(image_path, image_height, image_width, labels, bbox_list), output_file)


def main(args):
    SUPPORTED_FORMATS = ["yolo", "voc", "labelme"]
    assert args.input_format in SUPPORTED_FORMATS
    assert args.output_format in SUPPORTED_FORMATS

    input_label_format = Detection2DLabelFormat[args.input_format.upper()]
    if input_label_format == Detection2DLabelFormat.YOLO:
        raise Exception("input of type yolo is not supported")

    output_label_format = Detection2DLabelFormat[args.output_format.upper()]

    classes = None
    if output_label_format == Detection2DLabelFormat.YOLO:
        classes = args.classes.split(",")
        assert len(classes) > 0

    output_file_format = DETECTION2D_LABEL_FILE_FORMAT_DICT[output_label_format]

    label_handler = Detection2DLabelHandler
    if args.single_file:
        assert os.path.isfile(args.input_single_label)
        output_file = os.path.basename(args.input_single_label).split(".")[0] + "." + output_file_format
        try:
            label_handler.save_label(
                output_label_format,
                *label_handler.load_label(args.input_single_label, input_label_format),
                os.path.join(args.output_path, output_file),
                classes
            )
        except Exception as e:
            print("{} : {}".format(args.input_single_label, e))
    else:
        assert os.path.isdir(args.input_path)
        input_file_format = DETECTION2D_LABEL_FILE_FORMAT_DICT[input_label_format]
        all_input_files = get_all_files_with_format_from_path(args.input_path, input_file_format, concat_dir_path=False)
        for input_file in all_input_files:
            output_file = input_file.split(".")[0] + "." + output_file_format
            try:
                label_handler.save_label(
                    output_label_format,
                    *label_handler.load_label(os.path.join(args.input_path, input_file), input_label_format),
                    os.path.join(args.output_path, output_file),
                    classes
                )
            except Exception as e:
                print("{} : {}".format(input_file, e))
