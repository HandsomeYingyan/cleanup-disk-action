# Cleanup Disk Action

![unitest](https://github.com/curoky/cleanup-disk-action/workflows/test/badge.svg)

**Note**: Currently only ubuntu is supported.

## Usage

```yaml
steps:
  - name: Cleanup disk
    uses: HandsomeYingyan/cleanup-disk-action@v2.0
```

### retain some packages

```yaml
steps:
  - name: Cleanup Disk
    uses: HandsomeYingyan/cleanup-disk-action@v2.0
    with:
      retain: 'python,node'
```

By default, python and node is retained, you can remove all package with set `retain: ''`.

## Which packages were removed

- android
- az
- dotnet
- firefox
- ghc
- go
- google-cloud-sdk
- gradle
- julia
- jvm
- linuxbrew
- llvm
- miniconda
- mono
- node
- php
- pypy
- python
- ruby
- rust
- swift
- vcpkg

## Effect

### before clean

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb1        84G   61G   23G  73% /
```

### after clean

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb1        84G   20G   64G  24% /
```
