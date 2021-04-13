from distutils.core import setup

setup(
    name='course-scheduler',
    version='0.2',
    packages=['db', 'models', 'CIS_API'],
    package_dir={'': 'course_scheduler_server'},
    url='',
    license='',
    author='Dun Ma, Yiyin Shen',
    author_email='dunma2@illinois.edu',
    description='UIUC Course Scheduler'
)
