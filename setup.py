try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="bambulabs_api",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="API for BambuLabs 3D Printers over MQTT",
    long_descritpion="""
    API for BambuLabs 3D Printers over MQTT
    """,
    url="https://github.com/acse-ci223/bambulabs_api",
    author="Chris Ioannidis",
    author_email="chris.ioannidis23@imperial.ac.uk",
    packages=["bambulabs_api"],
)
