
from dataclasses import dataclass
import math

@dataclass
class Node:
    id: str

    def ends_with_z(self):
        return self.id[-1] == 'Z'

    def __hash__(self):
        return hash(self.id)


def parse_nodes(lines: list[str]) -> dict[Node, tuple[Node, Node]]:
    node_map = {}
    for line in lines:
        key_node_id, target_node_ids = line.split(' = ')
        key_node = Node(key_node_id)
        target_node_id1, target_node_id2 = target_node_ids.split()
        key_target_left = "".join([c for c in target_node_id1 if c.isalpha()])
        key_target_right = "".join([c for c in target_node_id2 if c.isalpha()])
        node_map[key_node] = (Node(key_target_left), Node(key_target_right))
    return node_map

def traverse_paths(current_nodes: list[Node],
                   node_map: dict[Node, tuple[Node, Node]],
                   instructions: str,
                   exercise: str,
                   begin_counter: int = 0,
                   repeating_factor: int = 100000) -> int:
    counter = begin_counter
    if counter % 100000 == 0:
        print(f"At step {counter}")
    is_done = False
    for n in instructions * repeating_factor:
        counter += 1
        if n == 'L':
            current_nodes = [node_map[cn][0] for cn in current_nodes]
        else:
            current_nodes = [node_map[cn][1] for cn in current_nodes]
        if exercise == 'a' and current_nodes[0] == Node("ZZZ"):
            is_done = True
            break
        if exercise == 'b' and any([cn.ends_with_z() for cn in current_nodes]):
            print(current_nodes)
            print(counter)
        if exercise == 'b' and all([cn.ends_with_z() for cn in current_nodes]):
            is_done = True
            break
    if not is_done:
        return traverse_paths(current_nodes, node_map, instructions, exercise, counter)
    else:
        return counter

# N1: 11567 - 23134
# N2: 19637 - 39274
# N3: 15871 - 31724
# N4: 21251 - 42502
# N5: 12643 - 25286
# N6: 19099 - 38198

def main():
    with open("data/day8.csv", "r") as file:
        data = file.read().splitlines()
    instructions = data[0]
    node_data = data[2:]
    node_map = parse_nodes(node_data)

    steps_taken = traverse_paths(
        [Node("AAA")],
        node_map,
        instructions,
        exercise='a'
    )
    print(steps_taken)

    # steps_taken = traverse_paths(
    #     [n for n in node_map.keys() if n.id[-1] == 'A'],
    #     node_map,
    #     instructions,
    #     exercise='b'
    # )
    # todo: all 6 nodes separately will get to some cycle. We can probably
    #  approach this by separately determining each cycle, and analytically calculate
    #  when the six cycles align.
    answer_c = math.lcm(11567,
    19637,
    15871,
    21251,
    12643,
    19099)
    print(answer_c)


if __name__ == "__main__":
    main()
