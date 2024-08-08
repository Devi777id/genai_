from setuptools import find_packages,setup

setup(
    name='mcqgen',
    version='0.0.1',
    author='bekiab',
    install_requires=["openai", "streamlit", "langchain","Python-dotenv", "PyPDF2"],
    packages=find_packages()
    
)