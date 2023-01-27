import moremethods
ability = input()

def func():
    print("Ability is copy")
if ability != "copy":
    title = ability + "func"
    function = getattr(moremethods,title)
    function()
else:
    func()

