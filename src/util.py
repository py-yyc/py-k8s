import socket
import time

def read(filename):
    "Return contents of filename"
    with open(filename, 'r') as f:
        return f.read()

def try_connect_until_timeout(host, port, timeout=30, poll=0.1):
    """
    Attempt to connect to (host, port) and return the start of what is received
    from that socket. Keep trying until the timeout expires.
    """
    start_time = time.time()
    tries = 0
    response = None

    while time.time() - start_time < timeout:
        try:
            tries += 1
            with socket.socket() as sock:
                sock.settimeout(poll)
                sock.connect((host, port))
                response = sock.recv(128)
                break
        except Exception as e:
            print(f"Socket exception: {e}")
            time.sleep(poll)
    print(f'{tries} tries in {time.time() - start_time}s')
    return response

def replace_dict_values(input, **kwargs):
    """
    Return a copy of input, replacing string values according to kwargs. Input
    is processed recursively, and can contain nested dicts and lists,

    >>> replace_dict_values({'foo': 'bar'}, bar='baz')
    {'foo': 'baz'}
    """
    if type(input) == str:
        if input in kwargs:
            return kwargs[input]
        return input
    elif type(input) == dict:
        return dict((k, replace_dict_values(v, **kwargs)) for k, v in input.items())
    elif type(input) == list:
        return [replace_dict_values(e, **kwargs) for e in input]
    elif type(input) == int or type(input) == float:
        return input
    else:
        raise Exception(f'Don’t know how to replace {input!r}')

def test_replace_dict_values():
    assert replace_dict_values({
        "foo": "bar",
        "baz": {
            "qux": ["a", "bar", 1, 2.0]
        }
    }, bar='bar2') == {
        "foo": "bar2",
        "baz": {
            "qux": ["a", "bar2", 1, 2.0]
        }
    }

