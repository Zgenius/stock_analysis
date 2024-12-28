from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.yaml'):
                paths.append(os.path.join(path, filename))
    return paths

extra_files = package_files('src/config')

# 可编辑模块
setup(
    name="cair_analysis",
    version="0.1",
    packages=find_packages(where = "src"),
    package_dir={"": "src"},
    package_data={
        '': extra_files,
    },
    include_package_data=True,
    install_requires=open('src/cair_analysis.egg-info/requires.txt').read().splitlines()
)