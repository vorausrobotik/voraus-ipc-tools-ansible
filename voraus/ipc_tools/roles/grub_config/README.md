# voraus.ipc_tools.grub_config

Configures GRUB config entries. Any existing config entries are kept, but existing keys are overwritten with the given config.

The role also adds a drop-in that skips `grub-common.service` while `/boot/grub` is read-only. The service clears the GRUB `recordfail` flag in `/boot/grub/grubenv`, which fails on the read-only `/boot` of the IPCs and leaves the unit `failed`. GRUB cannot set that flag on a read-only `/boot` either, so there is nothing to clear.

## Requirements

None.

## Role Variables

The `defaults/main.yml` file always provides a complete list of the variables.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all

  vars:
    grub_config_entries_to_set:
      foo: bar # Will be written as foo=bar
      nomodeset: # Will be written as nomodeset (flag without value)
  roles:
    - voraus.ipc_tools.grub_config
```
