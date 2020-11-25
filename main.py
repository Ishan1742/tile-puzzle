from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
import copy

expanded_nodes = 0


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class node:
    h = 0
    g = 0
    f = 0
    tile = ""
    neighbours = []
    selfptr = None
    parent = None

    def __init__(self, h, g, f, tile, selfptr, parent):
        self.h = h
        self.g = g
        self.f = f
        self.tile = tile
        self.neighbours = []
        self.selfptr = selfptr
        self.parent = parent

    def heuristic_B_location(self):
        blocs = 0
        for i in range(7):
            if self.tile[i] == 'B':
                blocs += i

        return 12 - blocs

    def heuristic_misplaced_tiles(self):
        wnos = 0
        for i in range(7):
            if self.tile[i] == '_':
                continue
            elif self.tile[i] == 'W':
                wnos += 1

        return 2 * wnos

    def find_successor(self, priority_queue, explored_states, unexplored_states, heuristic):
        global expanded_nodes
        pos = self.tile.find('_')
        node_found = False

        temp_nodes = []
        for i in range(6):
            new_node = node(self.h, self.g, self.f, self.tile, self.selfptr, self.parent)
            new_node.selfptr = new_node
            temp_nodes.append(new_node)

        curr_node = -1
        curr_pos = pos
        for curr_pos in range(curr_pos - 3, pos + 3 + 1):
            if ((curr_pos != pos) and (curr_pos >= 0 and curr_pos <= 6)):
                curr_node += 1
                strlist = list(temp_nodes[curr_node].tile)
                strlist[pos] = strlist[curr_pos]
                strlist[curr_pos] = '_'
                temp_nodes[curr_node].tile = "".join(strlist)

                if heuristic == 1:
                    temp_nodes[curr_node].h = temp_nodes[curr_node].heuristic_misplaced_tiles(
                    )
                else:
                    temp_nodes[curr_node].h = temp_nodes[curr_node].heuristic_B_location()

                if abs(pos - curr_pos) == 1:
                    temp_nodes[curr_node].g = 1
                else:
                    temp_nodes[curr_node].g = abs(pos - curr_pos) - 1
                temp_nodes[curr_node].f = temp_nodes[curr_node].g + \
                    temp_nodes[curr_node].h

                for obj in explored_states:
                    if obj.tile == temp_nodes[curr_node].tile:
                        node_found = True
                        break

                for obj in unexplored_states:
                    if obj.tile == temp_nodes[curr_node].tile and obj.f <= temp_nodes[curr_node].f:
                        node_found = True
                        break

                if node_found:
                    node_found = False
                    continue

                temp_nodes[curr_node].parent = self.selfptr
                print(f"**: {temp_nodes[curr_node].tile} {temp_nodes[curr_node].f} {temp_nodes[curr_node].g} {temp_nodes[curr_node].h}")
                unexplored_states.append(temp_nodes[curr_node])
                priority_queue.put(PrioritizedItem(
                    temp_nodes[curr_node].f, temp_nodes[curr_node]))
                self.neighbours.append(temp_nodes[curr_node])
                expanded_nodes += 1

        return priority_queue, explored_states, unexplored_states

    def display_predecessors(self):
        curr_node = self
        path = []
        while curr_node.parent != None:
            path.append(curr_node.tile)
            curr_node = curr_node.parent

        print("Path:")
        for i in reversed(path):
            print(i)


def main():
    global expanded_nodes
    expanded_nodes = 0
    goal_set = {"WBBB", "_BBB", "B_BB", "BB_B", "BBB_"}
    print("Enter Valid Input:")
    print("Example Input: 'BBB_WWW'")
    input_str = input()
    input_str = "BBB_WWW"
    print("Enter Heuristic Type:")
    print("1. Misplaced Tiles")
    print("2. Location of B")
    heuristic_type = int(input())

    root_node = node(6, 0, 6, input_str, None, None)
    root_node.selfptr = root_node
    if heuristic_type == 2:
        root_node.h = 12
        root_node.f = 12

    pq = PriorityQueue()
    explored_states = []
    unexplored_states = []
    pq.put(PrioritizedItem(root_node.f, root_node))
    expanded_nodes += 1

    while not pq.empty():
        curr_node = pq.queue[0].item
        print(f"Popped: {curr_node.tile} {curr_node.f} {curr_node.g} {curr_node.h}")
        for goal in goal_set:
            if curr_node.tile.find(goal, 3) != -1:
                print(curr_node.tile.find(goal))
                if curr_node.f <= pq.queue[0].item.f:
                    pq.get()
                    print("Goal")
                    curr_node.display_predecessors()
                    explored_states.clear()
                    unexplored_states.clear()
                    while not pq.empty():
                        pq.get()
                    exit()
                else:
                    pq.get()
                    pq.put(PrioritizedItem(curr_node.f, curr_node))
                    expanded_nodes += 1

        explored_states.append(curr_node)
        pq.get()
        pq, explored_states, unexplored_states = curr_node.find_successor(
            pq, explored_states, unexplored_states, heuristic_type)


main()
# if __name__ == "__main__":
#     expanded_nodes = 0
#     main()
