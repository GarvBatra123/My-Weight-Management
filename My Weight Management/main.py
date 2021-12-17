import flask, datetime, calendar, json, os
from flask import render_template
from flask import request


# app=flask.Flask(__name__)
app = flask.Flask(__name__, static_url_path='/static')  



# @app.route("/te
# mplate")
# def template():
#     return render_template("template.html")

# THIS FUNCTION ALLOWS US TO USE PYTHON MODULES IN WEBPAGES THROUGH JINJA2 TEMPLATING
@app.context_processor
def handle_context():
    return dict(os=os)

@app.route("/")
@app.route("/home")
def homePage():
    return render_template("home.html")


@app.errorhandler(404)
def error404(e):
	return render_template("error_404.html")

@app.route("/createAcc-Pg1")
def loginPage1():      
    return render_template("createAcc-Pg1.html")


@app.route("/createAcc-Pg2", methods=["post"])
def loginPage2():
    keys, values = list((request.form).keys()), list((request.form).values()) #obtains the name of the input boxes in list `keys` | obtains the value in each input box entered by the user in list `values`
    if "" in values: #check if user entered email or not
        values[values.index("")] = "-" #f user does not enter email address, then display "NA" to confirm that email is not given by user   
    userData={}
    username = request.form['Username']
    userData[request.form['Username']] = request.form
    with open('userData.json', 'w') as datafile:
        json.dump(userData, datafile)       
    
    return render_template("createAcc-Pg2.html", keys=keys, values=values)


@app.route("/profile", methods=["post"]) #specifically to be used by `loginPage2()` because "createAcc-Pg2.html" is sending data to this page
@app.route("/profile") #this allows the profile page to be accessed from a page which does not submit data to this page
def profile_Page():
    
    # ----------------------------------------------------------------------------
    # PROCESSING USER DATA
    # Check if the user has created account or not, by checking if this "userData.json" file exists in the server storage
    # ------------------------------------------------------------------------------
    if os.path.exists("userData.json"):
        with open('userData.json') as datafile:
            userdata = json.load(datafile)

        # obtains the name of the input boxes in list `keys` | obtains the value in each input box entered by the user in list `values`
        keys, values = list((request.form).keys()), list((request.form).values())
        # returns the keys in the dict and stores it as a list
        username = list(userdata.keys())[0]
        for i in keys:
            userdata[username][i] = values[keys.index(i)]

        # obtains the name of the input boxes in list `keys` | obtains the value in each input box entered by the user in list `values`
        keys, values = list((userdata[username]).keys()), list(
            (userdata[username]).values())

        with open('userData.json', 'w') as datafile:
            json.dump(userdata, datafile)
        
        Fullname = f"{values[0]} {values[1]}"
        
        # ------------------------------------------------------------------------------
        # CHECKING FOR USER'S WEIGHTS
        if os.path.exists("UserWeightData.json"):
            with open("UserWeightData.json") as weightFile:
                weightData = json.load(weightFile)
            key = list(weightData.keys())[-1] #extract the latest weight readings made by the user
            weightData = weightData[key]
            
            Weight_values = [] #create an empty list to store the weight inputted by the user
            keys, values = list((weightData).keys()), list((weightData).values()) #obtains the name of the input boxes in list `keys` | obtains the value in each input box entered by the user in list `values`
            for i in keys:
                if "Dates" in i:
                    Date = str(values[keys.index(i)]).split("-") #removes the "-" in the dates, and stores the year, month, day as seperate strings in one list
                elif "Day_" in i: #check if the input box is for user weight
                    if "." in (values[keys.index(i)]): #check if user entered a decimal
                        Weight_values.append(float(values[keys.index(i)]))
                    else: #check if the user entered an int
                        Weight_values.append(int(values[keys.index(i)]))
                elif "goal" in i:  #check if the input box is for goal weight
                    if "." in (values[keys.index(i)]):  # check if user entered a decimal
                        goal = (float(values[keys.index(i)]))
                    else:  # check if the user entered an int
                        goal = int(values[keys.index(i)])
            averageWeight = float("{:.2f}".format(sum(Weight_values)/len(Weight_values))) #calculate Average weight of person
                
            # Date = Date.split("-") #troubleshoot
            # print("Date: ",Date)   #troubleshoot
            # print(type(Date))      #troubleshoot
            year = int(Date[0]) 
            month = int(Date[1])
            day = int(Date[2])
            # print(f"{year}, {month}, {day}") #troubleshoot
            Date = datetime.datetime(year, month, day) #obtains the date of given the year, month, and the day
            datelist = [Date.date()] #GETS the date without the time
            for i in range(4):
                Date += datetime.timedelta(days=1) #append the date in the list by 1 for each iteration: calculates the dates for the next 4 days -> Mon - Fri
                datelist.append(Date.date())
            
            daysInMonth = calendar.monthrange(year, month)[1] #calculate the numberof days in a given month
                                                            #using indexer [1] extracts the number of days because this function returns a tuple with (month, numberOfDays)
            daysLeft = daysInMonth-day #calculate the number of days left for the month to end
            weightToLosePerDay = "{:.2f}".format((averageWeight-goal)/daysLeft) #calculates how much weight the user must lose in order to achieve their target weight
                
            return render_template("profilePage.html", Fullname=Fullname, Weight_values=Weight_values, datelist=datelist, goal=goal,
                               averageWeight=averageWeight, daysLeft=daysLeft, weightToLosePerDay=weightToLosePerDay)
        else: 
            return render_template("profilePage.html", Fullname=Fullname)
            
    else:
        return render_template("PLEASE_CREATE_ACCOUNT.html")


