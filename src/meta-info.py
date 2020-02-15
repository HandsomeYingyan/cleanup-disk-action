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
#
# -----------------------------------------------------------------------------
# @file: meta-info.py
# -----------------------------------------------------------------------------

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

meta_data = {
    "go": {
        "default": ["/opt/hostedtoolcache/go"]
    },
    "ruby": {
        "2.5.8": ["/opt/hostedtoolcache/Ruby/2.5.8"],
        "2.6.6": ["/opt/hostedtoolcache/Ruby/2.6.6"],
        "2.7.1": ["/opt/hostedtoolcache/Ruby/2.7.1"]
    },
    "pypy": {
        "2.7.13": ["/opt/hostedtoolcache/PyPy/2.7.13"],
        "3.6.9": ["/opt/hostedtoolcache/PyPy/3.6.9"]
    },
    "node": {
        "default": ["/usr/local/lib/node_modules"],
        "cached-8.17.0": ["/opt/hostedtoolcache/node/8.17.0"],
        "cached-10.22.0": ["/opt/hostedtoolcache/node/10.22.0"],
        "cached-12.18.3": ["/opt/hostedtoolcache/node/12.18.3"],
        "cached-14.7.0": ["/opt/hostedtoolcache/node/14.7.0"]
    },
    "dotnet": {
        "default": ["/usr/share/dotnet"]
    },
    "swift": {
        "default": ["/usr/share/swift"]
    },
    "rust": {
        "default": ["/usr/share/rust"]
    },
    "miniconda": {
        "default": ["/usr/share/miniconda"]
    },
    "gradle": {
        "6.5.1": ["/usr/share/gradle-6.5.1"]
    },
    "az": {
        "default": ["/opt/az"],
        "4.5.0": ["/usr/share/az_4.5.0"],
        "4.8.0": ["/usr/share/az_4.8.0"]
    },
    "android": {
        "default": ["/usr/local/lib/android"]
    },
    "python": {
        "sys-2.7": ["/usr/local/lib/python2.7"],
        "sys-3.8": ["/usr/local/lib/python3.8"],
        "cached-2.7.18": ["/opt/hostedtoolcache/Python/2.7.18"],
        "cached-3.6.11": ["/opt/hostedtoolcache/Python/3.6.11"],
        "cached-3.6.12": ["/opt/hostedtoolcache/Python/3.6.12"],
        "cached-3.5.9": ["/opt/hostedtoolcache/Python/3.5.9"],
        "cached-3.5.10": ["/opt/hostedtoolcache/Python/3.5.10"],
        "cached-3.7.8": ["/opt/hostedtoolcache/Python/3.7.8"],
        "cached-3.7.9": ["/opt/hostedtoolcache/Python/3.7.9"],
        "cached-3.8.5": ["/opt/hostedtoolcache/Python/3.8.5"],
        "cached-3.8.6": ["/opt/hostedtoolcache/Python/3.8.6"],
        "cached-3.9.0": ["/opt/hostedtoolcache/Python/3.9.0"]
    },
    "julia": {
        "1.5.0": ["/usr/local/julia1.5.0"],
        "1.5.3": ["/usr/local/julia1.5.3"]
    },
    "vcpkg": {
        "default": ["/usr/local/share/vcpkg"]
    },
    "jvm": {
        "default": ["/usr/lib/jvm"]
    },
    "mono": {
        "default": ["/usr/lib/mono"]
    },
    "llvm": {
        "6": ["/usr/lib/llvm-6.0", "/usr/include/llvm-6.0"],
        "8": ["/usr/lib/llvm-8", "/usr/include/llvm-8"],
        "9": ["/usr/lib/llvm-9", "/usr/include/llvm-9"],
        "10": ["/usr/lib/llvm-10", "/usr/include/llvm-10"]
    },
    "firefox": {
        "default": ["/usr/lib/firefox"]
    },
    "google-cloud-sdk": {
        "default": ["/usr/lib/google-cloud-sdk"]
    },
    "php": {
        "default": ["/usr/include/php"]
    },
    "ghc": {
        "8.6.5": ["/opt/ghc/8.6.5"],
        "8.8.3": ["/opt/ghc/8.8.3"],
        "8.8.4": ["/opt/ghc/8.8.4"],
        "8.10.1": ["/opt/ghc/8.10.1"],
        "8.10.2": ["/opt/ghc/8.10.2"]
    },
    "linuxbrew": {
        "default": ["/home/linuxbrew"]
    }
}


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
        n_name.name = f"{n_name.name} (ignored)"
        return n_name

    all_size = 0
    for vid, paths in versions.items():
        n_vid = Node(vid, parent=n_name)

        vid_size = 0
        for p in paths:
            if os.path.isfile(p) or os.path.isdir(p):
                file_size = getPathSize(p) if FLAGS.show_stat else 0
                vid_size += file_size
                file_size = f"{file_size}Mb"
            else:
                file_size = "--- not found"

            n_path = Node(f"{file_size} [{p}]", parent=n_vid)
        n_vid.name = f"{n_vid.name} ({vid_size}Mb)"
        all_size += vid_size
    n_name.name = f"{n_name.name} ({all_size}Mb)"
    return n_name


def main(_):
    if not os.path.isfile(FLAGS.meta_path):
        logging.fatal(f"file {FLAGS.meta_path} not exits")

    with codecs.open(FLAGS.meta_path, 'r', 'utf-8') as f:
        content = f.read()

    FLAGS.retain_list = FLAGS.retain_list or ["python", "node"]

    try:
        meta = json.loads(content)
        logging.info(f"meta size: {len(meta)}", )
    except Exception as e:
        logging.fatal(f"load file {FLAGS.meta_path} failed {e}")

    with multiprocessing.Pool(processes=4) as pool:
        func = partial(collectPathInfo, FLAGS.retain_list, FLAGS.clean)
        results = pool.map(func, meta.items())

    n_root = Node("root")
    with codecs.open(FLAGS.result_path, 'w', 'utf-8') as f:
        for r in results:
            r.parent = n_root
        if FLAGS.show_stat:
            print(RenderTree(n_root).by_attr())
        print(RenderTree(n_root).by_attr(), file=f)


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    app.run(main)
