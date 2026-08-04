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

1. Install ansible and the collection. This pulls in the `ansible.posix` and
   `community.general` collections that this collection depends on.

```bash
uv tool install ansible-core

ansible-galaxy collection install voraus.ipc_tools
```

2. Copy the [example inventory][3] to a `inventory.yml` file and change it according to your needs.
   In this example, we assume that the IPC is reachable via the IP address `192.168.1.1`.

3. Run the [example playbook][4]
   shipped with the collection.

```bash
ansible-playbook voraus.ipc_tools.example -i inventory.yml
```

<br />

# Documentation

Please refer to the [official documentation](https://vorausrobotik.github.io/voraus-ipc-tools-ansible/).

<br />

# Development

This project is managed with [uv][5]. The following creates `.venv`, installs the Python version pinned in
`.python-version` and installs the exact dependency versions recorded in `uv.lock`:

```bash
uv sync --locked --all-extras
source .venv/bin/activate
```

All checks run through tox. Each tox environment is installed from `uv.lock` as well, so local runs and CI use
identical package versions.

| Command        | Purpose                                                           |
| -------------- | ----------------------------------------------------------------- |
| `tox -e lint`  | ansible-lint, prettier, isort, black, mypy, ruff, pylint and doc8 |
| `tox -e docs`  | Run the doctests and build the Sphinx docs into `docs/build/html` |
| `tox -e build` | Build the collection tarball                                      |
| `tox -e test`  | Run the molecule test suite, see below                            |

Without activating the environment, prefix the commands with `uv run --all-extras`, for example
`uv run --all-extras tox -e lint`.

After changing a dependency in `pyproject.toml`, refresh the lockfile and commit the result. CI installs with
`--locked` and fails on a stale `uv.lock`:

```bash
uv lock
```

## Molecule tests

`tox -e test` is intended for local use only. CI runs molecule per role in [`test.yml`][6], because every
scenario boots a virtual machine and needs root privileges on the runner. Locally, `vagrant` and `libvirt` have to be
available on the host.

```bash
# Run every scenario
tox -e test

# Run a single scenario
tox -e test -- test -s grub_config
```

## Releasing

Releases are cut by [release-please][7]. It keeps a release pull request open that collects every
[Conventional Commit][8] merged into `main`, and derives the next version from those commit types. Merging that pull
request is the release:

1. `CHANGELOG.md`, `voraus/ipc_tools/galaxy.yml`, `pyproject.toml` and `uv.lock` are bumped to the same version.
2. The `X.Y.Z` tag and the GitHub release are created.
3. The tag triggers [`pipeline.yml`][9], which publishes the collection to Ansible Galaxy and the docs to GitHub Pages.

Nothing is tagged or published by hand, so the only thing that decides the next version is the commit history. The
sections of the changelog are configured in [`release-please-config.json`][10].

<br />

[1]: https://vorausrobotik.com/produkte/#core
[2]: https://www.debian.org/releases/trixie/
[3]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/inventory.example.yml
[4]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/voraus/ipc_tools/playbooks/example.yml
[5]: https://docs.astral.sh/uv/
[6]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/.github/workflows/test.yml
[7]: https://github.com/googleapis/release-please
[8]: https://www.conventionalcommits.org/en/v1.0.0/
[9]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/.github/workflows/pipeline.yml
[10]: https://github.com/vorausrobotik/voraus-ipc-tools-ansible/blob/main/release-please-config.json
