import argparse


def parse():
    parser = argparse.ArgumentParser(
            description="Serve HTTP response."
            )
    parser.add_argument(
            "-s", "--server", 
            help="Select a server implementation.",
            choices=["Basic", "SelfSigned", "FlaskServer", "WSGI" ],
            default=None
            )
    parser.add_argument(
            "-a", "--addr",
            help="Set the IP address.",
            default=None
            )
    parser.add_argument(
            "-p", "--port",
            help="Set port number.",
            type=int,
            default=None
            )
    parser.add_argument(
            "-t", "--threads",
            help="Set the number of threads to serve from.",
            type=int,
            default=None
            )
    return parser.parse_args()
