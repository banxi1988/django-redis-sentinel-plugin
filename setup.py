from setuptools import setup

from django_redis_sentinel import __version__

description = """
Full featured redis cache backend for Django for Sentinel Redis Clusters.
"""

setup(
    name="django-redis-sentinel-plugin",
    url="https://github.com/banxi1988/django-redis-sentinel-plugin",
    author="Dani Gonzalez @danigosa,banxi1988",
    author_email="danigosa@gmail.com,banxi1988@gmail.com",
    version=__version__,
    packages=["django_redis_sentinel", "django_redis_sentinel.client"],
    description=description.strip(),
    install_requires=["django-redis==4.9.0"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
