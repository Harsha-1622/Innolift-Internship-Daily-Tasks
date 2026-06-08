# Function to print multiplication table
def times_table(n):
    print(f"\nMultiplication Table of {n}")
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")

# Call the function for 3 different numbers
times_table(5)
times_table(7)
times_table(10)