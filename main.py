import collector
import sys


def get_flags():
    out = {"filter": False, "fake_send": False, "immediate_send": False, "collect": False, "send": False, "pass": 7}
    args = sys.argv[1:]
    for idx, arg in enumerate(args):
        if arg == "-f":
            out["filter"] = True
        elif arg == "-fs":
            out["fake_send"] = True
        elif arg == "-i":
            out["immediate_send"] = True
        elif arg == "-c":
            out["collect"] = True
        elif arg == "-s":
            out["send"] = True
        elif arg == "-p":
            out["pass"] = args[idx+1]
    return out


if __name__ == '__main__':
    flags = get_flags()
    # print(flags)
    if not flags["send"]:
        collector.collect(flags["pass"], flags)
    if not flags["collect"]:
        collector.do_send(flags)
