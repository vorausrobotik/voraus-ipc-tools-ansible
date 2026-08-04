from typing import Any

import pytest
from testinfra.host import Host
from testinfra.modules.package import Package

LICENSING_PORT = 22350
WEBADMIN_PORT = 22352
NFT_TABLE = "inet wibu_codemeter"
NFT_CONFIG_PATH = "/etc/nftables.d/wibu-codemeter.nft"
FIREWALL_SERVICE = "wibu-codemeter-firewall"
FIREWALL_UNIT_PATH = f"/etc/systemd/system/{FIREWALL_SERVICE}.service"
# The verifier runs the tests through sudo, `nft` is not in the connecting user's PATH though
NFT = "/usr/sbin/nft"


def firewall_enabled(host: Host) -> bool:
    return bool(host.ansible.get_variables()["wibu_packages_firewall"])


def firewall_probes(host: Host) -> list[dict[str, Any]]:
    return list(host.ansible.get_variables()["wibu_packages_firewall_probes"])


def probe_can_connect(host: Host, probe: dict[str, Any], port: int) -> bool:
    # Dropped packets make the connection attempt time out instead of being refused, so netcat
    # needs a timeout to not block forever.
    result = host.run("ip netns exec %s nc -z -w 2 %s %s", probe["namespace"], probe["host_address"], str(port))
    return result.rc == 0


@pytest.mark.parametrize(
    ("package_name", "package_version"),
    [("codemeter-lite", "9.10.8166.500"), ("axprotector", "11.80.8031.500")],
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


def test_firewall_rules_loaded(host: Host) -> None:
    ruleset = host.run(f"{NFT} list table {NFT_TABLE}")

    if not firewall_enabled(host):
        assert not host.file(NFT_CONFIG_PATH).exists
        assert not host.file(FIREWALL_UNIT_PATH).exists
        # Either nftables was never installed or the table is gone, both are acceptable
        assert ruleset.rc != 0, f"The '{NFT_TABLE}' table is still loaded although the firewall is disabled"
        return

    assert host.file(NFT_CONFIG_PATH).exists
    assert host.service(FIREWALL_SERVICE).is_enabled
    assert host.service(FIREWALL_SERVICE).is_running
    assert ruleset.rc == 0, f"The '{NFT_TABLE}' table is not loaded: {ruleset.stderr}"

    expected_rules = [
        # The licensing port is reachable from the host itself and from container bridges
        f'iifname "lo" tcp dport {LICENSING_PORT} accept',
        f'iifname "lo" udp dport {LICENSING_PORT} accept',
        f'iifname "docker0" tcp dport {LICENSING_PORT} accept',
        f'iifname "br-*" tcp dport {LICENSING_PORT} accept',
        f"tcp dport {LICENSING_PORT} drop",
        f"udp dport {LICENSING_PORT} drop",
        # WebAdmin is restricted to the host itself, containers included
        f'iifname "lo" tcp dport {WEBADMIN_PORT} accept',
        f"tcp dport {WEBADMIN_PORT} drop",
    ]
    for expected_rule in expected_rules:
        assert expected_rule in ruleset.stdout, f"Missing rule '{expected_rule}' in:\n{ruleset.stdout}"

    assert f'iifname "docker0" tcp dport {WEBADMIN_PORT} accept' not in ruleset.stdout


def test_licensing_port_reachable_from_localhost(host: Host) -> None:
    assert host.run("nc -z -w 2 127.0.0.1 %s", str(LICENSING_PORT)).rc == 0


def test_licensing_port_access(host: Host) -> None:
    for probe in firewall_probes(host):
        # Without the firewall every source may connect
        expected = probe["licensing_allowed"] or not firewall_enabled(host)
        connected = probe_can_connect(host, probe, LICENSING_PORT)
        assert connected == expected, (
            f"{probe['namespace']} (via {probe['interface']}) "
            f"{'could not' if expected else 'could'} reach port {LICENSING_PORT}"
        )


def test_webadmin_port_not_reachable_from_remote_sources(host: Host) -> None:
    # Only meaningful while the firewall is enabled: without it the result depends on whether the
    # installed CodeMeter variant serves WebAdmin at all.
    if not firewall_enabled(host):
        pytest.skip("The firewall is disabled on this host")

    for probe in firewall_probes(host):
        assert not probe_can_connect(
            host, probe, WEBADMIN_PORT
        ), f"{probe['namespace']} (via {probe['interface']}) could reach port {WEBADMIN_PORT}"
