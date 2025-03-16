from latex_generator import generate_latex_table

data = [
    ["Name", "Age", "City"],
    ["Alice", 24, "New York"],
    ["Bob", 30, "Los Angeles"],
    ["Charlie", 22, "Chicago"],
    ["Diana", 28, "Houston"]
]

latex_table = generate_latex_table(data)

with open("../artifacts/2_1_latex_table.tex", "w", encoding="utf-8") as file:
    file.write(latex_table)
