from setuptools import setup, find_packages

setup(
    name="insurance_analytics",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'xgboost>=1.5.0'
    ],
    python_requires='>=3.8',
)