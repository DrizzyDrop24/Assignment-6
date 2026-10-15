# hash_table.py
# implementation of simple hash table
# we'll use separate chaining with Python's built-in 
# list type acting as the chains
# Strongly suggest you turn off LLMs like
# GitHub Copilot, TabNine, etc. when working on this file.
# Writing a data structure yourself is the best
# way to learn how it works.
# Modified by: 
from random import randint


class HashTable:
    MAX_LOAD_FACTOR = 0.7
    GROWTH_FACTOR = 2

    def __init__(self, slots=10):
        self.slots = slots
        self.num_items = 0
        self.backing_store = [[] for _ in range(slots)]

    def _hash(self, key):
        return hash(key) % self.slots

    # insert a new key-value pair into the 
    # hash table or if the key is already present
    # update its associated value
    # make sure to resize if MAX_LOAD_FACTOR is exceeded
    def insert(self, key, value):
        index = self._hash(key)
        chain = self.backing_store[index]

        for i, (existing_key, existing_value) in enumerate(chain):
            if existing_key == key:
                chain[i] = (key, value)
                return

                # Resize before adding if the load factor would be exceeded
        if (self.num_items + 1) / self.slots > self.MAX_LOAD_FACTOR:
            self._resize()
            index = self._hash(key)
            chain = self.backing_store[index]

        chain.append((key, value))
        self.num_items += 1

    # return the value associated with the key
    def get(self, key):
        index = self._hash(key)
        chain = self.backing_store[index]

        for existing_key, value in chain:
            if existing_key == key:
                return value

        return None

    # eliminate the key-value pair associated with key
    def remove(self, key):
        index = self._hash(key)
        chain = self.backing_store[index]

        for i, (existing_key, value) in enumerate(chain):
            if existing_key == key:
                del chain[i]
                self.num_items -= 1
                return True

        return False

    # update the hash table based on GROWTH_FACTOR
    # make sure to move everything over to the new table
    def _resize(self):
        old_store = self.backing_store

        self.slots *= self.GROWTH_FACTOR
        self.backing_store = [[] for _ in range(self.slots)]

        # Reinsert existing entries into the larger table
        for chain in old_store:
            for key, value in chain:
                index = self._hash(key)
                self.backing_store[index].append((key, value))

    def __str__(self):
        return str(self.backing_store)
