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
                         seed: int = 55283621) -> float:
    """
    """
    # Unpack the coin counts and biases
    l, m, n = coin_counts
    p = coin_bias

    n_players = len(coin_counts)
    player_status = np.array([l, m, n])

    # Initialize the random number generator
    rng = np.random.default_rng(seed=seed)

    batch_size = n_players * n_trials

    flip_count = 0
    elimination_count = 0

    while elimination_count < n_trials:

        # A coin flip round can be represented as a 3-element array of binary
        # values. We want to generate a long array of these 3-element arrays and
        # post-process the results to simulate the game.
        flips = rng.binomial(n=1, p=p, size=[n_players, batch_size])

        # Sum the coin flips to determine if a win occured. If the sum is equal
        # to zero or the number of players, then no one has won. Otherwise, we have
        # a winner and we can determine who it is by finding the odd one out.
        flip_sum = np.sum(flips, axis=0)

        no_win = ((flip_sum == 0) + (flip_sum == n_players))
        heads_win = (flip_sum == 1)
        tails_win = (flip_sum == 2)

        # Find the index of the winning player. If the flip sum is equal to 1,
        # the winner is the player whose coin is 1. If the flip sum is equal to
        # 2, the winner is the player whose coins is 0. For cases with no winner,
        # the index is set to -1.
        winners = np.empty(flip_sum.size, dtype=int)

        winners[no_win] = -1
        winners[heads_win] = np.argmax(flips[:, heads_win], axis=0)
        winners[tails_win] = np.argmin(flips[:, tails_win], axis=0)

        # Update the number of coins for each player. The winner gains two coins,
        # each of the losers loses one.
        sequence_count = 0

        for i in range(winners.size):

            # Elimination -
            if np.less_equal(player_status.all(), 0):

                # Tally results
                elimination_count += 1
                flip_count += sequence_count

                # Reset counters
                sequence_count = 0
                player_status = np.array([l, m, n])

                continue

            # No winner, increment the flip count but no change in player status
            if winners[i] == -1:
                sequence_count += 1

            # Winner, increment the flip count and update the player status. The
            # winner gains two coins, each of the losers loses one.
            else:
                sequence_count += 1

                # Subtracting 1 from everybody then adding 3 back to the winner
                # is more succinct than trying to mask the non-winning indices to
                # subtract 1 from just the losing players.
                player_status -= 1
                player_status[winners[i]] += 3

    return flip_count / elimination_count


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
    coin_counts = create_coin_counts(l=4, m=7, n=9)
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