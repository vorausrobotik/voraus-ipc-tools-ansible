# voraus.ipc_tools.grub_config

Configures GRUB config entries. Any existing config entries are kept, but existing keys are overwritten with the given config.

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
