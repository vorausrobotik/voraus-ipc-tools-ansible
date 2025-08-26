# voraus.ipc_tools.realtime_kernel

Installs a realtime kernel on the host.

## Requirements

Currently we only support 64-bit systems.

## Role Variables

None.

## Dependencies

None.

## Example Playbook

.. code-block:: yaml

- hosts: servers
  collections:
  - voraus.ipc_tools
    roles:
  - voraus.ipc_tools.realtime_kernel
