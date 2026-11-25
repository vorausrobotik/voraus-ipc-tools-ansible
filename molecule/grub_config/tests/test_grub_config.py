from testinfra.host import Host

from ...shared.test_utils import assert_kernel_params

GRUB_COMMON_DROP_IN = "/etc/systemd/system/grub-common.service.d/boot-read-only.conf"


def test_expected_kernel_params(host: Host) -> None:
    """Test that expected kernel parameters are present with correct values."""
    host_variables = host.ansible.get_variables()
    assert_kernel_params(host=host, expected_params=host_variables.get("expected_cmdline_params", {}))


def test_grub_common_drop_in(host: Host) -> None:
    """Test that the drop-in makes grub-common.service depend on a writable /boot/grub."""
    drop_in = host.file(GRUB_COMMON_DROP_IN)
    assert drop_in.exists
    assert drop_in.user == "root"
    assert drop_in.mode == 0o644
    assert "ConditionPathIsReadWrite=/boot/grub" in drop_in.content_string.splitlines()


def test_grub_common_service(host: Host) -> None:
    """Test that grub-common.service is skipped on a read-only /boot/grub and runs otherwise."""
    boot_read_only = host.ansible.get_variables().get("grub_config_test_boot_read_only", False)

    # The unit runs only at boot, so start it once to evaluate the current state
    with host.sudo():
        host.run_expect([0], "systemctl start grub-common.service")
        properties = host.check_output(
            "systemctl show grub-common.service --property=ConditionResult,Result,ActiveState"
        )

    state = dict(line.split("=", 1) for line in properties.splitlines())
    assert state["ConditionResult"] == ("no" if boot_read_only else "yes")
    assert state["Result"] == "success"
    assert state["ActiveState"] != "failed"