@app.route("/obtainGraphData")
def obtainGraphData(): #this is used to obtain the weight data from the user
    return render_template("obtainGraphData.html")


@app.route("/renderGraph", methods = ["post"])
def renderGraphData():
    Weight_values = [] #create an empty list to store the weight inputted by the user
    keys, values = list((request.form).keys()), list((request.form).values()) #obtains the name of the input boxes in list `keys` | obtains the value in each input box entered by the user in list `values`
    for i in keys:
        if "Dates" in i:
            Date = str(values[keys.index(i)]).split("-") #removes the "-" in the dates, and stores the year, month, day as seperate strings in one list
        elif "Day_" in i: #check if the input box is for user weight
            if "." in (values[keys.index(i)]): #check if user entered a decimal
                Weight_values.append(float(values[keys.index(i)]))
            else: #check if the user entered an int
                Weight_values.append(int(values[keys.index(i)]))
        elif "goal" in i:  #check if the input box is for goal weight
            if "." in (values[keys.index(i)]):  # check if user entered a decimal
                goal = (float(values[keys.index(i)]))
            else:  # check if the user entered an int
                goal = int(values[keys.index(i)])
    averageWeight = float("{:.2f}".format(sum(Weight_values)/len(Weight_values))) #calculate Average weight of person
        
    # Date = Date.split("-") #troubleshoot
    # print("Date: ",Date)   #troubleshoot
    # print(type(Date))      #troubleshoot
    year = int(Date[0]) 
    month = int(Date[1])
    day = int(Date[2])
    # print(f"{year}, {month}, {day}") #troubleshoot
    Date = datetime.datetime(year, month, day) #obtains the date of given the year, month, and the day
    datelist = [Date.date()] #GETS the date without the time
    for i in range(4):
        Date += datetime.timedelta(days=1) #append the date in the list by 1 for each iteration: calculates the dates for the next 4 days -> Mon - Fri
        datelist.append(Date.date())
    
    daysInMonth = calendar.monthrange(year, month)[1] #calculate the numberof days in a given month
                                                      #using indexer [1] extracts the number of days because this function returns a tuple with (month, numberOfDays)
    daysLeft = daysInMonth-day #calculate the number of days left for the month to end
    weightToLosePerDay = "{:.2f}".format((averageWeight-goal)/daysLeft) #calculates how much weight the user must lose in order to achieve their target weight
    
    # CREATING JSON FILE
    if os.path.exists("UserWeightData.json"): #check if json file exists on the server or not
        with open("UserWeightData.json") as datafile:
            data=json.load(datafile) #load the current data in the json file onto this dict
    else: #if not, create an empty dict
        data={}
    
    data[request.form["weightDates"]] = request.form
    with open("UserWeightData.json", "w") as datafile:
        json.dump(data, datafile)
        
    
    return render_template("renderGraph.html", Weight_values=Weight_values, datelist=datelist, goal=goal, 
                           averageWeight=averageWeight, daysLeft=daysLeft, weightToLosePerDay = weightToLosePerDay)
 
if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449, debug=True)
    # app.run(host="0.0.0.0", port=8080, debug=True)