# voraus.ipc_tools.core_isolation

Installs configuration files on the target to isolate specified cores. Defaults to isolating the second core (id 1).
You can pass further cores to be isolated by either passing the variable via CLI
`-e '{"core_isolation_isolated_core_ids":"1,2"}'` or by setting it in your `inventory.yaml` or `defaults.yml`.

## Requirements

Currently we only support 64-bit systems. The target needs to be running systemd.

## Role Variables

None.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: servers
  collections:
    - voraus.ipc_tools
  roles:
    - voraus.ipc_tools.core_isolation
```
