from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair


class Cred:
    def __init__(self, groupObj):
        global group
        group = groupObj

    def Setup(self, n=1, secparam = None):
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])
        g1, g2 = group.random(G1), group.random(G2)
        sk = group.random(ZR)
        pk = g2 ** sk
        hp = group.random(G1)
        PP = {'g1':g1, 'g2':g2, 'secparam':secparam, 'pk':pk, 'n':n, 'hp':hp, 'H':group.hash}
        for i in range(0, n+1):
            h = group.random(G1)
            PP['h'+str(i)] = h
        # group.EndBenchmark()
        return PP, sk #, group.GetGeneralBenchmarks()
        
    def Issue(self, buf, PP, Attr):
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])
        Credential = dict()
        sk = group.deserialize(buf)
        Credential['x'], Credential['s'] = group.random(ZR), group.random(ZR)
        g1, h0 = PP['g1'], PP['h0']

        A = g1 * (h0 ** Credential['s'])
        for i in range(1, 1 + PP['n']):
            A  = A * (PP['h'+str(i)] ** Attr['m'+str(i)])
        Credential['A'] = A ** (1/(sk + Credential['x']))
        # group.EndBenchmark()
        return Credential #, group.GetGeneralBenchmarks()

    def PMgen(self, PP, rid, Attr, Credential):
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])
        pm = ((PP['H'](rid, G1)) ** Attr['m1']) * ((PP['H'](rid, G1)) ** Credential['s'])
        # group.EndBenchmark()
        return pm #, group.GetGeneralBenchmarks()

    def Show1(self, PP, rid, Attr, Credential):
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])
        sigma_1 = dict()
        rt, r0 = group.random(ZR), group.random(ZR)
        sigma_1['R'] = ((PP['H'](rid, G1)) ** rt) * ((PP['H'](rid, G1)) ** r0)
        c = PP['H']([sigma_1['R']], ZR)
        sigma_1['zt'] = rt + c * Attr['m1']
        sigma_1['z0'] = r0 + c * Credential['s']
        # group.EndBenchmark()
        return sigma_1 #, group.GetGeneralBenchmarks()

    def Verify1(self, PP, sigma_1, Credential, pm, rid):
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])
        R = sigma_1['R']
        c = PP['H']([R], ZR)
        LHS = R * (pm ** c)
        RHS = (PP['H'](rid, G1) ** sigma_1['zt']) * (PP['H'](rid, G1) ** sigma_1['z0'])
        # group.EndBenchmark()
        return (LHS==RHS) #, group.GetGeneralBenchmarks()

    def Show2(self, PP, Credential, Attr, rid, Nh=1):  ## Nh >= 1 (hide at least one attribute: mt=m1)
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])   
        A = Credential['A']
        x = Credential['x']
        s = Credential['s']
        sigma_2 = dict()
        ### Step 1
        r, rr = group.random(ZR), group.random(ZR)
        # print(len(Attr))
        Attr_disclose = Attr.copy()
        # print(len(Attr_disclose))

        ### Step 2
        g1, h0 = PP['g1'], PP['h0']
        B = g1 * (h0 ** s)
        for i in range(1, 1 + PP['n']):
            B  = B * (PP['h'+str(i)] ** Attr['m'+str(i)])

        ### Step 3
        A_prime = A ** r
        sigma_2['A_prime'] = A_prime

        ### Step 4
        A_Bar = (A_prime ** (-x)) * (B ** r)
        sigma_2['A_Bar'] = A_Bar

        ### Step 5
        hp = PP['hp']
        d = (B ** r) * (hp ** rr)
        sigma_2['d'] = d

        ### Step 6 - 7
        alpha, beta = 1/r, -rr/r
        r_x, r_r, r_s, r_alpha, r_beta = group.random(ZR), group.random(ZR), group.random(ZR), group.random(ZR), group.random(ZR)


        ### Step 8
        r_i = []
        for i in range(1, Nh+1):
            r_i = r_i + [group.random(ZR)]
            del Attr_disclose['m'+str(i)]
        
        ### Step 9
        R1 = (A_prime ** (-r_x) ) * (hp ** r_r)
        # print('R1=', R1)

        ### Step 10
        R2 = (d ** r_alpha) * (hp ** (-r_beta)) * (h0 ** (-r_s))
        for i in range(1, Nh+1):
            # print(i)
            hi = PP['h'+str(i)]
            R2 = R2 * (hi ** (-r_i[i-1]) )
        # print('R2=', R2)

        ### Step 11
        R3 = ((PP['H'](rid, G1)) ** r_i[0]) * ((PP['H'](rid, G1)) ** r_s)
        sigma_2['R3'] = R3
        # print(type(rid))
        # R3 = PP['H'](rid, G1)

        ### Step 12
        c = PP['H']([A_prime, A_Bar, d, R1, R2, R3], ZR)
        sigma_2['c'] = c

        ### Step 13
        sigma_2['zx'] = r_x + c * x
        sigma_2['zr'] = r_r - c * rr
        sigma_2['zalpha'] = r_alpha + c * alpha
        sigma_2['zbeta']  = r_beta  - c * beta
        sigma_2['zs'] = r_s + c * s
        for i in range(1, Nh+1):
            sigma_2['z'+str(i)] = r_i[i-1] + c * Attr['m'+str(i)]
        # group.EndBenchmark()
        return sigma_2, Attr_disclose #, group.GetGeneralBenchmarks()

    def Verify2(self, PP, sigma_2, Attr_disclose, pm, rid, Nh):
        # group.StartBenchmark(["CpuTime", "RealTime", "Add", "Sub", "Mul", "Div", "Exp", "Pair", "Granular"])
        A_prime, A_Bar, d, c, R3= sigma_2['A_prime'], sigma_2['A_Bar'], sigma_2['d'], sigma_2['c'], sigma_2['R3']
        zx, zr, zs, zalpha, zbeta = sigma_2['zx'], sigma_2['zr'], sigma_2['zs'], sigma_2['zalpha'], sigma_2['zbeta']
        R1 = (A_prime ** (-zx)) * (PP['hp'] ** zr) * ((A_Bar / d) ** (-c))
        R2 = (d ** zalpha) * (PP['hp'] ** (-zbeta)) * (PP['h0'] ** (-zs)) 
        for i in range(1, Nh+1):
            R2 = R2 * (PP['h'+str(i)] ** (-sigma_2['z'+str(i)]))
        temp = PP['g1']
        for mi in Attr_disclose.keys():
            temp = temp * (PP['h'+mi[1:]] ** (Attr_disclose[mi] ))
        R2 = R2 * (temp ** (-c))

        e_l = pair(A_Bar, PP['g2'])
        e_r = pair(A_prime, PP['pk'])
        c_H  = PP['H']([A_prime, A_Bar, d, R1, R2, R3], ZR)

        eq3_l = (R3 * (pm**sigma_2['c']))
        eq3_r = ((PP['H'](rid, G1) ** sigma_2['z1']) * (PP['H'](rid, G1) ** sigma_2['zs']))
        # group.EndBenchmark()
        return (e_l==e_r)and(c==c_H)and(eq3_l==eq3_r) #, group.GetGeneralBenchmarks()

groupObj = PairingGroup('MNT224')
cred = Cred(groupObj)
# assert group.InitBenchmark(), "failed to initialize benchmark"
N = 10
pp, sk = cred.Setup(N)
buf = group.serialize(sk)
Attr = dict()
for i in range(1, N+1):
    Attr['m'+str(i)] = group.random(ZR)
Credential = cred.Issue(buf, pp, Attr)
rid = group.random(ZR)
pm = cred.PMgen(pp, rid, Attr, Credential)
sigma_1 = cred.Show1(pp, rid, Attr, Credential)
resVerif1 = cred.Verify1(pp, sigma_1, Credential, pm, rid)
print("verify1 result=", resVerif1)
Nh = 5
sigma_2, Attr_d = cred.Show2(pp, Credential, Attr, rid, Nh)
resVerif2 = cred.Verify2(pp, sigma_2, Attr_d, pm, rid, Nh)
print("verify2 result=", resVerif2)

