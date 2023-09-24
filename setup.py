from setuptools import setup, find_packages

setup(
    name='voice-ai-app',
    version='1.0.0',
    description='Voice AI AIY ',
    long_description='Python application which interact with AIY Voice Kit, which help you build intelligent systems that can understand what they hear.',
    author='Anton Leliuk',
    author_email='anton.leluk@gmail.com',
    project_urls={
        'GitHub: issues': 'https://github.com/google/aiyprojects-raspbian/issues',
        'GitHub: repo': 'https://github.com/google/aiyprojects-raspbian',
    },
    license='Apache 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'gpiozero==1.6.2',
        'RPi.GPIO==0.7.1',
        'wit==6.0.1',
        'SQLite4==0.1.1',
        'pyttsx3==2.90',
        'python-dotenv==0.21.1',
        'paho-mqtt==1.6.1'
    ],
    python_requires='==3.7.3',
)