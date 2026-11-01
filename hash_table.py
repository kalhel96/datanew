# ==========================================================
# Hash Table Contact Book
# A phone book that stores contacts in a hash table.
# Collisions are handled with "separate chaining" (linked lists).
# ==========================================================


# STEP 2: Contact class 
# A Contact is just a small box holding a name and a phone number.
class Contact:
    def __init__(self, name, number):
        self.name = name        # e.g. "Riley"
        self.number = number    # e.g. "123-456-7890"

    def __str__(self):
        # This controls what print(contact) shows
        return f"{self.name}: {self.number}"


# ---------- STEP 3: Node class ----------
# A Node is one link in a chain (linked list).
# It holds a key (the name), a value (the Contact), and
# a pointer to the next Node in the same slot.
class Node:
    def __init__(self, key, value):
        self.key = key          # the contact's name
        self.value = value      # the Contact object
        self.next = None        # next Node in the chain (none yet)


# STEP 4: HashTable class 
class HashTable:
    def __init__(self, size):
        self.size = size                 # how many slots the table has
        self.data = [None] * size        # every slot starts empty

    def hash_function(self, key):
        # Turn a name into a slot number:
        # 1) add up the Unicode number of every letter (ord)
        # 2) we use % size so the answer is always 0 to size-1
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size

    def insert(self, key, value):
        # key = name, value = phone number
        index = self.hash_function(key)
        new_contact = Contact(key, value)

        # Case 1: the slot is empty -> put the first Node here
        if self.data[index] is None:
            self.data[index] = Node(key, new_contact)
            return

        # Case 2: the slot already has a chain -> walk through it
        current = self.data[index]
        while current:
            # Same name already saved? Just update the number.
            if current.key == key:
                current.value.number = value
                return
            # Reached the last Node? Stop here.
            if current.next is None:
                break
            current = current.next

        # Name was not found -> add a new Node to the end (collision)
        current.next = Node(key, new_contact)

    def search(self, key):
        # Go straight to the right slot, then walk the chain
        index = self.hash_function(key)
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value   # found the Contact
            current = current.next
        return None                    # not in the table

    def print_table(self):
        # Show every slot and the contact(s) inside it
        for i in range(self.size):
            current = self.data[i]
            if current is None:
                print(f"Index {i}: Empty")
            else:
                line = f"Index {i}:"
                while current:
                    line += f" - {current.value}"
                    current = current.next
                print(line)


# ---------- STEPS 5 & 6: Testing ----------
if __name__ == "__main__":
    # Quick checks for Contact and Node
    contact_1 = Contact("Riley", "123-456-7890")
    print(contact_1)                 # Riley: 123-456-7890
    node_1 = Node(contact_1.name, contact_1)
    print(node_1.key)                # Riley
    print(node_1.value)              # Riley: 123-456-7890
    print(node_1.next)               # None
    print()

    # empty table
    table = HashTable(10)
    table.print_table()
    print()

    # Add some contacts
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    table.print_table()

    # Search
    contact = table.search("John")
    print("\nSearch result:", contact)   # John: 909-876-1234
    print()

    # Edge Case 1: collision (Amy and May land in the same slot)
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    table.print_table()
    print()

    # Edge Case 2: duplicate name -> number gets updated
    table.insert("Rebecca", "999-444-9999")
    table.print_table()
    print()

    # Edge Case 3: searching for someone who isn't there
    print(table.search("Chris"))         # None



"""
Design Memo

A hash table is the right structure for fast lookups because it does
not need to check every item. A list is like searching a messy pile of
papers one by one. A hash table is like a filing cabinet with labeled
drawers. The hash function takes a name, turns it into a number, and
tells the program exactly which drawer to open. Because of this, finding
a contact takes about the same time whether the table has 10 contacts
or 100,000. This is called O(1), or constant time.

My hash function adds up the Unicode value of each letter in the name
using ord(), then uses the modulus operator (% size) so the result is
always a valid index. Sometimes two different names give the same
index. This is called a collision. For example, "Amy" and "May" have the
same letters, so they add up to the same total and land in the same
slot. I handled collisions with separate chaining. Each slot holds a
linked list of Node objects, so many contacts can share one slot. When
I insert, I walk down the chain. If the name already exists, I update
the phone number instead of adding a copy. If it does not exist, I add
a new Node to the end of the chain.

An engineer might choose a hash table over a list or tree when the main
job is looking things up quickly by a unique key, like a username, a
student ID, or a product SKU. A list is better when the order of items
matters. A tree is better when the data needs to stay sorted or when you
often need the smallest or largest value. Hash tables trade extra memory
for speed, so they fit best when speed matters more than order.
"""