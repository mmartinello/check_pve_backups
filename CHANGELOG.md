# Changelog

## 1.2

- `backups` check: add cluster mode, used when `--node` is not given. All
  the VMs of the cluster are checked and the backups are read from the
  cluster nodes where the storage is available (previously the plugin
  queried `/nodes/None/...` and failed).
- `backups` check: fix the creation time printed for each VM (the same
  time was printed for all the VMs, and the check failed with
  `local variable 'backup' referenced before assignment` when no VM had
  backups).

## 1.1

- Add automatic retry on retryable Proxmox API HTTP errors (e.g. `596`
  connection timeout), configurable via `--retry-times` and
  `--retry-interval`.
- Add README documentation.

## 1.0

First stable release.
