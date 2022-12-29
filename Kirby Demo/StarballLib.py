def StarballUpdate(ball,S1,S2):
    if ball.blockedLeft == True and ball.location[0] < 33:
        ball.respawn()
        S2 += 1
        print(f"P2 Scores\nCurrent Scores:\nP1:{S1}\nP2:{S2}")
    elif ball.blockedRight == True and ball.location[0] > 464:
        S1 += 1
        print(f"P1 Scores\nCurrent Scores:\nP1:{S1}\nP2:{S2}")
        ball.respawn()


    return S1,S2
        
