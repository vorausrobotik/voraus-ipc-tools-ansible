import re

from testinfra.host import Host


def test_only_realtime_kernel_is_installed(host: Host) -> None:
    menuentry_pattern = r"^\s*linux\s+.*(?P<kernel>vmlinuz-[\.\d-]*-rt[^\s]+)"
    grub_cfg_cmd = host.run("cat /boot/grub/grub.cfg")
    assert grub_cfg_cmd.rc == 0
    menu_entries = list(re.finditer(pattern=menuentry_pattern, string=grub_cfg_cmd.stdout, flags=re.MULTILINE))
    assert len(menu_entries) > 0, "No menu entries found in grub configuration."
    for match in menu_entries:
        assert "rt-amd64" in match.group("kernel")


def test_realtime_kernel_is_loaded(host: Host) -> None:
    kernel_cmd = host.run("uname -r")
    assert kernel_cmd.rc == 0
    assert kernel_cmd.stdout.strip().endswith(
        "rt-amd64"
    ), f"Loaded kernel is not a realtime kernel: {kernel_cmd.stdout}"
