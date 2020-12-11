import lib.systems.lockdown.utils.commands as utils
import os


RESTRICTED_EXT = ['mp3', 'wav', 'wma', 'aac', 'mp4', 'mov', 'avi']


''' os lockdown base class '''
class OSLockdown:

    def __init__(self, sys_root: str, osname: str):
        self.sys_root = sys_root
        self.osname = osname

    def remove_restricted_files(self):
        restricted_files = []
        for ext in RESTRICTED_EXT:
            directories, files = utils.search_from(root_dir=self.sys_root, ext=ext)
            restricted_files = restricted_files + files
        for file in files:
            os.remove(file)

    def disable_guest(self):
        raise NotImplementedError()

    def set_password(self, user, password):
        raise NotImplementedError()

    def set_password_policy(self):
        raise NotImplementedError()

    def add_user(self, user, password):
        raise NotImplementedError()

    def remove_user(self, user):
        raise NotImplementedError()

    def add_user_to_group(self, user, group):
        raise NotImplementedError()

    def remove_user_from_group(self, user, group):
        raise NotImplementedError()

    def set_admin(self, user):
        raise NotImplementedError()

    def remove_admin(self, user):
        raise NotImplementedError()
