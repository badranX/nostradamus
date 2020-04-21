from distutils.core import setup, Extension

module = Extension("bobcatModule", sources = ["bobcatmodule.c"])

setup(name="BobcatPackage",
        version = "0.1",
        description = "This is a bobcat hash function package",
        ext_modules = [module]
        ) 
