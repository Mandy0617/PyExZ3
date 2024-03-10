
#source: https://github.com/SRJaffry/GridWorld_Environment

class GridWorld_Env:
    def __init__(self, hor, ver):
        self.actions = ["left", "up", "right", "down"] # 0=Left, 1=Up, 2=right, 3=Down 
        self.x = 0
        self.y = 0
        self.MAX_HOR_VAL = hor-1
        self.MAX_VER_VAL = ver-1
        self.done = False
        self.episode_length = 0
        self.no_operation = False
        self.state_observation = [self.x, self.y]
        
    def reset(self):
        self.done = False
        self.episode_length = 0
        self.x, self.y = 0, 0
        self.state_observation = [self.x, self.y]
        return [self.x, self.y]
    
    def action_space(self):
        return self.actions
  
    def step(self, action):
        if self.state_observation == [self.MAX_HOR_VAL, self.MAX_VER_VAL]:
            self.done = True
            self.no_operation = False
            return np.array(self.state_observation), self.reward, self.done, self.no_operation, self.episode_length
        elif self.episode_length > 200:
            self.done = True
            self.no_operation = True
            return np.array(self.state_observation), self.reward, self.done, self.no_operation, self.episode_length
        
        self.action = action
        self.reward = self.get_reward()
        self.state_observation = self.take_action()
        self.episode_length += 1
        self.no_operation = False
        
        if(self.episode_length >= 200):
            self.done = True
        
        return np.array(self.state_observation), self.reward, self.done, self.no_operation, self.episode_length
    
    def get_reward(self):
        '''
        Return value : rewards
        Input argument. 
        '''
        if (self.x == 0 and self.action == "left") or (self.x == self.MAX_HOR_VAL and self.action == "right"):
            return -2
        elif (self.y == 0 and self.action == "down") or (self.y == self.MAX_VER_VAL and self.action == "up"):
            return -2
        elif (self.x, self.y) == (self.MAX_HOR_VAL-1, self.MAX_VER_VAL) and self.action == "right":
            return 0
        elif (self.x, self.y) == (self.MAX_HOR_VAL, self.MAX_VER_VAL-1) and self.action == "up":
            return 0
        else:
            return -1
    
    def take_action(self):
#         # Check Errors
#         if self.x < 0 or self.y < 0 or self.x > self.MAX_HOR_VAL or self.y > self.MAX_VER_VAL:
#             print("Error in getting the state. Please execute the reset() function")
#             return (np.inf*-1)
                
        if self.x > -1 and self.x <= self.MAX_HOR_VAL:
            if (self.action == "left" and self.x == 0) or (self.action == "right" and self.x == self.MAX_HOR_VAL):
                self.x = self.x
            elif(self.action == "left"):
                self.x -= 1
            elif(self.action == "right"):
                self.x += 1
            else:
                self.x = self.x
                
        if self.y > -1 and self.y <= self.MAX_VER_VAL:
            if (self.action == "down" and self.y == 0) or (self.action == "up" and self.y == self.MAX_HOR_VAL):
                self.y = self.y
            elif(self.action == "down"):
                self.y -= 1
            elif(self.action == "up"):
                self.y += 1
            else:
                self.y = self.y
                        
        return [self.x, self.y]
    

