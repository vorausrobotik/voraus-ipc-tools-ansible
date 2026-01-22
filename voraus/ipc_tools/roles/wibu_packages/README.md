# voraus.ipc_tools.wibu_packages

Install WiBu packages on the system that are required for handling licensed components

- [CodeMeter](https://www.wibu.com/products/codemeter.html) (lite variant per default)
- [AxProtector](https://www.wibu.com/products/protection-suite/axprotector.html)

## Requirements

None.

## Role Variables

The `defaults/main.yml` file always provides a complete list of the variables.

## Dependencies

None.

## Example Playbooks

```yaml
- name: Install WiBu packages in the default configuration (versions are pinned, downgrades allowed)
  hosts: all
  roles:
    - voraus.ipc_tools.wibu_packages
```

```yaml
- name: Install WiBu packages in a specific version
  hosts: all
  vars:
    wibu_packages_install:
      codemeter-lite: 8.20.6539.500
      axprotector: 11.70.7131.502
  roles:
    - voraus.ipc_tools.wibu_packages
```

```yaml
- name: Install WiBu packages in the latest versions available
  hosts: all
  vars:
    wibu_packages_install:
      codemeter-lite:
      axprotector:
  roles:
    - voraus.ipc_tools.wibu_packages
```
