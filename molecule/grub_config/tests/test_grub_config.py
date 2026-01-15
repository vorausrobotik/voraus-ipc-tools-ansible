from testinfra.host import Host

from ...shared.test_utils import assert_kernel_params


def test_expected_kernel_params(host: Host) -> None:
    """Test that expected kernel parameters are present with correct values."""
    host_variables = host.ansible.get_variables()
    assert_kernel_params(host=host, expected_params=host_variables.get("expected_cmdline_params", {}))
