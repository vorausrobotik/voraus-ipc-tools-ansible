from testinfra.host import Host


def test_expected_kernel_params(host: Host) -> None:
    """Test that expected kernel parameters are present with correct values."""
    cmdline = host.run("cat /proc/cmdline")
    assert cmdline.rc == 0, "Failed to read /proc/cmdline"

    kernel_parameters = cmdline.stdout.strip().split()
    kernel_parameter_dict = {}

    for param in kernel_parameters:
        if "=" in param:
            key, value = param.split("=", 1)
        else:
            key = param
            value = None

        if key in kernel_parameter_dict:
            raise AssertionError(f"Kernel param '{key}' defined multiple times in {kernel_parameters}")

        kernel_parameter_dict[key] = value

    # Get expected parameters from host variables
    host_variables = host.ansible.get_variables()
    expected_params_dict = host_variables.get("expected_cmdline_params", {})

    # Verify all expected parameters are present with correct values
    for expected_key, expected_value in expected_params_dict.items():
        assert expected_key in kernel_parameter_dict, (
            f"Expected param '{expected_key}' not found in kernel cmdline. "
            f"Available params: {list(kernel_parameter_dict.keys())}"
        )

        actual_value = kernel_parameter_dict[expected_key]
        assert (
            actual_value == expected_value
        ), f"Parameter '{expected_key}': expected value '{expected_value}', but got '{actual_value}'"
