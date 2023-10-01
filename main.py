import requests, json, slack, random
from datetime import datetime, timedelta

start_date = datetime.now()
end_date = start_date + timedelta(days=9)

days = []
current_date = start_date

while current_date <= end_date:
    days.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)

with open("auth/notion", "r") as notion_f, open("auth/slack-bot", "r") as bot_f, open("auth/slack-user") as user_f:
    notion_token = notion_f.read()
    user_token = user_f.read()
    bot_token = bot_f.read()

#Notion
databaseID ="d65faac0b020427181c364f3dd4ff401"
headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

#Slack
channel_id = "C05UEQC8S6A" # dev : C05V1309DCZ, main : C05UEQC8S6A
client_user = slack.WebClient(token=user_token)
client_bot = slack.WebClient(token=bot_token)

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
    "Maths Exp" : ":pill:"
}

phrases_motivantes = [
    "Allez, vous pouvez le faire! 💪",
    "Révisez avec passion! 🔥",
    "Foncez vers le succès! 🚀",
    "Devoirs? À vous de jouer! 📚",
    "Révisez, triomphez, répétez! 📝",
    "Devoirs terminés, sourire activé! 😊",
    "Rien n'arrête un étudiant motivé! 🎓",
    "Réussissez avec détermination! 💫",
    "Chaque effort compte, allez-y! 💯",
    "Soyez curieux, apprenez toujours! 🌟",
    "Devoirs faits, superhéros reposé! 🦸‍♂️",
    "La réussite vous attend, foncez! 🏆",
    "Petits pas, grandes victoires! 👣",
    "Étudiez dur, rêvez grand! 🌌",
    "Votre avenir commence maintenant! 🌈",
    "La persévérance mène à l'excellence! 🌟",
    "Visez haut, atteignez loin! 🚀",
    "Révisez, ça vaut le coup! 💡",
    "C'est l'heure du cerveau! 🧠",
    "Devoirs = Pouvoir! 💪",
    "Devoirs, défiez-vous! 🎯",
    "Révisez avec un clin d'œil! 😉",
    "Devoirs: votre super-pouvoir! 💥",
    "Luttez avec les devoirs! 🥋",
    "Révisez, c'est magique! 🎩",
    "Soyez génial, révisez maintenant! 👍",
    "Devoirs = Victoire! 🏆",
    "Révisez en dansant! 💃",
    "Devoirs: un jeu d'enfant! 🎮",
    "Devoirs? Défiez-les avec un sourire! 😊",
    "Révisez comme si le café était en danger! ☕️",
    "Devoirs: domptez-les comme un pro! 🎩",
    "Révisez aujourd'hui, brillez demain! ✨",
    "Les devoirs sont votre ticket vers le succès! 🎫",
    "Devoirs = Défi accepté! 💪",
    "Devoirs: battez-les avec votre intelligence! 🧠",
]

debut_messages = [
    "Hello les amis! 😊",
    "Hey les étudiants! 📚",
    "Yo la team! 👋",
    "Salut les cerveaux! 🧠",
    "Hello tout le monde! 🌟",
    "Coucou les apprentis! 🎓",
    "Salut les bosseurs! 💪",
    "Hello les génies! 🚀",
    "Hey les ptits potes! 😄",
    "Coucou la gang! 🤗",
    "Bonjour les cracks! 👍",
    "Salut les travailleurs! 💼",
    "Hello la fam! ❤️",
    "Yo les champions! 🏆",
    "Salut les apprenants! 📖",
    "Hello les têtes pensantes! 🤔",
    "Hey la famille! 👨‍👩‍👧‍👦"
]

introduction_messages = [
    "Les devoirs attendent, mettez-vous au travail! 💪",
    "Révisons ensemble pour briller demain! 📚",
    "Temps de se plonger dans les devoirs! 🎓",
    "Révisez avec passion, succès assuré! 🔥",
    "Les devoirs nous attendent, commençons! 📝",
    "Prêts pour une séance productive? 💼",
    "Chaussez vos lunettes, c'est l'heure! 🤓",
    "Devoirs appellent, ne les faites pas attendre! ⏳",
    "Sortez vos stylos, c'est parti! ✒️",
    "Révisons ensemble pour un avenir brillant! 🌟",
    "Les devoirs nous défient, relevons-les! 💪",
    "Révisez avec enthousiasme, réussite assurée! 😊",
    "Devoirs aujourd'hui, succès demain! 🌈",
    "Révisez bien, rêvez en grand! 🚀",
    "Prêts à conquérir les devoirs? 📚",
    "Chaussez vos baskets, c'est l'heure! 👟",
    "Devoirs nous appellent, répondons! 📖",
    "Sortez vos cahiers, c'est parti! 📔",
    "Révisons ensemble pour un avenir meilleur! 🌱",
    "Les devoirs nous inspirent, commençons! 💡",
    "Souriez, les devoirs sont là! 😊",
]


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
        msg+= "\n • _Pour le *%s*_," % reverse_date(day[0]["date"][-5:])
        for e in day:
            msg += "\n%s *%s* %s: %s <%s|Accès à la page>" % (table_emoji[e["matiere"]], e["matiere"], table_emoji[e["matiere"]], e["titre"], e["url"])
        msg+="\n"
    return msg

def clear_msg():
    messages = client_bot.conversations_history(channel=channel_id)["messages"]
    for msg in messages:
        timestamp = msg["ts"]
        client_user.chat_delete(channel=channel_id, ts=timestamp)

def send_rappel(days_segregation):
    clear_msg()
    msg="Devoirs pour la semaine prochaine,"

    if days_segregation["DS"]!=[]:
        msg += "\n*DS prévu(s) :*"
        msg = struct_by_date(days_segregation["DS"], msg)
        
    if days_segregation["DM"]!=[]:
        msg += "\n*DM à rendre :*"
        msg = struct_by_date(days_segregation["DM"], msg)

    if days_segregation["EX"]!=[]:
        msg += "\n*Exercices :*"
        msg = struct_by_date(days_segregation["EX"], msg)
    
    msg+= "\n" + phrases_motivantes[random.randint(0,len(phrases_motivantes)-1)]
    client_bot.chat_postMessage(channel=channel_id, text=msg)



if __name__ == "__main__":
    send_rappel(segregation(getHomework()))