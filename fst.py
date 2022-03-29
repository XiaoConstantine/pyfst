class Node:
    _edges: dict
    _id: int
    _char: str
    last_child_key: str
    final: bool
    byte_pos: int

    def __init__(self):
        self._edges = {}
        self._char = ""
        self._id = 0
        self.last_child_key = ""
        self.final = False

    def has_children(self):
        return len(self._edges)

    def hash(self):
        result = self._char

        if self.final:
            result += "1"
        else:
            result += "0"

        tmp = []
        for k, v in self._edges.items():
            tmp.append(k + str(v._id))
        sorted(tmp)
        result += '_'.join(tmp)
        return result

    def __str__(self):
        return f"{self.hash()}"


class Tree:
    _root: Node
    _id_counter: int
    _node_count: int
    _register: dict
    _prev_w: str

    def __init__(self):
        self._root = Node()
        self._register = {}
        self._prev_w = ""
        self._id_counter = 0
        self._node_count = 0

    def insert(self, word:str):
        if word < self._prev_w:
            raise ValueError(f"Insert word {word} is not performed in lexicographical order")

        prefix_l, max_l = 0, min(len(word), len(self._prev_w))

        for idx in range(max_l):
            if word[idx] != self._prev_w[idx]:
                break
            prefix_l += 1

        self._prev_w = word
        common_prefix = word[:prefix_l]

        last_state = self.traverse(common_prefix)
        if last_state and last_state.has_children():
            self.replace_or_register(last_state)

        current_suffix = word[prefix_l:]
        self.add_suffix(last_state, current_suffix)

    def traverse(self, word:str):
        node = self._root

        for _, ch in enumerate(word):
            if ch in node._edges:
                node = node._edges[ch]
            else:
                return None
        return node

    def contains(self, word:str):
        node = self.traverse(word)
        return node and node.final

    def add_suffix(self, last_state: Node, suffix:str):
        node = last_state
        for _, char in enumerate(suffix):
            new_node = Node()
            new_node._char = char
            new_node._id = self._id_counter
            node._edges[char] = new_node
            node.last_child_key = char
            node = new_node
            self._id_counter += 1
            self._node_count += 1
        node.final = True

    def replace_or_register(self, last_state: Node):
        child = last_state._edges[last_state.last_child_key]
        if child.has_children():
            self.replace_or_register(child)

        child_hash = child.hash()
        if child_hash in self._register:
            last_state._edges[self._register[child_hash]._char] = self._register[child_hash]
            self._node_count -= 1
        else:
            self._register[child_hash] = child

    def finish(self):
        self.replace_or_register(self._root)

    def _ordered_edges(self, node):
        ret = []
        for k, _ in node._edges.items():
            ret.append(k)
        return ret

    def _recursive_str(self, node, str, level):
        keys = self._ordered_edges(node)
        for _, ch in enumerate(keys):
            child = node._edges[ch]
            str += f"{level *' '}{child._char}{'<->'}{child} \n"
            str = self._recursive_str(child, str, level + 1)
        return str
         
    def __str__(self):
        return self._recursive_str(self._root, "", 0)

if __name__ == "__main__":
    t = Tree()
    t.insert("abc")
    t.insert("abd")

    t.finish()
    print(t)

    print(t.contains("abc"))


