import os, pickle, shutil

Pin = os.urandom(10).hex()


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
        os.mkdir(self.path + "\\Vault")
        self.fill_vault(self.tree, self.path)
        with open(self.path + "\\Vault\\Vault.pickle", "wb") as fobj:
            pickle.dump(self.Vault, fobj)
        shutil.copyfile(".\Vault.exe", self.path + "\\Vault\\Vault.exe")
        return None


if __name__ == "__main__":
    main = Vault(Pswrd="1234", path="F:\\Python\\Projects\\Crypto-Win\\Test")
    main.main()
