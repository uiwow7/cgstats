import csv

#region boilerplate

TOURNS = {
    2024: ["Beagle Brawl 2024", "No Response 2024", "Black Hole Battles 2024", "Meteor Stop Off 2024", "Global Day Cup 2024", "Mallow Royale 2024", "Chaos Galaxy Invitational LCQ 2024"],
    "24Format": ["Beagle Brawl 2024", "No Response 2024", "Meteor Stop Off 2024", "Global Day Cup 2024", "Mallow Royale 2024", "Chaos Galaxy Invitational LCQ 2024"]
}

PLANETS = ["Sindian", "Sindell", "Gaios", "Palicium", "Sheos", "Rokah", "Teklar", "Baro"]

tf_ = {}
tourndata = {}

def deckFormat(deck: str):
    lists = deck.split("//")[1:]
    main = {}
    side = {}
    side_ = ""
    planet = ""
    main_ = "NONE"
    for item in lists:
        if "sideboard" in item:
            side_ = item.split("-1")[1][1:]
        if "deck-2" in item:
            side_ = item.split("-2")[1][1:]
        if "deck-1" in item:
            main_ = item.split("-1")[1]
        else:
            for p in PLANETS:
                if p in item:
                    planet = p
    #print(main_)
    main_ = main_.split("\n")[1:-2]
    for card in main_:
        main[card[2:].split("(")[0].rstrip()] = int(card[0])
    side_ = side_.split("\n")[1:-2]
    for card in side_:
        side[card[2:].split("(")[0].rstrip()] = int(card[0])
    return {"main": main, "side": side, "planet": planet}

# for year in TOURNS.values():
#     for tournament in year:
for tournament in TOURNS["24Format"]: # FORMAT GOES HERE!!!!!!!
    file =  open(f"C:/coding/cgstats/data/{tournament}.csv", "r")
    parsedFile = csv.DictReader(file)
    tf_[tournament] = parsedFile
    #print(tournament)
    for name, data in tf_.items():
        for line in data:
            tourndata[name + " - " + line["Discord username (with numbers)"]] = {"name": line["Discord username (with numbers)"], "deck": deckFormat(line["Deck (Paste Here)"]), "tourn": name}

#endregion

#region functions

def archetype(deck):
    tags = []
    if "The Undying Blue-Flame" and "Jakrah of the Blue-Flame Jar" and "Laji of the Blue-Flame Lamp" in deck["deck"]["main"]:
        tags.append("Blue Flames (Package)")
        if "Scoria Carrier" and "Zomatle" in deck["deck"]:
            tags.pop()
            tags.append("Pure Blue Flames")
    if "Shape Knight Lionel" and "Shape Knight Trongulon" and "Shape Knight Hexataur" and "Shape Knight Octorius" in deck["deck"]["main"]:
        tags.append("Shape Knights")
    if "The Magical Zarmelion Tree" and "Thorngabork" and "Gluuh - Beast of the Nightjungle" in deck:
        tags.append("Gaios Midrange")
    # TODO: Continue this; ask for help from secret/fish/other good people

def cardFrequencyMain(cardname):
    totaldecks = 0
    freq = 0
    for n, deck in tourndata.items():
        totaldecks += 1
        freq += int(cardname in deck["deck"]["main"])
    
    return freq/totaldecks

def cardFrequencySide(cardname):
    totaldecks = 0
    freq = 0
    for n, deck in tourndata.items():
        totaldecks += 1
        freq += int(cardname in deck["deck"]["side"])
    
    return freq/totaldecks

def mostFrequentMain():
    bestcards = ""
    bestperc = 0
    for name, deck in tourndata.items():
        for card in deck["deck"]["main"]:
            perc = cardFrequencyMain(card)
            if perc >= bestperc:
                bestperc = perc
                bestcard = card

    return bestcard

def topXMostFrequentMainCount(topX):
    allcards = {}

    for deck in tourndata.values():
        for card in deck["deck"]["main"]:
            if card in allcards:
                allcards[card] += deck["deck"]["main"][card]
            else:
                allcards[card] = deck["deck"]["main"][card]

    # print(allcards)
    res = dict(sorted(allcards.items(), key = lambda x: x[1], reverse = True)[:topX])

    return res

def topXMostFrequentMainDecks(topX):
    allcards = {}

    for deck in tourndata.values():
        for card in deck["deck"]["main"]:
            if card in allcards:
                allcards[card] += 1
            else:
                allcards[card] = 1

    #print(allcards)
    res = dict(sorted(allcards.items(), key = lambda x: x[1], reverse = True)[:topX])

    return res

#endregion

# print("BF:",            str(round(cardFrequencyMain("The Undying Blue-Flame"    ), 4) * 100) + "%")
# print("SK:",            str(round(cardFrequencyMain("Shape Knight Lionel"       ), 4) * 100) + "%")
# print("G Middy:",       str(round(cardFrequencyMain("The Magical Zamelion Tree" ), 4) * 100) + "%")
# print("Serp:",          str(round(cardFrequencyMain("Great Serpent of the Falls"), 4) * 100) + "%")
# print("Sindell Tempo:", str(round(cardFrequencyMain("Bone Ladder"               ), 4) * 100) + "%")
# print("Monument:",      str(round(cardFrequencySide("Monument To Creation"      ), 4) * 100) + "%")
# print("Squarn:",        str(round(cardFrequencySide("Shape Knight Squarn"       ), 4) * 100) + "%")
# print("Abandonment:",   str(round(cardFrequencySide("Abandonment"               ), 4) * 100) + "%")
# print("Lighthouse:",    str(round(cardFrequencySide("Deepspace Lightouse"       ), 4) * 100) + "%")
# print("Tramp:",         str(round(cardFrequencySide("Super Bouncy Trampoline"   ), 4) * 100) + "%")

#print(tourndata)
print(topXMostFrequentMainCount(50))
print(topXMostFrequentMainDecks(50))