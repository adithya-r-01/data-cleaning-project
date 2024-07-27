'''
Converts Jupyter notebooks into standalone Python scripts
'''

import nbformat

# Load the Jupyter notebook
with open("./DataCleaningChanges.ipynb", "r", encoding="utf-8") as file:
    notebook = nbformat.read(file, as_version=4)

# Collect all code into a single script
script_code = ""
for cell in notebook.cells:
    if cell.cell_type == "code":
        script_code += "\n".join(cell.source.split("\n"))
        script_code += "\n\n"

# Save the code to a single Python file
script_path = "./DataCleaningChanges.py"
with open(script_path, "w", encoding="utf-8") as file:
    file.write(script_code)

script_path
