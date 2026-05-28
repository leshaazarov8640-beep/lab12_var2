def calc(b, r, bk, d):
    p = 0
    for i in range(len(b)):
        if b[i][4] is None:
            dd = (d - b[i][3]).days
            if dd > 14:
                f = dd * 0.5
                p = p + f
                if r[i][3] == "premium":
                    p = p - p * 0.1
                if r[i][3] == "student":
                    if f > 5:
                        p = p - 2
    for i in range(len(b)):
        if b[i][4] is None:
            for j in range(len(bk)):
                if bk[j][0] == b[i][1]:
                    if bk[j][5] == 0:
                        p = p + 10
    return p


def sv(d, fn):
    f = open(fn, "w")
    for x in d:
        f.write(f"{x[0]},{x[1]},{x[2]},{x[3]}\n")
    f.close()
