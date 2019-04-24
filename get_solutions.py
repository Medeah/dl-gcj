from get_scoreboard import get
from sys import argv
from time import time, sleep
from pickle import load, dump

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x):
        return x


def main():
    round_id = argv[1]

    users = load(open("scoreboard" + round_id + ".pickle", "rb"))

    solutions = []
    last = 0
    for name in tqdm(map(lambda x: x["displayname"], users), total=len(users)):
        sleep(max(0., 1. - (time() - last)))
        last = time()
        res = get({'nickname': name}, id=round_id, type="attempts")
        for attempt in res["attempts"]:
            attempt["nickname"] = name
            attempt["challenge"] = round_id
        solutions.extend(res["attempts"])

    dump(solutions, open("solutions" + round_id + ".pickle", 'wb'))


if __name__ == "__main__":
    main()
