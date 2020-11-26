import sys
import heapq
import logging
from tqdm import tqdm
from itertools import permutations
import matplotlib.pyplot as plt

MAX_VALUE = sys.maxsize
BOLD = '\033[1m'
END = '\033[0m'
logging.basicConfig(filename='output.log', level=logging.INFO)
logging.info("=================================================")
logging.info("\n\n")


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def pop(self):
        return heapq.heappop(self.queue)

    def remove(self, node_id):
        self.queue.pop(node_id)
        heapq.heapify(self.queue)

    def __iter__(self):
        return iter(sorted(self.queue))

    def __str__(self):
        return 'PQ:%s' % self.queue

    def append(self, node):
        heapq.heappush(self.queue, node)

    def __contains__(self, key):
        return key in [n for _, n in self.queue]

    def __eq__(self, other):
        return self.queue == other.queue

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def top(self):
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return 0, None


def uniform_cost_search(start, goalset):
    path = []
    explored_nodes = list()

    if start in goalset:
        path.append(start)
        return path, explored_nodes, 0
    # for goal in goalset:
    #     if start.find(goal, 3) != -1:
    #         path.append(start)
    #         return path, explored_nodes, 0

    path.append(start)
    path_cost = 0

    frontier = [(path_cost, path)]
    while len(frontier) > 0:
        path_cost_till_now, path_till_now = pop_frontier(frontier)
        current_node = path_till_now[-1]
        explored_nodes.append(current_node)

        if current_node in goalset:
            return path_till_now, explored_nodes, path_cost_till_now
        # for goal in goalset:
        #     if current_node.find(goal, 3) != -1:
        #         return path_till_now, explored_nodes, path_cost_till_now

        logging.debug(
            f"Popped: {current_node} g: {path_cost_till_now}")

        pos = current_node.find('_')
        for curr_pos in range(pos - 3, pos + 3 + 1):
            if curr_pos != pos and (curr_pos >= 0 and curr_pos <= 6):
                strlist = list(current_node)
                strlist[pos] = strlist[curr_pos]
                strlist[curr_pos] = '_'
                neighbour = "".join(strlist)

                path_to_neighbour = path_till_now.copy()
                path_to_neighbour.append(neighbour)
                extra_cost = 1 if abs(
                    pos - curr_pos) == 1 else (abs(pos - curr_pos) - 1)
                neighbour_cost = extra_cost + path_cost_till_now
                new_element = (neighbour_cost, path_to_neighbour)

                logging.debug(f"{neighbour} g: {neighbour_cost}")

                is_there, indexx, neighbour_old_cost, _ = get_frontier_params_new(
                    neighbour, frontier)

                if (neighbour not in explored_nodes) and not is_there:
                    frontier.append(new_element)
                elif is_there:
                    if neighbour_old_cost > neighbour_cost:
                        frontier.pop(indexx)
                        frontier.append(new_element)
        logging.debug("\n")

    return None, None, -1


def get_white_heuristic(current):
    wnos = 0
    for i in range(7):
        if current[i] == 'B':
            for j in range(i, 7):
                if current[j] == 'W':
                    wnos += 1
    return wnos


def get_misplaced_heuristic(current):
    wnos = 0
    for i in range(3, 7):
        if current[i] == '_':
            continue
        elif current[i] == 'W':
            wnos += 1

    return 2 * wnos


def astar_search(start, goalset):
    path = []
    explored_nodes = list()

    if start in goalset:
        path.append(start)
        return path, explored_nodes, 0
    # for goal in goalset:
    #     if start.find(goal, 3) != -1:
    #         path.append(start)
    #         return path, explored_nodes, 0

    path.append(start)
    path_cost = get_white_heuristic(start)
    frontier = [(path_cost, path)]
    while len(frontier) > 0:
        path_cost_till_now, path_till_now = pop_frontier(frontier)
        current_node = path_till_now[-1]
        logging.debug(
            f"Popped: {current_node} f: {path_cost_till_now} g: " +
            f"{path_cost_till_now - get_white_heuristic(current_node)} h: {get_white_heuristic(current_node)}")
        path_cost_till_now = (path_cost_till_now -
                              get_white_heuristic(current_node))
        explored_nodes.append(current_node)

        if current_node in goalset:
            return path_till_now, explored_nodes, path_cost_till_now
        # for goal in goalset:
        #     if current_node.find(goal, 3) != -1:
        #         return path_till_now, explored_nodes, path_cost_till_now

        pos = current_node.find('_')
        for curr_pos in range(pos - 3, pos + 3 + 1):
            if curr_pos != pos and (curr_pos >= 0 and curr_pos <= 6):
                strlist = list(current_node)
                strlist[pos] = strlist[curr_pos]
                strlist[curr_pos] = '_'
                neighbour = "".join(strlist)

                path_to_neighbour = path_till_now.copy()
                path_to_neighbour.append(neighbour)
                extra_cost = 1 if abs(
                    pos - curr_pos) == 1 else (abs(pos - curr_pos) - 1)
                extra_cost += path_cost_till_now
                neighbour_cost = (extra_cost +
                                  get_white_heuristic(neighbour))
                new_element = (neighbour_cost, path_to_neighbour)

                logging.debug(
                    f"{neighbour} f: {neighbour_cost} g: {extra_cost} h: {get_white_heuristic(neighbour)}")

                is_there, indexx, neighbour_old_cost, _ = get_frontier_params_new(
                    neighbour, frontier)
                if (neighbour not in explored_nodes) and not is_there:
                    frontier.append(new_element)
                elif is_there:
                    if neighbour_old_cost > neighbour_cost:
                        frontier.pop(indexx)
                        frontier.append(new_element)
        logging.debug("\n")

    return None, None, -1


