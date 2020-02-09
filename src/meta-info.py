#!/usr/bin/env python3
# Copyright 2020 curoky(cccuroky@gmail.com).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Usage:
#   1. show meta info
#      ./meta-info.py --meta_path=meta.json --result_path=meta.txt
#   2. clean with meta
#      ./meta-info.py --meta_path=meta.json --result_path=meta.txt \
#           --clean=1 --retain_list="go,py"

import os
import json
import codecs
import shutil
import multiprocessing
from absl import app
from absl import flags
from absl import logging
from functools import partial
from anytree import Node, RenderTree

FLAGS = flags.FLAGS
flags.DEFINE_string("meta_path", None, "path to meta file.")
flags.mark_flag_as_required("meta_path")

flags.DEFINE_string("result_path", None, "path to result file.")
flags.mark_flag_as_required("result_path")

flags.DEFINE_list("retain_list", "", "don't remove some package")
flags.DEFINE_bool("clean", False, "clean path with meta info")


def getPathSize(start_path):
    # ref: https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
    total_size = 0
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        for dirpath, _, filenames in os.walk(start_path, followlinks=False):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    total_size = total_size // 1024 // 1024
    return total_size


def collectPathInfo(ingore_list, clean, data):
    name, versions = data
    n_name = Node(name)

    if name in ingore_list and clean:
        n_name.name = "{} (ignored)".format(n_name.name)
        return n_name

    all_size = 0
    for vid, paths in versions.items():
        n_vid = Node(vid, parent=n_name)

        vid_size = 0
        for p in paths:
            if os.path.isfile(p) or os.path.isdir(p):
                file_size = getPathSize(p)
                vid_size += file_size
                file_size = "{}Mb".format(file_size)
            else:
                file_size = "--- not found"

            n_path = Node("{} [{}]".format(file_size, p), parent=n_vid)
        n_vid.name = "{} ({}Mb)".format(n_vid.name, vid_size)
        all_size += vid_size
    n_name.name = "{} ({}Mb)".format(n_name.name, all_size)
    return n_name


def main(_):
    if not os.path.isfile(FLAGS.meta_path):
        logging.fatal("file [%s] not exits", FLAGS.meta_path)

    with codecs.open(FLAGS.meta_path, 'r', 'utf-8') as f:
        content = f.read()

    FLAGS.retain_list = FLAGS.retain_list or ["python", "node"]

    try:
        meta = json.loads(content)
        logging.info("meta size: %d", len(meta))
    except Exception as e:
        logging.fatal("load file %s failed %s", FLAGS.meta_path, str(e))

    with multiprocessing.Pool(processes=4) as pool:
        func = partial(collectPathInfo, FLAGS.retain_list, FLAGS.clean)
        results = pool.map(func, meta.items())

    n_root = Node("root")
    with codecs.open(FLAGS.result_path, 'w', 'utf-8') as f:
        for r in results:
            r.parent = n_root
        print(RenderTree(n_root).by_attr())
        print(RenderTree(n_root).by_attr(), file=f)


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    app.run(main)
