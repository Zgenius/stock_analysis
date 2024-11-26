from setuptools import setup, find_packages

# 可编辑模块
setup(
    name="cair_analysis",
    version="0.1",
    packages=find_packages(where = "src"),
    package_dir={"": "src"}
)