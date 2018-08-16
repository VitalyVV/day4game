from Hero import Hero

class MyHero(Hero):
    def run(self):
        while(self._enabled):
            #Write your code here




            #until here
            #This should be the last line of your program
            self._receive()

    def attack_function(self):
        """
        Implement this function to return an array of tuples
        with (x,y) coordinates
        """
        #Write your code here


        pass # Remove this if you don't need it

def main():
    #Change the calling to Suitable for you.
    #You can't have Strength and Intelligence together be greater than 40 points
    hero = MyHero('yourname', strength=1, intelligence=1)
    hero.run()

if __name__ == '__main__':
    main()
