import unittest
import Task_1.main

class TestsAllFunctions(unittest.TestCase):

    def setUp(self):
        self.shell = Task_1.main.Shell("test_user", "files_archive.tar", "")

#----------------------test _ls function--------------------------------
    def test_ls_root(self):
        output = self.shell._ls()
        self.assertTrue(output =="documents\nusers" or output =="users\ndocuments")

    def test_ls_file(self):
        self.shell.path = "files_archive/users/"
        output = self.shell._ls()
        self.assertEqual(output, "alena.txt")

    def test_ls_non_existing_path(self):
        output = self.shell._ls("dir3")
        self.assertEqual(output, "")

    def test_ls_path(self):
        output = self.shell._ls("documents/school/")
        self.assertTrue(output == "ege.doc\nclass11.txt" or output == "class11.txt\nege.doc")

    # ----------------------test _cd function--------------------------------

    def test_cd_to_existing_directory(self):
        self.shell._cd("documents")
        self.assertEqual(self.shell.path, "files_archive/documents/")

    def test_cd_to_non_existing_directory(self):
        response = self.shell._cd("non_existing_dir")
        self.assertEqual(response, "No such directory")

    def test_cd_to_parent_directory(self):
        self.shell._cd("documents")
        self.shell._cd("../")
        self.assertEqual(self.shell.path, "files_archive/")

    def test_cd_to_directory_in_parent_directory(self):
        self.shell._cd("documents")
        self.shell._cd("../users")
        self.assertEqual(self.shell.path, "files_archive/users/")

    # --------------------------test _tail function

    def test_tail_with_relative_path(self):
        self.shell._cd("documents/school")
        res = self.shell._tail("class11.txt")
        self.assertEqual(res, "1.This is a placeholder for class11.txt.\r\n"
                              "2.This is a placeholder for class11.txt.\r\n"
                              "3.This is a placeholder for class11.txt.\r\n"
                              "4.This is a placeholder for class11.txt.\r\n"
                              "5.This is a placeholder for class11.txt.\r\n"
                              "6.This is a placeholder for class11.txt.\r\n"
                              "7.This is a placeholder for class11.txt.\r\n"
                              "8.This is a placeholder for class11.txt.\r\n"
                              "9.This is a placeholder for class11.txt.\r\n"
                              "10.This is a placeholder for class11.txt.\r\n")


    def test_tail_not_such_file(self):
        self.shell._cd("documents")
        res = self.shell._tail("school/world.txt")
        self.assertEqual(res, "No such file")

    # --------------test _du function------------------

    def test_du_not_such_file(self):
        self.shell._cd("documents")
        res = self.shell._du("school/world.txt")
        self.assertEqual(res, "No such path")

    def test_du_not_such_dir(self):
        self.shell._cd("documents")
        res = self.shell._du("world")
        self.assertEqual(res, "No such path")

    def test_du_(self):
        self.shell._cd("documents")
        res = self.shell._du("school")
        self.assertTrue(res =="419\t/school/ege.doc\n463\t/school/class11.txt\nTotal size: 882 bytes" or res == "463\t/school/class11.txt\n419\t/school/ege.doc\nTotal size: 882 bytes")

    # --------------test _chown function------------------

    def test_chown_not_such_file(self):
        self.shell._cd("documents")
        res = self.shell._chown("alena","school/world.txt")
        self.assertEqual(res, "No such path")

    def test_chown_not_such_dir(self):
        self.shell._cd("documents")
        res = self.shell._chown("alena", "school/world.txt")
        self.assertEqual(res, "No such path")

    def test_chown(self):
        self.shell._cd("documents")
        self.shell._chown("alena", "school")
        for name in self.shell.list_uname:
            if name[0] == "files_archive/documents/school":
                self.assertEqual(name[1], "alena")

    def test_chown_R(self):
        self.shell._cd("documents")
        self.shell._chown("alena", "school", "-R")
        for name in self.shell.list_uname:
            if name[0].startswith( "files_archive/documents/school"):
                self.assertEqual(name[1], "alena")



if __name__ == "__main__":
    unittest.main()
