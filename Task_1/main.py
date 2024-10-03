import tarfile
import argparse
import os

class Shell:
    path = "/"
    root_path = ""

    user_name = ""
    vfs_path = ""
    start_script =  ""

    def __init__(self, user_name, vfs_path, script_path):
        self.user_name = user_name
        self.vfs_path = vfs_path
        self.script_path = script_path

        self.path = self.vfs_path.replace(".tar", "") + "/"
        self.root_path = self.path

    def execute(self, command):
        parts_command = command.split()

    def run_start_script(self, script_path):
        if os.path.exists(script_path):
            with open(script_path, 'r') as script:
                for line in script:
                    line.strip()
                    exit_status = self.execute(line)
                    if exit_status:
                        break


def run_program(username, vfs_path, script_path):
    if not os.path.exists(vfs_path):
        print(f"Error: The archive '{ vfs_path}'was not found.")
        return
    if not os.path.exists(script_path):
        print(f"Error: The script '{script_path}' was not found.")
        return

    shell = Shell(username, vfs_path, script_path)
    shell.run_start_script(script_path)
    #shell.run_console()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shell emulator')
    parser.add_argument('username', type=str, help='The username to show in the input prompt')
    parser.add_argument('vfs_path', type=str, help='The path to the archive of the virtual file system.')
    parser.add_argument('script_path', type=str, help='The path to the start script.')

    args = parser.parse_args()
    run_program(args.username, args.vfs_path, args.script_path)
