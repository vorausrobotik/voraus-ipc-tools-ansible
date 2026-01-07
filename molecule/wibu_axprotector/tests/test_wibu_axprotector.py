from testinfra.host import Host
from testinfra.modules.package import Package


def test_axprotector_is_installed(host: Host) -> None:
    package: Package = host.package("axprotector")
    assert package.is_installed
    assert package.version == "11.70.7131.502"
