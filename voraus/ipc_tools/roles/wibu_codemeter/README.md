# voraus.ipc_tools.wibu_codemeter

Installs a WiBu CodeMeter license server on the host.

## Requirements

None.

## Role Variables

The `defaults/main.yml` file always provides a complete list of the variables.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: servers
  collections:
    - voraus.ipc_tools
  roles:
    - voraus.ipc_tools.wibu_codemeter
```
