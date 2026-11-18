import argparse


def add(left: float, right: float) -> float:
    return left + right


def main() -> None:
    parser = argparse.ArgumentParser(description="计算两个数字的和")
    parser.add_argument("left", type=float, help="第一个数字")
    parser.add_argument("right", type=float, help="第二个数字")
    args = parser.parse_args()
    print(f"{add(args.left, args.right):g}")


if __name__ == "__main__":
    main()
