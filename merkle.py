import math

from eth_hash.auto import keccak as keccak_256


class MerkleTree:
    """
    Class for build perfect binary trees, generating merkle roots and proof.
    """
    def __init__(self):
        self.hash_func = keccak_256
        self.nodes = []
        self.tree_levels = None
        self.is_ready = False

    @staticmethod
    def _to_hex(x):
        return x.hex()

    @staticmethod
    def _from_hex(x):
        return bytes.fromhex(x)

    def add_node(self, value):
        """
        Adds node to a tree. `value` has to be hex string
        """
        self.is_ready = False
        if isinstance(value, str):
            value = self._from_hex(value)
        self.nodes.append(value)

    def get_node(self, index):
        """
        Returns node hash as hex string.
        """
        return self._to_hex(self.nodes[index])

    @property
    def node_count(self):
        """
        Complete number of nodes in a tree.
        """
        return len(self.nodes)

    def _calc_next_level(self):
        if len(self.tree_levels[0]) % 2 == 1:
            raise ValueError('Level length cannot be odd')

        next_level = []
        for left_node, right_node in zip(self.tree_levels[0][0::2], self.tree_levels[0][1::2]):
            next_level.append(self.hash_func(left_node + right_node))
        self.tree_levels = [next_level, ] + self.tree_levels

    @staticmethod
    def _next_power_of_2(x):
        return 1 if x == 0 else 2 ** math.ceil(math.log2(x))

    def _fill_to_power_of_2(self):
        """
        Fills tree with extra nodes (with hashes of empty strings) to form a perfect binary tree.
        """
        next_power_of_2 = self._next_power_of_2(self.node_count)
        nodes_to_append = next_power_of_2 - self.node_count
        empty_str_hash = self.hash_func(self._from_hex(''))
        for i in range(nodes_to_append):
            self.add_node(empty_str_hash)

    def make(self):
        """
        Build a complete tree from given nodes.
        """
        self.is_ready = False
        self._fill_to_power_of_2()
        self.tree_levels = [self.nodes, ]
        while len(self.tree_levels[0]) > 1:
            self._calc_next_level()
        self.is_ready = True

    def get_root(self):
        """
        Returns merkle root for a complete tree.
        """
        if self.is_ready and self.tree_levels is not None:
            return self._to_hex(self.tree_levels[0][0])
        raise ValueError('The tree is not ready. Call `make` to build the tree.')

    def get_proof_for_hash(self, hash_value):
        """
        Returns proof for a given node hash value.
        """
        if isinstance(hash_value, str):
            hash_value = self._from_hex(hash_value)
        return self.get_proof(self.nodes.index(hash_value))

    def get_proof(self, index):
        """
        Returns proof for a given tree index.

        Proof example
        [
            {'right': 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'},
            {'left': '49d03a195e239b52779866b33024210fc7dc66e9c2998975c0aa45c1702549d5'}
        ]
        """
        if self.tree_levels is None or not self.is_ready:
            raise ValueError('The tree is not ready. Call `make` to build the tree.')

        if index < 0 or index > self.node_count - 1:
            raise ValueError('Specify the correct index (from 0 to {}).'.format(self.node_count - 1))

        proof = []
        for level in range(len(self.tree_levels) - 1, 0, -1):
            is_right_node = index % 2
            sibling_index = index - 1 if is_right_node else index + 1
            index = int(index / 2)

            sibling_position = 'left' if is_right_node else 'right'
            sibling_value = self._to_hex(self.tree_levels[level][sibling_index])
            proof.append({sibling_position: sibling_value})

        return proof

    def validate_proof(self, proof, target_hash, merkle_root):
        """
        Validates that provided `target_hash` and `proof` form a merkle root equal to provided one.
        """

        if len(proof) == 0:
            raise ValueError('Proof is empty.')

        proof_hash = self._from_hex(target_hash)
        root_hash = self._from_hex(merkle_root)
        for p in proof:
            if 'left' in p:
                proof_value = self._from_hex(p['left']) + proof_hash
            elif 'right' in p:
                proof_value = proof_hash + self._from_hex(p['right'])
            else:
                raise ValueError('Inconsistent proof.')
            proof_hash = self.hash_func(proof_value)
        return proof_hash == root_hash
