import Navigation.prod.Fix as Fix

def main():
    # ---------- constructor ----------
    theFix = Fix.Fix()
    theFix.setSightingFile("sightings.xml")
    approximatePosition = theFix.getSightings()

if __name__ ==  "__main__":
    main()