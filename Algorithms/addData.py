import random
import argparse


def addData(file):
    with open(file, 'w') as r:
        for _ in range(22):
            value = random.randint(-1000, 1000)
            r.write(str(value))
            r.write(" ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dopisz losowe liczby do pliku.")
    parser.add_argument("--file", required=True, help="Nazwa pliku, do którego mają zostać dopisane liczby.")
    args = parser.parse_args()

    addData(args.file)