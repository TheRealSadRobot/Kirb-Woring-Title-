import gameLib
def Copy(obj):

    obj.inhalingnum = 0
    for enemy in obj.objlist:
        if enemy.inhaled == True:
            obj.inhalingnum += 1
            
    #print(obj.inhalingnum)
    if obj.firePressed == False:
        if obj.crouching == False:
            if (obj.mouthfull == 0):# or obj.inhalingnum > 0):
                obj.floating = False
                if obj.attack == False:
                    obj.playAnimationOnce("InhaleStart","Inhale")
                else:
                    obj.playAnimation("Inhale")
                obj.attack = True
            elif obj.mouthfull > 0:
                #print(type(obj.inmouth).__name__)
                if type(obj.inmouth).__name__ == "Enemy":
                    if obj.dir == "left":
                        star = gameLib.Attack("Star","None",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,100,[-4,0,1],obj,"line")
                        obj.inmouth = None
                    else:
                        star = gameLib.Attack("Star","None",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,100,[4,0,1],obj,"line")
                        obj.inmouth = None
                if type(obj.inmouth).__name__ == "Ball":
                    obj.inmouth.mouthed = None
                    #print("Young Dippa")
                    if obj.dir == "left":
                        obj.inmouth.speed = [-4,0]
                        obj.inmouth.location[0] -= 18
                        obj.inmouth.location[1] -= 3
                    else:
                        obj.inmouth.speed = [4,0]
                        obj.inmouth.location[0] += 18
                        obj.inmouth.location[1] -= 3
                    obj.inmouth = None
                obj.mouthfull = 0
                obj.attack = False
                obj.playAnimationOnce("Spit","Idle")
            else:
                if obj.speed == 0:
                    obj.playAnimation("Full")
                #obj.attack = False
                """if obj.attack == False:
                    obj.mouthfull = False
                    obj.startInhale = True"""
        else:
            obj.attack = False
    
    if obj.attack == True and obj.mouthfull == 0:
        for enemy in obj.collide:
            if enemy != None and enemy.mouthed == None:# and type(enemy).__name__ != "NPC":
                if obj.dir == "right" and enemy.right[0] > obj.right[0]:
                    obj.mouthfull += 1
                    obj.inmouth = enemy
                    if type(enemy).__name__ == "Enemy":
                        enemy.Kill()
                        obj.collide.remove(enemy)
                    else:
                        enemy.mouthed = obj
                        obj.collide.remove(enemy)
                elif obj.dir == "left" and enemy.left[0] < obj.left[0]:
                    obj.mouthfull += 1
                    obj.inmouth = enemy
                    if type(enemy).__name__ == "Enemy":
                        enemy.Kill()
                        obj.collide.remove(enemy)
                    else:
                        enemy.mouthed = obj
                        obj.collide.remove(enemy)
                else:
                    if type(enemy).__name__ == "Enemy":
                        obj.Kill()
            #else:
                #self.inmouth = None
    #print(obj.inhalingnum)
    if obj.attack == True and (obj.mouthfull == 0 or obj.inhalingnum > 0):
        for enemy in obj.objlist:
            if type(enemy).__name__ != "NPC":
                if obj.dir == "right" and (enemy.location[0]-obj.right[0]) <= 48 and (enemy.location[0]-obj.right[0]) > 0:
                    if (obj.top[1]-enemy.location[1]-enemy.spriteSize[1]) <= 24 and (obj.bottom[1]-enemy.location[1]) > -24:
                        #print(f"RIGHT: Suck in {enemy.pallateName}")
                        if enemy.left[1] > obj.right[1]:
                            #enemy.location[1] += (enemy.location[1] - obj.bottom[1])/5
                            enemy.speed[1] -= 1
                        elif enemy.left[1] < obj.right[1]:
                            #enemy.location[1] -= (enemy.location[1] - obj.bottom[1])/5
                            enemy.speed[1] += 1
                        else:
                            enemy.speed[1] = 0
                        if enemy.left[0] > obj.right[0]:
                            #enemy.location[0] -= (enemy.location[0] - obj.right[0])/5
                            enemy.speed[0] -= 1
                elif obj.dir == "left" and (obj.left[0]-enemy.right[0]) <= 48 and (obj.left[0]-enemy.right[0]) > 0:
                    if (obj.top[1]-enemy.location[1]-enemy.spriteSize[1]) <= 24 and (obj.bottom[1]-enemy.location[1]) > -24:
                        #print(f"LEFT: Suck in {enemy.pallateName}")
                        if enemy.right[1] > obj.left[1]:
                            #enemy.location[1] += (enemy.location[1] - obj.bottom[1])/5
                            enemy.speed[1] -= 2
                        elif enemy.right[1] < obj.left[1]:
                            #enemy.location[1] -= (enemy.location[1] - obj.bottom[1])/5
                            enemy.speed[1] += 2
                        else:
                            enemy.speed[1] = 0
                        if enemy.right[0] < obj.left[0]:
                            #enemy.location[0] -= (enemy.location[0] - obj.right[0])/5
                            enemy.speed[0] += 1
    else:
        obj.attack = False
        obj.inhalingNum = 0
    obj.firePressed = True


