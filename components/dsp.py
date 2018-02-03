

def forwarddiff(tlist, vallist):
    difflist = []
    for i in range(1, len(tlist)):
        difflist += [(vallist[i] - vallist[i - 1]) / (tlist[i] - tlist[i - 1])]
    return (tlist[1:], difflist)
