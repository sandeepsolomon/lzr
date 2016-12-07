import Navigation.prod.Fix as Fix

# ---------- constructor ----------
theFix = Fix.Fix()
sightingFilePath = theFix.setSightingFile("sightings.xml")
starFilePath = theFix.setStarFile("star.txt")
ariesFilePath = theFix.setAriesFile("aries.txt")
assumedLatitude = "N27d59.5"
assumedLongitude = "85d33.4"
approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)

