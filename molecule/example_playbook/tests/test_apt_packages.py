import pytest
from testinfra.host import Host


@pytest.mark.parametrize(
    "package",
    [
        "htop",
        "ncdu",
        "zip",
        "unzip",
        "curl",
        "wget",
        "less",
        "nano",
        "gnupg2",
        "nmap",
        "tcpdump",
        "docker-ce",
        "docker-ce-cli",
        "docker-compose-plugin",
    ],
)
def test_apt_packages(package: str, host: Host) -> None:
    assert host.package(package).is_installed
