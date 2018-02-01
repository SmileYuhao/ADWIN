#!/usr/bin/env python

from distutils.core import setup

config = {
    'description': 'Algorithms for detecting changes from a data stream.',
    'author': 'Smile Yuhao',
    'url': 'https://github.com/SmileYuhao/ConceptDrift',
    'download_url': 'https://github.com/SmileYuhao/ConceptDrift',
    'version': '1.0',
    'install_requires': [
        'numpy',
        'pandas'
        'scikit-learn'
    ],
    'packages': ['concept_drift', 'classifier'],
    'name': 'ConceptDrift'
}

setup(**config)
