from testinfra.host import Host

DROP_IN = "/etc/systemd/network/99-default.link.d/10-no-onboard-names.conf"
# The initramfs hook copies the link files from /etc to /usr/lib, and lsinitramfs lists them without a leading slash
INITRAMFS_DROP_IN = "usr/lib/systemd/network/99-default.link.d/10-no-onboard-names.conf"


def test_drop_in(host: Host) -> None:
    """Test that the drop-in leaves the firmware-provided names out of the naming policy."""
    drop_in = host.file(DROP_IN)
    assert drop_in.exists
    assert drop_in.user == "root"
    assert drop_in.mode == 0o644
    assert "NamePolicy=keep kernel database path" in drop_in.content_string.splitlines()


def test_drop_in_in_initramfs(host: Host) -> None:
    """Test that the initramfs of the running kernel contains the drop-in."""
    kernel = host.check_output("uname -r")
    with host.sudo():
        content = host.check_output(f"lsinitramfs /boot/initrd.img-{kernel}")
    assert INITRAMFS_DROP_IN in content.splitlines()


def test_drop_in_applied(host: Host) -> None:
    """Test that udev applies the drop-in to an interface that only the default link file matches."""
    # The NIC of the test VM matches a netplan link file instead, unlike the NICs of the IPCs
    interface = "nicnamingtest"
    with host.sudo():
        host.run_expect([0], f"ip link add {interface} type dummy")
        try:
            output = host.check_output(f"udevadm test-builtin net_setup_link /sys/class/net/{interface} 2>&1")
        finally:
            host.run_expect([0], f"ip link delete {interface}")
    assert f"ID_NET_LINK_FILE_DROPINS={DROP_IN}" in output.splitlines()


def test_boot_mount_restored(host: Host) -> None:
    """Test that /boot is read-only again if it was read-only before."""
    boot_read_only = host.ansible.get_variables().get("nic_naming_test_boot_read_only", False)
    expected_rc = 0 if boot_read_only else 1
    host.run_expect([expected_rc], "findmnt --mountpoint /boot --options ro")
