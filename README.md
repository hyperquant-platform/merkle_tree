# Table of Contents
- [About](#about)
- [Installation](#installation)
- [Documentation](#documentation)
- [Usage](#usage)
  - [Add nodes and make tree](#add-nodes-and-make-tree)
  - [Get root and proof](#get-root-and-proof)
  - [Validate proof](#validate-proof)

# About

[Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree) implementation which supports:
- Calculating merkle root
- Generating proofs
- Validation proofs

Uses [Keccak-256](https://keccak.team/keccak.html) hash function in tree building.

Merkle root is calculated from a [perfect (complete) binary tree](https://en.wikipedia.org/wiki/Binary_tree#Types_of_binary_trees).
If there are not enough nodes provided, tree is padded with hashes of empty strings.

# Installation

Requirements: python3.7

```bash
source setenv.sh install
```

# Documentation

### add_node(value)

Adds node to a tree. `value` has to be hex string.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
```

### get_node(index)

Returns node hash as hex string.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
> tree.get_node(0)
'8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531'
```

### make()

Build a complete tree from given nodes.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
> tree.add_node('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
> tree.make()
```

### get_root()

Returns merkle root for a complete tree.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
> tree.add_node('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
> tree.make()
> tree.get_root()
'cd179bae7880f32ab6090519099d3ee0b196d70a620cdce9ea3a823e6bdb071c'
```

### get_proof(index)

Returns proof for a given tree index.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
> tree.add_node('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
> tree.make()
> tree.get_proof(1)
[{'left': '8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531'}]
```

### get_proof_for_hash(hash_value)

Returns proof for a given node hash value.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
> tree.add_node('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
> tree.make()
> tree.get_proof_for_hash('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
[{'left': '8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531'}]
```

### validate_proof(proof, target_hash, merkle_root)

Validates that provided `target_hash` and `proof` form a merkle root equal to provided one.

```python
> tree = MerkleTree()
> tree.add_node('8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531')
> tree.add_node('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
> tree.make()
> tree.validate_proof([{'left': '8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531'}], 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', 'cd179bae7880f32ab6090519099d3ee0b196d70a620cdce9ea3a823e6bdb071c')
True
```

# Usage

## Add nodes and make tree
```python
> tree = MerkleTree()

# raw bytes or str bytes
> tree.add_node('00')
> tree.add_node('01')
> tree.add_node('02')

# extra node is added during make to provide a perfect binary tree
> tree.make()
```

## Get root and proof
```python
> tree.get_root()
'8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531'
> tree.get_proof(2) # node index
[{'right': 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'}, {'left': '49d03a195e239b52779866b33024210fc7dc66e9c2998975c0aa45c1702549d5'}]
```

## Validate proof
```python
> proof = [{'right': 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'}, {'left': '49d03a195e239b52779866b33024210fc7dc66e9c2998975c0aa45c1702549d5'}]
> root = '8633f3f58bd5719152d1f244ad09616dbad359515721e8a59ad0eb1823ae3531'
> tree.validate_proof(proof, '02', root)
True
```