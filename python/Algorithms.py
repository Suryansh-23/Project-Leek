from PIL import Image


class aes_encrypt:
    ##class for ecryption of data using aes##
    def __init__(self, cipherkey, plaintext, N):
        self.N = N
        self.cipherkey = cipherkey
        self.plaintext = plaintext
        ##plaintext MUST be entered in a STRING of HEXADECIMAL numbers with thw 0x prefix##
        ##Cipherkey MUST be a 128, 192, 256 bit key entered as a string of hexadecimal numbers with the 0x prefix##
        ##N is the encryption type. 128 bit is 0, 192 is 1 and 256 is 2##

    def state_array(self):
        ##Function to convert the plaintext to a 3D array of hexadecimal numbers##
        if len(self.plaintext) % 2 != 0:
            self.plaintext += "0"
        a = []
        for i in range(34, len(self.plaintext), 32):
            out = [[], [], [], []]
            block = self.plaintext[i - 32: i]
            for l in range(0, 16):
                out[l // 4].append("0x" + block[l * 2] + block[(l * 2) + 1])
            a.append(out)
            b = i
        if len(self.plaintext) < 35:
            b = 2
        out = [[], [], [], []]
        if len(self.plaintext[b:-1]) > 0:
            k = 0
            for l in range(b, len(self.plaintext) - 1, 2):
                out[k // 4].append(("0x" + self.plaintext[l] +
                                   self.plaintext[l + 1]))
                k += 1
            else:
                for i in range(0, len(out)):
                    while len(out[i]) < 4:
                        out[i].append("0x00")
            a.append(out)
        return a

    def str_shift_R_2(self, str1):
        return "0x" + str1[4: len(str1)] + str1[2:4]

    def key_conversion(self):
        ##key conversion into 11 round keys. Each round key consists of 32,48,64 bit words which are decided by the cipherkey##
        Rkey0 = self.cipherkey
        Rkeyt = [[]]
        for i in range(0, (10 + (self.N * 2))):
            Rkeyt.append([])
        for i in range(2, len(Rkey0), 8 + 4 * (self.N)):
            Rkey0Wi = int("0x" + Rkey0[i: i + 8 + ((self.N) * 4)], 16)
            Rkeyt[0].append(Rkey0Wi)
        Rconi = {
            1: 2,
            2: 4,
            3: 8,
            4: 16,
            5: 32,
            6: 64,
            7: 128,
            8: 27,
            9: 54,
            10: 108,
            11: 216,
            12: 171,
            13: 77,
            14: 154,
        }
        for i in range(1, (11 + (self.N * 2))):
            RkeyiW0 = (
                (Rkeyt[i - 1])[0]
                ^ (int(self.str_shift_R_2(hex((Rkeyt[i - 1])[2])), 16))
                ^ Rconi[i]
            )
            Rkeyt[i].append(RkeyiW0)
            for j in range(0, 3):
                RkeyiWj = (Rkeyt[i - 1])[j] ^ (Rkeyt[i])[j - 1]
                Rkeyt[i].append(RkeyiWj)
        for i in range(0, len(Rkeyt)):
            for j in range(0, 4):
                Rkeyt[i][j] = hex(Rkeyt[i][j])
                if len(Rkeyt[i][j])<10:
                    for k in range(10-len(Rkeyt[i][j])):
                        Rkeyt[i][j]=Rkeyt[i][j]+'0'
        return Rkeyt

    def SubBytes(self, statearray):
        ##First step of the encryption. The plaintext is substituted using an S-box##
        S_box = {'0': {'0': '63', '1': '7c', '2': '77', '3': '7b', '4': 'f2', '5': '6b', '6': '6f', '7': 'c5', '8': '30', '9': '01', 'a': '67', 'b': '2b', 'c': 'fe', 'd': 'd7', 'e': 'ab', 'f': '76'},
                 '1': {'0': 'ca', '1': '82', '2': 'c9', '3': '7d', '4': 'fa', '5': '59', '6': '47', '7': 'f0', '8': 'ad', '9': 'd4', 'a': 'a2', 'b': 'af', 'c': '9c', 'd': 'a4', 'e': '72', 'f': 'c0'},
                 '2': {'0': 'b7', '1': 'fd', '2': '93', '3': '26', '4': '36', '5': '3f', '6': 'f7', '7': 'cc', '8': '34', '9': 'a5', 'a': 'e5', 'b': 'f1', 'c': '71', 'd': 'd8', 'e': '31', 'f': '15'},
                 '3': {'0': '04', '1': 'c7', '2': '23', '3': 'c3', '4': '18', '5': '96', '6': '05', '7': '9a', '8': '07', '9': '12', 'a': '80', 'b': 'e2', 'c': 'eb', 'd': '27', 'e': 'b2', 'f': '75'},
                 '4': {'0': '09', '1': '83', '2': '2c', '3': '1a', '4': '1b', '5': '6e', '6': '5a', '7': 'a0', '8': '52', '9': '3b', 'a': 'd6', 'b': 'b3', 'c': '29', 'd': 'e3', 'e': '2f', 'f': '84'},
                 '5': {'0': '53', '1': 'd1', '2': '00', '3': 'ed', '4': '20', '5': 'fc', '6': 'b1', '7': '5b', '8': '6a', '9': 'cb', 'a': 'be', 'b': '39', 'c': '4a', 'd': '4c', 'e': '58', 'f': 'cf'},
                 '6': {'0': 'd0', '1': 'ef', '2': 'aa', '3': 'fb', '4': '43', '5': '4d', '6': '33', '7': '85', '8': '45', '9': 'f9', 'a': '02', 'b': '7f', 'c': '50', 'd': '3c', 'e': '9f', 'f': 'a8'},
                 '7': {'0': '51', '1': 'a3', '2': '40', '3': '8f', '4': '92', '5': '9d', '6': '38', '7': 'f5', '8': 'bc', '9': 'b6', 'a': 'da', 'b': '21', 'c': '10', 'd': 'ff', 'e': 'f3', 'f': 'd2'},
                 '8': {'0': 'cd', '1': '0c', '2': '13', '3': 'ec', '4': '5f', '5': '97', '6': '44', '7': '17', '8': 'c4', '9': 'a7', 'a': '7e', 'b': '3d', 'c': '64', 'd': '5d', 'e': '19', 'f': '73'},
                 '9': {'0': '60', '1': '81', '2': '4f', '3': 'dc', '4': '22', '5': '2a', '6': '90', '7': '88', '8': '46', '9': 'ee', 'a': 'b8', 'b': '14', 'c': 'de', 'd': '5e', 'e': '0b', 'f': 'db'},
                 'a': {'0': 'e0', '1': '32', '2': '3a', '3': '0a', '4': '49', '5': '06', '6': '24', '7': '5c', '8': 'c2', '9': 'd3', 'a': 'ac', 'b': '62', 'c': '91', 'd': '95', 'e': 'e4', 'f': '79'},
                 'b': {'0': 'e7', '1': 'c8', '2': '37', '3': '6d', '4': '8d', '5': 'd5', '6': '4e', '7': 'a9', '8': '6c', '9': '56', 'a': 'f4', 'b': 'ea', 'c': '65', 'd': '7a', 'e': 'ae', 'f': '08'},
                 'c': {'0': 'ba', '1': '78', '2': '25', '3': '2e', '4': '1c', '5': 'a6', '6': 'b4', '7': 'c6', '8': 'e8', '9': 'dd', 'a': '74', 'b': '1f', 'c': '4b', 'd': 'bd', 'e': '8b', 'f': '8a'},
                 'd': {'0': '70', '1': '3e', '2': 'b5', '3': '66', '4': '48', '5': '03', '6': 'f6', '7': '0e', '8': '61', '9': '35', 'a': '57', 'b': 'b9', 'c': '86', 'd': 'c1', 'e': '1d', 'f': '9e'},
                 'e': {'0': 'e1', '1': 'f8', '2': '98', '3': '11', '4': '69', '5': 'd9', '6': '8e', '7': '94', '8': '9b', '9': '1e', 'a': '87', 'b': 'e9', 'c': 'ce', 'd': '55', 'e': '28', 'f': 'df'},
                 'f': {'0': '8c', '1': 'a1', '2': '89', '3': '0d', '4': 'bf', '5': 'e6', '6': '42', '7': '68', '8': '41', '9': '99', 'a': '2d', 'b': '0f', 'c': 'b0', 'd': '54', 'e': 'bb', 'f': '16'}}       
        substext = [[], [], [], []]
        for i in range(0, len(statearray)):
            for j in statearray[i]:
                if j == "0x0":
                    j = "0x00"
                substext[i].append("0x" + (S_box[j[-2]])[j[-1]])
        return substext

    def Round_Shift_R(self, L, n):
        ##Round shifting a list to the right for shiftrows##
        out = []
        for i in range(n, 0, -1):
            out.append(L[-i])
        out.extend(L[0:-n])
        return out

    def Round_Shift_L(self, L, n):
        ##Round Shifting a list to the left for inverse shiftrows##
        out = L[n:]
        out.extend(L[0:n])
        return out

    def ShiftRows(self, statearray, Inverse=False):
        ##Function to round shift rows by a value depending on the row number##
        out = [[], [], [], []]
        for i in range(0, len(statearray)):
            temp = []
            for j in range(0, len(statearray[i])):
                temp.append(statearray[i][j])
            if Inverse == False:
                out[i] = self.Round_Shift_R(temp, i)
            else:
                out[i] = self.Round_Shift_L(temp, i)
        if not Inverse:
            out[0]=statearray[0]
        return out

    def multi(self, n1, n2):
        ##Defining the matrix multiplication##
        if n2 == '0x00' or n1 == '0x00':
            return 0
        elif n2 == '0x01':
            return int(n1, 16)
        elif n1 == '0x01':
            return int(n2, 16)
        else:
            lookup_dict = {'0x02': ['0x00', '0x02', '0x04', '0x06', '0x08', '0x0a', '0x0c', '0x0e', '0x10', '0x12', '0x14', '0x16', '0x18', '0x1a', '0x1c', '0x1e', '0x20', '0x22', '0x24', '0x26', '0x28', '0x2a', '0x2c', '0x2e', '0x30', '0x32', '0x34', '0x36', '0x38', '0x3a', '0x3c', '0x3e', '0x40', '0x42', '0x44', '0x46', '0x48', '0x4a', '0x4c', '0x4e', '0x50', '0x52', '0x54', '0x56', '0x58', '0x5a', '0x5c', '0x5e', '0x60', '0x62', '0x64', '0x66', '0x68', '0x6a', '0x6c', '0x6e', '0x70', '0x72', '0x74', '0x76', '0x78', '0x7a', '0x7c', '0x7e', '0x80', '0x82', '0x84', '0x86', '0x88', '0x8a', '0x8c', '0x8e', '0x90', '0x92', '0x94', '0x96', '0x98', '0x9a', '0x9c', '0x9e', '0xa0', '0xa2', '0xa4', '0xa6', '0xa8', '0xaa', '0xac', '0xae', '0xb0', '0xb2', '0xb4', '0xb6', '0xb8', '0xba', '0xbc', '0xbe', '0xc0', '0xc2', '0xc4', '0xc6', '0xc8', '0xca', '0xcc', '0xce', '0xd0', '0xd2', '0xd4', '0xd6', '0xd8', '0xda', '0xdc', '0xde', '0xe0', '0xe2', '0xe4', '0xe6', '0xe8', '0xea', '0xec', '0xee', '0xf0', '0xf2', '0xf4', '0xf6', '0xf8', '0xfa', '0xfc', '0xfe', '0x1b', '0x19', '0x1f', '0x1d', '0x13', '0x11', '0x17', '0x15', '0x0b', '0x09', '0x0f', '0x0d', '0x03', '0x01', '0x07', '0x05', '0x3b', '0x39', '0x3f', '0x3d', '0x33', '0x31', '0x37', '0x35', '0x2b', '0x29', '0x2f', '0x2d', '0x23', '0x21', '0x27', '0x25', '0x5b', '0x59', '0x5f', '0x5d', '0x53', '0x51', '0x57', '0x55', '0x4b', '0x49', '0x4f', '0x4d', '0x43', '0x41', '0x47', '0x45', '0x7b', '0x79', '0x7f', '0x7d', '0x73', '0x71', '0x77', '0x75', '0x6b', '0x69', '0x6f', '0x6d', '0x63', '0x61', '0x67', '0x65', '0x9b', '0x99', '0x9f', '0x9d', '0x93', '0x91', '0x97', '0x95', '0x8b', '0x89', '0x8f', '0x8d', '0x83', '0x81', '0x87', '0x85', '0xbb', '0xb9', '0xbf', '0xbd', '0xb3', '0xb1', '0xb7', '0xb5', '0xab', '0xa9', '0xaf', '0xad', '0xa3', '0xa1', '0xa7', '0xa5', '0xdb', '0xd9', '0xdf', '0xdd', '0xd3', '0xd1', '0xd7', '0xd5', '0xcb', '0xc9', '0xcf', '0xcd', '0xc3', '0xc1', '0xc7', '0xc5', '0xfb', '0xf9', '0xff', '0xfd', '0xf3', '0xf1', '0xf7', '0xf5', '0xeb', '0xe9', '0xef', '0xed', '0xe3', '0xe1', '0xe7', '0xe5'],
                           '0x03': ['0x00', '0x03', '0x06', '0x05', '0x0c', '0x0f', '0x0a', '0x09', '0x18', '0x1b', '0x1e', '0x1d', '0x14', '0x17', '0x12', '0x11', '0x30', '0x33', '0x36', '0x35', '0x3c', '0x3f', '0x3a', '0x39', '0x28', '0x2b', '0x2e', '0x2d', '0x24', '0x27', '0x22', '0x21', '0x60', '0x63', '0x66', '0x65', '0x6c', '0x6f', '0x6a', '0x69', '0x78', '0x7b', '0x7e', '0x7d', '0x74', '0x77', '0x72', '0x71', '0x50', '0x53', '0x56', '0x55', '0x5c', '0x5f', '0x5a', '0x59', '0x48', '0x4b', '0x4e', '0x4d', '0x44', '0x47', '0x42', '0x41', '0xc0', '0xc3', '0xc6', '0xc5', '0xcc', '0xcf', '0xca', '0xc9', '0xd8', '0xdb', '0xde', '0xdd', '0xd4', '0xd7', '0xd2', '0xd1', '0xf0', '0xf3', '0xf6', '0xf5', '0xfc', '0xff', '0xfa', '0xf9', '0xe8', '0xeb', '0xee', '0xed', '0xe4', '0xe7', '0xe2', '0xe1', '0xa0', '0xa3', '0xa6', '0xa5', '0xac', '0xaf', '0xaa', '0xa9', '0xb8', '0xbb', '0xbe', '0xbd', '0xb4', '0xb7', '0xb2', '0xb1', '0x90', '0x93', '0x96', '0x95', '0x9c', '0x9f', '0x9a', '0x99', '0x88', '0x8b', '0x8e', '0x8d', '0x84', '0x87', '0x82', '0x81', '0x9b', '0x98', '0x9d', '0x9e', '0x97', '0x94', '0x91', '0x92', '0x83', '0x80', '0x85', '0x86', '0x8f', '0x8c', '0x89', '0x8a', '0xab', '0xa8', '0xad', '0xae', '0xa7', '0xa4', '0xa1', '0xa2', '0xb3', '0xb0', '0xb5', '0xb6', '0xbf', '0xbc', '0xb9', '0xba', '0xfb', '0xf8', '0xfd', '0xfe', '0xf7', '0xf4', '0xf1', '0xf2', '0xe3', '0xe0', '0xe5', '0xe6', '0xef', '0xec', '0xe9', '0xea', '0xcb', '0xc8', '0xcd', '0xce', '0xc7', '0xc4', '0xc1', '0xc2', '0xd3', '0xd0', '0xd5', '0xd6', '0xdf', '0xdc', '0xd9', '0xda', '0x5b', '0x58', '0x5d', '0x5e', '0x57', '0x54', '0x51', '0x52', '0x43', '0x40', '0x45', '0x46', '0x4f', '0x4c', '0x49', '0x4a', '0x6b', '0x68', '0x6d', '0x6e', '0x67', '0x64', '0x61', '0x62', '0x73', '0x70', '0x75', '0x76', '0x7f', '0x7c', '0x79', '0x7a', '0x3b', '0x38', '0x3d', '0x3e', '0x37', '0x34', '0x31', '0x32', '0x23', '0x20', '0x25', '0x26', '0x2f', '0x2c', '0x29', '0x2a', '0x0b', '0x08', '0x0d', '0x0e', '0x07', '0x04', '0x01', '0x02', '0x13', '0x10', '0x15', '0x16', '0x1f', '0x1c', '0x19', '0x1a'],
                           '0x09': ['0x00', '0x09', '0x12', '0x1b', '0x24', '0x2d', '0x36', '0x3f', '0x48', '0x41', '0x5a', '0x53', '0x6c', '0x65', '0x7e', '0x77', '0x90', '0x99', '0x82', '0x8b', '0xb4', '0xbd', '0xa6', '0xaf', '0xd8', '0xd1', '0xca', '0xc3', '0xfc', '0xf5', '0xee', '0xe7', '0x3b', '0x32', '0x29', '0x20', '0x1f', '0x16', '0x0d', '0x04', '0x73', '0x7a', '0x61', '0x68', '0x57', '0x5e', '0x45', '0x4c', '0xab', '0xa2', '0xb9', '0xb0', '0x8f', '0x86', '0x9d', '0x94', '0xe3', '0xea', '0xf1', '0xf8', '0xc7', '0xce', '0xd5', '0xdc', '0x76', '0x7f', '0x64', '0x6d', '0x52', '0x5b', '0x40', '0x49', '0x3e', '0x37', '0x2c', '0x25', '0x1a', '0x13', '0x08', '0x01', '0xe6', '0xef', '0xf4', '0xfd', '0xc2', '0xcb', '0xd0', '0xd9', '0xae', '0xa7', '0xbc', '0xb5', '0x8a', '0x83', '0x98', '0x91', '0x4d', '0x44', '0x5f', '0x56', '0x69', '0x60', '0x7b', '0x72', '0x05', '0x0c', '0x17', '0x1e', '0x21', '0x28', '0x33', '0x3a', '0xdd', '0xd4', '0xcf', '0xc6', '0xf9', '0xf0', '0xeb', '0xe2', '0x95', '0x9c', '0x87', '0x8e', '0xb1', '0xb8', '0xa3', '0xaa', '0xec', '0xe5', '0xfe', '0xf7', '0xc8', '0xc1', '0xda', '0xd3', '0xa4', '0xad', '0xb6', '0xbf', '0x80', '0x89', '0x92', '0x9b', '0x7c', '0x75', '0x6e', '0x67', '0x58', '0x51', '0x4a', '0x43', '0x34', '0x3d', '0x26', '0x2f', '0x10', '0x19', '0x02', '0x0b', '0xd7', '0xde', '0xc5', '0xcc', '0xf3', '0xfa', '0xe1', '0xe8', '0x9f', '0x96', '0x8d', '0x84', '0xbb', '0xb2', '0xa9', '0xa0', '0x47', '0x4e', '0x55', '0x5c', '0x63', '0x6a', '0x71', '0x78', '0x0f', '0x06', '0x1d', '0x14', '0x2b', '0x22', '0x39', '0x30', '0x9a', '0x93', '0x88', '0x81', '0xbe', '0xb7', '0xac', '0xa5', '0xd2', '0xdb', '0xc0', '0xc9', '0xf6', '0xff', '0xe4', '0xed', '0x0a', '0x03', '0x18', '0x11', '0x2e', '0x27', '0x3c', '0x35', '0x42', '0x4b', '0x50', '0x59', '0x66', '0x6f', '0x74', '0x7d', '0xa1', '0xa8', '0xb3', '0xba', '0x85', '0x8c', '0x97', '0x9e', '0xe9', '0xe0', '0xfb', '0xf2', '0xcd', '0xc4', '0xdf', '0xd6', '0x31', '0x38', '0x23', '0x2a', '0x15', '0x1c', '0x07', '0x0e', '0x79', '0x70', '0x6b', '0x62', '0x5d', '0x54', '0x4f', '0x46'],
                           '0x0b': ['0x00', '0x0b', '0x16', '0x1d', '0x2c', '0x27', '0x3a', '0x31', '0x58', '0x53', '0x4e', '0x45', '0x74', '0x7f', '0x62', '0x69', '0xb0', '0xbb', '0xa6', '0xad', '0x9c', '0x97', '0x8a', '0x81', '0xe8', '0xe3', '0xfe', '0xf5', '0xc4', '0xcf', '0xd2', '0xd9', '0x7b', '0x70', '0x6d', '0x66', '0x57', '0x5c', '0x41', '0x4a', '0x23', '0x28', '0x35', '0x3e', '0x0f', '0x04', '0x19', '0x12', '0xcb', '0xc0', '0xdd', '0xd6', '0xe7', '0xec', '0xf1', '0xfa', '0x93', '0x98', '0x85', '0x8e', '0xbf', '0xb4', '0xa9', '0xa2', '0xf6', '0xfd', '0xe0', '0xeb', '0xda', '0xd1', '0xcc', '0xc7', '0xae', '0xa5', '0xb8', '0xb3', '0x82', '0x89', '0x94', '0x9f', '0x46', '0x4d', '0x50', '0x5b', '0x6a', '0x61', '0x7c', '0x77', '0x1e', '0x15', '0x08', '0x03', '0x32', '0x39', '0x24', '0x2f', '0x8d', '0x86', '0x9b', '0x90', '0xa1', '0xaa', '0xb7', '0xbc', '0xd5', '0xde', '0xc3', '0xc8', '0xf9', '0xf2', '0xef', '0xe4', '0x3d', '0x36', '0x2b', '0x20', '0x11', '0x1a', '0x07', '0x0c', '0x65', '0x6e', '0x73', '0x78', '0x49', '0x42', '0x5f', '0x54', '0xf7', '0xfc', '0xe1', '0xea', '0xdb', '0xd0', '0xcd', '0xc6', '0xaf', '0xa4', '0xb9', '0xb2', '0x83', '0x88', '0x95', '0x9e', '0x47', '0x4c', '0x51', '0x5a', '0x6b', '0x60', '0x7d', '0x76', '0x1f', '0x14', '0x09', '0x02', '0x33', '0x38', '0x25', '0x2e', '0x8c', '0x87', '0x9a', '0x91', '0xa0', '0xab', '0xb6', '0xbd', '0xd4', '0xdf', '0xc2', '0xc9', '0xf8', '0xf3', '0xee', '0xe5', '0x3c', '0x37', '0x2a', '0x21', '0x10', '0x1b', '0x06', '0x0d', '0x64', '0x6f', '0x72', '0x79', '0x48', '0x43', '0x5e', '0x55', '0x01', '0x0a', '0x17', '0x1c', '0x2d', '0x26', '0x3b', '0x30', '0x59', '0x52', '0x4f', '0x44', '0x75', '0x7e', '0x63', '0x68', '0xb1', '0xba', '0xa7', '0xac', '0x9d', '0x96', '0x8b', '0x80', '0xe9', '0xe2', '0xff', '0xf4', '0xc5', '0xce', '0xd3', '0xd8', '0x7a', '0x71', '0x6c', '0x67', '0x56', '0x5d', '0x40', '0x4b', '0x22', '0x29', '0x34', '0x3f', '0x0e', '0x05', '0x18', '0x13', '0xca', '0xc1', '0xdc', '0xd7', '0xe6', '0xed', '0xf0', '0xfb', '0x92', '0x99', '0x84', '0x8f', '0xbe', '0xb5', '0xa8', '0xa3'],
                           '0x0d': ['0x00', '0x0d', '0x1a', '0x17', '0x34', '0x39', '0x2e', '0x23', '0x68', '0x65', '0x72', '0x7f', '0x5c', '0x51', '0x46', '0x4b', '0xd0', '0xdd', '0xca', '0xc7', '0xe4', '0xe9', '0xfe', '0xf3', '0xb8', '0xb5', '0xa2', '0xaf', '0x8c', '0x81', '0x96', '0x9b', '0xbb', '0xb6', '0xa1', '0xac', '0x8f', '0x82', '0x95', '0x98', '0xd3', '0xde', '0xc9', '0xc4', '0xe7', '0xea', '0xfd', '0xf0', '0x6b', '0x66', '0x71', '0x7c', '0x5f', '0x52', '0x45', '0x48', '0x03', '0x0e', '0x19', '0x14', '0x37', '0x3a', '0x2d', '0x20', '0x6d', '0x60', '0x77', '0x7a', '0x59', '0x54', '0x43', '0x4e', '0x05', '0x08', '0x1f', '0x12', '0x31', '0x3c', '0x2b', '0x26', '0xbd', '0xb0', '0xa7', '0xaa', '0x89', '0x84', '0x93', '0x9e', '0xd5', '0xd8', '0xcf', '0xc2', '0xe1', '0xec', '0xfb', '0xf6', '0xd6', '0xdb', '0xcc', '0xc1', '0xe2', '0xef', '0xf8', '0xf5', '0xbe', '0xb3', '0xa4', '0xa9', '0x8a', '0x87', '0x90', '0x9d', '0x06', '0x0b', '0x1c', '0x11', '0x32', '0x3f', '0x28', '0x25', '0x6e', '0x63', '0x74', '0x79', '0x5a', '0x57', '0x40', '0x4d', '0xda', '0xd7', '0xc0', '0xcd', '0xee', '0xe3', '0xf4', '0xf9', '0xb2', '0xbf', '0xa8', '0xa5', '0x86', '0x8b', '0x9c', '0x91', '0x0a', '0x07', '0x10', '0x1d', '0x3e', '0x33', '0x24', '0x29', '0x62', '0x6f', '0x78', '0x75', '0x56', '0x5b', '0x4c', '0x41', '0x61', '0x6c', '0x7b', '0x76', '0x55', '0x58', '0x4f', '0x42', '0x09', '0x04', '0x13', '0x1e', '0x3d', '0x30', '0x27', '0x2a', '0xb1', '0xbc', '0xab', '0xa6', '0x85', '0x88', '0x9f', '0x92', '0xd9', '0xd4', '0xc3', '0xce', '0xed', '0xe0', '0xf7', '0xfa', '0xb7', '0xba', '0xad', '0xa0', '0x83', '0x8e', '0x99', '0x94', '0xdf', '0xd2', '0xc5', '0xc8', '0xeb', '0xe6', '0xf1', '0xfc', '0x67', '0x6a', '0x7d', '0x70', '0x53', '0x5e', '0x49', '0x44', '0x0f', '0x02', '0x15', '0x18', '0x3b', '0x36', '0x21', '0x2c', '0x0c', '0x01', '0x16', '0x1b', '0x38', '0x35', '0x22', '0x2f', '0x64', '0x69', '0x7e', '0x73', '0x50', '0x5d', '0x4a', '0x47', '0xdc', '0xd1', '0xc6', '0xcb', '0xe8', '0xe5', '0xf2', '0xff', '0xb4', '0xb9', '0xae', '0xa3', '0x80', '0x8d', '0x9a', '0x97'],
                           '0x0e': ['0x00', '0x0e', '0x1c', '0x12', '0x38', '0x36', '0x24', '0x2a', '0x70', '0x7e', '0x6c', '0x62', '0x48', '0x46', '0x54', '0x5a', '0xe0', '0xee', '0xfc', '0xf2', '0xd8', '0xd6', '0xc4', '0xca', '0x90', '0x9e', '0x8c', '0x82', '0xa8', '0xa6', '0xb4', '0xba', '0xdb', '0xd5', '0xc7', '0xc9', '0xe3', '0xed', '0xff', '0xf1', '0xab', '0xa5', '0xb7', '0xb9', '0x93', '0x9d', '0x8f', '0x81', '0x3b', '0x35', '0x27', '0x29', '0x03', '0x0d', '0x1f', '0x11', '0x4b', '0x45', '0x57', '0x59', '0x73', '0x7d', '0x6f', '0x61', '0xad', '0xa3', '0xb1', '0xbf', '0x95', '0x9b', '0x89', '0x87', '0xdd', '0xd3', '0xc1', '0xcf', '0xe5', '0xeb', '0xf9', '0xf7', '0x4d', '0x43', '0x51', '0x5f', '0x75', '0x7b', '0x69', '0x67', '0x3d', '0x33', '0x21', '0x2f', '0x05', '0x0b', '0x19', '0x17', '0x76', '0x78', '0x6a', '0x64', '0x4e', '0x40', '0x52', '0x5c', '0x06', '0x08', '0x1a', '0x14', '0x3e', '0x30', '0x22', '0x2c', '0x96', '0x98', '0x8a', '0x84', '0xae', '0xa0', '0xb2', '0xbc', '0xe6', '0xe8', '0xfa', '0xf4', '0xde', '0xd0', '0xc2', '0xcc', '0x41', '0x4f', '0x5d', '0x53', '0x79', '0x77', '0x65', '0x6b', '0x31', '0x3f', '0x2d', '0x23', '0x09', '0x07', '0x15', '0x1b', '0xa1', '0xaf', '0xbd', '0xb3', '0x99', '0x97', '0x85', '0x8b', '0xd1', '0xdf', '0xcd', '0xc3', '0xe9', '0xe7', '0xf5', '0xfb', '0x9a', '0x94', '0x86', '0x88', '0xa2', '0xac', '0xbe', '0xb0', '0xea', '0xe4', '0xf6', '0xf8', '0xd2', '0xdc', '0xce', '0xc0', '0x7a', '0x74', '0x66', '0x68', '0x42', '0x4c', '0x5e', '0x50', '0x0a', '0x04', '0x16', '0x18', '0x32', '0x3c', '0x2e', '0x20', '0xec', '0xe2', '0xf0', '0xfe', '0xd4', '0xda', '0xc8', '0xc6', '0x9c', '0x92', '0x80', '0x8e', '0xa4', '0xaa', '0xb8', '0xb6', '0x0c', '0x02', '0x10', '0x1e', '0x34', '0x3a', '0x28', '0x26', '0x7c', '0x72', '0x60', '0x6e', '0x44', '0x4a', '0x58', '0x56', '0x37', '0x39', '0x2b', '0x25', '0x0f', '0x01', '0x13', '0x1d', '0x47', '0x49', '0x5b', '0x55', '0x7f', '0x71', '0x63', '0x6d', '0xd7', '0xd9', '0xcb', '0xc5', '0xef', '0xe1', '0xf3', '0xfd', '0xa7', '0xa9', '0xbb', '0xb5', '0x9f', '0x91', '0x83', '0x8d']}
            return int(lookup_dict[n2][int(n1, 16)], 16)

    def MixColumns(self, statearray, I=False):
        ##Function to mix the columns##
        out = [[], [], [], []]
        if I == False:
            Multi_Matrix = [['0x02', '0x03', '0x01', '0x01'], ['0x01', '0x02', '0x03', '0x01'], [
                '0x01', '0x01', '0x02', '0x03'], ['0x03', '0x01', '0x01', '0x02']]
        else:
            Multi_Matrix = [['0x0e', '0x0b', '0x0d', '0x09'], ['0x09', '0x0e', '0x0b', '0x0d'], [
                '0x0d', '0x09', '0x0e', '0x0b'], ['0x0b', '0x0d', '0x09', '0x0e']]
        for i in range(0, len(statearray)):
            temp = []
            outtemp = []
            for j in range(0, len(statearray[i])):
                temp.append(statearray[j][i])
            for k in range(0, len(temp)):
                outtemp.append(hex(self.multi(temp[0], Multi_Matrix[k][0]) ^ self.multi(temp[1], Multi_Matrix[k][1]) ^ self.multi(
                    temp[2], Multi_Matrix[k][2]) ^ self.multi(temp[3], Multi_Matrix[k][3])))
                if len(outtemp[k]) < 4:
                    outtemp[k] = "0x0"+outtemp[k][-1]
            for k in range(0, len(outtemp)):
                out[k].insert(i, outtemp[k])
        return out

    def AddroundKeys(self, Rkeys, round, statearray):
        out = [[], [], [], []]
        for i in range(0, len(statearray)):
            for j in range(2, 10, 2):
                out[i].append(
                    hex(int("0x"+Rkeys[round][j//4][j:j+2], 16) ^ int(statearray[i][(j-2)//2], 16)))
                if len(out[i][-1]) < 4:
                    out[i][-1] = "0x0"+out[i][-1][-1]
        return out

    def encrypt(self):
        out = self.state_array()
        Rkeys = self.key_conversion()
        for i in range(0, len(out)):
            temp = out[i]
            temp = self.AddroundKeys(Rkeys, 0, temp)
            for j in range(1, 10):
                temp = self.SubBytes(self.ShiftRows(
                    self.MixColumns(self.AddroundKeys(Rkeys, j, temp))))
            temp = self.SubBytes(self.ShiftRows(
                self.AddroundKeys(Rkeys, 10, (temp))))
            out[i] = temp
        outstr = '0x'
        for i in out:
            for j in i:
                for k in j:
                    outstr += k[-2] + k[-1]
        return outstr


class aes_decrypt(aes_encrypt):
    # Class for decryption of data using aes
    def ISubBytes(self, statearray):
        ##Inverse of the SubsBytes function##
        ISubsbox = {'0': {'0': '52', '1': '09', '2': '6a', '3': 'd5', '4': '30', '5': '36', '6': 'a5', '7': '38', '8': 'bf', '9': '40', 'a': 'a3', 'b': '9e', 'c': '81', 'd': 'f3', 'e': 'd7', 'f': 'fb'},
                    '1': {'0': '7c', '1': 'e3', '2': '39', '3': '82', '4': '9b', '5': '2f', '6': 'ff', '7': '87', '8': '34', '9': '8e', 'a': '43', 'b': '44', 'c': 'c4', 'd': 'de', 'e': 'e9', 'f': 'cb'},
                    '2': {'0': '54', '1': '7b', '2': '94', '3': '32', '4': 'a6', '5': 'c2', '6': '23', '7': '3d', '8': 'ee', '9': '4c', 'a': '95', 'b': '0b', 'c': '42', 'd': 'fa', 'e': 'c3', 'f': '4e'},
                    '3': {'0': '08', '1': '2e', '2': 'a1', '3': '66', '4': '28', '5': 'd9', '6': '24', '7': 'b2', '8': '76', '9': '5b', 'a': 'a2', 'b': '49', 'c': '6d', 'd': '8b', 'e': 'd1', 'f': '25'},
                    '4': {'0': '72', '1': 'f8', '2': 'f6', '3': '64', '4': '86', '5': '68', '6': '98', '7': '16', '8': 'd4', '9': 'a4', 'a': '5c', 'b': 'cc', 'c': '5d', 'd': '65', 'e': 'b6', 'f': '92'},
                    '5': {'0': '6c', '1': '70', '2': '48', '3': '50', '4': 'fd', '5': 'ed', '6': 'b9', '7': 'da', '8': '5e', '9': '15', 'a': '46', 'b': '57', 'c': 'a7', 'd': '8d', 'e': '9d', 'f': '84'},
                    '6': {'0': '90', '1': 'd8', '2': 'ab', '3': '00', '4': '8c', '5': 'bc', '6': 'd3', '7': '0a', '8': 'f7', '9': 'e4', 'a': '58', 'b': '05', 'c': 'b8', 'd': 'b3', 'e': '45', 'f': '06'},
                    '7': {'0': 'd0', '1': '2c', '2': '1e', '3': '8f', '4': 'ca', '5': '3f', '6': '0f', '7': '02', '8': 'c1', '9': 'af', 'a': 'bd', 'b': '03', 'c': '01', 'd': '13', 'e': '8a', 'f': '6b'},
                    '8': {'0': '3a', '1': '91', '2': '11', '3': '41', '4': '4f', '5': '67', '6': 'dc', '7': 'ea', '8': '97', '9': 'f2', 'a': 'cf', 'b': 'ce', 'c': 'f0', 'd': 'b4', 'e': 'e6', 'f': '73'},
                    '9': {'0': '96', '1': 'ac', '2': '74', '3': '22', '4': 'e7', '5': 'ad', '6': '35', '7': '85', '8': 'e2', '9': 'f9', 'a': '37', 'b': 'e8', 'c': '1c', 'd': '75', 'e': 'df', 'f': '6e'},
                    'a': {'0': '47', '1': 'f1', '2': '1a', '3': '71', '4': '1d', '5': '29', '6': 'c5', '7': '89', '8': '6f', '9': 'b7', 'a': '62', 'b': '0e', 'c': 'aa', 'd': '18', 'e': 'be', 'f': '1b'},
                    'b': {'0': 'fc', '1': '56', '2': '3e', '3': '4b', '4': 'c6', '5': 'd2', '6': '79', '7': '20', '8': '9a', '9': 'db', 'a': 'c0', 'b': 'fe', 'c': '78', 'd': 'cd', 'e': '5a', 'f': 'f4'},
                    'c': {'0': '1f', '1': 'dd', '2': 'a8', '3': '33', '4': '88', '5': '07', '6': 'c7', '7': '31', '8': 'b1', '9': '12', 'a': '10', 'b': '59', 'c': '27', 'd': '80', 'e': 'ec', 'f': '5f'},
                    'd': {'0': '60', '1': '51', '2': '7f', '3': 'a9', '4': '19', '5': 'b5', '6': '4a', '7': '0d', '8': '2d', '9': 'e5', 'a': '7a', 'b': '9f', 'c': '93', 'd': 'c9', 'e': '9c', 'f': 'ef'},
                    'e': {'0': 'a0', '1': 'e0', '2': '3b', '3': '4d', '4': 'ae', '5': '2a', '6': 'f5', '7': 'b0', '8': 'c8', '9': 'eb', 'a': 'bb', 'b': '3c', 'c': '83', 'd': '53', 'e': '99', 'f': '61'},
                    'f': {'0': '17', '1': '2b', '2': '04', '3': '7e', '4': 'ba', '5': '77', '6': 'd6', '7': '26', '8': 'e1', '9': '69', 'a': '14', 'b': '63', 'c': '55', 'd': '21', 'e': '0c', 'f': '7d'}}
        for i in range(0, len(statearray)):
            for j in range(0, len(statearray[i])):
                statearray[i][j] = (
                    "0x" + ISubsbox[(statearray[i][j])[-2]
                                    ][(statearray[i][j])[-1]]
                )
        return statearray

    def decrypt(self):
        out = self.state_array()
        Rkeys = self.key_conversion()
        for i in range(0, len(out)):
            temp = self.AddroundKeys(Rkeys, 10, self.ShiftRows(
                self.ISubBytes(out[i]), Inverse=True))
            for j in range(9, 0, -1):
                temp = self.AddroundKeys(Rkeys, j, self.MixColumns(
                    self.ShiftRows(self.ISubBytes(temp), Inverse=True), I=True))
            temp = self.AddroundKeys(Rkeys, 0, temp)
            out[i] = temp
        outstr = '0x'
        for i in out:
            for j in i:
                for k in j:
                    outstr += (k[-2]+k[-1])
        return outstr

class stegano:

    def __init__(self,data,img,fp=''):
        ## fp is the file path where file is to be saved
        ## img is the image address
        ## data is the plaintext string
        ## .jpg images can cause problems with PIL, .png is preferred
        self.data=data
        self.img=img
        if fp=='':
            self.fp=self.img

    def bindata(self):
        out=[]
        for i in self.data:
            out.append(bin(ord(i)).lstrip('0b'))
            if len(out[-1])<7:
                for j in range(7-len(out[-1])):
                    out[-1]='0'+out[-1]
        return out

    def encrypt(self):
        img=Image.open(self.img)
        bindat=self.bindata()
        pix=[i for i in img.convert('RGB').getdata()]
        for i in range(len(bindat)):
            k=((i)*8)%3
            o=((i+1)*8)%3
            m=(i*8)//3
            n=((i+1)*8)//3
            l=list(pix[m])
            L=list(pix[n])
            if l[k]%2==1:
                l[k]=l[k]-1
                pix[m]=tuple(l)
            if i==len(bindat)-1:
                if L[o]%2==0 and L[o]!=0:
                    L[o]=L[o]-1
                    pix[n]=tuple(L)
                else:
                    L[o]=L[o]+1
                    pix[n]=tuple(L)
            a=(k+1)%3
            for j in range(a,a+7):
                if j%3==0:
                    out=[]
                elif j==a:
                    if k==0:
                        out=[pix[(i*8)//3][0]]
                    elif k==1:
                        out=list(pix[(i*8)//3][:2])
                ppoint=pix[(i*8+j+1-a)//3][(i*8+j+1-a)%3]
                if bindat[i][j-a]=='0':
                    if ppoint%2==1:
                        out.append(ppoint-1)
                    else:
                        out.append(ppoint)
                else:
                    if ppoint%2==0 and ppoint!=0:
                        out.append(ppoint-1)
                    elif ppoint==0:
                        out.append(ppoint+1)
                    else:
                        out.append(ppoint)
                if len(out)==3:
                    pix[(i*8+j+1-a)//3]=tuple(out)
                elif j==a+6:
                    if len(out)==1:
                        pix[(i*8+j+1-a)//3]=tuple(out+list(pix[(i*8+j+1-a)//3][1:]))
                    else:
                        pix[(i*8+j+1-a)//3]=tuple(out+[pix[(i*8+j+1-a)//3][2]])
        img.putdata(pix)
        print(pix[0],pix[1],pix[2],pix[3])
        img.save(self.fp)
        img.close()


class stegano_decrypt(stegano):

    def __init__(self,data,img):
        self.data=data
        self.img=img

    def decrypt(self):
        img=Image.open(self.img)
        pix=[i for i in img.convert("RGB").getdata()]
        print(pix[0],pix[1],pix[2])
        out=[]
        for i in range(len(pix)):
            for j in range(0,3):
                if (i*3+j)%8==0:
                    if i!=0:
                        out.append(chr(int(outstr,2)))
                    outstr='0b'
                    if pix[i][j]%2==1:
                        break
                else:
                    curp=pix[i][j]
                    if curp%2==0:
                        outstr=outstr+'0'
                    else:
                        outstr=outstr+'1'
            else:
                continue
            break
        return "".join(out)         