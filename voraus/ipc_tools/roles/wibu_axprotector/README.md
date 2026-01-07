# voraus.ipc_tools.wibu_axprotector

Installs WIBU's [AxProtector](https://www.wibu.com/products/protection-suite/axprotector.html) on the host.

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
    - voraus.ipc_tools.wibu_axprotector
```
