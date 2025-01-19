from app.runner import Runner


def main() -> None:
    runner = Runner()
    runner.start()
    try:
        runner.run()
    finally:
        runner.stop()


if __name__ == "__main__":
    main()
