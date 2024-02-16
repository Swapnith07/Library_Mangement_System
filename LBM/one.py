import ast
from datetime import date

# Your string representation of a tuple
tuple_string = "[('swa', '1', datetime.date(2024, 2, 15))]"

# Import the datetime module before evaluating the string
# This ensures that the reference to `datetime` in the string is resolved correctly
my_list = ast.literal_eval(tuple_string)

# Access the second element of the first tuple in the list
element_1 = my_list[0][1]

print(element_1)
