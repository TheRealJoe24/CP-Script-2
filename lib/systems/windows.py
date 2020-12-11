import  sys, os
import lib.systems.lockdown.utils.commands as utils
import lib.systems.lockdown.oslockdown as lockdown


class WindowsLockdown (lockdown.OSLockdown):

    def __init__(self):
        super(WindowsLockdown, self).__init__('/', 'Windows')

        self.windows_request_admin()

    def windows_request_admin(self):
        ''' modified from https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script '''
        try:
            import win32com.shell.shell as shell
            ASADMIN = 'asadmin'
        except ImportError:
            print('Unable to request windows admin (System is not Windows)')
            return

        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(
                lpVerb='runas', lpFile=sys.executable, lpParameters=params)

    def set_auto_login(self):
        ''' Enable or disable autologin. '''
        output = utils.run_command('netplwiz')
        print(output)

    def disable_guest(self):
        output = utils.run_command('net user guest /active:no')
        print(output)

    def set_password_policy(self):
        raise NotImplementedError()

    def add_user(self, user, password):
        ''' Add user "user" '''
        output = utils.run_command(
            'net user /add {user} {password}'.format(user=user, password=password))
        print(output)

    def remove_user(self, user):
        ''' Remove user "user" '''
        output = utils.run_command(
            'net user /delete {user}'.format(user=user))
        print(output)

    def add_user_to_group(self, user, group):
        ''' Move user to given group '''
        output = utils.run_command(
            'net localgroup {group} {user} /add'.format(group=group, user=user))
        print(output)

    def remove_user_from_group(self, user, group):
        ''' Remove user from given group '''
        output = utils.run_command(
            'net localgroup {group} {user} /delete'.format(group=group, user=user))
        print(output)

    def set_admin(self, user: str):
        ''' Add user to the admin group '''
        self.add_user_to_group(user=user, group='Administrator')

    def remove_admin(self, user: str):
        ''' Remove user from the admin group '''
        self.remove_user_from_group(user=user, group='Administrator')

    def set_password(self, user, password):
        ''' set user password '''
        output = utils.run_command(
            'net user {user} {password}'.format(user=user, password=password))
        print(output)
