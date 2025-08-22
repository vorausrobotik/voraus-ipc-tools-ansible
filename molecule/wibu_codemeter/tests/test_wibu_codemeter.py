from testinfra.host import Host


def test_codemeter_listens(host: Host) -> None:
    # https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.socket.Socket.is_listening
    # If you don’t specify a host for udp and tcp sockets, then the socket is listening if and only if the socket
    # listens on both all ipv4 and ipv6 addresses (ie 0.0.0.0 and ::)
    assert host.socket("tcp://22350").is_listening
