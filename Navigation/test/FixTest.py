import Navigation.prod.Fix as Fix

def main():
    # ---------- constructor ----------
    theFix = Fix.Fix()
    sightingFilePath = theFix.setSightingFile("sightings.xml")
    starFilePath = theFix.setStarFile('star.txt')
    ariesFilePath = theFix.setAriesFile('aries.txt')
    approximatePosition = theFix.getSightings()
if __name__ ==  "__main__":
    main()