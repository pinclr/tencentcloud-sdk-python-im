import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tencentcloud-sdk-python-im",
    version="0.8.0",
    author="Robert Wen",
    author_email="robert@pinclr.com",
    description="Python API Client for Tencent Cloud Instant Messaging Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinclr/tencentcloud-sdk-python-im",
    packages=['tencentcloud_im'],
    package_dir={'': 'src'},
    package_data={'': ['tcim.json', '*.py']},
    install_requires = ['tls-sig-api-v2>=1.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
