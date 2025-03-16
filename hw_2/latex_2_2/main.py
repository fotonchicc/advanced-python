from latex_generator_fotonchicc import latex_generator as lg

data = [
    ["Name", "Age", "City"],
    ["Alice", 24, "New York"],
    ["Bob", 30, "Los Angeles"],
    ["Charlie", 22, "Chicago"],
    ["Diana", 28, "Houston"]
]

latex_table = lg.generate_latex_table(data)

latex_image = lg.generate_latex_image("image.png")

latex_document = f"""\
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[english]{{babel}}
\\usepackage{{graphicx}}

\\begin{{document}}

{latex_table}

{latex_image}

\\end{{document}}
"""

with open("2_2_latex_doc.tex", "w", encoding="utf-8") as file:
    file.write(latex_document)
