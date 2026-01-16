###############
Getting Started
###############

Requirements
************

Create a python3 virtual environment and install the dependencies:

..  code-block:: shell

    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip tox && pip install .


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

    source venv/bin/activate
    pip install --upgrade ".[dev]"
