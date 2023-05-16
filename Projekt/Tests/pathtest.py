import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
correct_dir = os.path.abspath(os.path.join(parent_dir, './Simulation Files'))

# print the parent directory
print(parent_dir)
print(current_dir)
print(correct_dir)