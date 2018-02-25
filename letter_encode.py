import pprint
alpha = "qwertyuiopasdfghjklzxcvbnm1234567890\n-+()*`"
symbols = ["up","down","left","right","cross","circle","triangle"]
everything = {}
i = 0
for l in symbols:
    for k in symbols:
        try:
            everything[(l,k)] = alpha[i]
            i += 1
        except:
            break

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(everything)

