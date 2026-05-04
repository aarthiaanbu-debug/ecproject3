numbers= [1,2,3,4,5,3,2]
duplicate = []
for num in numbers:
    if numbers.count(num)> 1 and num not in duplicates:
    duplicates.append(num)
print("Duplicate elements:",duplicate)


