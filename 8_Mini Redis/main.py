"""
Mini Redis CLI - REPL 진입점

사용자가 명령어를 입력하면 즉시 실행 결과를 확인할 수 있는
대화형 인터페이스를 제공한다.
"""

from mini_redis import MiniRedis, parse_input, execute


def main():
    redis = MiniRedis()

    while True:
        try:
            raw = input("mini-redis> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        tokens = parse_input(raw)
        if len(tokens) == 0:
            continue

        result = execute(redis, tokens)
        if result == "__EXIT__":
            break
        if result is not None:
            print(result)


if __name__ == "__main__":
    main()
