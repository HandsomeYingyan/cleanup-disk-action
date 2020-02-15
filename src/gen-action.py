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

import os
import sys
import jinja2
import codecs

packages = {
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


def main():
    env = jinja2.Environment(trim_blocks=True,
                             lstrip_blocks=True,
                             loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template('action.yaml.j2')

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../action.yml'))
    with codecs.open(output_path, 'w', 'utf8') as f:
        f.write(template.render(packages=packages))
    for k in packages.keys():
        print(f'- {k}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
