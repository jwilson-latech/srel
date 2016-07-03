                                    srel.py
                        2+1D Special Relativity Toy Model

                    Originally written by Joshua Wilson
            Currently maintained by Joshua Wilson <iam.jwilson@me.com>

        Copyright 2016 Joshua Wilson <iam.jwilson@me.com>>. This software is distributed under a
        GNU GPL license. Please see the file LICENSE in the distribution
        for terms of use and redistribution.


MOTIVATION: 
    This project is a 2D toy model a spaceship traveling through 2D flat space under Lorentz transformations. 
    The physics of this model is meant to show what an oberver in an inertial reference frame would see.
    Moreover, since the inertial observer (the user) is  controlling the ship, appropirate time delays are 
    calculated for the response of the ship. Lorenz transformations are also used to calculate the shape of the 
    ship for any particular yaw and direction of motion. 

    This project is inspired by the Differential Geometry applet created by Izaak Meckler which is available at http://parametricity.com/pages/diffgeo/Main.html. This project meant as proof of concept for a more general program which would calculate trajectories in curved space as well. 

REQUIREMENTS:
    Python 2.7, PyGame, NumPy

CONTROLS: 

    UP      - accelerate forward
    DOWN    - accelerate backward
    LEFT    - turn counterclockwise
    RIGHT   - turn clockwise
    SPACE   - brake
    D       - shoot photon (constant speed)
    F       - shoot bullet (variable speed)
    T       - remove all photons and bullets


    


