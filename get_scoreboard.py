from base64 import urlsafe_b64encode, urlsafe_b64decode
from json import loads, dumps
from urllib import request
from sys import argv
from time import sleep, time
from pickle import dump


def get(req, id="0000000000051635", type="scoreboard"):
    req = dumps(req).encode('utf-8')
    req = urlsafe_b64encode(req).decode("utf-8")
    url = "https://codejam.googleapis.com/{}/{}/poll?p={}".format(type, id, req)
    res = request.urlopen(url).read()
    missing_padding = len(res) % 4
    res += b"=" * missing_padding
    res = urlsafe_b64decode(res)
    res = res.decode("utf-8")
    return loads(res)


def main():
    round_id = argv[1]
    res = get({'num_consecutive_users': 1, 'min_rank': 1}, round_id)
    scoreboard_size = res["full_scoreboard_size"]

    batch_size = 200
    users = []
    last = time()
    for i in range(1, scoreboard_size + 1, batch_size):
        print(len(users))
        res = get({'num_consecutive_users': batch_size, 'min_rank': i}, round_id)
        users.extend(res["user_scores"])
        sleep(max(0., 1. - (time() - last)))
        last = time()

    dump(users, open("scoreboard"+round_id+".pickle", 'wb'))


if __name__ == "__main__":
    main()
