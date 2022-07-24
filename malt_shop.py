import numpy as np

def analytical_solution(arrival_window: float = 30.0,
                        a_wait_time: float = 5.0,
                        b_wait_time: float = 7.0) -> float:
    """
    """

    # The feasible space of arrival times for Alice and Bob is given by the
    # product of each individual's arrival window. In this case, both Alice and
    # Bob have the same arrival window, so the feasible space is geometrically
    # a square.
    arrival_space = arrival_window**2

    # Consider the case when Alice and Bob arrive at the same time. This
    # corresponds to a line A=B in the feasible space. Since the space is a
    # square, the line bisects the square on the diagonal. Because each person
    # has a waiting time, they each have a line A = B + W_P, where W is the
    # wait time for person P.
    #
    # From Alice's perspective, the feasible space is bounded above by the line
    # A = B + W_B and below by the line A = B - W_A. Similar bounding lines can
    # be drawn for Bob's perspective, but is sufficient to choose one reference
    # individual.
    #
    # Given the constraints imposed by each person's waiting time, the feasible
    # space is reduced by subtracting the area of the triangles formed by the
    # lines A = B + W_B and A = B - W_A and the edges of the square.
    upper_edge_length = arrival_window - a_wait_time
    upper_triangle_area = (upper_edge_length * upper_edge_length) / 2

    lower_edge_length = arrival_window - b_wait_time
    lower_triangle_area = (lower_edge_length * lower_edge_length) / 2

    feasible_upper = (arrival_space/2) - upper_triangle_area
    feasible_lower = (arrival_space/2) - lower_triangle_area


    meeting_probability = (feasible_upper + feasible_lower) / arrival_space

    return meeting_probability

def monte_carlo_solution(n_trials: int,
                         arrival_window: float = 30.0,
                         a_wait_time: float = 5.0,
                         b_wait_time: float = 7.0,
                         seed_a: int = 23072022,
                         seed_b: int = 24072022) -> float:
    """
    """

    # Create two independent random number generators corresponding to the two
    # participants.
    rng_a = np.random.default_rng(seed_a)
    rng_b = np.random.default_rng(seed_b)

    # Generate arrays of random numbers in [0, arrival_window] for Alice and
    # Bob corresponding to their respective arrival times.
    arrivals_a = rng_a.uniform(0.0, arrival_window, n_trials)
    arrivals_b = rng_b.uniform(0.0, arrival_window, n_trials)

    # Determine the number of times that Alice and Bob meet. It's considered a
    # meeting if both participants arrive within the meeting window.
    meetings = np.sum((arrivals_a < arrivals_b + a_wait_time) & \
                      (arrivals_a > arrivals_b - b_wait_time))

    # Return the probability that Alice and Bob meet.
    return meetings / n_trials


def main():
    """
    Alice and Bob agree to meet at the malt shop sometime between 3:30 and 4:00
    in the afternoon. They agree on the 30-minute meeting window, but not on
    the exact arrival time. If Alice arrives first, she will wait 5 minutes
    before leaving. If Bob arrives first, he will wait 7 minutes before
    leaving. Neither will wait past 4:00, and all arrival times are equally
    likely.

    1. What is the probability that Alice and Bob meet?
    2. What is the probability that they will meet if Bob reduces his
       wait time to match Alice's (5 minutes)?
    3. What is the probability that they will meet if Alice increases her wait
       time to match Bob's (7 minutes)?
    """

    print("*** Will Alice and Bob meet at the Malt Shop? ***")


    # Run the Monte Carlo simulation.
    print("Solutions:")

    n_trials = 1000000

    # Case 1: Alice waits 5 minutes and Bob waits 7 minutes.
    a_time = 5
    b_time = 7

    meeting_probability = analytical_solution(a_wait_time=a_time,
                                              b_wait_time=b_time)

    mc_meeting_probability = monte_carlo_solution(n_trials,
                                                  a_wait_time=a_time,
                                                  b_wait_time=b_time,
                                                  seed_a=23072022,
                                                  seed_b=24072022)

    print(f"   1. Alice waits {a_time} minutes, Bob waits {b_time} minutes:\n" \
          f"      Analytical: {meeting_probability}\n" \
          f"      MC: {mc_meeting_probability}")

    # Case 2: Alice and Bob both wait 5 minutes.
    a_time = 5
    b_time = 5

    meeting_probability = analytical_solution(a_wait_time=a_time,
                                              b_wait_time=b_time)

    mc_meeting_probability = monte_carlo_solution(n_trials,
                                                  a_wait_time=a_time,
                                                  b_wait_time=b_time,
                                                  seed_a=23072022,
                                                  seed_b=24072022)

    print(f"   2. Alice waits {a_time} minutes, Bob waits {b_time} minutes:\n" \
          f"      Analytical: {meeting_probability}\n" \
          f"      MC: {mc_meeting_probability}")

    # Case 3: Alice and Bob both wait 7 minutes.
    a_time = 7
    b_time = 7

    meeting_probability = analytical_solution(a_wait_time=a_time,
                                              b_wait_time=b_time)

    mc_meeting_probability = monte_carlo_solution(n_trials,
                                                  a_wait_time=a_time,
                                                  b_wait_time=b_time,
                                                  seed_a=23072022,
                                                  seed_b=24072022)

    print(f"   3. Alice waits {a_time} minutes, Bob waits {b_time} minutes:\n" \
          f"      Analytical: {meeting_probability}\n" \
          f"      MC: {mc_meeting_probability}")


if __name__ == '__main__':
    main()