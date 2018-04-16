#   Primary Author: Anuj Khare <khareanuj18@gmail.com>
from argparse import ArgumentParser

from raft.node import Leader, Follower, States


def setup_arguments() -> 'ArgumentParser':
    parser = ArgumentParser()
    parser.add_argument('-s', '--state', action='store', dest='state', help='leader/follower/dead', default='follower')
    return parser


if __name__ == '__main__':
    # Set-up the command line arguments
    parser = setup_arguments()
    parsed_args = parser.parse_args()

    state = parsed_args.state

    print(state)
    node = None
    if state == 'leader':
        node = Leader()
    elif state == 'follower':
        node = Follower()

    print(node)
