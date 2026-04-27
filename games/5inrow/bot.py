from typing import Dict



class Bot:
    def __init__(self):
        self.eval_map: Dict[tuple[int,int],float] = {}
        self.state_map: Dict[tuple[int,int], None|int] = {}

        self.interest_zone_dist = 1

    def count_around(self,pos:tuple[int,int], distance_from_pos:int, count_at_pos:bool)->tuple[int,int]:
        """return: enemy, own

        """
        d = distance_from_pos
        enemy, own = 0,0

        for dy in range(-d, d+1):
            for dx in range(-d, d+1):
                x,y = pos[0]+dx,pos[1]+dy

                try:
                    if dx == 0 and dy == 0:
                        if count_at_pos:

                            match self.state_map[(x, y)]:
                                case 0:
                                    enemy += 1
                                case 1:
                                    own += 1

                    else:
                        match self.state_map[(x, y)]:
                            case 0:
                                enemy+=1
                            case 1:
                                own+=1
                except KeyError:
                    pass

        return enemy,own

    def interest_zone(self):
        for pos, field in self.state_map.items():
            print(f"looking around {pos}")
            if max(self.count_around(pos,self.interest_zone_dist,count_at_pos=False)) > 0:

                d = self.interest_zone_dist
                for dy in range(-d, d + 1):
                    for dx in range(-d, d + 1):
                        print(dx, dy)
                        x, y = pos[0] + dx, pos[1] + dy
                        print(x,y)
                        # check is pos is valid
                        if (x,y) in self.state_map.keys():
                            self.eval_map[(x, y)] = 0.0


    def calculate_eval_map(self, state_map: dict[tuple[int,int], None|int])->None:
        #update state
        self.state_map = state_map
        #reset eval_map
        self.eval_map = {}

        # calculate interest zone
        self.interest_zone()

    def best_move(self)->tuple[int,int]:
        self.eval_map = dict(
            sorted(self.eval_map.items(), key=lambda i: i[1], reverse=True)
        )

        # return first the x, y pos with highest score
        return next(iter(self.eval_map))



