from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
project='Causal Dynamics Generators'
author='Tiago Martinelli'
release='0.2.0'
extensions=['sphinx.ext.autodoc','sphinx.ext.napoleon','sphinx.ext.mathjax','sphinx.ext.doctest','sphinx.ext.viewcode']
html_theme='sphinx_rtd_theme'
exclude_patterns=[]
autodoc_member_order='bysource'

html_title='Causal Dynamics Generators · Documentation'
html_short_title='Causal Dynamics'
html_baseurl='https://martinellitiago.github.io/causal-information-benchmark/'
html_static_path=['_static']
html_css_files=['theme.css']
html_theme_options={'navigation_depth':3,'style_nav_header_background':'#142f43','collapse_navigation':False}
html_show_sourcelink=False
