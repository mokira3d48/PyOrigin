from setuptools import setup, find_packages


setup(
    name="package-name",
    version="0.1.0",
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["origin", "python3", "author-keywords"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1",
    ],
    project_urls={
        "Homepage": "https://github.com/your-username/my-python-package",
        "Bug Tracker": "https://github.com/your-username/my-python-package/issues",
    },
)
