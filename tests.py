import unittest

from merkle import MerkleTree


class MerkleTreeTestCase(unittest.TestCase):
    EMPTY_STR_HASH = 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'

    def setUp(self):
        self.tree = MerkleTree()

    def _make_tree(self):
        self.tree.add_node('00')
        self.tree.add_node(bytes.fromhex('01'))
        self.tree.add_node('02')

        self.tree.make()

        # Check extra node of power of 2 is appended
        self.assertEqual(self.tree.node_count, 4)

    def test_get_root(self):
        self._make_tree()
        self.assertEqual(self.tree.get_root(), '8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')

    def test_get_root_empty(self):
        self.tree.make()
        self.assertEqual(self.tree.get_root(), self.EMPTY_STR_HASH)

    def test_get_root_without_make(self):
        with self.assertRaises(ValueError) as e:
            self.tree.get_root()
        self.assertIn('tree is not ready', str(e.exception))

    def test_get_proof(self):
        self._make_tree()
        proof = self.tree.get_proof(2)
        self.assertEqual(proof[0]['right'], self.EMPTY_STR_HASH)
        self.assertEqual(proof[1]['left'], '49d03a195e239b52779866b33024210fc7dc66e9c2998975c0aa45c1702549d5')

    def test_get_proof_without_make(self):
        with self.assertRaises(ValueError) as e:
            self.tree.get_proof(0)
        self.assertIn('tree is not ready', str(e.exception))

    def test_get_proof_invalid_index(self):
        self._make_tree()
        with self.assertRaises(ValueError) as e:
            self.tree.get_proof(4)
        self.assertIn('Specify the correct index', str(e.exception))

    def test_validate_proof(self):
        self._make_tree()
        proof = self.tree.get_proof(2)
        self.assertTrue(self.tree.validate_proof(proof, '02', self.tree.get_root()))

    def test_validate_proof_invalid(self):
        self._make_tree()
        proof = self.tree.get_proof(2)
        self.assertFalse(self.tree.validate_proof(proof, '01', self.tree.get_root()))
