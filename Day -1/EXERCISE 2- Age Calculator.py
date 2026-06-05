# Program to calculate age and age after 10 years

birth_year = int(input("Enter your birth year: "))

try:
    age = 2026 - birth_year

    # Raise an error if the year is greater than 2026
    assert birth_year <= 2026, "Error: Birth year cannot be greater than 2026."

    print(f"Your age in 2026 is {age} years.")
    print(f"Your age after 10 years will be {age + 10} years.")

except AssertionError as e:
    print(e)