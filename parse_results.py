#!/usr/bin/env python

import parse_lib
import os
import sys
sys.path.append(os.path.abspath(os.path.curdir))

def parse(fname):
  infile =  os.path.join(os.path.curdir,fname)
  with open(infile) as file:
    corpus = file.readlines()

  for l in corpus:
    if l.startswith('param_order:'): param_order = int(l.split(':')[1])
    if l.startswith('param_lim_type:'): param_lim_type = int(l.split(':')[1])
    if l.startswith('param_grid_x:'): param_grid_x = int(l.split(':')[1])
    if l.startswith('param_grid_y:'): param_grid_y = int(l.split(':')[1])

    if l.startswith('param_problem:'): param_problem = l.split(':')[1].rstrip()
    if l.startswith('param_solver_type:'): param_solver_type = l.split(':')[1].rstrip()

    if l.startswith('time_weno:'): time_weno = float(l.split(':')[1])
    if l.startswith('time_rp:'): time_rp = float(l.split(':')[1])
    if l.startswith('time_flux1:'): time_flux1 = float(l.split(':')[1])
    if l.startswith('time_flux2:'): time_flux2 = float(l.split(':')[1])
    if l.startswith('time_total:'): time_total = float(l.split(':')[1])
  
  return [param_problem, param_solver_type, param_order, param_lim_type, param_grid_x, param_grid_y, time_weno, time_rp, time_flux1, time_flux2, time_total]

thisdir = os.getcwd()
print "Parsing the results directory: " + thisdir
files = os.listdir(thisdir)

results=[]
for fname in files:
  if (fname.startswith("shallow2D")): 
    print "Parsing: " + fname
    results.append(parse(fname))

#print results

with open('results.csv', 'wb') as file:
  parse_lib.to_csv(results, file, head=('param_problem', 'param_solver_type', 'param_order', 'param_lim_type', 'param_grid_x', 'param_grid_y', 'time_weno', 'time_rp', 'time_flux1', 'time_flux2', 'time_total'))


