from typing import List
from setuptools import find_packages, setup


HYPHEN_E_DOT='-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        # Strip leading/trailing spaces and newlines from each requirement
        requirements = [req.strip() for req in requirements if req.strip()]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements




setup(
    name='mlproject',
    version='0.0.1',
    author='Njagi',
    author_email='kevinnjagi83@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
