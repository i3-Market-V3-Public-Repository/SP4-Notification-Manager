import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        current_ip = s.getsockname()[0]
    except Exception:
        current_ip = '127.0.0.1'
    finally:
        s.close()
    return current_ip
