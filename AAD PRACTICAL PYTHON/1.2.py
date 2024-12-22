n = input("Enter Numbers: ").split(' ')
num = [int(x) for x in n]
print(num)
least = float('inf')
ans = []
for i in range(len(num)):
    for j in range(i + 1, len(num)):
        diff = abs(num[i] + num[j])
        if diff < least:
            least = diff
            ans = [(num[i], num[j])]
        elif diff == least:
            ans.append((num[i], num[j]))
for pair in ans:
    print(pair[0], pair[1])
