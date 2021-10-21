import itertools
import sys
from itertools import *

# global dicts containing probabilities of dice rolls
one_dice = {1: float(1 / 6), 2: float(1 / 6), 3: float(1 / 6), 4: float(1 / 6), 5: float(1 / 6), 6: float(1 / 6)}
two_dice = {2: float(1 / 36), 3: float(2 / 36), 4: float(3 / 36), 5: float(4 / 36), 6: float(5 / 36), 7: float(6 / 36),
            8: float(5 / 36), 9: float(4 / 36), 10: float(3 / 36), 11: float(2 / 36), 12: float(1 / 36)}


def get_difference(list1, list2):
    return set(list1)-set(list2)


def one_move(max_sum, given_tiles, roll, current_state, memo):
    next_states = {x: 0 for i in range(len(current_state), 0, -1) for x in
                   itertools.combinations(current_state, i) if sum(x) == sum(current_state) - roll}
    if sum(current_state) <= 6:
        for state in next_states:
            next_states[state] = one_dice[roll] * one_expect(max_sum, given_tiles, state, memo)
        max_state = max(next_states, key=next_states.get)
    if sum(current_state) > 6:
        for state in next_states:
            next_states[state] = two_dice[roll] * one_expect(max_sum, given_tiles, state, memo)
        max_state = max(next_states, key=next_states.get)
    return max_state


def one_expect(max_sum, given_tiles, current_state, memo):
    if current_state == ():
        return 1
    if current_state in memo:
        return memo[current_state]
    expected_value = 0

    if sum(current_state) <= 6:
        for key in one_dice:
            if sum(current_state) - key == 0:
                next_states = [()]
            else:
                next_states = [x for i in range(len(current_state), 0, -1) for x in
                               itertools.combinations(current_state, i) if sum(x) == sum(current_state) - key]
            if not next_states:
                temp_memo = {}
                expected_value += one_dice[key] * (1 - two_expect(max_sum, sum(current_state),
                                                                  given_tiles, temp_memo))
            if len(next_states) == 1:
                next_state = next_states[0]
                expected_value += one_dice[key] * one_expect(max_sum, given_tiles, next_state,
                                                             memo)
            if len(next_states) > 1:
                temp_list = [0] * len(next_states)
                for state in next_states:
                    temp_list[next_states.index(state)] += one_dice[key] * one_expect(max_sum, given_tiles,
                                                                                      state, memo)
                expected_value += max(temp_list)
        memo[current_state] = expected_value

    if sum(current_state) > 6:
        for key in two_dice:
            if sum(current_state) - key == 0:
                next_states = [()]
            else:
                next_states = [x for i in range(len(current_state), 0, -1) for x in
                               itertools.combinations(current_state, i) if sum(x) == sum(current_state) - key]
            if not next_states:
                temp_memo = {}
                expected_value += two_dice[key] * (1 - two_expect(max_sum, sum(current_state),
                                                                  given_tiles, temp_memo))
            if len(next_states) == 1:
                next_state = next_states[0]
                expected_value += two_dice[key] * one_expect(max_sum, given_tiles, next_state, memo)
            if len(next_states) > 1:
                temp_list = [0] * len(next_states)
                for state in next_states:
                    temp_list[next_states.index(state)] += two_dice[key] * one_expect(max_sum, given_tiles,
                                                                                      state, memo)
                expected_value += max(temp_list)
        memo[current_state] = expected_value
    return expected_value


def two_move(max_sum, p1_score, roll, current_state, memo):
    next_states = {x: 0 for i in range(len(current_state), 0, -1) for x in
                   itertools.combinations(current_state, i) if sum(x) == sum(current_state) - roll}
    if sum(current_state) <= 6:
        for state in next_states:
            next_states[state] = one_dice[roll] * two_expect(max_sum, p1_score, state, memo)
        max_state = max(next_states, key=next_states.get)
    if sum(current_state) > 6:
        for state in next_states:
            next_states[state] = two_dice[roll] * two_expect(max_sum, p1_score, state, memo)
        max_state = max(next_states, key=next_states.get)
    return max_state


def two_expect(max_sum, p1_score, current_state, memo):
    if sum(current_state) < p1_score:
        return 1
    if current_state in memo:
        return memo[current_state]
    expected_value = 0

    # iterate over each roll and its sub-paths
    if sum(current_state) <= 6:
        for key in one_dice:
            if sum(current_state) - key == 0:
                next_states = [()]
            else:
                next_states = [x for i in range(len(current_state), 0, -1) for x in
                               itertools.combinations(current_state, i) if sum(x) == sum(current_state) - key]
            if not next_states and sum(current_state) == p1_score:
                expected_value += one_dice[key] * 0.5
            if len(next_states) == 1:
                next_state = next_states[0]
                expected_value += one_dice[key] * two_expect(max_sum, p1_score, next_state,
                                                             memo)
            if len(next_states) > 1:
                temp_list = [0] * len(next_states)
                for state in next_states:
                    temp_list[next_states.index(state)] += one_dice[key] * two_expect(max_sum,
                                                                                      p1_score, state, memo)
                expected_value += max(temp_list)

        memo[current_state] = expected_value
    if sum(current_state) > 6:
        for key in two_dice:
            if sum(current_state) - key == 0:
                next_states = [()]
            else:
                next_states = [x for i in range(len(current_state), 0, -1) for x in
                               itertools.combinations(current_state, i) if sum(x) == sum(current_state) - key]
            if not next_states and sum(current_state) == p1_score:
                expected_value += two_dice[key] * 0.5
            if len(next_states) == 1:
                next_state = next_states[0]
                expected_value += two_dice[key] * two_expect(max_sum, p1_score, next_state,
                                                             memo)
            if len(next_states) > 1:
                temp_list = [0] * len(next_states)
                for state in next_states:
                    temp_list[next_states.index(state)] += two_dice[key] * two_expect(max_sum,
                                                                                      p1_score, state, memo)
                expected_value += max(temp_list)
        memo[current_state] = expected_value
    return expected_value


def main():
    args = sys.argv[1:]
    given_tiles = tuple(int(d) for d in str(args[2]))
    if args[0] == '--two' and args[1] == '--expect':
        p1_score = int(args[3])
        memo = {}
        max_sum = sum(given_tiles)
        expected_value = two_expect(max_sum, p1_score, given_tiles, memo)
        print(f'{expected_value:.6f}')

    if args[0] == '--two' and args[1] == '--move':
        p1_score = int(args[3])
        roll = int(args[4])
        memo = {}
        max_sum = sum(given_tiles)
        best_path = list(two_move(max_sum, p1_score, roll, given_tiles, memo))
        solution = list(get_difference(list(given_tiles), best_path))
        solution.sort()
        print(solution)

    if args[0] == '--one' and args[1] == '--expect':
        memo = {}
        max_sum = sum(given_tiles)
        expected_value = one_expect(max_sum, given_tiles, given_tiles, memo)
        print(f'{expected_value:.6f}')

    if args[0] == '--one' and args[1] == '--move':
        roll = int(args[3])
        memo = {}
        max_sum = sum(given_tiles)
        best_path = list(one_move(max_sum, given_tiles, roll, given_tiles, memo))
        solution = list(get_difference(list(given_tiles), best_path))
        solution.sort()
        print(solution)


if __name__ == '__main__':
    main()

