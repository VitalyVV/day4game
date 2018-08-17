from hero import Hero


class MyHero(Hero):
    def run(self):
        description = self._receive()

        while(self._enabled):
            #Write your code here
            #Example for you
            # Implement it in form of algorithm for better efficiency
            self.attack(self.attack_function)
            self.protect([(1,2), (2,1)])
            self.move(10, 10)

            pass
            #You can add code here


    def attack_function(self):
        """
        Implement this function to return an array of tuples
        with (x,y) coordinates
        """

        #Write your code here


        return []  # Remove this if you don't need it



def main():
    #Set the value of TA' machine IP address. All of you have to be in one network
    ta_ip = '127.0.0.1' # Update it, it will not work with local host

    #Change the calling to Suitable for you.
    hero = MyHero('yourname', ta_ip)
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
