from setuptools import setup, find_packages

from djangoyearlessdate import get_version


setup(
    name="django-yearlessdate",
    version=get_version(),
    description="Django field for storing dates without years. Forked from seddonym/django-yearlessdate.",
    author="Jiri Zamazal",
    author_email="zamazal.jiri@gmail.com",
    url="http://github.com/zamazaljiri/django-yearlessdate",
    packages=find_packages(),
    include_package_data=True,
    package_dir={"djangoyearlessdate": "djangoyearlessdate"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Django",
    ],
    install_requires = [
        'Django >= 1.6',
        'six >= 1.5.2',
        'South >= 0.8.4',
    ]
)
