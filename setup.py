import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="getfx",
    version="0.1.0",
    author="Kamil Niklasinski",
    license="Apache 2",
    author_email="kamil.niklasinski@gmail.com",
    keywords='NBP API FX',
    description="Get FX is tool to retrieve average FX rates from NBP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'getfx'},
    packages=setuptools.find_packages(where='getfx'),
    install_requires=['requests'],
    setup_requires=['wheel'],
    project_urls={
        'source': 'https://github.com/kniklas/get-fx'
    },
    url="https://github.com/kniklas/get-fx",
    #  py_modules=["getfxnbp"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
)
