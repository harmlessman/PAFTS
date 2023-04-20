from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt", 'r', encoding='utf-8') as f:
    requirements = f.read()

setup(
    name='pafts',
    version='0.0.0',
    author='harmlessman',
    author_email="harmlessman17@gmail.com",
    description='Library That Preprocessing Audio For TTS.',
    install_requires=requirements,
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/harmlessman/PAFTS',
    python_requires=">=3.8, <3.11",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]

)