import random
import numpy
from scipy import stats

def cochran(dispersion, m, G_table):
    return max(dispersion) / sum(dispersion) < G_table[m - 1]


def student(general_dispersion, m, y_mean, xn):
    statistic_dispersion = (general_dispersion / (N * m)) ** 0.5

    beta = [1 / N * sum(y_mean[j] for j in range(N))]
    for i in range(3):
        b = 0
        for j in range(N):
            b += y_mean[j] * xn[j][i]
        beta.append(1 / N * b)

    t = [abs(i) / statistic_dispersion for i in beta]

    return t[0] > stats.t.ppf((1 + (1 - 0.05)) / 2, (m - 1)*N), \
           t[1] > stats.t.ppf((1 + (1 - 0.05)) / 2, (m - 1)*N), \
           t[2] > stats.t.ppf((1 + (1 - 0.05)) / 2, (m - 1)*N), \
           t[3] > stats.t.ppf((1 + (1 - 0.05)) / 2, (m - 1)*N)


def phisher(m, d, y_mean, yo, dispersion_reproducibility):
    dispersion_adequacy = 0
    for i in range(N): dispersion_adequacy += (yo[i] - y_mean[i]) ** 2

    dispersion_adequacy = dispersion_adequacy * m / (N - d)
    fp = dispersion_adequacy / dispersion_reproducibility

    return fp < stats.f.ppf(1 - 0.05, N-d, (m - 1)*N)


def coef(x, y_mean):
    mx1, mx2, mx3 = sum([x[i][0] for i in range(N)]) / N, sum([x[i][1] for i in range(N)]) / N, \
                    sum([x[i][2] for i in range(N)]) / N

    my = sum(y_mean) / N

    a11, a22, a33 = sum([x[i][0] ** 2 for i in range(N)]) / N, sum([x[i][1] ** 2 for i in range(N)]) / N, \
                    sum([x[i][2] ** 2 for i in range(N)]) / N

    a12, a13, a23 = sum([x[i][0] * x[i][1] for i in range(N)]) / N, sum([x[i][0] * x[i][2] for i in range(N)]) / N, \
                    sum([x[i][1] * x[i][2] for i in range(N)]) / N

    a1, a2, a3 = sum([x[i][0] * y_mean[i] for i in range(N)]) / N, sum([x[i][1] * y_mean[i] for i in range(N)]) / N, \
                 sum([x[i][2] * y_mean[i] for i in range(N)]) / N

    a = numpy.array([[1, mx1, mx2, mx3], [mx1, a11, a12, a13], [mx2, a12, a22, a23], [mx3, a13, a23, a33]])
    c = numpy.array([my, a1, a2, a3])
    b = numpy.linalg.solve(a, c)
    return b


x1_min, x1_max = -10, 50
x2_min, x2_max = 25, 65
x3_min, x3_max = -10, 15

x_avg_min, x_avg_max = (x1_min + x2_min + x3_min) / 3, (x1_max + x2_max + x3_max) / 3
y_min, y_max = 200 + x_avg_min, 200 + x_avg_max

xn = [[-1, -1, -1],
      [-1, +1, +1],
      [+1, -1, +1],
      [+1, +1, -1]]

x = [[x1_min, x2_min, x3_min],
     [x1_min, x2_max, x3_max],
     [x1_max, x2_min, x3_max],
     [x1_max, x2_max, x3_min]]

m = 3
N = 4

y = [[random.randint(int(y_min), int(y_max)) for i in range(m)] for j in range(4)]
G_table = {1: 0.9065, 2: 0.7679, 3: 0.6841, 4: 0.6287, 5: 0.5892, 6: 0.5598, 7: 0.5365, 8: 0.5175, 9: 0.5017, 10: 0.488}

while True:
    while True:
        if m > 8:
            print("Error! ?????????????? ???????????????? m ???????????? ?????? ?????????????????????? ???????????????? ???? ???????????????? ?????????????????? ?????? ???????????????? ??????????????????.")
            exit(0)

        y_mean = [sum(y[i]) / m for i in range(N)]

        dispersion = []
        for i in range(len(y)):
            dispersion.append(0)
            for j in range(m):
                dispersion[i] += (y_mean[i] - y[i][j]) ** 2
            dispersion[i] /= m

        dispersion_reproducibility = sum(dispersion) / N

        if cochran(dispersion, m, G_table):
            break
        else:
            m += 1
            for i in range(N):
                y[i].append(random.randint(int(y_min), int(y_max)))

    k = student(dispersion_reproducibility, m, y_mean, xn)
    d = sum(k)

    b = coef(x, y_mean)
    b = [b[i] * k[i] for i in range(N)]

    yo = []
    for i in range(N):
        yo.append(b[0] + b[1] * x[i][0] + b[2] * x[i][1] + b[3] * x[i][2])

    if d == N:
        m += 1
        for i in range(N):
            y[i].append(random.randint(int(y_min), int(y_max)))

    elif phisher(m, d, y_mean, yo, dispersion_reproducibility):
        break
    else:
        m += 1
        for i in range(N):
            y[i].append(random.randint(int(y_min), int(y_max)))


table_values = ["#", "X1", "X2", "X3"]
for i in range(m): table_values.append("Yi{:d}".format(i + 1))

row_format = "|{:^11}" * (len(table_values))
header_separator_format = "+{0:=^11s}" * (len(table_values))
separator_format = "+{0:-^11s}" * (len(table_values))


print('\n\tx1 min:', x1_min, '\tx1 max:', x1_max, '\n\tx2 min:', x2_min, '\t\tx2 max:', x2_max,
      '\n\tx3 min:', x3_min, '\tx3 max:', x3_max, '\n\ty min:', "{:.2f}".format(y_min), '\ty max:', y_max, "\n\n" +
      header_separator_format.format("=") + "+\n" + row_format.format(*table_values) + "|\n" +
      header_separator_format.format("=") + "+")

for i in range(4):
    print("|{:^11}|{:^11}|{:^11}|{:^11}|".format(i+1, *x[i]), end="")
    for j in y[i]: print("{:^11}|".format(j), end="")
    print()

print(separator_format.format("-") + "+" + f"\n\n\t???????????????? ???????????????? ???????????????? ?????? m={m}: Y = {b[0]:.2f}", end='')
for i in range(1, 4):
    if b[i] != 0: print(" + {0:.2f}".format(b[i]) + "*X" + str(i), end="")
print("\n\n\t???? ?????????????????? ?????????????? ?????????????? ?????????????????? - ??????????????????."
      "\n\t???? ?????????????????? ?????????????????? ????????????????????: b0 - {}, b1 - {}, b2 - {}, b3 - {}.".format(*k),
      "\n\t???? ?????????????????? ???????????? ???????????????? ???????????????? ?????????????????? ??????????????????.")

print(f'\n\t?????????????????? ???????????????? ????????????????????????: {d}')

print("\n\t\t\t\t ??????????????????:")
print("+{0:-^14s}+{0:-^37s}+".format("-"))
for i in range(4):
    print("| Ys{0:1d} = {1:5.2f} | b0 + b1*X1 + b2*X2 + b3*X3 = {2:^7.2f}|\n".format(i+1, y_mean[i], b[0] + b[1] * x[i][0] + b[2] * x[i][1]), end="")
    print("+{0:-^14s}+{0:-^37s}+".format("-"))
