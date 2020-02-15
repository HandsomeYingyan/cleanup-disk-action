# Cleanup Disk Action

![disk info](https://github.com/curoky/cleanup-disk-action/workflows/disk%20info/badge.svg)
![meta info](https://github.com/curoky/cleanup-disk-action/workflows/meta%20info/badge.svg)
![check effect](https://github.com/curoky/cleanup-disk-action/workflows/check%20effect/badge.svg)

## Why need clean disk

### before clean

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        84G   56G   29G  67% /
/dev/sda15      105M  3.6M  101M   4% /boot/efi
/dev/sdb1        14G  4.1G  9.0G  32% /mnt
```

### after clean

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        84G   24G   61G  28% /
/dev/sda15      105M  3.6M  101M   4% /boot/efi
/dev/sdb1        14G  4.1G  9.0G  32% /mnt
```

## Usage

```yaml
steps:
  - name: Cleanup Disk
    uses: curoky/cleanup-disk-action@v1.0
```

retain some packages

```yaml
steps:
  - name: Cleanup Disk
    uses: curoky/cleanup-disk-action@v1.0
    with:
      retain: 'python,node,ruby'
```

don't show cleanup stat

```yaml
steps:
  - name: Cleanup Disk
    uses: curoky/cleanup-disk-action@v1.0
    with:
      show_stat: false
```

## Which packages were removed

**Note**: Currently only ubuntu is supported

The following installation packages will be removed, except for python/node.

```json
{
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
    "4.5.0": ["/usr/share/az_4.5.0"]
  },
  "android": {
    "default": ["/usr/local/lib/android"]
  },
  "python": {
    "sys-2.7": ["/usr/local/lib/python2.7"],
    "sys-3.8": ["/usr/local/lib/python3.8"],
    "cached-3.8.5": ["/opt/hostedtoolcache/Python/3.8.5"],
    "cached-3.7.8": ["/opt/hostedtoolcache/Python/3.7.8"],
    "cached-3.5.9": ["/opt/hostedtoolcache/Python/3.5.9"],
    "cached-3.6.11": ["/opt/hostedtoolcache/Python/3.6.11"],
    "cached-2.7.18": ["/opt/hostedtoolcache/Python/2.7.18"]
  },
  "julia": {
    "1.5.0": ["/usr/local/julia1.5.0"]
  },
  "vcpkg": {
    "default": ["/usr/local/share/vcpkg"]
  },
  "jvm": {
    "default": ["/usr/lib/jvm"]
  },
  "llvm": {
    "6": ["/usr/lib/llvm-6.0", "/usr/include/llvm-6.0"],
    "8": ["/usr/lib/llvm-8", "/usr/include/llvm-8"],
    "9": ["/usr/lib/llvm-9", "/usr/include/llvm-9"]
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
    "8.10.1": ["/opt/ghc/8.10.1"]
  },
  "linuxbrew": {
    "default": ["/home/linuxbrew"]
  }
}
```
