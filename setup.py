#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
import tempfile
import setuptools
import runpy

# Ref : https://packaging.python.org/single_source_version/#single-sourcing-the-version
# runpy is safer and a beter habit than exec
version = runpy.run_path('pyros_msgs/typecheck/_version.py')
__version__ = version.get('__version__')

# Including generator module directly from code to be able to generate our message classes
# Ref : http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
import imp
rosmsg_generator = imp.load_source('rosmsg_generator', 'pyros_msgs/importer/rosmsg_generator.py')


# Best Flow :
# Clean previous build & dist
# $ gitchangelog >CHANGELOG.rst
# change version in code and changelog
# $ python setup.py prepare_release
# WAIT FOR TRAVIS CHECKS
# $ python setup.py publish
# => TODO : try to do a simpler "release" command

# TODO : command to retrieve extra ROS stuff from a third party release repo ( for ROS devs ). useful in dev only so maybe "rosdevelop" ? or via catkin_pip ?
# TODO : command to release to Pip and ROS (bloom) same version one after the other...


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class GenerateMsgCommand(setuptools.Command):
    """Command to generate message class"""
    description = "generate messages for pyros_msgs"
    user_options = []

    def initialize_options(self):
        """init options"""
        # TODO : pass distro path [indigo|jade|etc.]
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""

        # generating message class
        generated = rosmsg_generator.generate_msgsrv_nspkg(
            [os.path.join(os.path.dirname(__file__), 'msg', 'OptionalFields.msg')],
            package='pyros_msgs',
            ns_pkg=False,  # no need to generate ns_pkg here, we can use the one we already have
        )

        # Note we have a tricky problem here since the ros distro for our target needs to be installed on the machine packaging this...
        # But pip packages are supposed to work on any platform, so we might need another way...

        print("Check that the messages classes have been generated properly...")
        sys.exit()


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PrepareReleaseCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "prepare a release of pyros"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""

        # TODO :
        # $ gitchangelog >CHANGELOG.rst
        # change version in code and changelog
        subprocess.check_call(
            "git commit CHANGELOG.rst pyros_msgs/typecheck/_version.py -m 'v{0}'".format(__version__), shell=True)
        subprocess.check_call("git push", shell=True)

        print("You should verify travis checks, and you can publish this release with :")
        print("  python setup.py publish")
        sys.exit()

# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PublishCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "releases pyros to Pypi"
    user_options = []

    def initialize_options(self):
        """init options"""
        # TODO : register option
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        # TODO : clean build/ and dist/ before building...
        subprocess.check_call("python setup.py sdist", shell=True)
        subprocess.check_call("python setup.py bdist_wheel", shell=True)
        # OLD way:
        # os.system("python setup.py sdist bdist_wheel upload")
        # NEW way:
        # Ref: https://packaging.python.org/distributing/
        subprocess.check_call("twine upload dist/*", shell=True)

        subprocess.check_call("git tag -a {0} -m 'version {0}'".format(__version__), shell=True)
        subprocess.check_call("git push --tags", shell=True)
        sys.exit()


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class RosDevelopCommand(setuptools.Command):

    """Command to mutate this package to a ROS package, using its ROS release repository"""
    description = "mutate this package to a ROS package using its release repository"
    user_options = []

    def initialize_options(self):
        """init options"""
        # TODO : add distro selector
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        # dynamic import for this command only to not need these in usual python case...
        import git
        import yaml

        """runner"""
        repo_path = tempfile.mkdtemp(prefix='rosdevelop-' + os.path.dirname(__file__))  # TODO get actual package name ?
        print("Getting ROS release repo in {0}...".format(repo_path))
        # TODO : get release repo from ROSdistro
        rosrelease_repo = git.Repo.clone_from('https://github.com/asmodehn/pyros-msgs-rosrelease.git', repo_path)

        # Reset our working tree to master
        origin = rosrelease_repo.remotes.origin
        rosrelease_repo.remotes.origin.fetch()  # assure we actually have data. fetch() returns useful information
        # Setup a local tracking branch of a remote branch
        rosrelease_repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()

        print("Reading tracks.yaml...")
        with open(os.path.join(rosrelease_repo.working_tree_dir, 'tracks.yaml'), 'r') as tracks:
            try:
                tracks_dict = yaml.load(tracks)
            except yaml.YAMLError as exc:
                raise

        patch_dir = tracks_dict.get('tracks', {}).get('indigo', {}).get('patches', {})

        print("Found patches for indigo in {0}".format(patch_dir))
        src_files = os.listdir(os.path.join(rosrelease_repo.working_tree_dir, patch_dir))

        working_repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))

        # adding patched files to ignore list if needed (to prevent accidental commit of patch)
        # => BETTER if the patch do not erase previous file. TODO : fix problem with both .travis.yml
        with open(os.path.join(working_repo.working_tree_dir, '.gitignore'), 'a+') as gitignore:
            skipit = []
            for line in gitignore:
                if line in src_files:
                    skipit += line
                else:  # not found, we are at the eof
                    for f in src_files:
                        if f not in skipit:
                            gitignore.write(f+'\n')  # append missing data

        working_repo.git.add(['.gitignore'])  # adding .gitignore to the index so git applies it (and hide new files)

        for file_name in src_files:
            print("Patching {0}".format(file_name))
            full_file_name = os.path.join(rosrelease_repo.working_tree_dir, patch_dir, file_name)
            if os.path.isfile(full_file_name):
                # Special case for package.xml and version template string
                if file_name == 'package.xml':
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'package.xml'), "wt") as fout:
                        with open(full_file_name, "rt") as fin:
                            for line in fin:
                                fout.write(line.replace(':{version}', __version__))  # TODO: proper template engine ?
                else:
                    shutil.copy(full_file_name, os.path.dirname(os.path.abspath(__file__)))

        sys.exit()


class ROSPublishCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "releases pyros-msgs to ROS"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        # TODO : distro from parameter. default : ['indigo', 'jade', 'kinetic']
        subprocess.check_call("git tag -a ros-{0} -m 'version {0} for ROS'".format(__version__), shell=True)
        subprocess.check_call("git push --tags", shell=True)
        # TODO : guess the ROS package name
        subprocess.check_call("bloom-release --rosdistro indigo --track indigo pyros_msgs", shell=True)
        sys.exit()


setuptools.setup(name='pyros_msgs',
    version=__version__,
    description='Pyros messages and services definition',
    url='http://github.com/asmodehn/pyros-msgs',
    author='AlexV',
    author_email='asmodehn@gmail.com',
    license='MIT',
    packages=[
        'pyros_msgs',
        # 'pyros_msgs.msg',  #TODO : generate this for pure python package, in a way that is compatible with catkin (so we can still use catkin_make with this)
        'pyros_msgs.typecheck', 'pyros_msgs.typecheck.tests',
        'pyros_msgs.opt_as_array', 'pyros_msgs.opt_as_array.tests',
        'pyros_msgs.opt_as_nested', 'pyros_msgs.opt_as_nested.tests',
    ],
    namespace_packages=['pyros_msgs'],
    # this is better than using package data ( since behavior is a bit different from distutils... )
    include_package_data=True,  # use MANIFEST.in during install.
    # Reference for optional dependencies : http://stackoverflow.com/questions/4796936/does-pip-handle-extras-requires-from-setuptools-distribute-based-sources
    install_requires=[
        # this is needed as install dependency since we embed tests in the package.
        # 'pyros_setup>=0.2.1',  # needed to grab ros environment even if distro setup.sh not sourced
        # 'pyros_utils',  # this must be satisfied by the ROS package system...
        # 'importlib2>=3.4;python_version<"3.4"',  # NOT working we use a patched version of it, through a symlink (to make linux deb release possible)
        'filefinder2; python_version<"3.4"',  # we rely on this for PEP420 on python 2.7
        'pyyaml>=3.10',  # genpy relies on this...
        'pytest>=2.8.0',  # as per hypothesis requirement (careful with 2.5.1 on trusty)
        'pytest-xdist',  # for --boxed (careful with the version it will be moved out of xdist)
        'hypothesis>=3.0.1',  # to target xenial LTS version
        'numpy>=1.8.2',  # from trusty version
    ],
    cmdclass={
        'generatemsg': GenerateMsgCommand,
        'rosdevelop': RosDevelopCommand,
        'rospublish': ROSPublishCommand,
    },
    zip_safe=False,  # TODO testing...
)

