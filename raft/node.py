#   Primary Author: Anuj Khare <khareanuj18@gmail.com>
from concurrent import futures
from typing import List
import argparse
import asyncio
import enum
import grpc
import time

from raft.protos import raft_pb2_grpc, raft_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class States(enum.Enum):
    Follower = 1
    Leader = 2
    Dead = 3


class FollowerNode(raft_pb2_grpc.NodeServicer):
    def __init__(self, state: int = States.Follower.value, timeout_in_sec: int = 10) -> None:
        self.state = state

        self.current_term = 0
        self.voted_for = None
        self.log = None
        print('A Follower was set-up!')

        # For the internal time-outs
        self.timeout_in_sec = timeout_in_sec
        self.check_interval_in_sec = 1

        # Initialize the last-heard from the server
        self.last_heard = time.monotonic()

    def AppendEntries(self, request, context) -> None:
        if not request.entries:
            print('heartbeat received!')
            self._record_heartbeat()
        return raft_pb2.AppendEntryReply()

    async def start(self) -> None:
        while True:
            await asyncio.sleep(self.check_interval_in_sec)
            current_time = time.monotonic()
            elapsed_in_sec = current_time - self.last_heard
            print('checking', elapsed_in_sec)
            if elapsed_in_sec >= self.timeout_in_sec:
                print('I timed out!!')
                raise TimeoutError('timed out!')

    def _record_heartbeat(self) -> None:
        self.last_heard = time.monotonic()


class LeaderNode(FollowerNode):
    def __init__(self, follower_ports: List[int], heartbeat_interval: int = 3) -> None:
        super().__init__(state=States.Leader.value)
        print('A Leader was set-up!')
        self.heartbeat_interval = heartbeat_interval
        self.follower_ports = follower_ports

    async def send_heartbeat(self) -> None:
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            for port in self.follower_ports:
                with grpc.insecure_channel('localhost:{}'.format(port)) as channel:
                    node_stub = raft_pb2_grpc.NodeStub(channel)
                    _ = node_stub.AppendEntries(request=raft_pb2.AppendEntryRequest())


def serve_follower(port_no: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    waiter = FollowerNode(timeout_in_sec=10)
    raft_pb2_grpc.add_NodeServicer_to_server(
        waiter, server
    )
    server.add_insecure_port('[::]:{}'.format(port_no))
    server.start()

    try:

        loop = asyncio.new_event_loop()
        tasks = [
            waiter.start(),
        ]

        # FIXME: I am not actually sure what having futures ThreadPool and asyncio loop together means, need to figure
        loop.run_until_complete(asyncio.wait(tasks))  # FIXME: figure out the exception handling for this
    except KeyboardInterrupt:
        server.stop(0)


def serve_leader(port_no, follower_ports):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    leader = LeaderNode(follower_ports=follower_ports)
    raft_pb2_grpc.add_NodeServicer_to_server(
        leader, server
    )
    server.add_insecure_port('[::]:{}'.format(port_no))
    server.start()

    try:
        loop = asyncio.new_event_loop()
        tasks = [
            leader.send_heartbeat()
        ]
        loop.run_until_complete(asyncio.wait(tasks))  # FIXME: figure out the exception handling for this
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='The port of the node', type=int, required=True)
    parser.add_argument('-s', '--state', help='The state of the node: leader/follower', type=str, default='follower')
    parser.add_argument('-f', '--follower-ports', help='The comma separated ports of the follower nodes', type=str)

    args = parser.parse_args()
    if args.state == 'leader':
        if not args.follower_ports:
            raise ValueError

        follower_ports = args.follower_ports.split(',')
        print(follower_ports)
        serve_leader(port_no=args.port, follower_ports=follower_ports)

    elif args.state == 'follower':
        serve_follower(port_no=args.port)


