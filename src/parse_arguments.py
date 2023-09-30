import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Fortune")
    parser.add_argument("-p", "--pigamma", action="store_true", help="enables Pi Gamma")
    parser.add_argument("--test", action="store_true", help="start only testing")
    parser.add_argument("--train", action="store_true", help="start only training")

    args = parser.parse_args()
    return vars(args)
