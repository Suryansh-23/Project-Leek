import os, pickle, shutil


class Vault:
    def __init__(self, Pswrd: str, path: str, file_paths: list, tui: bool) -> None:
        self.vault_name = "Vault"
        self.Pswrd = Pswrd
        self.path = path or os.getcwd()
        self.file_paths = file_paths
        self.tui = tui
        self.tree = self.tree_parser(self.path)
        self.Vault = self.create_vault()

    def tree_parser(self, path: str) -> dict:
        Tree = {}
        iter = -1
        for i in self.file_paths:
            iter += 1
            if os.path.splitext(i)[-1] != "":  # Filters Out File
                Tree[iter] = i
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
        self.fill_vault(self.tree, self.path)
        with open(self.path + "\\Vault.pickle", "wb") as fobj:
            pickle.dump(self.Vault, fobj)
        if self.tui:  # Check for tui flag
            shutil.copyfile(".\Vault.exe", self.path + "\\Vault\\Vault.exe")
        return None


if __name__ == "__main__":  # Driver Code
    main = Vault(
        Pswrd="1234", path="F:\\Project Leɘk\\python\\Test", file_paths=[], tui=False
    )
    main.main()
