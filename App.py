from Knapsack import *


def main():

    print("hello home")

    k = Knapsack(0, 0, 0, 0)
    k.readFromFile()
    N = 80
    M = 10
    k.run(N, M)


if __name__ == '__main__':
    main()