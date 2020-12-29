
from inspect import getframeinfo
from configator.utils.string_util import remove_prefix
from configator.utils.system_util import get_app_root

class CodeLocation():
    #
    __app_root_dir = get_app_root()
    #
    #
    def _get_filename_and_lineno(self, cf, depth=1):
        filename = None
        lineno = None
        #
        if cf is None:
            return (filename, lineno)
        while depth > 0:
            depth -= 1
            cf = cf.f_back
            if cf is None:
                return (filename, lineno)
        #
        info = getframeinfo(cf)
        filename = self.__remove_app_root_dir(info.filename)
        lineno = info.lineno
        #
        return (filename, lineno)
    #
    #
    def __remove_app_root_dir(self, module_file):
        return remove_prefix(module_file, self.__app_root_dir)
    #
    pass
