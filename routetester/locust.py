import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='Run Locust for stress testing', usage="%(prog)s [--mode MODE] [--testfile TESTFILE] [locust arguments]", add_help=False)
    parser.add_argument('--testfile', help='Test file')
    parser.add_argument('--mode', help='Planner: otp or valhalla', default='otp')
    args, unknownargs = parser.parse_known_args()

    locusfile = None
    if args.mode == "otp":
        locustfile = os.path.join(os.path.split(__file__)[0], "locust_otp.py")
    elif args.mode == "valhalla":
        locustfile = os.path.join(os.path.split(__file__)[0], "locust_valhalla.py")
    else:
        print("Unknown planner: %s"%args.mode)
        sys.exit(1)

    env = os.environ
    if args.testfile:
        env['LOCUST_TESTFILE'] = args.testfile
    cmd = ['locust', '-f', locustfile] + unknownargs
    os.execvpe('locust', cmd, env)

if __name__ == "__main__":
    main()