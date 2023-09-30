import requests, json, slack
from datetime import datetime, timedelta

start_date = datetime.now()
end_date = start_date + timedelta(days=9)

days = []
current_date = start_date

while current_date <= end_date:
    days.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)

print(days)

token = '*** TOKEN ***'
databaseID ="d65faac0b020427181c364f3dd4ff401"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}
client = slack.WebClient(token="*** TOKEN ***")
table_emoji = {
    "Chimie": ":scientist:",
    "Physique": ":astronaut:",
    "ES PC": ":astronaut:",
    "SVT" : ":dna:",
    "Histoire": ":military_helmet:",
    "Russe" : ":nesting_dolls:",
    "Philo": ":brain:",
    "Anglais": ":teapot:",
    "Espagnol" : ":dancer:",
    "Géographie" : ":earth_africa:",
    "EMC" : ":scales:",
    "Maths" : ":1234:",
    "Maths Exp" : ":pill::1234:"
}


# after : > 
# before : <
query="""{
  "filter": {
    "property": "Date",
    "date": {
        "after": "%s"
   }
  }
}""" % start_date.strftime("%Y-%m-%d")
def getHomework():

    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
    res = requests.request("POST", readUrl, headers=headers, data=query)

    data = res.json()
    data_elements = data["results"]
    full_hw = []

    for e in data_elements:
        full_hw.append({
            "url": e["url"],
            "date": e["properties"]["Date"]["date"]["start"],
            "matiere": e["properties"]["Matière"]["select"]["name"],
            "titre": e["properties"]["Titre"]["title"][0]["text"]["content"],
            "type": e["properties"]["Type"]["select"]["name"]
        })
    
    return full_hw

def segregation(full_hw):
    print(full_hw)
    segregated_hw = {
        "DS": list(filter(lambda x: x["type"]=="DS", full_hw)),
        "DM": list(filter(lambda x: x["type"]=="DM", full_hw)),
        "EX": list(filter(lambda x: x["type"]=="Exercices", full_hw))
    }
    days_segregation = {
        "DS": [list(filter(lambda x: x["date"]==i, segregated_hw["DS"])) for i in days],
        "DM": [list(filter(lambda x: x["date"]==i, segregated_hw["DM"])) for i in days],
        "EX": [list(filter(lambda x: x["date"]==i, segregated_hw["EX"])) for i in days],
    }


    days_segregation = {
        "DS": list(filter(None, days_segregation["DS"])),
        "DM": list(filter(None, days_segregation["DM"])),
        "EX": list(filter(None, days_segregation["EX"])),
    }

    return days_segregation

def reverse_date(date):
    date = date[-2:]+"-"+date[:2]
    return date

def struct_by_date(segregated, msg):
    for day in segregated:
        msg+= "\n\n • _Pour le *%s*_," % reverse_date(day[0]["date"][-5:])
        for e in day:
            msg += "\n%s*%s*: %s <%s|Accès à la page>" % (table_emoji[e["matiere"]], e["matiere"], e["titre"], e["url"])
    return msg

def send_rappel(days_segregation):
    msg="Devoirs pour la semaine prochaine,"

    if days_segregation["DS"]!=[]:
        msg += "\n\nDS prévu(s) :"
        msg = struct_by_date(days_segregation["DS"], msg)
        
    if days_segregation["DM"]!=[]:
        msg += "\n\nDM à rendre :"
        msg = struct_by_date(days_segregation["DM"], msg)

    if days_segregation["EX"]!=[]:
        msg += "\n\nExercices :"
        msg = struct_by_date(days_segregation["EX"], msg)
    
    msg+= "\n\nBon Courrage! :smile:"
    client.chat_postMessage(channel="#rappel-devoirs", text=msg)



if __name__ == "__main__":
    send_rappel(segregation(getHomework()))
