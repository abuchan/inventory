from qrtools import QR
import os
import glob
import subprocess

cwd = os.getcwd()

tex_dir = cwd + '/tex'
img_dir = tex_dir + '/img'
tex_filename = tex_dir + '/qr_codes.tex'

if not glob.glob(tex_dir):
  os.mkdir(tex_dir)

if not glob.glob(img_dir):
  os.mkdir(img_dir)


url_fmt = 'https://wiki.eecs.berkeley.edu/biomimetics/INV/%06d'

url_range = range(20)

tex_fmt = '''
\\documentclass{article}
\\usepackage{graphicx}
\\pagestyle{empty}

\\begin{document}
%s
\\end{document}
'''

figure_fmt = '\\includegraphics[width=%s]{%s}'

table_fmt = '''
\\begin{table}[h!]
\\begin{tabular}{%s}
%s
\\end{tabular}
\\end{table}
'''

def list_to_table(rows):
  n_col = len(rows[0])
  col_fmt = 'c'*n_col
  table_str = ''
  for row in rows:
    for elt in row:
      table_str += elt + ' & '
    table_str = table_str[:-3] + ' \\\\\n'

  return table_fmt % (col_fmt, table_str)

def generate(codes = range(20), width=2.0, cols = 5):
  width_str = '%fcm' % width

  tex_figs = ''

  c_strs = []
  f_strs = []

  for c in codes:
    c_str = '%06d' % c
    qr = QR(data = url_fmt % c)
    img_filename = img_dir + '/%s.png' % c_str 
    qr.encode(img_filename)
    c_strs.append(c_str)
    f_strs.append(figure_fmt % (width_str, img_filename))

  elts = []
  for i in range(0,len(codes),cols):
    elts.append(c_strs[i:i+cols])
    elts.append(f_strs[i:i+cols])

  tex_file = open(tex_filename, 'w')
  tex_file.write(tex_fmt % list_to_table(elts))
  tex_file.close()

  subprocess.check_call(['pdflatex',tex_filename],cwd=tex_dir)

if __name__ == '__main__':
  generate()
