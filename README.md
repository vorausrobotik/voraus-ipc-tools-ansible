# voraus IPC Tools Ansible

[![CI](https://github.com/vorausrobotik/voraus-ipc-tools-ansible/actions/workflows/pipeline.yml/badge.svg)](https://github.com/vorausrobotik/voraus-ipc-tools-ansible/actions/workflows/pipeline.yml)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

voraus IPC related Ansible roles and tools.
This collection helps to set up a real-time system with all prerequisites to deploy the [voraus.core][1].

> [!NOTE]
> This collection and its roles are tested against [Debian 13 (trixie)][2], and might need modifications
> for other systems.

<br />

# Prerequisites

- An IPC running debian
- SSH root access to this IPC

# Quickstart

1. Create a Python virtual environment and install ansible and the collection

```bash
python3 -m venv venv
source venv/bin/activate
pip install ansible

# Install the collection
ansible-galaxy collection install voraus.ipc_tools
```

1. Copy the [example inventory][3] to a `inventory.yml` file and change it according to your needs.
   In this example, we assume that the IPC is reachable via the IP address `192.168.1.1`.

2. Run the [example playbook][4]
   shipped with the collection.

```bash
ansible-playbook voraus.ipc_tools.example -i inventory.yml
```

<br />

# Documentation

Please refer to the [official documentation](https://vorausrobotik.github.io/voraus-ipc-tools-ansible/).

<br />

[1]: https://vorausrobotik.com/produkte/#core
[2]: https://www.debian.org/releases/trixie/
[3]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/inventory.example.yml
[4]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/voraus/ipc_tools/playbooks/example.yml
