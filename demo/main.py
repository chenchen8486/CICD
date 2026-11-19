import argparse


def add(left: float, right: float) -> float:
    return left + right


def subtract(left: float, right: float) -> float:
    return left - right


def main() -> None:
    parser = argparse.ArgumentParser(description="计算两个数字的和或差")
    parser.add_argument("left", type=float, help="第一个数字")
    parser.add_argument("right", type=float, help="第二个数字")
    parser.add_argument(
        "--subtract",
        action="store_true",
        help="使用减法；不提供该选项时默认使用加法",
    )
    args = parser.parse_args()

    if args.subtract:
        result = subtract(args.left, args.right)
    else:
        result = add(args.left, args.right)

    print(f"{result:g}")


if __name__ == "__main__":
    main()
