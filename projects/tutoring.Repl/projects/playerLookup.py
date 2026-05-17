from sportsreference.mlb.roster import Player , Roster



def LookupPlayer():
  #looks up a player
  lookup_player = Player('altuvjo01')
  print(lookup_player.name)  # Prints 'José Altuve'
  print(lookup_player.hits)  # Prints Altuve's career hits total
  # Prints a Pandas DataFrame of all relevant stats per season for Altuve
  print(lookup_player.dataframe)




def lookupTeam():
  #looks up a team
  lookup_team = Roster('HOU', slim = True)
  for player in lookup_team.players:
    print(player)






lookupTeam()