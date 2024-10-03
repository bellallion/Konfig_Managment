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


    # --------------commands-----------------------

    def _ls(self, append_path=""):
        path = self.get_path(append_path)

        result = set()
        with tarfile.open(self.vfs_path, "r") as tar:
            for member in tar.getmembers():
                if not member.name.startswith(path):
                    continue
                result.add(member.name.split("/")[path.count("/")])

        return "\n".join(result)

    def _cd(self, path):
        self.path = self.path.replace("//", "/")
        if type(path) != list:
            path = path.split("/")
        if path[0] == "" and len(path) > 1:
            self.path = "/".join(self.path.split("/")[:2]) + "/"
            return self._cd(path[1:])
        if path[0] == "":
            return

        if path[0] == "..":
            if self.path == "./" + self.root_path:
                return self._cd(path[1:])
            self.path = "/".join(self.path.split("/")[:-2]) + "/"
            return self._cd(path[1:])
        elif path[0] == ".":
            return self._cd(path[1:])
        else:
            with tarfile.open(self.vfs_path, "r") as tar:
                for member in tar.getmembers():
                    if member.name == self.path + "/".join(path) and \
                            member.isdir():
                        break
                else:
                    return "No such directory"

            self.path += "/".join(path) + "/"
            self.path = self.path.replace("//", "/")

    def _tail(self, path):
        path = self.get_path(path)[:-1]
        with tarfile.open(self.vfs_path, "r") as tar:
            for member in tar.getmembers():
                if member.name == path and member.isfile():
                    break
            else:
                return "No such file"

            with tar.extractfile(member) as f:
                lines = f.readlines()
                lines = [line.decode("utf-8") for line in lines]
                return "".join(lines[-min(len(lines), 10):])

    def _du(self, path=""):
        path = self.get_path(path)[:-1]
        with tarfile.open(self.vfs_path, "r") as tar:
            for member in tar.getmembers():
                if member.name == path and member.isdir():
                    break
            else:
                return "No such directory"
            result = set()
            total_size = 0
            for member in tar.getmembers():
                if member.name.startswith(path):
                    if not member.isfile():
                        continue
                    name = "/" + "/".join(member.name.split("/")[2:])

                    size_file = member.size
                    total_size += size_file
                    result.add(f'{size_file}\t{name}')

            return "\n".join(result) + "\n" + f"Total size: {total_size} bytes"

    def _chown(self, user, path, operation=""):

        path = self.get_path(path)[:-1]
        with tarfile.open(self.vfs_path, "r") as tar:
            for member in tar.getmembers():
                if operation == "-R":
                    if member.name.startswith(path):
                        member.uname = user
                else:
                    if member.name == path:
                        member.uname = user
            else:
                return "No such path"

    #---------------------------------------------

    def get_path(self, path):
        path = path.split("/")
        result_path = self.path

        for p in path:
            if p == "..":
                result_path = "/".join(result_path.split("/")[:-2]) + "/"
            elif p == ".":
                continue
            else:
                result_path += p + "/"
            result_path = result_path.replace("//", "/")
        return result_path

    def execute(self, command):
        parts_command = command.split()
        if not args:
            return

        cmd = parts_command[0]
        if cmd == 'exit':
            print("...")
            return True
        elif cmd == 'ls':
            print(self._ls())
        elif cmd == 'cd':
            if len(parts_command) == 2:
                ans = self._cd(parts_command[1])
                if ans is not None:
                    print(ans)
            else:
                print(f"{cmd}:incorrect command")
        elif cmd == 'tail':
            if len(parts_command) == 2:
                print(self._tail(parts_command[1]))
            else:
                print(f"{cmd}:incorrect command")

        elif cmd == 'du':
            if len(parts_command) == 2:
                print(self._du(parts_command[1]))
            else:
                print(f"{cmd}:incorrect command")
        elif cmd == 'chown':
            if len(parts_command) == 3:
                ans = self._chown(parts_command[1], parts_command[2])
                if ans is not None:
                    print(ans)
            elif len(parts_command) == 4:
                ans = self._chown(parts_command[1], parts_command[2], parts_command[3])
                if ans is not None:
                    print(ans)
            else:
                print(f"{cmd}:incorrect command")
        else:
            print(f"{cmd}: not found")

    def run_start_script(self, script_path):
        if os.path.exists(script_path):
            with open(script_path, 'r') as script:
                for line in script:
                    line.strip()
                    exit_status = self.execute(line)
                    if exit_status:
                        break

    def run_console(self):
        while True:
            command = input(f"{self.path}$ ")
            exit_status = self.execute(command)
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
    shell.run_console()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shell emulator')
    parser.add_argument('username', type=str, help='The username to show in the input prompt')
    parser.add_argument('vfs_path', type=str, help='The path to the archive of the virtual file system.')
    parser.add_argument('script_path', type=str, help='The path to the start script.')

    args = parser.parse_args()
    run_program(args.username, args.vfs_path, args.script_path)

