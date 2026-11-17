from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
project='Omega D generators'
author='Tiago Martinelli'
release='0.1.0'
extensions=['sphinx.ext.autodoc','sphinx.ext.napoleon','sphinx.ext.mathjax','sphinx.ext.doctest','sphinx.ext.viewcode']
html_theme='sphinx_rtd_theme'
exclude_patterns=[]
autodoc_member_order='bysource'
