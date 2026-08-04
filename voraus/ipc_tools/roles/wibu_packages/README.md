# voraus.ipc_tools.wibu_packages

Install WiBu packages on the system that are required for handling licensed components

- [CodeMeter](https://www.wibu.com/products/codemeter.html) (lite variant per default)
- [AxProtector](https://www.wibu.com/products/protection-suite/axprotector.html)

## Requirements

None. The `nftables` package is installed by the role if the firewall is enabled.

## Role Variables

The `defaults/main.yml` file always provides a complete list of the variables.

## Firewall

With `wibu_packages_firewall` enabled (the default), access to the CodeMeter ports is restricted to
the host itself and to container networks:

| Port                                    | Reachable from                                                     |
| --------------------------------------- | ------------------------------------------------------------------ |
| 22350/tcp+udp (licensing and discovery) | the host itself, `docker0` and user defined `br-*` docker networks |
| 22352/tcp (WebAdmin)                    | the host itself                                                    |

The WebAdmin interface is therefore no longer reachable from other machines. Use an SSH tunnel to
access it: `ssh -L 22352:127.0.0.1:22352 <ipc>`, then open <http://127.0.0.1:22352>.

Connections that the host makes to its own LAN address are routed through the loopback interface,
so local clients work regardless of whether they use `127.0.0.1` or the host address.

The rules live in their own nftables table (`inet wibu_codemeter`). Setting `wibu_packages_firewall`
to `false` removes the table, the rules and the unit again.

`wibu_packages_cm_bind_address` intentionally stays at `0.0.0.0`: binding CodeMeter to the loopback
interface would also cut off containers, because their traffic arrives on the bridge address.

### Interaction with other rulesets

The table is loaded by the `wibu-codemeter-firewall.service` unit, **not** by `nftables.service`:
`/etc/nftables.d/` is not a Debian convention, the directory belongs to this role. Loading the file
through the distribution's `/etc/nftables.conf` was rejected on purpose, because that file starts
with `flush ruleset` and would therefore drop the rules of Docker, Kubernetes and everyone else on
every reload.

Because the rules live in their own table, no other ruleset is touched and no other ruleset can
re-open the ports: a `drop` is final, while an `accept` only ends the evaluation of its own chain.
That also holds the other way round, which matters on hardened hosts:

- A `policy drop` in another table blocks the CodeMeter ports regardless of the rules of this role.
  On such a host, 22350 needs to be allowed in that ruleset as well, otherwise the license server
  stays unreachable.
- Anything that flushes the whole ruleset removes this table too, `nft flush ruleset` as well as
  `nftables.service`, which flushes through its config and on stop. The unit is ordered after that
  service so that a boot is safe, but a flush at runtime leaves the ports open until the role runs
  again or `systemctl reload wibu-codemeter-firewall` is called. Note that such a flush also drops
  the rules of Docker and Kubernetes, so it is not something to expect on a running IPC.

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
- name: Install WiBu packages without restricting access to the CodeMeter ports
  hosts: all
  vars:
    wibu_packages_firewall: false
  roles:
    - voraus.ipc_tools.wibu_packages
```

```yaml
- name: Allow an additional network to access the CodeMeter license server
  hosts: all
  vars:
    wibu_packages_firewall_licensing_interfaces:
      - lo
      - docker0
      - 'br-*'
      - eno1
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
