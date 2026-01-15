# voraus.ipc_tools.core_isolation

Installs configuration files on the target to isolate specified cores. Defaults to isolating the second core (id 1).
You can pass further cores to be isolated by either passing the variable via CLI
`-e '{"core_isolation_isolated_core_ids":"1,2"}'` or by setting it in your `inventory.yaml` or `defaults.yml`.

## Requirements

Currently we only support 64-bit systems. The target needs to be running systemd.

## Role Variables

The `defaults/main.yml` file always provides a complete list of the variables.

## Dependencies

The following packages are installed by this role

- [tuna](https://salsa.debian.org/python-team/packages/tuna)
- [ethtool](https://salsa.debian.org/kernel-team/ethtool)
- [iproute2](https://salsa.debian.org/kernel-team/iproute2)

## Example Playbook

```yaml
- hosts: servers
  vars:
    grub_config_entries_to_set:
      core_isolation_isolated_core_ids: 1,3,4,5,12,21
      core_isolation_isolated_network_interfaces:
        eno1: 3
        enp6s0f0: 4,5
  roles:
    - voraus.ipc_tools.core_isolation
```
