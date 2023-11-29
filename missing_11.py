from requests_html import HTMLSession
import random
import nextcord
from unidecode import unidecode

def get_player_name(player_link):
  url = f"https://www.transfermarkt.com{player_link}"
  session = HTMLSession()
  r = session.get(url)
  player_name = r.html.find('.data-header__headline-wrapper', first=True).text.replace("#", "").replace("\n", " ")
  player_name = ''.join([i for i in player_name if not i.isdigit()])
  return player_name


#get_matches_from_team_and_year
def get_matches(team_id, year):
    url = f"https://www.transfermarkt.com/manchester-united/spielplandatum/verein/{team_id}/plus/0?saison_id={year}&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-"
    session = HTMLSession()
    r = session.get(url)
    matches = r.html.find('.ergebnis-link')
    matches_ids = [
        int(match.attrs["href"].split("/")[-1]) for match in matches
    ]
    return matches_ids

#get_match_info_from_match
def get_match_info(match_id, my_team_id):
  url = f"https://www.transfermarkt.com/spielbericht/index/spielbericht/{match_id}"
  session = HTMLSession()
  r = session.get(url)
  match_result = r.html.find('.sb-endstand', first=True).text.split("\n")[0]
  match_date = r.html.find('.sb-datum',first=True).find('a')
  for element in match_date:
    if 'href' in element.attrs:
      link = element.attrs["href"]
      if 'datum' in link.split("/")[-2]:
        match_date = link.split("/")[-1]
        break
  home_team_name = r.html.find('.sb-heim',first=True).find('a',first=True).attrs["title"]
  home_team_id =  int(r.html.find('.sb-heim',first=True).find('a',first=True).attrs["href"].split("/")[4])
  away_team_name = r.html.find('.sb-gast',first=True).find('a',first=True).attrs["title"]
  match_result = home_team_name + " " + match_result + " " + away_team_name
  two_teams_players = r.html.find('.aufstellung-spieler-container')
  two_teams_players_list = []
  for player in two_teams_players:
    if '.' not in player.text.split("\n")[1]:
      two_teams_players_list.append(player.text.split("\n")[1])
    else:
      player_link = player.find('a', first=True).attrs["href"]
      player_name = get_player_name(player_link)
      two_teams_players_list.append(player_name)
  home_team_lu = two_teams_players_list[0:11]
  away_team_lu = two_teams_players_list[11:22]

  try:
    home_f= r.html.find('.aufstellung-unterueberschrift')[0].text.split()[2].split("-")
    home_f = [int(home_f[0]),sum(int(home_f[i]) for i in range(1,len(home_f)-1)),int(home_f[-1])]
    away_f= r.html.find('.aufstellung-unterueberschrift')[1].text.split()[2].split("-")
    away_f = [int(away_f[0]),sum(int(away_f[i]) for i in range(1,len(away_f)-1)),int(away_f[-1])]

  except:
    try:
      home_f= r.html.find('.aufstellung-unterueberschrift-mannschaft')[0].text.split()[2].split("-")
      home_f = [int(home_f[0]),sum(int(home_f[i]) for i in range(1,len(home_f)-1)),int(home_f[-1])]
      away_f= r.html.find('.aufstellung-unterueberschrift')[1].text.split()[2].split("-")
      away_f = [int(away_f[0]),sum(int(away_f[i]) for i in range(1,len(away_f)-1)),int(away_f[-1])]
    except:
      return "Error!"
  
  teams_fs = [home_f, away_f]
  teams_lu = [home_team_lu, away_team_lu]
  teams_names = [home_team_name, away_team_name]
  if my_team_id == home_team_id:
    team_index = 0
  else:
    team_index = 1
  guess_team_name = teams_names[team_index]
  guess_team_lu = teams_lu[team_index]
  guess_team_f = teams_fs[team_index]
  guess_gk = [guess_team_lu[0]]
  guess_df = guess_team_lu[1:(1+guess_team_f[0])]
  guess_mf = guess_team_lu[(1+guess_team_f[0]):(1+guess_team_f[0]+guess_team_f[1])]
  guess_fw = guess_team_lu[(1+guess_team_f[0]+guess_team_f[1]):11]
  question_string = f"Can you guess the players of {guess_team_name} in this Missing 11?"
  guess_f = '-'.join([str(i) for i in guess_team_f])
  return [question_string, match_result, match_date, guess_f, guess_team_lu, guess_gk, guess_df, guess_mf, guess_fw]


clubs = {
  #epl
  "mu": 985,
  "ars": 11,
  "mci": 281,
  "liv": 31,
  "chel": 631,
  "tots": 148,
  # "new": -1,
  # "leiceister": -1,


  #bundesliga
  "bayern": 27,
  "dort": 16,
  # "leipzig": -1,

  #la liga
  "barca": 131,
  "real": 418,
  "atm": 13,


  #serie a
  "ac": 5,
  "inter": 46,
  "juve": 506,
  # "as roma": -1,
  # "lazio": -1,

  #ligue 1
  "psg": 583,

  #others
  # "ajax": -1,

  #international
  # "argentina": -1,
  # "brazil": -1,
  # "netherlands": -1,
  # "italy": -1,
  # "spain": -1,
  # "england": -1,
  # "portugal": -1,
  # "belgium": -1,
  # "france": -1,
  # "germany": -1
}

def create_game():
    team_id = random.choice(list(clubs.values()))
    year = random.randint(2000, 2021)
    matches_ids = get_matches(team_id, year)
    check = True
    while check:
      check = False
      match_id = random.choice(matches_ids)
      if get_match_info(match_id, team_id) == "Error!":
        check = True
      else:
        bruh = get_match_info(match_id, team_id)
    return bruh

def create_embed(title, result,date,formation,gk_done=[],df_done=[],mf_done=[],fw_done=[]):
  embed=nextcord.Embed(title=title, color=0x15003d)
  embed.add_field(name="Match Result", value=str("""```fix\n""")+result+str("""```"""), inline=False)
  embed.add_field(name="Match Date", value=str("""```fix\n""")+date+str("""```"""), inline=True)
  embed.add_field(name="Team Formation", value=str("""```fix\n""")+formation+str("""```"""), inline=True)
  if gk_done == []:
    gk_done = ["__"]
  if df_done == []:
    df_done = ["__"]
  if mf_done == []:
    mf_done = ["__"]
  if fw_done == []:
    fw_done = ["__"]
  embed.add_field(name="GK", value=str("""```fix\n""")+"\n".join(gk_done)+str("""```"""), inline=True)
  embed.add_field(name="DF", value=str("""```fix\n""")+"\n".join(df_done)+str("""```"""), inline=True)
  embed.add_field(name="MF", value=str("""```fix\n""")+"\n".join(mf_done)+str("""```"""), inline=True)
  embed.add_field(name="FW", value=str("""```fix\n""")+"\n".join(fw_done)+str("""```"""), inline=True)
  return embed
