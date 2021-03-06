from distutils.core import setup
from Cython.Build import cythonize
import sys

'''
Compiling python into cyton code to speedup execution
'''

print("Cytonizing your files")
setup(
  name = 'test',
  ext_modules = cythonize(["tags_similarity.py", "API_methods_similarity.py", "textual_similarity.py"]),
)
