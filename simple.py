import sys
import os
import json

cwd = os.getcwd()
input_file = '{}/{}'.format(cwd, sys.argv[1])
output_file = '{}/{}'.format(cwd, sys.argv[2])

START_TOKEN = '#+begin_src jupyter'
END_TOKEN = '#+end_src'

notebook = ''

# print(input_file)
# print(output_file)

def construct_cell(cell_type, source):
    cell = {'cell_type': cell_type,
            'metadata': {},
            'source': source
            }
    return cell

def construct_notebook(cells):
    notebook = {'cells': cells,
             'metadata': {
                 'kernelspec': {
                     'display_name': 'Python 3',
                     'language': 'python',
                     'name': 'python3'
                 },
                 'language_info': {
                     'codemirror_mode': {
                         'name': 'ipython',
                         'version': 3
                     },
                     'file_extension': '.py',
                     'mimetype': 'text/x-python',
                     'name': 'python',
                     'nbconvert_exporter': 'python',
                     'pygments_lexer': 'ipython3',
                     'version': '3.8.5'
                 }
             },
             'nbformat': 4,
             'nbformat_minor': 4
            }
    return notebook

with open(input_file, 'r') as f:
    lines = f.readlines()
    tmp_cell_source = []
    cells = []
    for line in lines:
        if START_TOKEN in line:
            # Construct cell with current markdown source.
            cells.append(construct_cell('markdown', tmp_cell_source))
            tmp_cell_source = []

        elif END_TOKEN in line:
            # Construct cell with current code source.
            cells.append(construct_cell('code', tmp_cell_source))
            tmp_cell_source = []
        else:
            tmp_cell_source.append(line)

    notebook = construct_notebook(cells)

with open(output_file, 'w') as f:
    json.dump(notebook, f)
