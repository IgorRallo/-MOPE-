import random

m = [[random.randint(0, 20) for i in range(3)] for i in range(8)]
print("Значення факторів у точках експерименту:")
for i in m:
    print(i)

a0 = random.randint(0, 20)
a1 = random.randint(0, 20)
a2 = random.randint(0, 20)
a3 = random.randint(0, 20)

Y_list = []
for x in m:
    Y = a0 + a1 * x[0] + a2 * x[1] + a3 * x[2]
    Y_list.append(Y)
print(f"\nФункції відгуку у кожній точці експерименту:\n{Y_list}\n")

Yc = (max(Y_list) + min(Y_list)) / 2

x0_1_list = {m[i][0] for i in range(8)}
x0_2_list = {m[i][1] for i in range(8)}
x0_3_list = {m[i][2] for i in range(8)}

x0_1 = (max(x0_1_list) + min(x0_1_list)) / 2
dx_1 = x0_1 - min(x0_1_list)

x0_2 = (max(x0_2_list) + min(x0_2_list)) / 2
dx_2 = x0_2 - min(x0_2_list)

x0_3 = (max(x0_3_list) + min(x0_3_list)) / 2
dx_3 = x0_3 - min(x0_3_list)

print(
    f"0 рівень для 1 фактору :\nX0 = {x0_1}\ndx = {dx_1}\n\n0 рівень для 2 фактору :\nX0 = {x0_2}\ndx = {dx_2}\n\n0 рівень для 3 фактору :\nX0 = {x0_3}\ndx = {dx_3}\n")

x0_list = [x0_1, x0_2, x0_3]
dx_list = [dx_1, dx_2, dx_3]

normalization = []
print("Значення факторів у точках експерименту після нормалізації:")
for i in range(8):
    normalization.append([])
    for j in range(3):
        normalization[i].append(round(((m[i][j] - x0_list[j]) / dx_list[j]), 5))
        if j == 2:
            print(normalization[i])

Yet = a0 + a1 * x0_1 + a2 * x0_2 + a3 * x0_3

print(f"\nФ-ція відгуку від нульових рівнів факторів :\nYет = {Yet}")

distinc = []  # (Yi - Yет)

for Y in Y_list:
    distinc.append(Y - Yet)
print(f"\nРізниця ф-цій відгуку і ф-ції відгуку від нульових рівнів факторів:\n{distinc}")

min_d = distinc[0]
for d in distinc:
    if d < 0:
        continue
    else:
        if min_d < 0:
            min_d = d
        elif d < abs(min_d):
            min_d = d
print(f"\nЗначення функції відгуку, яке найблище до значення еталонної ф-ції відгуку:\n{min_d + Yet}")

k = 0
for i in range(len(Y_list)):
    if (Yc == Y_list[i]):
        print(f"\nТочка плану, що задовольняє критерій оптимальності (Y <--):\n{m[i]}")
        k += 1

if k == 0:
    print(f"\nТочки плану, що задовольняє критерій оптимальності не існує")