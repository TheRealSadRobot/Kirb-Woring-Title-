import gameLib
import pygame

def beamAttack(obj):
    if obj.firePressed == False:
        obj.firePressed = True
        obj.actTimer = 25
        obj.playAnimationOnce("Prebeam","Beam")
        obj.fallspeed = 0
        num = 8
        anglemod = 0
        if obj.dir == "left":
            while num <= 40:
                beam = gameLib.Attack(0,"Beam",obj.location[0],obj.location[1],obj.objlist,
                 obj.renderLayer,"Normal",obj.currentLevel,[25,[-8-num,8+num,1,obj.location,-90-anglemod],obj,"circle",None])
                anglemod += 0.125
                num+=8
        else:
            while num <= 40:
                beam = gameLib.Attack(0,"Beam",obj.location[0],obj.location[1],obj.objlist,
                 obj.renderLayer,"Normal",obj.currentLevel,[25,[8+num,8+num,1,obj.location,-90-anglemod],obj,"circle",None])
                anglemod += 0.125
                num+=8

def WaterSpit(obj):
    if obj.firePressed == False:
        obj.firePressed = True
        obj.actTimer = 25
        obj.fallspeed = 0
        if obj.keys[pygame.K_UP]:
            spout = gameLib.Attack(0,"Star",
                                   obj.location[0],obj.location[1],
                                   obj.objlist,obj.renderLayer,"Shoot1",
                                   obj.currentLevel,[25,[0,-8,1],obj,"parent",
                                   "submergedCheck"])
        elif obj.keys[pygame.K_DOWN]:
            spout = gameLib.Attack(0,"Star",
                                   obj.location[0],obj.location[1],
                                   obj.objlist,obj.renderLayer,"Shoot1",
                                   obj.currentLevel,[25,[0,8,1],obj,"parent",
                                   "submergedCheck"])
        elif obj.dir == "left":
            spout = gameLib.Attack(0,"Star",
                                   obj.location[0],obj.location[1],
                                   obj.objlist,obj.renderLayer,"Shoot1",
                                   obj.currentLevel,[25,[-8,0,1],obj,"parent",
                                   "submergedCheck"])
        else:
            spout = gameLib.Attack(0,"Star",
                                   obj.location[0],obj.location[1],
                                   obj.objlist,obj.renderLayer,"Shoot1",
                                   obj.currentLevel,[25,[8,0,1],obj,"parent",
                                   "submergedCheck"])
    else:
        print("dip")
