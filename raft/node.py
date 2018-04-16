#   Primary Author: Anuj Khare <khareanuj18@gmail.com>
class States:
    Follower = 1
    Leader = 2
    Dead = -1


class Node:
    def __init__(self, state: int = States.Follower) -> None:
        self.state = state


class Leader(Node):
    def heartbeat(self) -> None:
        """
        Tell the followers that he is still alive!
        """
        pass

    def __init__(self) -> None:
        super().__init__(state=States.Leader)
        print('A Leader was set-up!')


class Follower(Node):
    def __init__(self) -> None:
        super().__init__(state=States.Leader)
        print('A Follower was set-up!')
