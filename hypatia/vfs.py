import os
import io
import pkgutil
import threading

class VFSException(Exception):
    pass

class MountPointInUse(VFSException):
    def __init__(self, path):
        self.path = path

class IsADirectory(VFSException):
    def __init__(self, path):
        self.path = path

class FileNotFound(VFSException):
    def __init__(self, path):
        self.path = path

class VFS(object):
    PATH_SEPARATOR = "/"

    def __init__(self):
        self._lock = threading.RLock() 
        self._mountpoints = {}

    def mount(self, mountpoint, provider):
        if mountpoint in self._mountpoints:
            raise MountPointInUse(mountpoint)

        self._mountpoints[mountpoint] = provider
        self._mountpoints[mountpoint]._cache_files()

    def unmount(self, mountpoint):
        if not mountpoint in self._mountpoints:
            return

        del self._mountpoints[mountpoint]

    def isdir(self, path):
        spath = path.split(VFS.PATH_SEPARATOR)
        spath.remove('')

        # work forwards and try and find a mountpoint matching the file's path
        looked = []
        for i in spath:
            lookpath = VFS.PATH_SEPARATOR + VFS.PATH_SEPARATOR.join(looked)

            if lookpath in self._mountpoints:
                p = VFS.PATH_SEPARATOR.join(spath[len(looked):])
                return self._mountpoints[lookpath].isdir(p)

            looked.append(i)

        return False

    def exists(self, path):
        spath = path.split(VFS.PATH_SEPARATOR)
        spath.remove('')

        # work forwards and try and find a mountpoint matching the file's path
        looked = []
        for i in spath:
            lookpath = VFS.PATH_SEPARATOR + VFS.PATH_SEPARATOR.join(looked)

            if lookpath in self._mountpoints:
                p = VFS.PATH_SEPARATOR.join(spath[len(looked):])
                return self._mountpoints[lookpath].exists(p)

            looked.append(i)

        return False

    def open(self, path):
        spath = path.split(VFS.PATH_SEPARATOR)
        spath.remove('')

        # work forwards and try and find a mountpoint matching the file's path
        looked = []
        for i in spath:
            lookpath = VFS.PATH_SEPARATOR + VFS.PATH_SEPARATOR.join(looked)

            if lookpath in self._mountpoints:
                p = VFS.PATH_SEPARATOR.join(spath[len(looked):])
                return self._mountpoints[lookpath].open(p)

            looked.append(i)

        raise FileNotFound(path)

# _contents = {
#     "dirname": {
#         "isdir": True,
#         "children": {
#             "test": {
#                 "isdir": False,
#                 "contents": BytesIO(b"test"),
#             }
#         },
#     },
# }

class VFSProvider(object):
    def __init__(self):
        self._contents = {}

    def isdir(self, path):
        if path.startswith("/"):
            path = path.strip("/")

        spath = path.split(VFS.PATH_SEPARATOR)
        dir = self._contents
        if spath[0] in dir:
            dir = dir[spath[0]]
        else:
            raise FileNotFound(path)

        for fragment in spath[1:]:
            if fragment not in dir["children"]:
                raise FileNotFound(path)

            dir = dir["children"][fragment]

        return dir["isdir"]

    def exists(self, path):
        if path.startswith("/"):
            path = path.strip("/")

        spath = path.split(VFS.PATH_SEPARATOR)
        dir = self._contents
        if spath[0] in dir:
            dir = dir[spath[0]]
        else:
            return False

        for fragment in spath[1:]:
            if fragment not in dir["children"]:
                return False

            dir = dir["children"][fragment]

        return True

    def open(self, path):
        if path.startswith("/"):
            path = path.strip("/")

        spath = path.split(VFS.PATH_SEPARATOR)
        dir = self._contents
        if spath[0] in dir:
            dir = dir[spath[0]]
        else:
            raise FileNotFound(path)

        for fragment in spath[1:]:
            if fragment not in dir["children"]:
                raise FileNotFound(path)

            dir = dir["children"][fragment]

        if dir["isdir"]:
            raise IsADirectory(path)

        return dir["contents"]

    def _cache_files(self):
        pass

class FilesystemProvider(VFSProvider):
    def __init__(self, path):
        super(FilesystemProvider, self).__init__()
        self._path = os.path.abspath(path)

    def _cache_files(self):
        for root, dirs, files in os.walk(self._path):
            sroot = root[len(self._path):].split(os.sep)[1:]

            if len(sroot) is 0:
                for file in files:
                    with open(os.path.join(self._path, file), 'r') as fh:
                        contents = fh.read()

                    self._contents[file] = {
                        "isdir": False,
                        "contents": io.BytesIO(contents),
                    }

                continue
    
            if not sroot[0] in self._contents:
                self._contents[sroot[0]] = {
                    "isdir": True,
                    "children": {},
                }

            nest = self._contents[sroot[0]]
            for fragment in sroot[1:]:
                if not fragment in nest["children"]:
                    nest["children"][fragment] = {
                        "isdir": True,
                        "children": {},
                    }

                nest = nest["children"][fragment]

            for file in files:
                path = os.path.join(self._path, *sroot)
                path = os.path.join(path, file)
                with open(path, 'r') as fh:
                    contents = fh.read()

                nest["children"][file] = {
                    "isdir": False,
                    "contents": io.BytesIO(contents),
                }

