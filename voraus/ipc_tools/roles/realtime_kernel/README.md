# voraus.ipc_tools.realtime_kernel

Installs a realtime kernel on the host.

## Requirements

None.

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