def Copy(obj):
    rdist = obj.distanceToCollide(obj.bottom,1,1)
    ldist = obj.distanceToCollide(obj.bottom,1,1)
    if ldist > rdist:
        bottom = obj.bottom
    else:
        bottom = obj.bottom

    obj.inhalingnum = 0
    for enemy in obj.objlist:
        if issubclass(type(enemy), gameLib.Object):
            if enemy.inhaled == True:
                obj.inhalingnum += 1
            
    #print(obj.attack)
    if obj.firePressed == False:
        if obj.crouching == False:
            if (obj.mouthfull == 0):# or obj.inhalingnum > 0):
                obj.floating = False
                if obj.attack == False:
                    obj.playAnimationOnce("InhaleStart","Inhale")
                    obj.setCollideBoxSize(16,22)
                else:
                    obj.playAnimation("Inhale")
                obj.attack = True
            elif obj.mouthfull > 0:
                for item in obj.inmouth:
                    if issubclass(type(item), gameLib.Object):
                        #print(type(obj.inmouth).__name__)
                        item.mouthed = None
                        if type(item).__name__ == "Enemy":
                            if obj.dir == "left":
                                if obj.mouthfull > 1:
                                    star = gameLib.Attack(0,"Star",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,[100,[-4,0,1],obj,"line",None])
                                    lilstar = gameLib.Attack(0,"Star",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,[100,[16,16,-1,star.location,0],obj,"circle",None])
                                else:
                                    star = gameLib.Attack(0,"Star",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,[100,[-4,0,1],obj,"line",None])
                            else:
                                if obj.mouthfull > 1:
                                    star = gameLib.Attack(0,"Star",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,[100,[4,0,1],obj,"line",None])
                                    lilstar = gameLib.Attack(0,"Star",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,[100,[16,16,1,star.location,0],obj,"circle",None])
                                else:
                                    star = gameLib.Attack(0,"Star",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Shoot1",obj.currentLevel,[100,[4,0,1],obj,"line",None])
                            obj.inmouth = []
                            obj.mouthfull = 0
                            break
                        if type(item).__name__ == "Ball":
                            #print("Young Dippa")
                            if obj.dir == "left":
                                item.speed = [-4,0]
                                item.location[0] -= 18
                                item.location[1] -= 3
                            else:
                                item.speed = [4,0]
                                item.location[0] += 18
                                item.location[1] -= 3
                            obj.inmouth.remove(item)
                        obj.mouthfull -= 1
                        obj.attack = False
                obj.playAnimationOnce("Spit","Idle")
                obj.setCollideBoxSize(16,20)
            else:
                if obj.speed == 0:
                    obj.playAnimation("Full")
                #obj.attack = False
                """if obj.attack == False:
                    obj.mouthfull = False
                    obj.startInhale = True"""
        else:
            obj.attack = False
    
    if obj.attack == True:# and obj.mouthfull == 0:
        for enemy in obj.collide:
            if issubclass(type(enemy), gameLib.Object):
                #print(enemy.mouthed, enemy.inhaled)
                if enemy != None and enemy.mouthed == None and enemy.inhaled == True:# and type(enemy).__name__ != "NPC":
                    #print("dip")
                    if obj.dir == "right" and enemy.right[0] > obj.left[0]:
                        obj.mouthfull += 1
                        obj.inmouth.append(enemy)
                        if type(enemy).__name__ == "Enemy":
                            enemy.Kill()
                        enemy.mouthed = obj
                        obj.collide.remove(enemy)
                    elif obj.dir == "left" and enemy.left[0] < obj.right[0]:
                        obj.mouthfull += 1
                        obj.inmouth.append(enemy)
                        if type(enemy).__name__ == "Enemy":
                            enemy.Kill()
                        enemy.mouthed = obj
                        obj.collide.remove(enemy)
                    else:
                        if type(enemy).__name__ == "Enemy":
                            obj.Kill()
                            #print(enemy.mouthed, enemy.inmouth)
                        #else:
                    #self.inmouth = None
    #print(obj.inhalingnum)
    if obj.attack == True and (obj.mouthfull == 0 or obj.inhalingnum > 0):
        for enemy in obj.objlist:
            if issubclass(type(enemy), gameLib.Object):
                if type(enemy).__name__ != "NPC":
                    if obj.dir == "right" and (enemy.location[0]-obj.right[0]) <= 48 and (enemy.location[0]-obj.right[0]) > 0:
                        if (obj.top[1]-enemy.location[1]-enemy.spriteSize[1]) <= 24 and (bottom[1]-enemy.location[1]) > -24:
                            #print(f"RIGHT: Suck in {enemy.pallateName}")
                            if enemy.left[1] > obj.right[1]:
                                #enemy.location[1] += (enemy.location[1] - bottom[1])/5
                                enemy.speed[1] -= 1
                            elif enemy.left[1] < obj.right[1]:
                                #enemy.location[1] -= (enemy.location[1] - bottom[1])/5
                                enemy.speed[1] += 1
                            else:
                                enemy.speed[1] = 0
                            if enemy.left[0] >= obj.right[0]:
                                #enemy.location[0] -= (enemy.location[0] - obj.right[0])/5
                                enemy.speed[0] -= 1
                    elif obj.dir == "left" and (obj.left[0]-enemy.right[0]) <= 48 and (obj.left[0]-enemy.right[0]) > 0:
                        if (obj.top[1]-enemy.location[1]-enemy.spriteSize[1]) <= 24 and (bottom[1]-enemy.location[1]) > -24:
                            #print(f"LEFT: Suck in {enemy.pallateName}")
                            if enemy.right[1] > obj.left[1]:
                                #enemy.location[1] += (enemy.location[1] - bottom[1])/5
                                enemy.speed[1] -= 2
                            elif enemy.right[1] < obj.left[1]:
                                #enemy.location[1] -= (enemy.location[1] - bottom[1])/5
                                enemy.speed[1] += 2
                            else:
                                enemy.speed[1] = 0
                            if enemy.right[0] <= obj.left[0]:
                                #enemy.location[0] -= (enemy.location[0] - obj.right[0])/5
                                enemy.speed[0] += 1
    else:
        obj.attack = False
        obj.inhalingNum = 0
    obj.firePressed = True


