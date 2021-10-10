# Cleanup Disk Action

**Note**: Currently only ubuntu is supported.

## Usage

```yaml
steps:
  - name: Cleanup disk
    uses: HandsomeYingyan/cleanup-disk-action@v3.0
```

### retain some packages

```yaml
steps:
  - name: Cleanup Disk
    uses: HandsomeYingyan/cleanup-disk-action@v3.0
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
- r
- jdk
- linux header

## Effect

### before clean

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        84G   51G   34G  61% /
```

### after clean

```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        84G   20G   64G  24% /
```

## You can use this with [easimon/maximize-build-space](https://github.com/easimon/maximize-build-space) to get more space!

```bash
$ df -h
Filesystem                   Size  Used Avail Use% Mounted on
/dev/mapper/buildvg-buildlv   78G   57M   78G   1% /home/runner/work/halium
```

