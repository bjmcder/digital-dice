import numpy as np

from collections import namedtuple

# We can avoid cluttering up downstream function arguments by creating
# namedtuple structures for the number of coins for each player.
CoinCounts = namedtuple('CoinCounts', ['l', 'm', 'n'])


def create_coin_counts(l: int, m: int, n: int) -> CoinCounts:
    """
    Return a namedtuple containing the number of coins for each player.

    Parameters
    ----------
    l : int
        The number of coins for player 1.
    m : int
        The number of coins for player 2.
    n : int
        The number of coins for player 3.

    Returns
    -------
    CoinCounts
        A namedtuple containing the number of coins for each player.
    """
    return CoinCounts(l, m, n)


def analytical_solution(coin_counts: CoinCounts,
                        coin_bias: float = 0.5) -> float:
    """
    The analytical solution is currently only known for the case in which all
    coins are fair (p = 0.5). In this case, the average number of coin flips
    required to eliminate one player is:

    E_avg = (4 * l * m * n) / (3 * (l + m + n - 2))

    where E_avg is the average number of coin flips required to eliminate one
    player.

    Parameters
    ----------
    coin_counts : CoinCounts
        A namedtuple containing the number of coins for each player.
    coin_bias : float
        The global bias of all coins in play.

    Returns
    -------
    float
        The average number of coin flips required to eliminate one player.
    """

    # Unpack the coin counts and biases
    l, m, n = coin_counts
    p = coin_bias

    # Return None if any bias is not 0.5
    if not (p == 0.5):
        return None

    # If all the coins are fair, then the average number of coin flips before
    # one player has no coins is:
    solution = (4 * l * m * n) / (3 * (l + m + n - 2))

    return solution

def monte_carlo_solution(n_trials: int,
                         coin_counts: CoinCounts,
                         coin_bias: float = 0.5,
                         seed_l: int = 26072302,
                         seed_m: int = 97181713,
                         seed_n: int = 55283621) -> float:
    """
    """
    # Unpack the coin counts and biases
    l, m, n = coin_counts
    p = coin_bias

    # Initialize three independent random number generators corresponding
    # to the three players.
    rng_l = np.random.default_rng(seed_l)
    rng_m = np.random.default_rng(seed_m)
    rng_n = np.random.default_rng(seed_n)

    # This is a naive loopy implementation of the Monte Carlo solution.
    # TODO: Implement a more efficient vectorized solution using numpy arrays.

    total_flips = 0

    for _ in range(n_trials):

        # Initialize the coin counts for each player.
        player_status = np.array(coin_counts)
        trial_flips = 0

        while not np.isin(0, player_status):

            # Flip the coins
            flip = np.array([rng_l.binomial(1, p),
                             rng_m.binomial(1, p),
                             rng_n.binomial(1, p)])

            trial_flips += 1

            # If all coins show the same side, then nothing happens.
            if flip.sum() == 0 or flip.sum() == 3:
                pass

            # If two coins show the same side, then those players give their coins
            # to the odd person whose coins showed the opposite side.
            elif flip.sum() == 1:
                player_status[flip == 0] -= 1
                player_status[flip == 1] += 1

            elif flip.sum() == 2:
                player_status[flip == 0] += 1
                player_status[flip == 1] -= 1

        total_flips += trial_flips

    return total_flips / n_trials

def main():
    """
    Three people have l, m, and n coins each. Each person selects a coin and
    all three simultaneously flip them. If two coins show the same side, then
    those people give their coins to the odd person whose coins showed the
    opposite side. If all three coins show the same side, then no one gives
    their coins to anyone. The game continues until one person has no more
    coins remaining.

    Assuming all coins have the same probability of showing heads or tails,
    what is the average number of coin flips required to eliminate one player?
    Note that while all coins have the same bias, the bias may not necessarily
    be equal to 0.5.
    """

    print("*** A Curious Coin-Flipping Game***")

    # Case 1: All coins are fair (p = 0.5)
    coin_counts = create_coin_counts(l=1, m=2, n=3)
    coin_bias = 0.5

    # Analytical solution
    analytical_flips = analytical_solution(coin_counts, coin_bias)

    # Monte Carlo solution
    monte_carlo_flips = monte_carlo_solution(n_trials=100000,
                                             coin_counts=coin_counts,
                                             coin_bias=coin_bias)

    print(f"Analytical solution: {analytical_flips}")
    print(f"Monte Carlo solution: {monte_carlo_flips}")


if __name__ == "__main__":
    main()