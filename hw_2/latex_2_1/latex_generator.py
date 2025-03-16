from typing import List


def generate_latex_table(data: List[List[str]]) -> str:
    columns_format = "{" + "|c" * len(data[0]) + "|}"
    rows_data = []
    for row in data:
        rows_data.append((" & ".join(map(str, row)) + " \\\\"))

    latex_code = ("\\centering\n"
                  f"\\begin{{tabular}}{columns_format}"
                  "\n\hline\n" +
                  rows_data[0] +
                  "\n\hline \hline\n" +
                  "\n\hline\n".join(rows_data[1:]) +
                  "\n\hline\n"
                  "\\end{tabular}"
                  )
    return latex_code
