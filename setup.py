import setuptools
from glob import glob
from os.path import basename
from os.path import splitext

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="getfx",
    author="Kamil Niklasinski",
    license="Apache 2",
    author_email="kamil.niklasinski@gmail.com",
    version="0.1.0",
    keywords='NBP API FX',
    description="Get FX is tool to retrieve average FX rates from NBP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=['requests'],
    setup_requires=['setuptools', 'wheel'],
    entry_points={
        "console_scripts": ["getfx = getfx.getfxnbp:init_cmd"]},
    project_urls={
        'source': 'https://github.com/kniklas/get-fx'
    },
    url="https://github.com/kniklas/get-fx",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7',
    platforms='any',
)
