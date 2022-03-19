import collector
import sys


def get_flags():
    out = {"filter": False, "fake_send": False, "immediate_send": False}
    args = sys.argv[1:]
    for arg in args:
        if arg == "-f":
            out["filter"] = True
        elif arg == "-fs":
            out["fake_send"] = True
        elif arg == "-i":
            out["immediate_send"] = True
    return out


if __name__ == '__main__':
    flags = get_flags()
    collector.collect(6)
    collector.do_send()
