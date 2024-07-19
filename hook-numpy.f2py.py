# hook-numpy.f2py.py
from PyInstaller.utils.hooks import copy_metadata, collect_submodules

hiddenimports = collect_submodules('numpy.f2py')
datas = copy_metadata('numpy')
