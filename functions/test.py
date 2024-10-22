a = [[True, True, True, True, False],
[True, True, True, True, False],
[True, True, False, True, False],
[True, True, True, True, True],
[True, True, True, False, False],
[False, False, True, False, False],
[True, True, False, True, False],
[True, True, True, True, False],
[True, True, True, True, False],
[True, False, True, True, True],
[True, True, True, True, False],
[False, False, True, False, False]]
for j in a:
    for i in range(len(j) - 1, -1, -1):
        print(5555)
        if (True in j[0:i]) and (True in j[i + 1: len(j)]):
            j[i] = True
    print(j)