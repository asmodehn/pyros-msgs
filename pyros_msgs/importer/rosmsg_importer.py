from __future__ import absolute_import, division, print_function

import imp

import py

"""
A module to setup custom importer for .msg and .srv files
Upon import, it will first find the .msg file, then generate the python module for it, then load it.

TODO...
"""

# We need to be extra careful with python versions
# Ref : https://docs.python.org/dev/library/importlib.html#importlib.import_module

# Ref : http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
# Note : Couldn't find a way to make imp.load_source deal with packages or relative imports (necessary for our generated message classes)
import os
import sys

# This will take the ROS distro version if ros has been setup
import genpy.generator
import genpy.generate_initpy

import logging


class ROSLoader(object):
    def __init__(self, generator, ext):
        self.ext = ext
        self.generator = generator

    # defining this to benefit from backward compat import mechanism in python 3.X
    def get_filename(self, name):
        os.sep.join(name.split(".")) + '.' + self.ext

    # defining this to benefit from backward compat import mechanism in python 3.X
    def is_package(self, name):
        return None  # TODO : implement check

    def load_module(self, fullname):


        return

# https://pymotw.com/2/sys/imports.html#sys-imports
class NoisyImportFinder(object):
    PATH_TRIGGER = 'NoisyImportFinder_PATH_TRIGGER'

    def __init__(self, path_entry):
        print('Checking NoisyImportFinder support for %s' % path_entry)
        if path_entry != self.PATH_TRIGGER:
            print('NoisyImportFinder does not work for %s' % path_entry)
            raise ImportError()
        return

    def find_module(self, fullname, path=None):
        print('NoisyImportFinder looking for "%s"' % fullname)
        return None

# https://pymotw.com/3/sys/imports.html#sys-imports

# class NoisyImportFinder:
#
#     PATH_TRIGGER = 'NoisyImportFinder_PATH_TRIGGER'
#
#     def __init__(self, path_entry):
#         print('Checking {}:'.format(path_entry), end=' ')
#         if path_entry != self.PATH_TRIGGER:
#             print('wrong finder')
#             raise ImportError()
#         else:
#             print('works')
#         return
#
#     def find_module(self, fullname, path=None):
#         print('Looking for {!r}'.format(fullname))
#         return None
#
#
# sys.path_hooks.append(NoisyImportFinder)





if sys.version_info >= (3, ):
    class ROSImportFinder(object):

        PATH_TRIGGER = 'ROSFinder_PATH_TRIGGER'

        def __init__(self, path_entry):

            self.logger = logging.getLogger(__name__)
            self.logger.debug('Checking ROSImportFinder support for %s' % path_entry)
            if path_entry != self.PATH_TRIGGER:
                self.logger.debug('ROSImportFinder does not work for %s' % path_entry)
                raise ImportError()

            self.loaders = {
                '.srv': ROSLoader(genpy.generator.SrvGenerator(), 'srv'),
                '.msg': ROSLoader(genpy.generator.MsgGenerator(), 'msg')
            }

        def find_module(self, fullname, path=None):
            print('ROSImportFinder looking for "%s"' % fullname)
            return None

elif sys.version_info >= (2, 7, 12):
    class ROSImportFinder(object):
        PATH_TRIGGER = 'ROSFinder_PATH_TRIGGER'

        def __init__(self, path_entry):
            self.logger = logging.getLogger(__name__)
            self.logger.debug('Checking ROSImportFinder support for %s' % path_entry)
            if path_entry != self.PATH_TRIGGER:
                self.logger.debug('ROSImportFinder does not work for %s' % path_entry)
                raise ImportError()

            self.loaders = {
                '.srv': ROSLoader(genpy.generator.SrvGenerator(), 'srv'),
                '.msg': ROSLoader(genpy.generator.MsgGenerator(), 'msg')
            }

        def find_module(self, fullname, path=None):
            print('ROSImportFinder looking for "%s"' % fullname)
            return None

