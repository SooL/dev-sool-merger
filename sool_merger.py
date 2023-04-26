#!/usr/bin/python3
#-*-coding:utf-8 -*

# ******************************************************************************
#  Copyright (c) 2018-2023 FAUCHER Julien & FRANCE Loic.                       *
#                                                                              *
#  This file is part of SooL generator.                                        *
#                                                                              *
#  SooL generator is free software: you can redistribute it and/or modify      *
#  it under the terms of the GNU Lesser General Public License                 *
#  as published by the Free Software Foundation, either version 3              *
#  of the License, or (at your option) any later version.                      *
#                                                                              *
#  SooL core Library is distributed in the hope that it will be useful,        *
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              *
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                *
#  GNU Lesser General Public License for more details.                         *
#                                                                              *
#  You should have received a copy of the GNU Lesser General Public License    *
#  along with SooL core Library. If not, see  <https://www.gnu.org/licenses/>. *
# ******************************************************************************

import argparse
import sys
import os
import typing as T
import glob

from data_structure import GroupFileSet
from data_structure import MergeHandler

from data_structure import SooLTag

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

parser = argparse.ArgumentParser(description="Simple tool to merge files generated by AnalyseHeaderST.py")


parser.add_argument("--definition-dir","-d",
					help="Definition files directrory",
					required=True,
					type=str)

parser.add_argument("--structure-dir","-s",
					help="Structure files directrory",
					required=True,
					type=str)
parser.add_argument("--merge-dir","-m",
					help="Destination directory to write in.",
					required=True,
					type=str)

parser.add_argument("--root-filename","-f",
					help="Root for the filenames, as in <root>_definition.h for the split part and <root>.h for the merged one",
					required=True,
					type=str)
parser.add_argument("--reverse",
					help="Reverse the merge (writting from merged to split)",
					action="store_true")
parser.add_argument("--exclude-tags",
					help="Exclude tags from merged files",
					action="store_true")


runtime_args = None

if __name__ == "__main__" :
	# if len(sys.argv) < 6 and runtime_args is None:
	# 	runtime_args = "-s testcase -m testcase/output -f TESTR --reverse".split(" ")

	args = parser.parse_args(runtime_args)

	GroupFileSet.default_merged_folder = args.merge_dir
	GroupFileSet.default_definition_folder = args.definition_dir
	GroupFileSet.default_struct_folder = args.structure_dir
	SooLTag.exclude_boundaries = args.exclude_tags if not args.reverse else False

	base_descr = GroupFileSet(args.root_filename)

	global_fileset : T.Dict[str,MergeHandler] = dict()

	for fpath in glob.glob(base_descr.definition_file) :
		new_fs = GroupFileSet.from_path(fpath)
		try :
			if new_fs.base_name not in global_fileset :
				global_fileset[new_fs.base_name] = MergeHandler(new_fs)
		except FileNotFoundError :
			print(f"Some file not found for base name {new_fs.base_name}. Output not generated.")
			

	for fpath in glob.glob(base_descr.struct_file) :
		new_fs = GroupFileSet.from_path(fpath)
		if new_fs.base_name not in global_fileset :
			global_fileset[new_fs.base_name] = MergeHandler(new_fs)


	for fpath in glob.glob(base_descr.definition_file) :
		new_fs = GroupFileSet.from_path(fpath)
		if new_fs.base_name not in global_fileset :
			global_fileset[new_fs.base_name] = MergeHandler(new_fs)

	for fpath in glob.glob(base_descr.merged_file) :
		new_fs = GroupFileSet.from_path(fpath)
		if new_fs.base_name not in global_fileset :
			global_fileset[new_fs.base_name] = MergeHandler(new_fs)

	for name, handler in global_fileset.items() :
		handler.read_split_tags()
		if not args.reverse :
			handler.split_to_merge()
		else :
			handler.read_merged_tags()
			handler.merge_to_definition()
			if not handler.files.struct_exists :
				handler.merge_to_struct()

	quit(0)