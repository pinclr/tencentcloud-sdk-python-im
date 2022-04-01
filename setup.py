import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tencentcloud-sdk-python-tim",
    version="0.0.1",
    author="Robert Wen",
    author_email="robert@pinclr.com",
    description="Python API Client for Tencent IM Product",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinclr/tencentcloud-sdk-python-tim",
    packages=['tencentcloud_tim'],
    package_dir={'': 'src'},
    package_data={'': ['tim.json', '*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
