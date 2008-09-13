#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-


__author__ = 'Justin S Bayer, bayer.justin@googlemail.com'


import os

from setuptools import setup, find_packages
from distutils.ccompiler import new_compiler


def compileArac():
    sources = [
        'arac/src/c/arac.c',
        'arac/src/c/common.c',
        'arac/src/c/functions.c',
        'arac/src/c/connections/common.c',
        'arac/src/c/connections/connections.c',
        'arac/src/c/connections/full.c',
        'arac/src/c/connections/identity.c',
        'arac/src/c/layers/bias.c',
        'arac/src/c/layers/common.c',
        'arac/src/c/layers/layers.c',
        'arac/src/c/layers/linear.c',
        'arac/src/c/layers/lstm.c',
        'arac/src/c/layers/mdlstm.c',
        'arac/src/c/layers/sigmoid.c',
    ]
    
    compiler = new_compiler(verbose=True)

    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        # Workaround for distutils to recognize .c files as c++files.
        compiler.language_map['.c'] = 'c++'
        executables = {'preprocessor' : None,
                   'compiler'     : ["g++"],
                   'compiler_so'  : ["g++"],
                   'compiler_cxx' : ["g++"],
                   'linker_so'    : ["g++", "-shared"],
                   'linker_exe'   : ["g++"],
                   'archiver'     : ["ar", "-cr"],
                   'ranlib'       : None,
                  }
        compiler.set_executables(**executables)
        # Add some directories, this should maybe more sophisticated
        compiler.add_include_dir('/usr/local/include')
        compiler.add_include_dir('/usr/include')
        compiler.add_include_dir('/sw/include')
        compiler.add_include_dir('/sw/lib')
        compiler.add_library_dir('/usr/local/lib')
        compiler.add_library_dir('/usr/lib')
        output_dir = '/usr/local/lib'
    elif sys.platform.startswith('win'):
        raise NotImplementedError("No support for arac on windows yet.")
    else:
        raise NotImplementedError("Unknown platform: %s." % sys.platform)        
        
    compiler.add_library('m')
    compiler.add_library('blas')
    compiler.add_library('c')
    compiler.add_library('stdc++')
    objects = compiler.compile(sources)
    compiler.link_shared_lib(objects=objects, 
                             output_libname='arac', 
                             target_lang='c++', 
                             output_dir=output_dir)


setup(
    name="PyBrain",
    version="0.2pre",
    description="PyBrain is the swiss army knife for neural networking.",
    license="BSD",
    keywords="Neural Networks Machine Learning",
    url="http://pybrain.org",
    
    packages=find_packages(exclude=['examples', 'docs']),
    include_package_data=True,
    
    test_suite='pybrain.tests.runtests.make_test_suite',
)