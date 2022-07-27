import numpy as np

def analytical_solution():
    pass

def compute_nearest_neighbors(car_positions: np.ndarray) -> np.ndarray:
    """
    Given a sorted array of car parking positions, compute each car's nearest
    neighbor.

    Parameters
    ----------
    car_positions : numpy.ndarray
        The array of car parking positions.

    Returns
    -------
    numpy.ndarray
        The array of nearest neighbors.
    """

    n_cars = car_positions.shape[0]
    n_trials = car_positions.shape[1]

    # Start by generating n_trials columns of sequential numbers from 0 to
    # n_cars-1. We will adjust these indices to correspond to the nearest
    # neighbor of each car, e.g. i+1 or i-1.
    nearest_neighbors = np.indices([n_cars, n_trials], dtype=int)[0]

    # For each car position, compute the distances to the cars in front and
    # behind it.
    next_positions = np.roll(car_positions, -1, axis=0)
    prev_positions = np.roll(car_positions, 1, axis=0)

    fwd_distances = next_positions - car_positions
    bwd_distances = car_positions - prev_positions

    # If the backward distance is less than the forward distance, then the
    # the index of the nearest neighbor is one less than the index of the car.
    fwd_mask = bwd_distances < fwd_distances
    bwd_mask = bwd_distances > fwd_distances

    nearest_neighbors[fwd_mask] += 1
    nearest_neighbors[bwd_mask] -= 1

    # Boundary conditions: The nearest neighbor of the first car is always the
    # second car, and the nearest neighbor of the last car is always the
    # second-to-last car.
    nearest_neighbors[0, :] = 1
    nearest_neighbors[-1, :] = n_cars - 2

    return nearest_neighbors


def monte_carlo_solution(n_trials: int,
                         n_cars: int = 3,
                         seed: int = 24072022) -> float:
    """
    Using the Monte Carlo method, determine if a car drawn at random from N
    cars parking along a street of length L is one of a pair of mutual nearest
    neighbors. We can assume L is of unit length.

    Parameters
    ----------
    n_trials : int
        The number of trials to run.
    n_cars : int
        The number of cars on the street.
    seed : int
        The seed for the random number generator.

    Returns
    -------
    float
        The probability of a car drawn at random from N cars being one of a pair
        of mutual nearest neighbors.
    """

    # Generate a random sequence of N cars' parking positions.
    rng = np.random.default_rng(seed)
    car_positions = rng.uniform(0, 1, [n_cars, n_trials])

    # Sort the car positions in ascending order.
    car_positions.sort(axis=0)

    # Compute the nearest neighbors of each car.
    nearest_neighbors = compute_nearest_neighbors(car_positions)

    # We can formally define a mututal nearest neighbor pair with the
    # condition:
    #
    # (nearest_neighbors[i] == i+1) & (nearest_neighbors[i+1] == i)
    idxs = np.indices([n_cars, n_trials], dtype=int)[0]
    next_idxs = np.roll(idxs, -1, axis=0)

    next_nns = np.roll(nearest_neighbors, -1, axis=0)

    mnn_mask = (nearest_neighbors == next_idxs) & (next_nns == idxs)

    # The probability of a car drawn at random from N cars being one of a pair
    # of mutual nearest neighbors is the fraction of trials that satisfy the
    # condition.
    total_mutual_nns = np.count_nonzero(mnn_mask)

    mutual_probability = (2*total_mutual_nns) / (n_cars*n_trials)

    return mutual_probability



def main():
    """
    Suppose that N >= 2 cars are parked along a street of length L.
    Approximating the cars as points (that is, they have no spatial extent),
    we denote the parking position of a car as lying in the interval [0, L].

    If a car is drawn at random, what is the probability that the nearest
    neighbor of the car also has the original car as its nearest neighbor? In
    other words, what is the probability that a car drawn at random is one of
    a pair of mutual nearest neighbors?
    """

    mc_probability = monte_carlo_solution(n_trials=1000000,
                                          n_cars=100,
                                          seed=24072022)

    print(mc_probability)

if __name__ == '__main__':
    main()