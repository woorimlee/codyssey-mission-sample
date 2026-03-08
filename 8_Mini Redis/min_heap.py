"""
최소 힙 (Min Heap)

TTL 만료 시간 관리를 위한 자료구조.
(expire_at, key) 형태의 요소를 다루며, expire_at이 가장 작은 요소가 루트에 위치한다.
"""


class MinHeap:
    """
    배열 기반 최소 힙.

    내부 저장소로 Python 리스트를 사용하되,
    힙 연산(_heapify_up, _heapify_down)은 직접 구현한다.
    """

    def __init__(self):
        self._data = []  # 리스트를 배열 저장소로 사용

    def push(self, item):
        """요소를 힙에 삽입한다. O(log n)"""
        self._data.append(item)
        self._heapify_up(len(self._data) - 1)

    def pop(self):
        """최솟값을 제거하고 반환한다. 비어 있으면 None. O(log n)"""
        if len(self._data) == 0:
            return None
        if len(self._data) == 1:
            return self._data.pop()

        root = self._data[0]
        self._data[0] = self._data.pop()  # 마지막 요소를 루트로
        self._heapify_down(0)
        return root

    def peek(self):
        """최솟값을 제거하지 않고 반환한다. 비어 있으면 None. O(1)"""
        if len(self._data) == 0:
            return None
        return self._data[0]

    def size(self):
        """힙에 저장된 요소 수를 반환한다."""
        return len(self._data)

    def _heapify_up(self, idx):
        """삽입된 요소를 부모와 비교하며 위로 올린다."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx] < self._data[parent]:
                self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
                idx = parent
            else:
                break

    def _heapify_down(self, idx):
        """루트 요소를 자식과 비교하며 아래로 내린다."""
        n = len(self._data)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest != idx:
                self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
                idx = smallest
            else:
                break
