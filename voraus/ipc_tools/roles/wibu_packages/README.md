# voraus.ipc_tools.wibu_packages

Install WiBu packages on the system that are required for handling licensed components

- [CodeMeter](https://www.wibu.com/products/codemeter.html) (lite variant per default)

## Requirements

None.

## Role Variables

The `defaults/main.yml` file always provides a complete list of the variables.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: servers
  roles:
    - voraus.ipc_tools.wibu_packages
```
