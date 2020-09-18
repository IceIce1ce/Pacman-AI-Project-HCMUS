from mainLevel3_4 import *

def main():
    while True:
        print("Welcome to the pacman world")
        print("Easy challenge (level 1 of pacman)")
        print("Medium challenge (level 2 of pacman)")
        print("Hard challenge (level 3 and level 4 of pacman)")
        option = int(input("Input your choice (1->3): "))
        if option == 1:
            import level1 # import here to avoid turtle's window auto open
            level1.mainLevel1()
        elif option == 2:
            import level2 # import here to avoid turtle's window auto open
            level2.mainLevel2()
        elif option == 3:
            mainLevel3_4()
            exit(0)
        else: print("Invalid input, try-again !!!")

if __name__ == '__main__':
    main()