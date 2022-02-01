#!/usr/bin/python
# -*- coding: UTF-8 -*-

import nbformat as nbf
import nbconvert as nb
import os
import re
from matplotlib import pyplot as plt

JUP_PATH='../jupyter'

def main():    
    for file in os.listdir(JUP_PATH):
        fname = os.fsdecode(file)
        print(f"nummerates {fname}")
        if fname.endswith(".ipynb"): 
            recount_and_replace(fname,'#### Eksempel')
            recount_and_replace(fname,'#### Oppgave')
            convert_ipynb_to_html(fname)


def recount_and_replace(fname,what):
    if len(what.split(' '))!=2 or not ('#' in what):
        raise RuntimeError(f'what needs to be on the form "#### word", not {what}')
    f=open(JUP_PATH+"/"+fname)
    s=f.read()
    i=1
    n=0
    while True:
        m=re.search(what+' (\d+)',s[n:])
        if m is None:
            break
        old=s[m.start()+n:m.end()+n]
        new=f'{what} {i}'
        s=s[:m.start()+n]+new+s[m.end()+n:]
        s=replace_references(s, old, new)
        n+=m.end()
        i+=1
    f.close()
    if i>1:
        f=open(JUP_PATH+"/"+fname,'w',newline='')
        f.write(s)        
        f.close()

        
def replace_references(s,old,new):
    n=0
    old=old[old.find(' ')+1:]
    new=new[new.find(' ')+1:]
    if old==new:
        return s
    while True:
        m=re.search(f"\\w*(?<!#### ){old}",s[n:])
        if m is None:
            break
        s=s[:m.start()+n]+new+s[m.end()+n:]
        n+=m.end()
    return s

def convert_ipynb_to_html(file):
    html,res=nb.HTMLExporter(template_name='Classic').from_filename(JUP_PATH+"/"+file)
    html=html.replace('.ipynb">','.html">')
    f=open("../"+file.replace('.ipynb','.html'),'w',encoding="utf-8")
    f.write(html)
    f.close()


main()