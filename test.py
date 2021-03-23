import re
import random 

testcases = ["hello, My name is Bob Marley",
             "My favorite fruits are apples, mangos, and pears.",
             "I like vodka.", 
             "I don't like to drink gin."
             "I love the color purple.",
             "I like it when it is weak.",
             "I prefer strong drinks.",
             "This is my new favorite drink!",
             "I like apples and oranges",
             "I normally have oranges and pears in my drink.",
             "I mix oranges and pears",
             "Apples and oranges are my favorite",
             "I like apples and oranges because they are yellow",
             "I love you Bot10der"]


#ingredientList = ["apple", "banana", "pear", "mango", "pear", "cherry", "cherries"]
responseDict = {}


import json


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

class bartender:

    def __init__(self, responsePath, questionPath, cocktailPath, fruitPath, drinkPath):
        self.name = "BOT-10DER"
        self.responseFilePath = responsePath
        self.questionFilePath = questionPath
        self.cocktailList = readCocktailJson(cocktailPath)
        self.knownFruits = getTextFileInfo(fruitPath)
        self.knownDrinks = getTextFileInfo(drinkPath)
        self.questionKeys = self.getKeys()
        self.usedQuestions = []

    def getKeys(self):
        file = open(self.responseFilePath, "r")
        reading = True
        keys = []
        while reading:
            line = file.readline()[:-1]
            if "key:" in line:
                keys.append(line["key: ":])
            if line[:3] == "end":
                reading = False
        return keys
    
    def getResponse(self, path, key):
        file = open(path, "r")
        reading = True
        possibleResponses = []
        while reading:
            line = file.readline()[:-1]
            if "key:" in line and key in line:
                line = file.readline()[:-1]
                while "resp:" in line:
                    possibleResponses.append(line[len(" resp: "):])
                    line = file.readline()[:-1]
            if line[:3] == "end":
                reading = False
        
        return random.choice(possibleResponses)

    def readMessage(self, response):
        strippedResponse = re.sub(r'[^A-z0-9 ]+', "", response).lower()
        splitResponse = strippedResponse.split(" ")
        return splitResponse
    
    def getQuestions(self):
        questionChosen = random.randrange(len(self.questionKeys))
        self.usedQuestions.append(self.questionKeys[questionChosen])
        questionToAsk = getResponseText(self.questionKeys[questionChosen])
        return questionToAsk

    def welcome(self):
        print("Welcome, my name is {}".format(self.name)) # + introduction
        print(self.getResponse(self.responseFilePath, "name"))
        userName = input(">")
        if self.isValidName(userName):
            print(self.getResponse(self.responseFilePath, "greeting").format(userName))
        else:
            print("That is an interesting name {}.".format)

    def isValidName(self, userInput):
        nameRecPattern = "[A-z]{3,15}( [A-z]{3,15})*"  
        isNameReal = re.fullmatch(nameRecPattern, userInput)
    
        return bool(isNameReal)

    
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

    def chatLoop(self):
        


        
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
    ingredientMasterList = []
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
                        if ingredients["ingredient"] not in ingredientMasterList:
                            ingredientMasterList.append(ingredients["ingredient"])
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
    
    for i in ingredientMasterList:
        print(i)

    return cocktailList



print(getResponseText("welcome"))


# ingredientCheck = ["vodka", "rum", "pizza", "lemons", "lemon"]

# for check in ingredientCheck:
#     confirm = cocktailList[0].hasIngredient(check.lower())
#     print("{} -> {}".format(check, confirm))