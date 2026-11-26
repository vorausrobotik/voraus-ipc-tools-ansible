# voraus.ipc_tools.nic_naming

Keeps the path-based network interface names, such as `enp3s0`, when a BIOS update adds onboard indexes.

By default, systemd names an interface after its onboard index (`eno1`) if the firmware reports one, and after its PCI
path (`enp3s0`) otherwise. Some BIOS updates start to report onboard indexes. After such an update, the primary
interface of an UP Squared turns from `enp3s0` into `eno1`, and `/etc/network/interfaces` no longer configures it. The
IPC then has no network.

The role installs a drop-in for systemd's `99-default.link` that leaves the firmware-provided names out of the naming
policy. It then rebuilds the initramfs, because the initramfs names the interfaces first. The names take effect on the
next boot.

## Requirements

The target needs to be running systemd and `initramfs-tools`.

## Role Variables

None.

## Dependencies

- `voraus.ipc_tools.boot_mount` to rebuild the initramfs on a read-only `/boot`.

## Example Playbook

```yaml
- hosts: all
  roles:
    - voraus.ipc_tools.nic_naming
```
