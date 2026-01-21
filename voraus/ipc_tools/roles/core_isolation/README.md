# voraus.ipc_tools.core_isolation

This role configures CPU core isolation to enable deterministic execution of realtime applications on Linux systems.
By isolating specific CPU cores from general system and user processes, it creates a dedicated environment for
time-critical workloads such as robotic control systems, industrial automation, and realtime network communication.

**Key Features:**

- **CPU Core Isolation**: Isolates specified CPU cores using the `isolcpus` kernel parameter, preventing the scheduler
  from assigning regular system tasks and user processes to these cores.
- **IRQ Affinity Management**: Automatically configures interrupt request (IRQ) affinity to route system interrupts
  away from isolated cores, minimizing latency and jitter.
- **Network Interface Pinning**: Optionally pins network interface IRQ threads to specific CPU cores,
  enabling deterministic realtime network communication.
- **RCU Offloading**: Offloads Read-Copy-Update (RCU) callbacks from isolated cores using
  `rcu_nocbs` and `rcu_nocb_poll` kernel parameters.
- **Environment Variable Export**: Exports isolated core IDs and network interface pinning configuration
  to `/etc/environment` for easy access by applications.

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
    core_isolation_isolated_core_ids: 1,3,4,5,12,21
    core_isolation_isolated_network_interfaces:
      eno1: 3
      enp6s0f0: 4
    core_isolation_enable_nomodeset: true
  roles:
    - voraus.ipc_tools.core_isolation
```

```{warning}
It is not recommended to isolate CPU 0. It should be available for the OS and housekeeping tasks.
```

For this example playbook, the following environment variables are exported system-wide:

- `VRT_INTERFACE_PINNING__eno1=[3]`
- `VRT_INTERFACE_PINNING__enp6s0f0=[4]`
- `VRT_COREISOLATION__IDS=[1,3,4,5,12,21]`
