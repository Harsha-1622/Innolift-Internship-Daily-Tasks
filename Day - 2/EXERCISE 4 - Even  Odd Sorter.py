# Function to separate even and odd numbers
def sort_numbers(numbers):
    even = []
    odd = []
    for num in numbers:
        if num % 2 == 0:
            even.append(num)
        else:
            odd.append(num)
    return even, odd
# Test with 10 numbers
numbers = [12, 19, 54, 69, 96, 28, 1, 60, 51, 30]

even_numbers, odd_numbers = sort_numbers(numbers)

print("Original List:", numbers)
print("Even Numbers List:", even_numbers)
print("Odd Numbers List:", odd_numbers)