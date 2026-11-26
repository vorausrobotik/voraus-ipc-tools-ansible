# voraus.ipc_tools.boot_mount

Makes `/boot` writable for a change and restores the read-only mount afterwards.

The IPCs mount `/boot` read-only so that a power failure cannot corrupt it. Anything that writes to `/boot`, such as
`update-grub` or `update-initramfs`, therefore has to remount it first. The role does nothing if `/boot` is not its own
read-only mount.

The role has no `main.yml`. Include its two task files around the change instead:

- `read_write.yml` remounts `/boot` read-write if it is a read-only mount.
- `read_only.yml` remounts it read-only again, but only if `read_write.yml` changed it.

## Requirements

The target needs `findmnt` from `util-linux`.

## Role Variables

None.

## Dependencies

None.

## Example Playbook

```yaml
- name: Make /boot writable
  ansible.builtin.include_role:
    name: voraus.ipc_tools.boot_mount
    tasks_from: read_write

- name: Update GRUB
  ansible.builtin.command: update-grub2

- name: Make /boot read-only again
  ansible.builtin.include_role:
    name: voraus.ipc_tools.boot_mount
    tasks_from: read_only
```
