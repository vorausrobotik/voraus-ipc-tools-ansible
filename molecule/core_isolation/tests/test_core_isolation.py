import pytest
from testinfra.host import Host


@pytest.mark.parametrize(
    ("unit_name", "section_type"),
    [
        ("init.scope", "Scope"),
        ("system.slice", "Slice"),
        ("user.slice", "Slice"),
    ],
)
def test_systemd_cpu_isolation_config(host: Host, unit_name: str, section_type: str) -> None:
    """Test that the CPU isolation config file exists with correct content."""
    config_file = host.file(f"/etc/systemd/system/{unit_name}.d/50-cpu_isolation.conf")
    assert config_file.exists
    assert config_file.is_file
    assert config_file.mode == 0o644
    assert f"[{section_type}]" in config_file.content_string
    assert "AllowedCPUs=0,2" in config_file.content_string


def test_environment_variable_is_set(host: Host) -> None:
    """Test that VRT_COREISOLATION__IDS is set in /etc/environment."""
    env_file = host.file("/etc/environment")
    assert env_file.exists
    assert "VRT_COREISOLATION__IDS=[1,3]" in env_file.content_string


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
