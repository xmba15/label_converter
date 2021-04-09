#!/usr/bin/env python
import os


__all__ = ["get_all_files_with_format_from_path"]


def get_all_files_with_format_from_path(dir_path, suffix_format, concat_dir_path=True):
    def _human_sort(s):
        """Sort list the way humans do"""
        import re

        pattern = r"([0-9]+)"
        return [int(c) if c.isdigit() else c.lower() for c in re.split(pattern, s)]

    all_files = [elem for elem in os.listdir(dir_path) if elem.endswith(suffix_format)]
    all_files.sort(key=_human_sort)
    if concat_dir_path:
        all_files = [os.path.join(dir_path, cur_file) for cur_file in all_files]

    return all_files
