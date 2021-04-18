import numpy as np


class LinkedList:
    class Node:
        def __init__(self, data):
            self.next = None
            self.data = data
            
    def __init__(self):
        self.head = None
        self.tail = None
        self.n = 0
   
    def push(self, data):
        u = self.Node(data)
        u.next = self.head
        self.head = u

        if self.n == 0:
            self.tail = u

        self.n += 1
        return data
        
    def pop(self) -> np.object:
        try:
            data = self.head.data
            self.head = self.head.next
            self.n -= 1

            if self.n == 0:
                self.tail = None

            return data
        except:
            raise IndexError()

    def size(self) -> int:
        return self.n