else:
    class ROSImportFinder(object):

        PATH_TRIGGER = 'ROSFinder_PATH_TRIGGER'

        def __init__(self, path_entry=None):
            self.logger = logging.getLogger(__name__)
            self.logger.debug('Checking ROSImportFinder support for %s' % path_entry)
            if path_entry is None:  # called on very old python (< 2.7.12)
                pass
            elif path_entry != self.PATH_TRIGGER:  # python following correct PEP ( 302 ?)
                self.logger.debug('ROSImportFinder does not work for %s' % path_entry)
                raise ImportError()

            self.loaders = {
                '.srv': ROSLoader(genpy.generator.SrvGenerator(), 'srv'),
                '.msg': ROSLoader(genpy.generator.MsgGenerator(), 'msg')
            }

        def find_module(self, name, path=None):
            self.logger.debug('ROSImportFinder looking for "%s"' % name)

            # implementation inspired from pytest.rewrite
            names = name.rsplit(".", 1)
            lastname = names[-1]
            pth = None
            if path is not None:
                # Starting with Python 3.3, path is a _NamespacePath(), which
                # causes problems if not converted to list.
                path = list(path)
                if len(path) == 1:
                    pth = path[0]


            if pth is None:


                try:
                    fd, fn, desc = imp.find_module(lastname, path)
                except ImportError:
                    return None
                if fd is not None:
                    fd.close()




                tp = desc[2]
                if tp == imp.PY_COMPILED:
                    if hasattr(imp, "source_from_cache"):
                        try:
                            fn = imp.source_from_cache(fn)
                        except ValueError:
                            # Python 3 doesn't like orphaned but still-importable
                            # .pyc files.
                            fn = fn[:-1]
                    else:
                        fn = fn[:-1]
                elif tp != imp.PY_SOURCE:
                    # Don't know what this is.
                    return None
            else:
                fn = os.path.join(pth, name.rpartition(".")[2] + ".py")

            # fn_pypath = py.path.local(fn)
            # if not self._should_rewrite(name, fn_pypath, state):
            #     return None
            #
            # self._rewritten_names.add(name)

    # def find_module(self, name, path=None):
    #     """
    #     Return the loader for the specified module.
    #     """
    #     # Ref : https://www.python.org/dev/peps/pep-0302/#specification-part-1-the-importer-protocol
    #
    #     #
    #     loader = None
    #
    #     # path = path or sys.path
    #     # for p in path:
    #     #     for f in os.listdir(p):
    #     #         filename, ext = os.path.splitext(f)
    #     #         # our modules generated from messages are always a leaf in import tree so we only care about this case
    #     #         if ext in self.loaders.keys() and filename == name.split('.')[-1]:
    #     #             loader = self.loaders.get(ext)
    #     #             break  # we found it. break out.
    #     #
    #     # return loader
    #
    #     # implementation inspired from pytest.rewrite
    #     self.logger.debug("find_module called for: %s" % name)
    #     names = name.rsplit(".", 1)
    #     lastname = names[-1]
    #     pth = None
    #     if path is not None:
    #         # Starting with Python 3.3, path is a _NamespacePath(), which
    #         # causes problems if not converted to list.
    #         path = list(path)
    #         if len(path) == 1:
    #             pth = path[0]
    #
    #
    #     if pth is None:
    #
    #
    #
    #
    #
    #         try:
    #             fd, fn, desc = imp.find_module(lastname, path)
    #         except ImportError:
    #             return None
    #         if fd is not None:
    #             fd.close()
    #
    #
    #
    #
    #         tp = desc[2]
    #         if tp == imp.PY_COMPILED:
    #             if hasattr(imp, "source_from_cache"):
    #                 try:
    #                     fn = imp.source_from_cache(fn)
    #                 except ValueError:
    #                     # Python 3 doesn't like orphaned but still-importable
    #                     # .pyc files.
    #                     fn = fn[:-1]
    #             else:
    #                 fn = fn[:-1]
    #         elif tp != imp.PY_SOURCE:
    #             # Don't know what this is.
    #             return None
    #     else:
    #         fn = os.path.join(pth, name.rpartition(".")[2] + ".py")
    #
    #     fn_pypath = py.path.local(fn)
    #     if not self._should_rewrite(name, fn_pypath, state):
    #         return None
    #
    #     self._rewritten_names.add(name)
    #
    #     # The requested module looks like a test file, so rewrite it. This is
    #     # the most magical part of the process: load the source, rewrite the
    #     # asserts, and load the rewritten source. We also cache the rewritten
    #     # module code in a special pyc. We must be aware of the possibility of
    #     # concurrent pytest processes rewriting and loading pycs. To avoid
    #     # tricky race conditions, we maintain the following invariant: The
    #     # cached pyc is always a complete, valid pyc. Operations on it must be
    #     # atomic. POSIX's atomic rename comes in handy.
    #     write = not sys.dont_write_bytecode
    #     cache_dir = os.path.join(fn_pypath.dirname, "__pycache__")
    #     if write:
    #         try:
    #             os.mkdir(cache_dir)
    #         except OSError:
    #             e = sys.exc_info()[1].errno
    #             if e == errno.EEXIST:
    #                 # Either the __pycache__ directory already exists (the
    #                 # common case) or it's blocked by a non-dir node. In the
    #                 # latter case, we'll ignore it in _write_pyc.
    #                 pass
    #             elif e in [errno.ENOENT, errno.ENOTDIR]:
    #                 # One of the path components was not a directory, likely
    #                 # because we're in a zip file.
    #                 write = False
    #             elif e in [errno.EACCES, errno.EROFS, errno.EPERM]:
    #                 state.trace("read only directory: %r" % fn_pypath.dirname)
    #                 write = False
    #             else:
    #                 raise
    #     cache_name = fn_pypath.basename[:-3] + PYC_TAIL
    #     pyc = os.path.join(cache_dir, cache_name)
    #     # Notice that even if we're in a read-only directory, I'm going
    #     # to check for a cached pyc. This may not be optimal...
    #     co = _read_pyc(fn_pypath, pyc, state.trace)
    #     if co is None:
    #         state.trace("rewriting %r" % (fn,))
    #         source_stat, co = _rewrite_test(self.config, fn_pypath)
    #         if co is None:
    #             # Probably a SyntaxError in the test.
    #             return None
    #         if write:
    #             _make_rewritten_pyc(state, source_stat, pyc, co)
    #     else:
    #         state.trace("found cached rewritten pyc for %r" % (fn,))
    #     self.modules[name] = co, pyc
    #     return self

_ros_finder_instance_obsolete_python = ROSImportFinder


def activate():
    if sys.version_info >= (2, 7, 12):  # TODO : which exact version matters ?
        sys.path_hooks.append(ROSImportFinder)
    else:  # older (trusty) version
        sys.path_hooks.append(_ros_finder_instance_obsolete_python)

    for hook in sys.path_hooks:
        print('Path hook: {}'.format(hook))

    sys.path.insert(0, ROSImportFinder.PATH_TRIGGER)


def deactivate():
    if sys.version_info >= (2, 7, 12):  # TODO : which exact version matters ?
        sys.path_hooks.remove(ROSImportFinder)
    else:  # older (trusty) version
        sys.path_hooks.remove(_ros_finder_instance_obsolete_python)

    sys.path.remove(ROSImportFinder.PATH_TRIGGER)
