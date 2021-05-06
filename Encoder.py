import os, pickle, shutil

Pin = os.urandom(10).hex()
Prog = f"""import os, pickle, shutil, getpass


class locker:
    def __init__(self, vault, tree, dir):
        self.Vault = vault
        self.tree = tree
        self.directory = dir + "\\\\Files\\\\"

    def make_file(self, tree, path=""):
        for i in tree:
            if str.isdigit(str(i)):
                if path == "":
                    file_path = self.directory + tree[i]
                else:
                    file_path = self.directory + "\\\\" + tree[i]
                with open(file_path, "wb") as fobj:
                    fobj.write(self.Vault[tree[i]])
            else:
                self.directory += i
                os.mkdir(self.directory)
                self.make_file(tree=tree[i], path=i)
                self.directory = self.directory.replace(i, "")

        return None

    def main(self):
        if not os.path.isdir("Files"):
            os.mkdir(self.directory)
        else:
            print("Vault is already unlocked.")
            return None
        self.make_file(self.tree)

os.chdir(".\\\\Vault\\\\")
with open("Vault.pickle", "rb") as fobj:
    dic = pickle.load(fobj)

pswrd = getpass.getpass(prompt="Enter the password to your locker : ")
if pswrd == dic["__Pswrd__"]:
    print("Choose from the following options : ")
    print("1. Unlock Files")
    print("2. Lock Files")
    opt = input("Enter Option : ").strip().lower()
    if opt == "1":
        chk = (
            input("Do you want to unlock the files in the Vault (y/n) : ")
            .strip()
            .lower()
        )
        app = locker(dic, dic["__Tree__"], os.getcwd())
        if app.main():
            print("Vault Unlocked.")
    elif opt == "2":
        chk = (
            input("Do you want to lock the files in the Vault (y/n) : ").strip().lower()
        )
        if chk == "y":
            if os.path.isdir(".\\Files"):
                shutil.rmtree(".\\Files")
                print("Vault Locked")
            else:
                print("Either Vault is already locked or is moved to some other address.")
else:
    print("Invalid Password Entered.")
"""


class Vault:
    def __init__(self, Pswrd, path) -> None:
        self.vault_name = "Vault"
        self.Pswrd = Pswrd
        self.path = path or os.getcwd()
        if os.path.isdir("Vault"):
            shutil.rmtree("Vault")
        if os.path.isdir(self.path + "\\Vault"):
            shutil.rmtree(self.path + "\\Vault")
        self.tree = self.tree_parser(self.path)
        self.Vault = self.create_vault()

    def tree_parser(self, path) -> dict:
        Tree = {}
        iter = -1
        for i in os.listdir(path):
            iter += 1
            if os.path.splitext(i)[-1] != "":
                Tree[iter] = i
            else:
                Tree[i] = self.tree_parser(path + "\\" + i)
        return Tree

    def create_vault(self) -> dict:
        shelf = {}
        return shelf

    def fill_vault(self, tree, path) -> None:
        for i in tree:
            if str.isdigit(str(i)):
                if path == "":
                    file_path = tree[i]
                else:
                    file_path = path + "\\" + tree[i]
                with open(file_path, "rb") as fobj:
                    self.Vault[tree[i]] = fobj.read()
            else:
                self.fill_vault(tree[i], i)
        return None

    def main(self) -> None:
        self.Vault["__Tree__"] = self.tree
        self.Vault["__Pswrd__"] = self.Pswrd
        # print("Deleting Previously Created Vault...")
        os.mkdir(self.path + "\\Vault")
        self.fill_vault(self.tree, self.path)
        with open(self.path + "\\Vault\\Vault.pickle", "wb") as fobj:
            pickle.dump(self.Vault, fobj)
        # with open(self.path + "\\Vault\\Vault.py", "wb") as fobj:
        #     fobj.write(Prog.encode("utf-8"))
        shutil.copyfile(".\Vault.exe", self.path + "\\Vault\\Vault.exe")
        return None


if __name__ == "__main__":
    main = Vault(Pswrd="1234", path="F:\\Python\\Projects\\Crypto-Win\\Test")
    main.main()