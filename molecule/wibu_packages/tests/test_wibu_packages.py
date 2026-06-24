import pytest
from testinfra.host import Host
from testinfra.modules.package import Package


@pytest.mark.parametrize(
    ("package_name", "package_version"),
    [("codemeter-lite", "9.0.8031.500"), ("axprotector", "11.80.8031.500")],
)
def test_packages_installed(package_name: str, package_version: str, host: Host) -> None:
    package: Package = host.package(package_name)
    assert package.is_installed
    assert package.version == package_version


def test_codemeter_listens(host: Host) -> None:
    # https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.socket.Socket.is_listening
    # If you don’t specify a host for udp and tcp sockets, then the socket is listening if and only if the socket
    # listens on both all ipv4 and ipv6 addresses (ie 0.0.0.0 and ::)
    assert host.socket("tcp://22350").is_listening


def test_old_repo_and_key_removed(host: Host) -> None:
    # The role must clean up the rotated-out wibu repo and GPG key, including on
    # machines that were previously provisioned with them.
    assert not host.file("/usr/share/keyrings/wibu-package-maintainers.gpg").exists
    assert not host.file("/etc/apt/sources.list.d/voraus-wibu.list").exists
