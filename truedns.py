from modules.Router import Router


def main():
    with Router('127.0.0.1', 53) as router:
        router.run()


if __name__ == '__main__':
    main()
