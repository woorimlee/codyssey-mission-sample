"""
이중 연결 리스트 (Doubly Linked List)

Redis LRU 추적과 해시맵 체이닝에 사용되는 핵심 자료구조.
모든 삽입/삭제/이동 연산이 O(1)로 동작한다.
"""


class Node:
    """이중 연결 리스트의 노드."""

    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    센티넬(dummy head/tail) 기반 이중 연결 리스트.

    센티넬 노드를 사용하면 삽입/삭제 시 경계 조건 처리가 단순해진다.
    """

    def __init__(self):
        self._head = Node()  # dummy head
        self._tail = Node()  # dummy tail
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    @property
    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def insert_front(self, data):
        """리스트 맨 앞에 노드를 삽입하고 해당 노드를 반환한다. O(1)"""
        node = Node(data)
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node
        self._size += 1
        return node

    def insert_back(self, data):
        """리스트 맨 뒤에 노드를 삽입하고 해당 노드를 반환한다. O(1)"""
        node = Node(data)
        node.prev = self._tail.prev
        node.next = self._tail
        self._tail.prev.next = node
        self._tail.prev = node
        self._size += 1
        return node

    def remove_front(self):
        """맨 앞 노드를 제거하고 data를 반환한다. 비어 있으면 None. O(1)"""
        if self.is_empty():
            return None
        node = self._head.next
        self._detach(node)
        return node.data

    def remove_back(self):
        """맨 뒤 노드를 제거하고 data를 반환한다. 비어 있으면 None. O(1)"""
        if self.is_empty():
            return None
        node = self._tail.prev
        self._detach(node)
        return node.data

    def remove_node(self, node):
        """특정 노드를 리스트에서 제거한다. O(1)"""
        self._detach(node)

    def move_to_front(self, node):
        """기존 노드를 리스트 맨 앞으로 이동시킨다. O(1)"""
        self._detach(node)
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node
        self._size += 1

    def peek_back(self):
        """맨 뒤 노드의 data를 제거하지 않고 반환한다."""
        if self.is_empty():
            return None
        return self._tail.prev.data

    def _detach(self, node):
        """노드를 리스트에서 분리한다(내부 헬퍼)."""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        self._size -= 1

    def __iter__(self):
        """리스트를 순회하며 data를 yield한다."""
        current = self._head.next
        while current is not self._tail:
            yield current.data
            current = current.next
