import numpy as np
import scipy.special as sps


def analytical_solution() -> float:
    """
    Compute the analytical probability of a dishwasher breaking 4 dishes in a
    row given that 5 dishes were broken in a week by 5 dishwashers in total.

    Returns
    -------
    float
        The probability of a dishwasher breaking 4 dishes in a row.
    """

    # The total number of ways to assign the 5 broken dishes to the 5
    # dishwashers is given by 5^5
    total_possibilities = np.power(5, 5)

    # There are 4*(5 choose 4) + (5 choose 5) ways to assign the 4 broken dishes to the clumsy
    # dishwasher
    clumsy_possibilities = 4 * sps.comb(5, 4) + sps.comb(5, 5)

    # The probability of a dishwasher breaking 4 dishes in a row is:
    clumsy_analytic = clumsy_possibilities/total_possibilities

    return clumsy_analytic

def monte_carlo_solution(n_trials: int,
                         n_dishwashers: int = 5,
                         clumsy_threshold: int = 4,
                         breakage_probability: float = 0.2,
                         seed: int = 23072022) -> float:
    """
    Using a Monte Carlo method, compute the probability of a dishwasher breaking
    4 dishes in a row given that 5 dishes were broken in a week by 5 dishwashers
    in total.

    Parameters
    ----------
    n_trials : int
        The number of trials to run.
    seed : int
        The seed for the random number generator.

    Returns
    -------
    float
        The probability of a dishwasher breaking 4 dishes in a row.
    """

    rng = np.random.default_rng(seed)

    # Generate a numpy array of random numbers in [0, 1]. Each row has 5
    # entries corresponding to the five dishwashers.
    random_numbers = rng.random([n_dishwashers, n_trials])

    # In each row, a dish was broken if the random number is less than 0.2.
    # The number of dishes broken is the number of entries in the row that are
    # less than 0.2.
    n_broken = np.sum(random_numbers < breakage_probability, axis=0)

    # If the number of dishes broken in a given trial is greater than 3, then
    # the dishwasher is considered to be clumsy.
    clumsy_count = n_broken[n_broken >= clumsy_threshold].size

    return clumsy_count / n_trials


def main():
    """
    Consider a restaurant that employs five dishwashers. In a one week
    interval, the team breaks five dishes, with four breakages attributable
    to the same individual. The individual claims he's not clumsy, and that
    it was just bad luck.

    Assuming the probability of breakage is truly random, and assuming all
    dishwashers are equally competant, what is the probability that any
    given dishwasher would break 4 dishes in a row?
    """

    print("*** The Clumsy Dishwasher Problem ***")

    clumsy_analytic = analytical_solution()

    print(f"Analytical solution: {clumsy_analytic}")

    n_trials = 1000000
    clumsy_monte_carlo = monte_carlo_solution(n_trials, seed=1337)

    print(f"Monte Carlo solution: {clumsy_monte_carlo}")


if __name__ == '__main__':
    main()