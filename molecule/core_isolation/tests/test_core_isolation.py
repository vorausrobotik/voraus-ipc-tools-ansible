import pytest
from testinfra.host import Host

from ...shared.test_utils import assert_kernel_params


def test_expected_kernel_params(host: Host) -> None:
    # Get expected parameters from host variables
    host_variables = host.ansible.get_variables()
    assert_kernel_params(host=host, expected_params=host_variables.get("expected_cmdline_params", {}))


def test_environment_variables_are_set(host: Host) -> None:
    env_file = host.file("/etc/environment")
    expected_variables = host.ansible.get_variables().get("expected_environment_variables", {})
    assert env_file.exists
    for expected_variable in expected_variables:
        assert expected_variable in env_file.content_string


@pytest.mark.parametrize(
    ("shell_cmd", "description"),
    [
        ("su - vagrant -c 'echo $VRT_COREISOLATION__IDS'", "login shell (su -)"),
        ("su vagrant -c 'bash -c \"echo \\$VRT_COREISOLATION__IDS\"'", "non-interactive shell"),
        ("su vagrant -c 'bash -i -c \"echo \\$VRT_COREISOLATION__IDS\"'", "interactive shell"),
    ],
)
def test_environment_variable_in_shell_session(host: Host, shell_cmd: str, description: str) -> None:
    """Test that VRT_COREISOLATION__IDS is available in different shell types.

    Ansible's connection doesn't go through PAM like a regular SSH login,
    so we use 'su' to create new sessions that trigger PAM to load /etc/environment.
    """
    result = host.run(shell_cmd)
    assert result.rc == 0, f"Command failed for {description}: {result.stderr}"
    assert result.stdout.strip() == "[1,3]", f"Unexpected value in {description}: got '{result.stdout.strip()}'"
