#!/bin/bash
# Setup Ansible environment variables for molecule with vagrant plugins
# This script dynamically detects the active Python environment and sets the required paths
# Required because of https://github.com/ansible/molecule/pull/4380

# Detect Python site-packages path
if command -v python &> /dev/null; then
    PYTHON_LIB_PATH=$(python -c "import sys; print(f'{sys.prefix}/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages')")
else
    echo "Error: Python not found in PATH" >&2
    exit 1
fi

# Export Ansible environment variables
export ANSIBLE_REMOTE_TMP="${ANSIBLE_REMOTE_TMP:-/var/tmp/${USER}/ansible}"
export ANSIBLE_FILTER_PLUGINS="${PYTHON_LIB_PATH}/molecule/provisioner/ansible/plugins/filter:${HOME}/.ansible/plugins/filter:/usr/share/ansible/plugins/filter"
export ANSIBLE_LIBRARY="${PYTHON_LIB_PATH}/molecule/provisioner/ansible/plugins/modules:${PYTHON_LIB_PATH}/molecule_plugins/vagrant/modules:${HOME}/.ansible/plugins/modules:/usr/share/ansible/plugins/modules"

echo "Ansible environment configured:"
echo "  PYTHON_LIB_PATH: ${PYTHON_LIB_PATH}"
echo "  ANSIBLE_LIBRARY: ${ANSIBLE_LIBRARY}"
echo "  ANSIBLE_FILTER_PLUGINS: ${ANSIBLE_FILTER_PLUGINS}"
echo "  ANSIBLE_REMOTE_TMP: ${ANSIBLE_REMOTE_TMP}"
