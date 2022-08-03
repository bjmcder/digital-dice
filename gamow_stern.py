import numpy as np

def analytical_solution():
    """
    """
    pass

def monte_carlo_solution(n_trials: int,
                         n_floors: int,
                         n_elevators: int,
                         gamow_floor: int,
                         seed: int = 31072022) -> float:
    """
    """

    rng = np.random.default_rng(seed)

    # Convert Gamow's floor to the total fraction of the building height such
    # that the first floor is 0 and the top floor is 1.
    floor_fraction = gamow_floor / (n_floors-1)


def main():
    """
    The Gamow-Stern elevator problem: George Gamow's office in on the second
    floor of a seven-storey building and Marvin Stern's office is on the
    seventh floor. Gamow noted that whenever he wished to go up to the sixth
    floor to visit Stern, the elevator always seemd to be on its way down.
    Likewise, whenever Stern wished to go up to the second floor, the elevator
    always seemed to be on its way up.

    In a building with 7 floors and just one elevator, the probability that it
    would be below Gamow's office is 1/6, and the probability that it would
    above his office is 5/6. Thus, it would be expected that the elevator
    would almost always be on its way down when Gamow's office is visited. The
    converse is true for Stern's observations.

    For a building with F floors and E elevators, compute the probability that
    the elevator will be on its way down (the wrong direction) when Gamow's
    office on the G'th floor is visited.
    """

    n_trials = 100000
    n_floors = 7
    n_elevators = 1
    gamow_floor = 2
    seed = 31072022

    mc_solution = monte_carlo_solution(n_trials,
                                       n_floors,
                                       n_elevators,
                                       gamow_floor,
                                       seed)

    print("*** The Gamow-Stern Elevator Problem ***")

    print(f"Monte Carlo solution: {mc_solution}")



if __name__ == '__main__':
    main()
