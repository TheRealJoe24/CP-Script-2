
import lib.systems.lockdown.utils.commands as utils
import lib.systems.lockdown.oslockdown as lockdown

LIGHTDM_NO_GUEST = '''
    [SeatDefaults]
    greeter-session=unity-greeter
    allow-guest=false
'''

class LinuxLockdown (lockdown.OSLockdown):

    def __init__(self):
        super(LinuxLockdown, self).__init__('/', 'Linux')

    def open_firewall_settings(self):
        ''' open firewall '''
        output = utils.run_command(
            'sudo apt-get update & sudo apt-get install gufw & sudo gufw'
        )
        print(output)


    def disable_guest(self):
        ''' Disable guest user. '''
        output = utils.run_command(
                'echo "{contents}"/etc/lightdm/lightdm.conf.d/50-no-guest.conf'.format(contents=LIGHTDM_NO_GUEST))
        print(output)

    def set_password_policy(self):
        raise NotImplementedError()

    def add_user(self, user, password):
        ''' Add user "user" '''
        output = utils.run_command(
            'sudo useradd {user} -m -s /bin/bash'.format(user=user))
        if password != '':
            output += '\n' + \
                utils.run_command('sudo passwd {user}'.format(user=user), password)
        print(output)

    def remove_user(self, user):
        ''' Remove user "user" '''
        output = utils.run_command('sudo userdel -r {user}'.format(user=user))
        print(output)

    def add_user_to_group(self, user, group):
        ''' Move user to given group '''
        output = utils.run_command(
            'sudo gpasswd -a {user} {group}'.format(user=user, group=group))
        print(output)

    def remove_user_from_group(self, user, group):
        ''' Remove user from given group '''
        output = utils.run_command(
            'sudo gpasswd -d {user} {group}'.format(user=user, group=group))
        print(output)

    def set_admin(self, user: str):
        ''' Add user to the admin group '''
        self.add_user_to_group(user=user, group='adm')

    def remove_admin(self, user: str):
        ''' Remove user from the admin group '''
        self.remove_user_from_group(user=user, group='adm')

    def set_password(self, user, password):
        ''' set user password '''
        output = utils.run_command('sudo passwd {user}'.format(user=user), password)
        print(output)
