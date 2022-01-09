import os, pickle, shutil


class Vault:
    def __init__(self, Pswrd: str, path: str, tui: bool) -> None:
        self.vault_name = "Vault"
        self.Pswrd = Pswrd
        self.path = path or os.getcwd()
        self.tui = tui
        if os.path.isdir("Vault"):
            shutil.rmtree("Vault")
        if os.path.isdir(self.path + "\\Vault"):
            shutil.rmtree(self.path + "\\Vault")
        self.tree = self.tree_parser(self.path)
        self.Vault = self.create_vault()

    def tree_parser(self, path: str) -> dict:
        Tree = {}
        iter = -1
        for i in os.listdir(path):
            iter += 1
            if os.path.splitext(i)[-1] != "":  # Filters Out File
                Tree[iter] = path + "\\" + i
            else:  # Gets only the directories
                Tree[i] = self.tree_parser(path + "\\" + i)
        return Tree

    def create_vault(self) -> dict:
        shelf = {}
        return shelf

    def fill_vault(self, tree: dict, path: str) -> None:
        for i in tree:
            if type(i) == type(1):
                with open(tree[i], "rb") as fobj:
                    self.Vault[tree[i]] = fobj.read()
            else:
                self.fill_vault(tree[i], path + "\\" + i)
        return None

    def main(self) -> None:
        self.Vault["__Tree__"] = self.tree
        self.Vault["__Pswrd__"] = self.Pswrd
        os.mkdir(self.path + "\\Vault")
        self.fill_vault(self.tree, self.path)
        with open(self.path + "\\Vault\\Vault.pickle", "wb") as fobj:
            pickle.dump(self.Vault, fobj)
        if self.tui:  # Check for tui flag
            shutil.copyfile(".\Vault.exe", self.path + "\\Vault\\Vault.exe")
        return None


if __name__ == "__main__":  # Driver Code
    main = Vault(Pswrd="1234", path="F:\\Project Leɘk\\python\\Test", tui=False)
    main.main()
