"""
Mini Redis 코어 엔진

해시맵, 이중 연결 리스트, 최소 힙을 조합하여
LRU 캐시 + TTL 만료 + 메모리 제한 기능을 구현한다.
"""

import time

from hash_map import HashMap
from doubly_linked_list import DoublyLinkedList
from min_heap import MinHeap


class MiniRedis:
    """
    CLI 기반 Mini Redis 엔진.

    내부 구조:
    - store (HashMap): key → value 매핑
    - lru_list (DoublyLinkedList): 가장 최근 사용된 키가 앞(head), 가장 오래된 키가 뒤(tail)
    - lru_map (HashMap): key → DoublyLinkedList 노드 참조 (O(1) 접근용)
    - ttl_heap (MinHeap): (expire_at, key) 튜플로 가장 빠른 만료를 추적
    - ttl_map (HashMap): key → expire_at (만료 시간 조회/검증용)
    """

    def __init__(self):
        self.store = HashMap()        # key → value
        self.lru_list = DoublyLinkedList()  # LRU 순서 추적
        self.lru_map = HashMap()      # key → Node (LRU 리스트 노드 참조)
        self.ttl_heap = MinHeap()     # (expire_at, key) 최소 힙
        self.ttl_map = HashMap()      # key → expire_at

        self.maxmemory = 0            # 0 = 무제한
        self.used_memory = 0
        self.evicted_keys = 0

    # ================================================================== #
    #  유틸리티
    # ================================================================== #

    def _key_value_bytes(self, key, value):
        """키와 값의 UTF-8 바이트 길이 합산."""
        return len(key.encode('utf-8')) + len(value.encode('utf-8'))

    def _is_expired(self, key):
        """키가 만료되었는지 확인한다. 만료 시 삭제 처리 후 True 반환."""
        expire_at = self.ttl_map.get(key)
        if expire_at is not None and time.time() >= expire_at:
            self._remove_key(key)
            return True
        return False

    def _remove_key(self, key):
        """키를 모든 내부 구조(store, LRU, TTL)에서 제거한다."""
        value = self.store.get(key)
        if value is None:
            return

        # 메모리 차감
        self.used_memory -= self._key_value_bytes(key, value)

        # store에서 제거
        self.store.remove(key)

        # LRU 구조에서 제거
        node = self.lru_map.get(key)
        if node is not None:
            self.lru_list.remove_node(node)
            self.lru_map.remove(key)

        # TTL 구조에서 제거 (힙은 lazy deletion 전략)
        self.ttl_map.remove(key)

    def _update_lru(self, key):
        """키를 LRU 리스트의 맨 앞으로 이동(최근 사용 표시)."""
        node = self.lru_map.get(key)
        if node is not None:
            self.lru_list.move_to_front(node)

    def _evict_expired_from_heap(self):
        """힙 상단의 만료된 엔트리를 정리한다 (lazy deletion)."""
        now = time.time()
        while self.ttl_heap.size() > 0:
            top = self.ttl_heap.peek()
            expire_at, key = top
            # 이미 삭제된 키이거나 만료 시간이 변경된 경우 스킵
            current_expire = self.ttl_map.get(key)
            if current_expire is None or current_expire != expire_at:
                self.ttl_heap.pop()
                continue
            if now >= expire_at:
                self.ttl_heap.pop()
                self._remove_key(key)
            else:
                break

    def _evict_lru(self):
        """LRU 정책으로 가장 오래된 키를 제거한다."""
        lru_key = self.lru_list.peek_back()
        if lru_key is not None:
            self._remove_key(lru_key)
            self.evicted_keys += 1

    # ================================================================== #
    #  String 타입 명령어
    # ================================================================== #

    def cmd_set(self, key, value):
        """SET key value"""
        entry_size = self._key_value_bytes(key, value)

        # 기존 키가 있으면 먼저 제거 (TTL 초기화 포함)
        if self.store.contains(key):
            self._remove_key(key)

        # 단일 엔트리가 maxmemory를 초과하는 경우 OOM
        if self.maxmemory > 0 and entry_size > self.maxmemory:
            return "(error) OOM command not allowed when used_memory > 'maxmemory'"

        # 저장
        self.store.put(key, value)
        self.used_memory += entry_size

        # LRU 등록
        node = self.lru_list.insert_front(key)
        self.lru_map.put(key, node)

        # 메모리 초과 시 LRU 제거
        if self.maxmemory > 0:
            while self.used_memory > self.maxmemory and self.store.size() > 1:
                self._evict_lru()

        return "OK"

    def cmd_get(self, key):
        """GET key"""
        # 만료 확인 우선
        if self._is_expired(key):
            return "(nil)"

        value = self.store.get(key)
        if value is None:
            return "(nil)"

        # LRU 갱신 (성공한 경우에만)
        self._update_lru(key)
        return '"' + value + '"'

    def cmd_del(self, key):
        """DEL key"""
        # 만료 확인
        self._is_expired(key)

        if not self.store.contains(key):
            return "(integer) 0"

        self._remove_key(key)
        return "(integer) 1"

    def cmd_exists(self, key):
        """EXISTS key"""
        self._is_expired(key)
        if self.store.contains(key):
            return "(integer) 1"
        return "(integer) 0"

    def cmd_dbsize(self):
        """DBSIZE"""
        self._evict_expired_from_heap()
        return "(integer) " + str(self.store.size())

    def cmd_keys(self):
        """KEYS"""
        self._evict_expired_from_heap()
        all_keys = self.store.keys()
        if len(all_keys) == 0:
            return "(empty array)"

        lines = []
        for i in range(len(all_keys)):
            lines.append(str(i + 1) + '. "' + all_keys[i] + '"')
        return "\n".join(lines)

    # ================================================================== #
    #  메모리 관리 명령어
    # ================================================================== #

    def cmd_config_set_maxmemory(self, value_str):
        """CONFIG SET maxmemory <bytes>"""
        try:
            val = int(value_str)
            if val < 0:
                return "(error) ERR value is not an integer or out of range"
        except (ValueError, TypeError):
            return "(error) ERR value is not an integer or out of range"

        self.maxmemory = val

        # 새 제한 적용: 초과분 LRU 제거
        if self.maxmemory > 0:
            while self.used_memory > self.maxmemory and self.store.size() > 0:
                self._evict_lru()

        return "OK"

    def cmd_info_memory(self):
        """INFO memory"""
        self._evict_expired_from_heap()
        lines = [
            "used_memory:" + str(self.used_memory),
            "maxmemory:" + str(self.maxmemory),
            "evicted_keys:" + str(self.evicted_keys),
        ]
        return "\n".join(lines)

    # ================================================================== #
    #  TTL 관리 명령어
    # ================================================================== #

    def cmd_expire(self, key, seconds_str):
        """EXPIRE key seconds"""
        # 만료 확인
        self._is_expired(key)

        if not self.store.contains(key):
            return "(integer) 0"

        try:
            seconds = int(seconds_str)
        except (ValueError, TypeError):
            return "(error) ERR value is not an integer or out of range"

        if seconds <= 0:
            # 즉시 만료 처리
            self._remove_key(key)
            return "(integer) 1"

        expire_at = time.time() + seconds
        self.ttl_map.put(key, expire_at)
        self.ttl_heap.push((expire_at, key))
        return "(integer) 1"

    def cmd_ttl(self, key):
        """TTL key"""
        self._is_expired(key)

        if not self.store.contains(key):
            return "(integer) -2"

        expire_at = self.ttl_map.get(key)
        if expire_at is None:
            return "(integer) -1"

        remaining = int(expire_at - time.time())
        if remaining < 0:
            remaining = 0
        return "(integer) " + str(remaining)


