import gameLib
def Copy(obj):
    if obj.firePressed == False:
        if obj.crouching == False:
            if (obj.mouthfull == 0 or obj.inhalingnum > 0):
                obj.floating = False
                if obj.attack == False:
                    obj.playAnimationOnce("InhaleStart","Inhale")
                else:
                    obj.playAnimation("Inhale")
                obj.attack = True
            elif obj.mouthfull > 0:
                obj.mouthfull = 0
                obj.playAnimationOnce("Swallow","Idle")
                star = gameLib.Attack("Kirby","None",obj.location[0],obj.location[1],obj.objlist,obj.renderLayer,"Dee",obj.currentLevel,100,obj,"line")
            else:
                if obj.speed == 0:
                    obj.playAnimation("Full")
                #obj.attack = False
                """if obj.attack == False:
                    obj.mouthfull = False
                    obj.startInhale = True"""
    
    if obj.attack == True:
        for enemy in obj.collide:
            if enemy != None and type(enemy).__name__ == "Enemy":
                if obj.dir == "right" and enemy.right[0] > obj.right[0]:
                    obj.mouthfull += 1
                    enemy.Kill()
                    obj.collide.remove(enemy)
                elif obj.dir == "left" and enemy.left[0] < obj.left[0]:
                    obj.mouthfull += 1
                    enemy.Kill()
                    obj.collide.remove(enemy)
                else:
                    obj.Kill()

    obj.inhalingnum = 0
    for enemy in obj.objlist:
        if enemy.inhaled == True:
            obj.inhalingnum += 1
    #print(obj.inhalingnum)
    if obj.mouthfull == 0 or obj.inhalingnum > 0:
        for enemy in obj.objlist:
            if type(enemy).__name__ == "Enemy":
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
                            enemy.speed[1] -= 1
                            print("dip")
                        elif enemy.right[1] < obj.left[1]:
                            #enemy.location[1] -= (enemy.location[1] - obj.bottom[1])/5
                            enemy.speed[1] += 1
                            print("dip")
                        else:
                            enemy.speed[1] = 0
                            print("dip")
                        if enemy.right[0] < obj.left[0]:
                            #enemy.location[0] -= (enemy.location[0] - obj.right[0])/5
                            enemy.speed[0] += 1
    else:
        obj.attack = False
    obj.firePressed = True


