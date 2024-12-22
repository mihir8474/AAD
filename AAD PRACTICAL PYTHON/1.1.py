chef1Inp = input("Enter Chef-1 ratings: ").split(' ')
chef2Inp = input("Enter Chef-2 ratings: ").split(' ')
chef1 = [int(rating) for rating in chef1Inp]
chef2 = [int(rating) for rating in chef2Inp]
chef1Points = 0
chef2Points = 0
output = []
for idx in range(len(chef1)):
    if chef1[idx] == chef2[idx]:
        continue
    elif chef1[idx] > chef2[idx]:
        chef1Points += 1
    else:
        chef2Points += 1

output.append(chef1Points)
output.append(chef2Points)
print(output)
