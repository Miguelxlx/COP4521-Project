def get_abbreviations():
    with open("other/abrv.txt", encoding='utf-8') as file:
        content = file.read().split("\n")
        
        team_dict = {}
        for team in content:
            team = team.split("-")
            abrv = team[0][0:3]
            full_name = team[1].lstrip()
            team_dict[full_name] = abrv

        return team_dict
        
    
