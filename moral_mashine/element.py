class Element:
    score_proc = {
        "red_light": -12,
        "ppl_index" : -12,
        "years" : 25,
        "anim" : -20,
        "woman_or_kid": 15
    }

    def __init__(self, red_light:bool, ppl_index:float, years:int|None, anim:bool, woman_or_kid:bool):
        self.red_light = red_light
        self.ppl_index = ppl_index # people_other / own ->
        """
        so if in 2 against 4 -> 4/2 -> 2 die for you 
        """
        self.years = years
        self.anim = anim
        self.woman_or_kid = woman_or_kid

        self.score = {x:0 for x in Element.score_proc.keys()}
        self.give_score()

        self.score_tot = sum(v for v in self.score.values())
    
    def give_score(self)->None:
        # red or green
        if self.red_light:
            self.score["red_light"] = Element.score_proc["red_light"]
     
        if self.anim:
            self.score["anim"] = Element.score_proc["anim"]
        else:
            # years only if not animal
            self.score["years"] = Element.score_proc["years"] * (100 - self.years) / 100

        if self.woman_or_kid:
            self.score["woman_or_kid"] = Element.score_proc["woman_or_kid"]

        # alive years
        self.score["ppl_index"] = Element.score_proc["ppl_index"] * (self.ppl_index - 1)

    def show_score_comps(self)->None:
        for (k,e) in self.score.items():
            print(f"{k:<15}:{e}")
        print("-----------------")

class Group:
    def __init__(self, *participants: Element):
        self.participants = participants

        self.group_score = sum(p.score_tot for p in self.participants)
        
        for p in self.participants:
            p.show_score_comps()

