def loadData(path):
    with open(path) as f:
        return list(map(int, f.read().strip().split()))
