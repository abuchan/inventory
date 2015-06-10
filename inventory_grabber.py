#!/usr/bin/python

from collections import OrderedDict
import glob
import re

#Produce an ordered dict of page text variables froma complete wiki page string
def wiki_to_dict(wiki_str):
  d = OrderedDict([('inv_no','')])
  name_match = re.search(r'name=.*\n',wiki_str)
  if name_match is not None:
    d['inv_no'] = name_match.group(0).strip().split('.')[-1]
  text_match = re.search(r'text=.*\n',wiki_str)
  if text_match is not None:
    lines = text_match.group(0).split('%0a')
    attr_list = [[i.strip() for i in l.split(':')][1:] for l in lines if re.match(r':.*:',l)]
    d.update(attr_list)
  return d

def grab_inventory():
  # Parse template to get default attributes and order
  template_filename = 'data/INV.Template'
  template_file = open(template_filename)
  template = wiki_to_dict(template_file.read())
  template_file.close()

  filenames = glob.glob('data/INV.0*')
  filenames.sort()

  items = []

  for fn in filenames:
    f = open(fn)
    d = wiki_to_dict(f.read())
    f.close()
    items.append(d)

    #Extend template dictionary with new attribute keys
    template.update(d)
  
  return template, items

def dict_to_csv(template, items):
  filename = 'inventory.csv'
  cfile = open(filename,'w')
  cfile.write(''.join([k+';' for k in template.keys()]) + '\n')
  for item in items:
    for key in template.keys():
      if key in item.keys():
        cfile.write(item[key])
      cfile.write(';')
    cfile.write('\n')
  cfile.close()
  
if __name__ == '__main__':
  template,items = grab_inventory()
  dict_to_cvs(template,items)
