import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Fortune')
    parser.add_argument('-p', '--pigamma', action='store_true', help='enables Pi Gamma')

    args = parser.parse_args()
    return vars(args)
