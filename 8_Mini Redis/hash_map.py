"""
해시맵 (HashMap) - 체이닝 방식 충돌 해결

직접 설계한 해시 함수와 이중 연결 리스트 기반 체이닝으로 구현.
로드 팩터 0.75 초과 시 버킷을 2배 확장한다.
"""

from doubly_linked_list import DoublyLinkedList

# 버킷 테이블로 사용할 고정 길이 리스트 생성 헬퍼
_INITIAL_CAPACITY = 16


class HashMap:
    """
    체이닝 기반 해시맵.

    - 해시 함수: 직접 구현 (FNV-1a 변형)
    - 충돌 해결: 이중 연결 리스트를 재사용한 체이닝
    - 로드 팩터 0.75 초과 시 자동 리사이즈
    """

    def __init__(self, capacity=_INITIAL_CAPACITY):
        self._capacity = capacity
        self._size = 0
        # 버킷 테이블: 고정 길이 리스트(인덱스 접근용)
        self._buckets = [None] * self._capacity

    # ------------------------------------------------------------------ #
    #  해시 함수 (FNV-1a 변형)
    # ------------------------------------------------------------------ #
    def _hash(self, key):
        """
        FNV-1a 해시 함수 변형.

        문자열 키의 각 바이트에 대해 XOR과 소수 곱셈을 반복하여
        해시값을 생성한 뒤, 버킷 인덱스로 변환한다.
        """
        h = 2166136261  # FNV offset basis (32-bit)
        for ch in str(key):
            h = h ^ ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF  # FNV prime, 32-bit 마스크
        return h % self._capacity

    # ------------------------------------------------------------------ #
    #  핵심 연산
    # ------------------------------------------------------------------ #
    def put(self, key, value):
        """
        키-값 쌍을 저장한다.
        이미 존재하는 키면 값을 갱신하고, 새 키면 삽입 후 리사이즈를 검사한다.
        """
        idx = self._hash(key)

        if self._buckets[idx] is None:
            self._buckets[idx] = DoublyLinkedList()

        # 기존 키 탐색
        chain = self._buckets[idx]
        for entry in chain:
            if entry[0] == key:
                # 값 갱신: 기존 노드를 찾아 교체
                current = chain._head.next
                while current is not chain._tail:
                    if current.data[0] == key:
                        current.data = (key, value)
                        return
                    current = current.next

        # 새 키 삽입
        chain.insert_back((key, value))
        self._size += 1

        # 로드 팩터 검사
        if self._size / self._capacity > 0.75:
            self._resize()

    def get(self, key):
        """키에 해당하는 값을 반환한다. 없으면 None."""
        idx = self._hash(key)
        chain = self._buckets[idx]
        if chain is None:
            return None
        for entry in chain:
            if entry[0] == key:
                return entry[1]
        return None

    def remove(self, key):
        """키를 삭제한다. 성공하면 True, 없으면 False."""
        idx = self._hash(key)
        chain = self._buckets[idx]
        if chain is None:
            return False

        current = chain._head.next
        while current is not chain._tail:
            if current.data[0] == key:
                chain.remove_node(current)
                self._size -= 1
                return True
            current = current.next
        return False

    def contains(self, key):
        """키 존재 여부를 반환한다."""
        return self.get(key) is not None

    def keys(self):
        """저장된 모든 키를 리스트로 반환한다."""
        result = []
        for i in range(self._capacity):
            chain = self._buckets[i]
            if chain is not None:
                for entry in chain:
                    result.append(entry[0])
        return result

    def size(self):
        """저장된 키-값 쌍의 개수를 반환한다."""
        return self._size

    # ------------------------------------------------------------------ #
    #  리사이즈
    # ------------------------------------------------------------------ #
    def _resize(self):
        """버킷을 2배 확장하고 모든 엔트리를 재해싱한다."""
        old_buckets = self._buckets
        old_capacity = self._capacity

        self._capacity = self._capacity * 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for i in range(old_capacity):
            chain = old_buckets[i]
            if chain is not None:
                for entry in chain:
                    self.put(entry[0], entry[1])
