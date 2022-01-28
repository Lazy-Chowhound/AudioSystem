import os
import pkgutil


class PackageUtil:

    @staticmethod
    def getPackageInfo():
        """
        获取项目所有包路径和包名
        :return: ['D:\\AudioSystem\\audio_python\\Audio',...]
        """
        package_info = []
        for importer, modname, isPackage in pkgutil.walk_packages(path=[os.getcwd()]):
            if isPackage:
                package_info.append([os.path.join(os.getcwd(), modname), modname])
        return package_info

    @staticmethod
    def getPackageModule():
        """
        获取所有项目所有包下的模块名
        :return: ['Audio.AudioProperty','Audio.AudioSetProperty',...]
        """
        module = []
        package_list = PackageUtil.getPackageInfo()
        for pkg in package_list:
            for file_path, file_name, isPackage in pkgutil.iter_modules(path=[pkg[0]]):
                module.append(pkg[1] + "." + file_name)
        return module
