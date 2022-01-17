from PIL import Image
import os


class stegano_encrypt:
    def __init__(self, data, img, fp):
        ## fp is the file path where file is to be saved
        ## img is the image address
        ## data is the plaintext string
        ## .jpg images can cause problems with PIL, .png is preferred
        self.data = data
        self.img = img
        self.fp = fp

    def conv_png(self):
        im = Image.open(self.img)
        im.save(r".//temp.png")

    def bindata(self):
        out = []
        for i in self.data:
            out.append(bin(ord(i)).lstrip("0b"))
            if len(out[-1]) < 7:
                for j in range(7 - len(out[-1])):
                    out[-1] = "0" + out[-1]
        return out

    def encrypt(self):
        self.conv_png()
        img = Image.open(r".//temp.png")
        bindat = self.bindata()
        pix = [i for i in img.convert("RGB").getdata()]
        for i in range(len(bindat)):
            k = ((i) * 8) % 3
            o = ((i + 1) * 8) % 3
            m = (i * 8) // 3
            n = ((i + 1) * 8) // 3
            l = list(pix[m])
            L = list(pix[n])
            if l[k] % 2 == 1:
                l[k] = l[k] - 1
                pix[m] = tuple(l)
            if i == len(bindat) - 1:
                if L[o] % 2 == 0 and L[o] != 0:
                    L[o] = L[o] - 1
                    pix[n] = tuple(L)
                else:
                    L[o] = L[o] + 1
                    pix[n] = tuple(L)
            a = (k + 1) % 3
            for j in range(a, a + 7):
                if j % 3 == 0:
                    out = []
                elif j == a:
                    if k == 0:
                        out = [pix[(i * 8) // 3][0]]
                    elif k == 1:
                        out = list(pix[(i * 8) // 3][:2])
                ppoint = pix[(i * 8 + j + 1 - a) // 3][(i * 8 + j + 1 - a) % 3]
                if bindat[i][j - a] == "0":
                    if ppoint % 2 == 1:
                        out.append(ppoint - 1)
                    else:
                        out.append(ppoint)
                else:
                    if ppoint % 2 == 0 and ppoint != 0:
                        out.append(ppoint - 1)
                    elif ppoint == 0:
                        out.append(ppoint + 1)
                    else:
                        out.append(ppoint)
                if len(out) == 3:
                    pix[(i * 8 + j + 1 - a) // 3] = tuple(out)
                elif j == a + 6:
                    if len(out) == 1:
                        pix[(i * 8 + j + 1 - a) // 3] = tuple(
                            out + list(pix[(i * 8 + j + 1 - a) // 3][1:])
                        )
                    else:
                        pix[(i * 8 + j + 1 - a) // 3] = tuple(
                            out + [pix[(i * 8 + j + 1 - a) // 3][2]]
                        )
        img.putdata(pix)
        os.remove(r".//temp.png")
        img.save(self.fp)
        img.close()


class stegano_decrypt(stegano_encrypt):
    def __init__(self, img):
        self.img = img

    def decrypt(self):
        self.conv_png()
        img = Image.open(r".//temp.png")
        pix = [i for i in img.convert("RGB").getdata()]
        out = []
        for i in range(len(pix)):
            for j in range(0, 3):
                if (i * 3 + j) % 8 == 0:
                    if i != 0:
                        out.append(chr(int(outstr, 2)))
                    outstr = "0b"
                    if pix[i][j] % 2 == 1:
                        break
                else:
                    curp = pix[i][j]
                    if curp % 2 == 0:
                        outstr = outstr + "0"
                    else:
                        outstr = outstr + "1"
            else:
                continue
            break
        os.remove(r".//temp.png")
        return "".join(out)
