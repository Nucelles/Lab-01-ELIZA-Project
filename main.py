import re
import json
import random

confirmationDict = {"yes":["yes yep yeah love okay sure like ".split()],
                    "no":["no not nope".split()]}
responseDict = {}
questionKeys = []
usedQuestions = []

def getTextFileInfo(path):
    file = open(path, "r")
    reading = True
    fileList = []

    while reading:
        line = file.readline()[:-1]
        if line != "end":
            fileList.append(line.lower())
        else:
            reading = False
    
    return fileList
            
class cocktail:
    
    def __init__(self, name, ingredients, prep, garnish = None):
        self.amount = 0
        self.ingredientList = []
        self.quantities = {}
        self.garnish = ""

        self.name = name
        self.prep = prep
        for ing in ingredients:
            try:
                self.amount += ing[1]
                self.ingredientList.append(ing[0])
                self.quantities.update({ing[0]:ing[1]})
            except:
                self.ingredientList.append(ing)
        if len(self.garnish) == 0:
            self.garnish = garnish

    def printCocktail(self):
        print("--{}--".format(self.name))
        print("Ingredients:")
        for ing in self.ingredientList:
            try:
                print("{}, {}cl".format(ing, self.quantities[ing]))
            except:
                print("{}".format(ing))
        print("Preperation:\n{}".format(self.prep))
        if self.garnish != None:
            print("Garnish with {}".format(self.garnish))

    def hasIngredient(self, ingredient):
        allIngredients = [x for x in [y.split() for y in self.ingredientList + [self.garnish]]]
        for cocktailIngredient in allIngredients:
            lowercaseCocktailIngredient = [x.lower() for x in cocktailIngredient]
            if ingredient in lowercaseCocktailIngredient:
                return True
            elif ingredient[:-1] in lowercaseCocktailIngredient:
                return True
        return False

def readCocktailJson(path):
    with open('cocktails.json', encoding="utf8") as f:
        data = json.load(f)

    cocktailList = []
    for i in range(77):
        ctName = ""
        ctIngredients = []
        ctprep = ""
        ctGarnish = ""

        for key, value in data[i].items():
            if key == "name":
                ctName = value
            elif key == "ingredients":
                for ingredients in value:
                    try:
                        ingredient = [ingredients["ingredient"], ingredients["amount"]]
                        if ingredient[0] == "Syrup":
                            ingredient = ingredients["label"] + " syrup"
                        ctIngredients.append(ingredient)
                    except:
                        ctIngredients.append(ingredients["special"])
            elif key == "garnish":
                ctGarnish = value
            elif key == "preparation":
                ctprep = value
        
        if len(ctGarnish) != 0:
            cocktailList.append(cocktail(ctName, ctIngredients, ctprep, ctGarnish))
        else:
            cocktailList.append(cocktail(ctName, ctIngredients, ctprep))
    return cocktailList

def isValidName(userInput):
    nameRecPattern = "[A-z]{3,15}( [A-z]{3,15})*"  
    isNameReal = re.fullmatch(nameRecPattern, userInput)
    
    return bool(isNameReal)

def getResponse(key): 
    #print(key)
    chosenResponse = random.choice(responseDict[key])
    return chosenResponse

def readResponseTxt(path):
    keyResponses = []
    currKey = None
    file = open(path, "r")
    reading = True
    while reading:
        line = file.readline()[:-1]
        if line[:3] == "key":
            if currKey != None:
                responseDict.update({currKey:keyResponses})
                questionKeys.append(currKey)
                keyResponses = []
            currKey = line[len("key: "):]
        elif line == "end":
            responseDict.update({currKey:keyResponses})
            questionKeys.append(currKey)
            keyResponses = []
            reading = False
        else:
            keyResponses.append(line[len(" response: "):])

def readMessage(response):
    strippedResponse = re.sub(r'[^A-z0-9 ]+', "", response).lower()
    splitResponse = strippedResponse.split(" ")
    return splitResponse

def checkConfirmation(userResponse):
    confirmationDict = {"yes":["yes yep yeah love okay sure like ".split()],
                    "no":["no not nope".split()]} 
    splitResponse = readMessage(userResponse)

    while True:
        yesOcc = len(set(confirmationDict["yes"]).intersection(splitResponse))
        noOcc = len(set(confirmationDict["no"]).intersection(splitResponse)) 
                     
        if yesOcc > 0 and noOcc == 0:
            return True
        elif yesOcc == 0 and noOcc > 0:
            return False
        else:
            print("Could you repeat that I couldn't quite understand")
            splitResponse = readMessage(input(">"))

def getQuestion():
    questionChosen = random.randrange(len(questionKeys))
    usedQuestions.append(questionKeys[questionChosen])
    questionToAsk = getResponse(questionKeys[questionChosen])
    return questionToAsk

def welcome():
    name = "BOT 10-DER"
    print("Welcome, my name is {}".format(name)) # + introduction
    print(getResponse("name"))
    userName = input(">")
    if isValidName(userName):
        print(getResponse("greeting").format(userName))
    else:
        print("That is an interesting name {}.".format)

def chatLoop(userName):
    loopNum = 0
    talking = True
    userLikes = []
    userDislikes = []
    possibleDrinks = readCocktailJson("cocktails.json")
    welcome()

    while talking:
        print(getQuestion)   

        if loopNum >= 2:
            print("Since I've gotten to know you I can also suprise you with a recommendation. Would you like that?")
            #response = input(">")

    return None

readResponseTxt("responses.txt")
print(responseDict)
print(questionKeys)
print(getQuestion())
print(usedQuestions)
