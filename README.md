# check_pve_backups

Icinga/Nagios plugin to monitor virtual machines (VMs and containers)
backups on a Proxmox VE cluster/node.

It connects to the Proxmox VE API and supports two check modes:

- **`not_backed_up`**: reports VMs/CTs that have no backup job at all
  (queries `/cluster/backup-info/not-backed-up`).
- **`backups`**: reports VMs/CTs whose last available backup on a given
  storage is older than configurable warning/critical thresholds.

## Requirements

- Python 3
- [proxmoxer](https://pypi.org/project/proxmoxer/) and its dependencies
  (see `requirements.txt`)
- A Proxmox VE API user with permissions to read backup info and storage
  content

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```
check_pve_backups.py [-h] [-V] [--debug] [--debug2] [-H HOST] [-P PORT]
                      -u USERNAME -p PASSWORD [--verify-ssl]
                      [-l {warning,critical}] [-s STORAGE] [-n NODE]
                      [-t TIMEOUT] [-i INCLUDED_VMIDS | -e EXCLUDED_VMIDS]
                      [-w WARNING] [-c CRITICAL] [--print-ok]
                      [--retry-times RETRY_TIMES]
                      [--retry-interval RETRY_INTERVAL]
                      {not_backed_up,backups}
```

### Positional arguments

| Argument | Description |
|---|---|
| `{not_backed_up,backups}` | The check to run: `not_backed_up` (VMs without a backup job) or `backups` (backup age check) |

### Options

| Option | Description |
|---|---|
| `-V`, `--version` | Show program's version number and exit |
| `--debug` | Print debugging info to console (not suitable for use with Icinga) |
| `--debug2` | Print exceptions to console (not suitable for use with Icinga) |
| `-H`, `--host HOST` | The Proxmox API host (default `localhost`) |
| `-P`, `--port PORT` | The Proxmox API port (default `8006`) |
| `-u`, `--username USERNAME` | The Proxmox API username (`username@realm`), required |
| `-p`, `--password PASSWORD` | The Proxmox API password, required |
| `--verify-ssl` | Verify the SSL certificate (default false) |
| `-l`, `--level {warning,critical}` | Icinga error level to raise on failure (`not_backed_up` check only, default `critical`) |
| `-s`, `--storage STORAGE` | The backup storage (required in `backups` check mode) |
| `-n`, `--node NODE` | Filter the VMs running on this Proxmox node |
| `-t`, `--timeout TIMEOUT` | API request timeout in seconds (default `300`) |
| `-i`, `--include`, `--vmid INCLUDED_VMIDS` | VM IDs to check (repeatable), mutually exclusive with `-e` |
| `-e`, `--exclude EXCLUDED_VMIDS` | VM IDs to exclude from the check (repeatable), mutually exclusive with `-i` |
| `-w`, `--warning WARNING` | Warning threshold in minutes (required in `backups` check mode) |
| `-c`, `--critical CRITICAL` | Critical threshold in minutes (required in `backups` check mode) |
| `--print-ok`, `-k` | Also print VMs/CTs with an up-to-date backup (default false) |
| `--retry-times RETRY_TIMES` | Number of retries on retryable API errors, e.g. HTTP 596 (default `10`) |
| `--retry-interval RETRY_INTERVAL` | Seconds to wait between retries on retryable API errors (default `5`) |

### Retry behaviour

Some Proxmox API calls occasionally fail with transient HTTP errors (e.g.
`596` connection timeouts during TLS negotiation). These specific status
codes are retried automatically up to `--retry-times` times, waiting
`--retry-interval` seconds between attempts, before giving up and
returning an `UNKNOWN` status.

## Examples

Check for VMs without any backup job, on a specific node, excluding some
VM IDs:

```bash
./check_pve_backups.py not_backed_up \
    --host pve.example.com --username icinga@pve --password secret \
    --node pve1 -e 100 -e 101 -l critical
```

Check backup age for all VMs on a node, using a PBS storage, with custom
warning/critical thresholds (in minutes) and a more aggressive retry
policy:

```bash
./check_pve_backups.py backups \
    --host pve.example.com --username icinga@pve --password secret \
    --node pve1 --storage backup-pbs \
    --warning 1800 --critical 3240 \
    --retry-times 5 --retry-interval 10
```

## Exit codes

Standard Icinga/Nagios exit codes are used:

| Code | Status |
|---|---|
| 0 | OK |
| 1 | WARNING |
| 2 | CRITICAL |
| 3 | UNKNOWN |

## License

See [LICENSE](LICENSE).
