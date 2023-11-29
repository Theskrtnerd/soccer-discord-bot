import requests
import random

def get_transfer_history(player_id):
  url = "https://transfermarket.p.rapidapi.com/players/get-transfer-history"
  querystring = {"id":str(player_id)}
  headers = {
	"X-RapidAPI-Key": "040cf78da3mshabe8ff16ad12f2dp185c5ejsnf353092b997b",
	"X-RapidAPI-Host": "transfermarket.p.rapidapi.com"}
  response = requests.request("GET", url, headers=headers, params=querystring).json()["transferHistory"]
  history_string = ""
  for i in range(len(response)-1,-1,-1):
    transfer = response[i]
    if transfer["loan"] == "ist":
      history_string += "*"
    history_string = history_string + transfer["newClubName"] +" - "+ transfer["date"]+"\n"
  return history_string

def get_league_teams_ids(league_id):
  url = "https://transfermarket.p.rapidapi.com/competitions/get-table"
  querystring = {"id":league_id,"seasonID":"2022"}
  headers = {
  	"X-RapidAPI-Key": "040cf78da3mshabe8ff16ad12f2dp185c5ejsnf353092b997b",
  	"X-RapidAPI-Host": "transfermarket.p.rapidapi.com"}
  response = requests.request("GET", url, headers=headers, params=querystring).json()["table"]
  for team in response:
    print(f'{team["id"]}: {team["clubName"]}')

def get_squad_players_ids(club_id):
  url = "https://transfermarket.p.rapidapi.com/clubs/get-squad"
  querystring = {"id":str(club_id)}
  headers = {
	"X-RapidAPI-Key": "040cf78da3mshabe8ff16ad12f2dp185c5ejsnf353092b997b",
	"X-RapidAPI-Host": "transfermarket.p.rapidapi.com"}
  response = requests.request("GET", url, headers=headers, params=querystring).json()["squad"]
  list_of_players={player["id"]: player["name"] for player in response}
  return list_of_players


clubs = {"mu": 985,"ars": 11, "mci":281, "liv":31, "chel": 631, "tots": 148, "bayern":27, "dort": 16, "barca": 131, "real": 418, "atm":13, "lei":1003, "westham":379,"ac":5, "inter":46,"juve":506,"psg":583}

def rtp():
  club_id = random.choice(list(clubs.values()))
  list_of_players = get_squad_players_ids(club_id)
  player_id = random.choice(list(list_of_players.keys()))
  return[list_of_players[player_id], get_transfer_history(player_id)]