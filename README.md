# 📝 utility to convert back and forth among popular dataset label formats #
***

## Installation ##
***

```bash
    python setup.py install --record files.txt
```

- conda environment:
```bash
    conda env create --file environment.yml
    conda activate label_converter
```

## :running: How to Run ##
***

- convert one single label file

```bash
    label_converter --single_file \
        --task [task type] \
        --input_single_label [path to label file] \
        --input_format {"yolo", "voc", "labelme"} \
        --output_format {"yolo", "voc", "labelme"}
        --classes {object classes needed for yolo label, separated by commas, eg: "cat,dog"}
```

- convert label files in an input path

```bash
    label_converter \
        --task [task type] \
        --input_path [path to label files] \
        --input_format {"yolo", "voc", "labelme"} \
        --output_format {"yolo", "voc", "labelme"} \
        --output_path [path to store converted label files]
        --classes {object classes needed for yolo label, separated by commas, eg: "cat,dog"}
```

- task list
```text
0: detection 2d
1: semantic segmentation
2: instance segmentation
```
