from ClientSide.hero import Hero


class MyHero(Hero):
    def run(self):
        while(self._enabled):
            #Write your code here




            #until here
            event = self._receive()
            #You can add code here


    def attack_function(self):
        """
        Implement this function to return an array of tuples
        with (x,y) coordinates
        """

        #Write your code here



        pass  # Remove this if you don't need it



def main():
    #Change the calling to Suitable for you.
    #You can't have Strength and Intelligence together be greater than 40 points
    hero = MyHero('yourname')
    #Your hero possesed 3 functions you may use:
    # attack(): given a trajectory performing long shot at the enemy or close range attack.
    #         It all depends on what trajectory you build using attack_function()
    # protect(): Builds a line that reduces damage from enemy attack. The reduction varies
    #         given the length of your line. Line of length 0.1 will reduce 90% of damage,
    #         however line of length more than 1.1 will reduce only 5% of damage.
    # move(): Make your hero to move to a certain point.
    #       Be careful
    #

    hero.run()

if __name__ == '__main__':
    main()
