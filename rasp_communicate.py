from paramiko import SSHClient, AutoAddPolicy

class RaspberryCommunication():

    def Connect(self, ip, username='pi', pw='password'):
        print('connecting to {}@{}...'.format(username, ip))
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ip, username=username, password=pw)
        print('connection status =', ssh.get_transport().is_active())
        return ssh

    def SendCommand(self, ssh, command, pw='password'):
        print('sending a command... ', command)
        stdin, stdout, stderr = ssh.exec_command(command)
        if "sudo" in command:
            stdin.write(pw+'\n')
        stdin.flush()