# ====================================================================== #
#  명령어 파서 및 실행기
# ====================================================================== #

def parse_input(raw):
    """
    사용자 입력을 토큰 리스트로 파싱한다.
    큰따옴표로 감싼 값을 지원한다.
    """
    tokens = []
    i = 0
    raw = raw.strip()
    while i < len(raw):
        if raw[i] == ' ':
            i += 1
            continue
        if raw[i] == '"':
            # 따옴표 안의 값 추출
            j = i + 1
            while j < len(raw) and raw[j] != '"':
                j += 1
            tokens.append(raw[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < len(raw) and raw[j] != ' ':
                j += 1
            tokens.append(raw[i:j])
            i = j
    return tokens


def execute(redis, tokens):
    """토큰 리스트를 해석하여 명령어를 실행하고 결과 문자열을 반환한다."""
    if len(tokens) == 0:
        return None

    cmd = tokens[0].upper()

    # --- SET ---
    if cmd == "SET":
        if len(tokens) != 3:
            return "(error) ERR wrong number of arguments for 'SET' command"
        return redis.cmd_set(tokens[1], tokens[2])

    # --- GET ---
    if cmd == "GET":
        if len(tokens) != 2:
            return "(error) ERR wrong number of arguments for 'GET' command"
        return redis.cmd_get(tokens[1])

    # --- DEL ---
    if cmd == "DEL":
        if len(tokens) != 2:
            return "(error) ERR wrong number of arguments for 'DEL' command"
        return redis.cmd_del(tokens[1])

    # --- EXISTS ---
    if cmd == "EXISTS":
        if len(tokens) != 2:
            return "(error) ERR wrong number of arguments for 'EXISTS' command"
        return redis.cmd_exists(tokens[1])

    # --- DBSIZE ---
    if cmd == "DBSIZE":
        if len(tokens) != 1:
            return "(error) ERR wrong number of arguments for 'DBSIZE' command"
        return redis.cmd_dbsize()

    # --- KEYS ---
    if cmd == "KEYS":
        return redis.cmd_keys()

    # --- CONFIG ---
    if cmd == "CONFIG":
        if len(tokens) >= 2 and tokens[1].upper() == "SET":
            if len(tokens) == 4 and tokens[2].lower() == "maxmemory":
                return redis.cmd_config_set_maxmemory(tokens[3])
            return "(error) ERR wrong number of arguments for 'CONFIG SET' command"
        return "(error) ERR unknown subcommand '" + (tokens[1] if len(tokens) > 1 else "") + "'"

    # --- INFO ---
    if cmd == "INFO":
        if len(tokens) == 2 and tokens[1].lower() == "memory":
            return redis.cmd_info_memory()
        return "(error) ERR wrong number of arguments for 'INFO' command"

    # --- EXPIRE ---
    if cmd == "EXPIRE":
        if len(tokens) != 3:
            return "(error) ERR wrong number of arguments for 'EXPIRE' command"
        return redis.cmd_expire(tokens[1], tokens[2])

    # --- TTL ---
    if cmd == "TTL":
        if len(tokens) != 2:
            return "(error) ERR wrong number of arguments for 'TTL' command"
        return redis.cmd_ttl(tokens[1])

    # --- EXIT / QUIT ---
    if cmd in ("EXIT", "QUIT"):
        return "__EXIT__"

    return "(error) ERR unknown command '" + tokens[0] + "'"
