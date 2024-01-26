import os
import subprocess
import get_config

def change_wazuh_permission(dir_path, sudoPassword):
    paths = dir_path.split('/')
    path = '/'.join(paths[:3])
    try:
        if oct(os.stat(path).st_mode)[-3:] == '777':
            print(path, 'is already 777')
            return
        else:
            cmd = f"sudo chmod 777 -R {path}"
            subprocess.run(['sudo', '-S', *cmd.split()], input=sudoPassword.encode(), check=True)
            return
    except:
        print(path, 'Permission denied')
        return

if __name__ == '__main__':
    change_wazuh_permission('/var/ossec/logs/alerts', 'ncku')
    config = get_config.get_variable()
    print("get_config:", config["sudoPassword"])