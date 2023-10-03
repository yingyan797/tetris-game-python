class Session:
    def findPlayer(pname):
        f = open("players.txt", "r")
        while True:
            pline = f.readline()
            if pline != "":
                pn = ""
                i = 0
                while True:
                    c = pline[i]
                    if c != " ":
                        pn += c
                    else:
                        i += 1
                        break
                    i += 1
                if Session.encr(pname) == pn:
                    return pline[i:len(pline)-1]
            else:
                return ""
                

    def regPlayer(pname, pwd):
        f = open("players.txt", "a")
        f.write(Session.encr(pname) + " " + Session.encr(pwd) + '\n')
        f.close()


    def encr(pwd):
        ref = pwd
        lim = len(pwd)
        for i in range(lim):
            ref = ref[i:] + pwd[i] + ref[:i]

        aord = ord('a')
        zerord = ord('0')
        trans = 0

        res01 = ["",""]
        for i in range(lim):
            trans = (trans + ord(ref[i]))%26
            res01[0] += chr(aord + (trans*(ord(ref[i]))) % 26)
        for i in range(lim, 2*lim):
            trans = (2*trans - ord(ref[i]))%10
            res01[1] += chr(zerord + (trans*(ord(ref[i]))) % 10)
        
        res = ""
        for i in range(lim):
            s = (i*i + ord(pwd[i])) % 5
            res += res01[s%2][i] + res01[(s+1)%2][i]
        return res

                


