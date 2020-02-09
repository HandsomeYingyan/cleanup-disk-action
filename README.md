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
  - uses: actions/checkout@v2

  - name: Cleanup Disk
    uses: curoky/cleanup-disk-action@master
```
