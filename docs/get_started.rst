###############
Getting Started
###############

Requirements
************

This project uses `uv <https://docs.astral.sh/uv/>`_. It creates the virtual
environment, installs the Python version pinned in ``.python-version`` and
installs the exact dependency versions recorded in ``uv.lock``:

..  code-block:: shell

    uv sync --locked


Roles
*****

The collection currently contains the following roles, please refer to their individual documentation for more details:

.. toctree::
   :glob:
   :maxdepth: 1

   roles/wibu_packages/README
   roles/grub_config/README
   roles/realtime_kernel/README
   roles/core_isolation/README


Development
***********

In order to modify and test the roles locally, install the development dependencies as well:


..  code-block:: shell

    uv sync --locked --all-extras

Run the checks through tox, which installs each environment from ``uv.lock``:

..  code-block:: shell

    uv run --extra tox tox -e lint

After changing a dependency in ``pyproject.toml``, refresh the lockfile and commit
it, otherwise the ``--locked`` flag makes CI fail:

..  code-block:: shell

    uv lock