def pop_frontier(frontier):
    if len(frontier) == 0:
        return None
    min = MAX_VALUE
    max_values = []
    for key, path in frontier:
        if key == min:
            max_values.append(path)
        elif key < min:
            min = key
            max_values.clear()
            max_values.append(path)

    max_values = sorted(max_values, key=lambda x: x[-1])
    desired_value = max_values[0]
    frontier.remove((min, max_values[0]))
    return min, desired_value


def get_frontier_params_new(node, frontier):
    for i in range(len(frontier)):
        curr_tuple = frontier[i]
        cost, path = curr_tuple
        if path[-1] == node:
            return True, i, cost, path

    return False, None, None, None


def get_frontier_params(node, frontier):
    for i in range(len(frontier.queue)):
        curr_tuple = frontier.queue[i]
        cost, path = curr_tuple
        if path[-1] == node:
            return True, i, cost, path

    return False, None, None, None


if __name__ == '__main__':

    print("Example Valid Input 'BBB_WWW'")
    print("Space is replaced with '_'")
    input_str = input("Enter Valid Input: ")
    copy_input_str = (input_str + '.')[:-1]

    count = input_str.count('W')
    if count < 3 or count > 3:
        logging.error("Invalid Input!!")
        print("Invalid Input!!")
        exit()
    count = input_str.count('B')
    if count < 3 or count > 3:
        logging.error("Invalid Input!!")
        print("Invalid Input!!")
        exit()
    count = input_str.count('_')
    if count < 1 or count > 1:
        logging.error("Invalid Input!!")
        print("Invalid Input!!")
        exit()
    logging.info(f"Input String: {input_str}")

    # goalset = {"WBBB", "_BBB", "B_BB", "BB_B", "BBB_"}
    goalset = {"_WWWBBB", "W_WWBBB", "WW_WBBB",
               "WWW_BBB", "WWWB_BB", "WWWBB_B", "WWWBBB_"}
    print()
    print("============ UCS ================")
    logging.info("============ UCS ================")
    path_ucs, explored_ucs, path_cost_ucs = uniform_cost_search(
        input_str, goalset)
    print(f"Solution: {path_ucs[-1]}")
    print(f"No. of Explored Nodes: {len(explored_ucs)}")
    print(f"Move Cost: {path_cost_ucs}")
    print()
    print(f"Lowest Path To Goal:")
    for node in path_ucs:
        print("       ", node)
    print()
    print()
    logging.info(f"Solution: {path_ucs[-1]}")
    logging.info(f"No. of Explored Nodes: {len(explored_ucs)}")
    logging.info(f"Move Cost: {path_cost_ucs}")
    logging.info("")
    logging.info(f"Lowest Path To Goal:")
    for node in path_ucs:
        logging.info(f"        {node}")
    logging.info("\n\n")

    print("============ A* Search ================")
    logging.info("============ A* Search ================")
    path_astar, explored_astar, path_cost_astar = astar_search(
        input_str, goalset)
    print(f"Solution: {path_astar[-1]}")
    print(f"No. of Explored Nodes: {len(explored_astar)}")
    print(f"Move Cost: {path_cost_astar}")
    print()
    print(f"Lowest Path To Goal:")
    for node in path_astar:
        print("       ", node)
    print()
    print()
    logging.info(f"Solution: {path_astar[-1]}")
    logging.info(f"No. of Explored Nodes: {len(explored_astar)}")
    logging.info(f"Move Cost: {path_cost_astar}")
    logging.info("")
    logging.info(f"Lowest Path To Goal:")
    for node in path_astar:
        logging.info(f"        {node}")
    logging.info("\n\n")
    wait = input("Press Enter to continue.")
    print()

    print("============ Comparing The Costs ================")
    logging.info("============ Comparing The Costs ================")
    print()
    permlist = permutations('_BBBWWW')
    permlist = set(permlist)
    ucs_cost = []
    astar_cost = []
    iterations = []
    count = 0
    for perm in tqdm(permlist, desc="Iterating all permutations:"):
        input_str = "".join(perm)
        _, explored_ucs, _ = uniform_cost_search(input_str, goalset)
        ucs_cost.append(len(explored_ucs))
        _, explored_astar, _ = astar_search(input_str, goalset)
        astar_cost.append(len(explored_astar))
        iterations.append(count)
        count += 1
        logging.info(
            f"Relative Costs: String: {input_str} ucs: {ucs_cost[-1]}, A*: {astar_cost[-1]}")
    plt.scatter(iterations, ucs_cost, label='UCS')
    plt.scatter(iterations, astar_cost, label='A*')
    plt.xlabel('Permutations of String')
    plt.ylabel('No. of explored Nodes')
    plt.title('Permuations vs Explored Node cost')
    plt.legend(loc='upper right')
    plt.savefig("output.png")
    print()
    print("Scatter Plot For Permutations vs Explored Node Cost Saved in 'output.png'!")
    print("From 'output.png':\nWe see that Uniform Cost Search has" +
          BOLD + " 'more' " + END + "explored nodes than A* Search.")
    print()
    wait = input("Press Enter to continue.")
    print()

    print("============ All Goal Configurations ================")
    logging.info("============ All Goal Configurations ================")
    print()
    print(f"All Goal Configurations For: '{copy_input_str}'")
    print()
    for goal in goalset:
        path_astar, explored_astar, path_cost_astar = astar_search(
            copy_input_str, {goal})
        print(f"Solution: {path_astar[-1]}")
        print(f"No. of Explored Nodes: {len(explored_astar)}")
        print(f"Move Cost: {path_cost_astar}")
        print(f"Lowest Path To Goal:")
        print(f"Lowest Path To Goal:")
        for node in path_astar:
            print("       ", node)
        print()
