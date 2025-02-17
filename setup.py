# Agency1/setup.py
from setuptools import setup, find_packages

setup(
    name="agency1",
    version="0.1.0",
    packages=find_packages(),
    
    # Dependencies
    install_requires=[
        "psutil>=5.9.0",
        "requests>=2.27.1",
    ],
    
    # Optional development dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.1.0',
            'mypy>=0.931',
        ]
    },
    
    # Metadata
    author="Agency1 Development Team",
    author_email="info@agency1.example.com",
    description="Advanced neural processing system with integrated services",
    keywords="neural, processing, AI, memory",
    url="https://github.com/agency1/agency1",
    
    # Entry points
    entry_points={
        'console_scripts': [
            'agency1=agency1.main:main',
        ],
    },
    
    # Package data
    include_package_data=True,
    package_data={
        'agency1.brain_v4.config': ['*.json', '*.md'],
    },
    
    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)