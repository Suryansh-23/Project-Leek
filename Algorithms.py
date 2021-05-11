class aes:  
    ##class for ecryption and decryption of data using aes##   
    def __init__(self, cipherkey, plaintext,N):
        self.N=N
        self.cipherkey=cipherkey
        self.plaintext=plaintext
        ##plaintext MUST be entered in a STRING of HEXADECIMAL numbers with thw 0x prefix##
        ##Cipherkey MUST be a 128, 192, 256 bit key entered as a string of hexadecimal numbers with the 0x prefix##
        ##N is the encryption type. 128 bit is 0, 192 is 1 and 256 is 2##
    def state_array(self):
        ##Function to convert the plaintext to a 3D array of hexadecimal numbers##
        if len(self.plaintext)%2!=0:
            self.plaintext+='0'
        a=[]
        for i in range(34,len(self.plaintext),32):
            out=[[],[],[],[]]
            block=self.plaintext[i-32:i]
            for l in range(0,16):
                out[l//4].append('0x'+block[l*2]+block[(l*2)+1])
            a.append(out)
            b=i
        if len(self.plaintext)<35:
            b=2
        out=[[],[],[],[]]
        if len(self.plaintext[b:-1])>0:
            k=0
            for l in range(b,len(self.plaintext)-1,2):
                out[k//4].append(('0x'+self.plaintext[l]+self.plaintext[l+1]))
                k+=1
            else:
                for i in range(0, len(out)):
                    while len(out[i])<4:
                        out[i].append('0x00')
            a.append(out)
        return a
    def key_conversion(self):
        ##key conversion into 11 round keys. Each round key consists of 32,48,64 bit words which are decided by the cipherkey##
        Rkey0=self.cipherkey
        Rkeyt=[[]]
        for i in range(0,(10+(self.N*2))):
            Rkeyt.append([])
        for i in range(2,len(Rkey0),8+4*(self.N)):
            Rkey0Wi=int('0x'+Rkey0[i:i+8+((self.N)*4)], 16)
            Rkeyt[0].append(Rkey0Wi)
        Rconi={1:2,2:4,3:8,4:16,5:32,6:64,7:128,8:27,9:54,10:108,11:216,12:171,13:77,14:154}
        for i in range(1,(11+(self.N*2))):
            RkeyiW0=(Rkeyt[i-1])[0]^(((Rkeyt[i-1])[2])>>8)^Rconi[i]
            Rkeyt[i].append(RkeyiW0)
            for j in range(0,3):
                RkeyiWj=(Rkeyt[i-1])[j]^(Rkeyt[i])[j-1]
                Rkeyt[i].append(RkeyiWj)
        for i in range(0,len(Rkeyt)):
            for j in range(0,4):
                Rkeyt[i][j]=hex(Rkeyt[i][j])
        return Rkeyt
    def SubBytes(self, statearray):
        ##First step of the encryption. The plaintext is substituted using an S-box##
        S_box={'0':{'0':'63','1':'7c','2':'77','3':'7b','4':'f2','5':'6b','6':'6f','7':'c5','8':'30','9':'01','a':'67','b':'2b','c':'fe','d':'d7','e':'ab','f':'76'},
        '1':{'0':'ca','1':'82','2':'c9','3':'7d','4':'fa','5':'59','6':'47','7':'f0','8':'ad','9':'d4','a':'a2','b':'af','c':'9c','d':'a4','e':'72','f':'c0'},
        '2':{'0':'b7','1':'fd','2':'93','3':'26','4':'36','5':'3f','6':'f7','7':'cc','8':'34','9':'a5','a':'e5','b':'f1','c':'71','d':'d8','e':'31','f':'15'},
        '3':{'0':'04','1':'c7','2':'23','3':'c3','4':'18','5':'96','6':'05','7':'9a','8':'07','9':'12','a':'80','b':'e2','c':'eb','d':'27','e':'b2','f':'75'},
        '4':{'0':'09','1':'83','2':'2c','3':'1a','4':'1b','5':'6e','6':'5a','7':'a0','8':'52','9':'3b','a':'d6','b':'b3','c':'29','d':'e3','e':'2f','f':'84'},
        '5':{'0':'53','1':'d1','2':'00','3':'ed','4':'20','5':'fc','6':'b1','7':'5b','8':'6a','9':'cb','a':'be','b':'39','c':'4a','d':'4c','e':'58','f':'cf'},
        '6':{'0':'d0','1':'ef','2':'aa','3':'fb','4':'43','5':'4d','6':'33','7':'85','8':'45','9':'f9','a':'02','b':'7f','c':'50','d':'3c','e':'9f','f':'a8'},
        '7':{'0':'51','1':'a3','2':'40','3':'8f','4':'92','5':'9d','6':'38','7':'f5','8':'bc','9':'b6','a':'da','b':'21','c':'10','d':'ff','e':'f3','f':'d2'},
        '8':{'0':'cd','1':'0c','2':'13','3':'ec','4':'5f','5':'97','6':'44','7':'17','8':'c4','9':'a7','a':'7e','b':'3d','c':'64','d':'5d','e':'19','f':'73'},
        '9':{'0':'60','1':'81','2':'4f','3':'dc','4':'22','5':'2a','6':'90','7':'88','8':'46','9':'ee','a':'b8','b':'14','c':'de','d':'5e','e':'0b','f':'db'},
        'a':{'0':'e0','1':'32','2':'3a','3':'0a','4':'49','5':'06','6':'24','7':'5c','8':'c2','9':'d3','a':'ac','b':'62','c':'91','d':'95','e':'e4','f':'79'},
        'b':{'0':'e7','1':'c8','2':'37','3':'6d','4':'8d','5':'d5','6':'4e','7':'a9','8':'6c','9':'56','a':'f4','b':'ea','c':'65','d':'7a','e':'ae','f':'08'},
        'c':{'0':'ba','1':'78','2':'25','3':'2e','4':'1c','5':'a6','6':'b4','7':'c6','8':'e8','9':'dd','a':'74','b':'1f','c':'4b','d':'bd','e':'8b','f':'8a'},
        'd':{'0':'70','1':'3e','2':'b5','3':'66','4':'48','5':'03','6':'f6','7':'0e','8':'61','9':'35','a':'57','b':'b9','c':'86','d':'c1','e':'1d','f':'9e'},
        'e':{'0':'e1','1':'f8','2':'98','3':'11','4':'69','5':'d9','6':'8e','7':'94','8':'9b','9':'1e','a':'87','b':'e9','c':'ce','d':'55','e':'28','f':'df'},
        'f':{'0':'8c','1':'a1','2':'89','3':'0d','4':'bf','5':'e6','6':'42','7':'68','8':'41','9':'99','a':'2d','b':'0f','c':'b0','d':'54','e':'bb','f':'16'}}
        substext=[[],[],[],[]]
        for i in range(0, len(statearray)):
            for j in statearray[i]:
                substext[i].append("0x"+(S_box[j[-2]])[j[-1]])
        return substext
    def Round_Shift_R(self,L,n):
        ##Round shifting a list to the right for shiftrows##
        out=[]
        for i in range(n,0,-1):
            out.append(L[-i])
        else:
            out.extend(L[0:-n])
        return out
    def Round_Shift_L(self, L,n):
        ##Round Shifting a list to the left for inverse shiftrows##
        out=L[n:]
        out.extend(L[0:n])
        return out
    def ShiftRows(self, statearray, Inverse=False):
        ##Function to round shift rows by a value depending on the row number##
        out=[[],[],[],[]]
        for i in range(0, len(statearray)):
            temp=[]
            for j in range(0,len(statearray[i])):
                temp.append(statearray[j][i])
            if Inverse==False:
                temp=self.Round_Shift_R(temp,i)
            else:
                temp=self.Round_Shift_L(temp,i)
            for k in range(0,len(temp)):
                out[k].insert(i,temp[k])
        for i in range(0, len(out)):
            out[i][0]=statearray[i][0]
        return out
    def multi(n1,n2):
        ##Defining the matrix multiplication##
        E_box={'0':{'0':'01','1':'03','2':'05','3':'0f','4':'11','5':'33','6':'55','7':'ff','8':'1a','9':'2e','a':'72','b':'96','c':'A1','d':'f8','e':'13','f':'35'},
        '1':{'0':'5f','1':'e1','2':'38','3':'48','4':'d8','5':'73','6':'95','7':'a4','8':'f7','9':'02','a':'06','b':'0A','c':'1e','d':'22','e':'66','f':'aa'},
        '2':{'0':'e5','1':'34','2':'5c','3':'e4','4':'37','5':'59','6':'eb','7':'26','8':'6a','9':'be','a':'D9','b':'70','c':'90','d':'ab','e':'e6','f':'31'},
        '3':{'0':'53','1':'f5','2':'04','3':'0c','4':'14','5':'3c','6':'44','7':'cc','8':'4f','9':'d1','a':'68','b':'b8','c':'d3','d':'6e','e':'b2','f':'cd'},
        '4':{'0':'4c','1':'d4','2':'67','3':'a9','4':'e0','5':'3b','6':'4d','7':'d7','8':'62','9':'a6','a':'f1','b':'08','c':'18','d':'28','e':'78','f':'88'},
        '5':{'0':'83','1':'9e','2':'b9','3':'d0','4':'6b','5':'bd','6':'dc','7':'7f','8':'81','9':'98','a':'b3','b':'ce','c':'49','d':'db','e':'76','f':'9a'},
        '6':{'0':'b5','1':'c4','2':'57','3':'f9','4':'10','5':'30','6':'50','7':'f0','8':'0b','9':'1d','a':'27','b':'69','c':'bb','d':'d6','e':'61','f':'a3'},
        '7':{'0':'fe','1':'19','2':'2b','3':'7d','4':'87','5':'92','6':'ad','7':'ec','8':'2f','9':'71','a':'93','b':'ae','c':'e9','d':'20','e':'60','f':'a0'},
        '8':{'0':'fb','1':'16','2':'3a','3':'4e','4':'d2','5':'6d','6':'b7','7':'c2','8':'5d','9':'e7','a':'32','b':'56','c':'fa','d':'15','e':'3f','f':'41'},
        '9':{'0':'c3','1':'5e','2':'e2','3':'3d','4':'47','5':'c9','6':'40','7':'c0','8':'5b','9':'ed','a':'2c','b':'74','c':'9c','d':'bf','e':'da','f':'75'},
        'a':{'0':'9f','1':'ba','2':'d5','3':'64','4':'ac','5':'ef','6':'2a','7':'7e','8':'82','9':'9d','a':'bc','b':'df','c':'7a','d':'8e','e':'89','f':'80'},
        'b':{'0':'9b','1':'b6','2':'c1','3':'58','4':'e8','5':'23','6':'65','7':'af','8':'ea','9':'25','a':'6f','b':'b1','c':'c8','d':'43','e':'c5','f':'54'},
        'c':{'0':'fc','1':'1f','2':'21','3':'63','4':'a5','5':'f4','6':'07','7':'09','8':'1b','9':'2d','a':'77','b':'99','c':'b0','d':'cb','e':'46','f':'ca'},
        'd':{'0':'45','1':'cf','2':'4a','3':'de','4':'79','5':'8b','6':'86','7':'91','8':'a8','9':'e3','a':'3e','b':'42','c':'c6','d':'51','e':'f3','f':'0e'},
        'e':{'0':'12','1':'36','2':'5a','3':'ee','4':'29','5':'7b','6':'8d','7':'8c','8':'8f','9':'8a','a':'85','b':'94','c':'a7','d':'f2','e':'0d','f':'17'},
        'f':{'0':'39','1':'4b','2':'dd','3':'7c','4':'84','5':'97','6':'a2','7':'fd','8':'1c','9':'24','a':'6c','b':'b4','c':'c7','d':'52','e':'F6','f':'01'}}

        L_box={'0':{'1':'00','2':'19','3':'01','4':'32','5':'02','6':'1a','7':'c6','8':'4B','9':'c7','a':'1b','b':'68','c':'33','d':'ee','e':'df','f':'03'},
        '1':{'0':'64','1':'04','2':'e0','3':'0e','4':'34','5':'8d','6':'81','7':'ef','8':'4c','9':'71','a':'08','b':'c8','c':'F8','d':'69','e':'1c','f':'c1'},
        '2':{'0':'7d','1':'c2','2':'1d','3':'b5','4':'f9','5':'b9','6':'27','7':'6a','8':'4d','9':'e4','a':'a6','b':'72','c':'9a','d':'c9','e':'09','f':'78'},
        '3':{'0':'65','1':'2f','2':'8a','3':'05','4':'21','5':'0f','6':'e1','7':'24','8':'12','9':'f0','a':'82','b':'45','c':'35','d':'93','e':'da','f':'8e'},
        '4':{'0':'96','1':'8f','2':'db','3':'bd','4':'36','5':'d0','6':'ce','7':'94','8':'13','9':'5c','a':'d2','b':'f1','c':'40','d':'46','e':'83','f':'38'},
        '5':{'0':'66','1':'dd','2':'fd','3':'30','4':'bf','5':'06','6':'8b','7':'62','8':'b3','9':'25','a':'e2','b':'98','c':'22','d':'88','e':'91','f':'10'},
        '6':{'0':'7e','1':'6e','2':'48','3':'c3','4':'a3','5':'b6','6':'1e','7':'42','8':'3a','9':'6b','a':'28','b':'54','c':'fa','d':'85','e':'3d','f':'ba'},
        '7':{'0':'2b','1':'79','2':'0a','3':'15','4':'9b','5':'9f','6':'5e','7':'ca','8':'4e','9':'d4','a':'ac','b':'e5','c':'f3','d':'73','e':'a7','f':'57'},
        '8':{'0':'af','1':'58','2':'ab','3':'50','4':'f4','5':'ea','6':'d6','7':'74','8':'4f','9':'ae','a':'e9','b':'d5','c':'e7','d':'e6','e':'ad','f':'e8'},
        '9':{'0':'2c','1':'d7','2':'75','3':'7a','4':'eb','5':'16','6':'0b','7':'f5','8':'59','9':'cb','a':'5f','b':'b0','c':'9c','d':'a9','e':'51','f':'a0'},
        'a':{'0':'7f','1':'0c','2':'f6','3':'6f','4':'17','5':'c4','6':'49','7':'ec','8':'d8','9':'43','a':'1f','b':'2d','c':'a4','d':'76','e':'7b','f':'b7'},
        'b':{'0':'cc','1':'bb','2':'3e','3':'5a','4':'fb','5':'60','6':'b1','7':'86','8':'3b','9':'52','a':'a1','b':'6c','c':'aa','d':'55','e':'29','f':'9d'},
        'c':{'0':'97','1':'b2','2':'87','3':'90','4':'61','5':'be','6':'dc','7':'fc','8':'bc','9':'95','a':'cf','b':'cd','c':'37','d':'3f','e':'5b','f':'d1'},
        'd':{'0':'53','1':'39','2':'84','3':'3c','4':'41','5':'a2','6':'6d','7':'47','8':'14','9':'2a','a':'9e','b':'5d','c':'56','d':'f2','e':'d3','f':'ab'},
        'e':{'0':'44','1':'11','2':'92','3':'d9','4':'23','5':'20','6':'2e','7':'89','8':'b4','9':'7c','a':'b8','b':'26','c':'77','d':'99','e':'e3','f':'a5'},
        'f':{'0':'67','1':'4a','2':'ed','3':'de','4':'c5','5':'31','6':'fe','7':'18','8':'0d','9':'63','a':'8C','b':'80','c':'c0','d':'f7','e':'70','f':'07'}}

        out1 = int('0x'+(L_box[n1[-2]])[n1[-1]],16)+int('0x'+(L_box[n2[-2]])[n2[-1]], 16)
        if out1>255:
           out1-=255
        out1=hex(out1)
        return (int(('0x'+(E_box[out1[-2]])[out1[-1]]),16))

    def MixColumns(self,statearray,I=False):
        ##Function to mix the columns##
            if I==False:
                Multi_Matrix=[['0x02','0x03','0x01','0x01'],['0x01','0x02','0x03','0x01'],['0x01','0x01','0x02','0x03'],['0x03','0x01','0x01','0x02']]
            else:
                Multi_Matrix=[['0x0e','0x0b','0x0d','0x09'],['0x09','0x0e','0x0b','0x0d'],['0x0d','0x09','0x0e','0x0b'],['0x0b','0x0d','0x09','0x0e']]
            for i in range(0, len(statearray)):
                statearray[i][0]=hex(self.multi(statearray[i][0],Multi_Matrix[i][0])^self.multi(statearray[i][1],Multi_Matrix[i][1])^self.multi(statearray[i][2],Multi_Matrix[i][2])^self.multi(statearray[i][3], Multi_Matrix[i][3]))
            return statearray 
    
    def AddroundKeys(self, Rkeys, round, statearray):
        out=[[],[],[],[]]
        for i in range(0,len(statearray)):
            for j in range(0,3):
                out[i].append(hex(int(Rkeys[round][j],16)^int(statearray[i][j],16)))
        return out
    def encrypt(self):
        out=self.state_array()
        Rkeys=self.key_conversion()
        for i in range(0,len(out)):
            temp=out[i]
            temp=self.AddroundKeys(Rkeys,0,temp)
            for j in range(1,10):
                temp=self.MixColumns(self.AddroundKeys(Rkeys,j,self.ShiftRows(self.SubBytes(temp))))
            temp=self.AddroundKeys(Rkeys,11,self.ShiftRows(self.SubBytes(temp)))
            out[i]=temp
        outstr='0x'
        for i in out:
            for j in i:
                for k in j:
                    outstr+=(k[-2]+k[-1])
        return outstr
    def ISubBytes(statearray):
        ##Inverse of the SubsBytes function##
        ISubsbox={'0':{'0':'52','1':'09','2':'6a','3':'d5','4':'30','5':'36','6':'a5','7':'38','8':'bf','9':'40','a':'a3','b':'9e','c':'81','d':'f3','e':'d7','f':'fb'},
        '1':{'0':'7c','1':'e3','2':'39','3':'82','4':'9b','5':'2f','6':'ff','7':'87','8':'34','9':'8e','a':'43','b':'44','c':'c4','d':'de','e':'e9','f':'cb'},
        '2':{'0':'54','1':'7b','2':'94','3':'32','4':'a6','5':'c2','6':'23','7':'3d','8':'ee','9':'4c','a':'95','b':'0b','c':'42','d':'fa','e':'c3','f':'4e'},
        '3':{'0':'08','1':'2e','2':'a1','3':'66','4':'28','5':'d9','6':'24','7':'b2','8':'76','9':'5b','a':'a2','b':'49','c':'6d','d':'8b','e':'d1','f':'25'},
        '4':{'0':'72','1':'f8','2':'f6','3':'64','4':'86','5':'68','6':'98','7':'16','8':'d4','9':'a4','a':'5c','b':'cc','c':'5d','d':'65','e':'b6','f':'92'},
        '5':{'0':'6c','1':'70','2':'48','3':'50','4':'fd','5':'ed','6':'b9','7':'da','8':'5e','9':'15','a':'46','b':'57','c':'a7','d':'8d','e':'9d','f':'84'},
        '6':{'0':'90','1':'d8','2':'ab','3':'00','4':'8c','5':'bc','6':'d3','7':'0a','8':'f7','9':'e4','a':'58','b':'05','c':'b8','d':'b3','e':'45','f':'06'},
        '7':{'0':'d0','1':'2c','2':'1e','3':'8f','4':'ca','5':'3f','6':'0f','7':'02','8':'c1','9':'af','a':'bd','b':'03','c':'01','d':'13','e':'8a','f':'6b'},
        '8':{'0':'3a','1':'91','2':'11','3':'41','4':'4f','5':'67','6':'dc','7':'ea','8':'97','9':'f2','a':'cf','b':'ce','c':'f0','d':'b4','e':'e6','f':'73'},
        '9':{'0':'96','1':'ac','2':'74','3':'22','4':'e7','5':'ad','6':'35','7':'85','8':'e2','9':'f9','a':'37','b':'e8','c':'1c','d':'75','e':'df','f':'6e'},
        'a':{'0':'47','1':'f1','2':'1a','3':'71','4':'1d','5':'29','6':'c5','7':'89','8':'6f','9':'b7','a':'62','b':'0e','c':'aa','d':'18','e':'be','f':'1b'},
        'b':{'0':'fc','1':'56','2':'3e','3':'4b','4':'c6','5':'d2','6':'79','7':'20','8':'9a','9':'db','a':'c0','b':'fe','c':'78','d':'cd','e':'5a','f':'f4'},
        'c':{'0':'1f','1':'dd','2':'a8','3':'33','4':'88','5':'07','6':'c7','7':'31','8':'b1','9':'12','a':'10','b':'59','c':'27','d':'80','e':'ec','f':'5f'},
        'd':{'0':'60','1':'51','2':'7f','3':'a9','4':'19','5':'b5','6':'4a','7':'0d','8':'2d','9':'e5','a':'7a','b':'9f','c':'93','d':'c9','e':'9c','f':'ef'},
        'e':{'0':'a0','1':'e0','2':'3b','3':'4d','4':'ae','5':'2a','6':'f5','7':'b0','8':'c8','9':'eb','a':'bb','b':'3c','c':'83','d':'53','e':'99','f':'61'},
        'f':{'0':'17','1':'2b','2':'04','3':'7e','4':'ba','5':'77','6':'d6','7':'26','8':'e1','9':'69','a':'14','b':'63','c':'55','d':'21','e':'0c','f':'7d'}}
        for i in range(0,len(statearray)):
            for j in range(0,len(statearray[i])):
                statearray[i][j]='0x'+ISubsbox[((statearray[i][j])[-2])[-1]]
    def decrypt(self):
        out=self.state_array(self.plaintext)
        Rkeys=self.key_conversion()
        for i in range(0,len(out)):
            temp=self.AddroundKeys(Rkeys,out[i])
            for j in range(0,9):
                temp=self.MixColumns(self.AddroundKeys(Rkeys,self.ISubBytes(self.ShiftRows(temp, Inverse=True))),I=True)
            temp=self.AddroundKeys(Rkeys,(self.SubBytes(self.ShiftRows(temp),Inverse=True)))
            out[i]=temp
        outstr='0x'
        for i in out:
            for j in i:
                for k in j:
                    outstr+=(k[-2]+k[-1])
        return outstr
