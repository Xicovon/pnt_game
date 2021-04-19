import math
import sys

MAX_TURN = True
MIN_TURN = False


# prime number function via https://www.programiz.com/python-programming/examples/prime-number
def is_prime(n):
    if n == 1:
        return True
    else:
        # check for factors
        for i in range(2, n):
            if (n % i) == 0:
                return False
        else:
            return True


def load(path):
    input_file = open(path)
    lines = input_file.readlines()

    list_of_states = []

    count = 0
    for line in lines:
        if len(line) > 1 and line.find("TakeTokens") >= 0:
            lst = line.strip().split()
            list_of_states.append(State(int(lst[1]), int(lst[2]), [int(x) for x in lst[3:-1]], int(lst[-1]), 0))

            # print(list_of_states[-1].tokens)
            # print(list_of_states[-1].tokens_taken)
            # print(list_of_states[-1].list_taken_tokens)
            # print(list_of_states[-1].search_depth)
            # print(list_of_states[-1].current_depth)

    input_file.close()
    return list_of_states


class State:
    def __init__(self, tokens, tokens_taken, list_taken_tokens, search_depth, current_depth):
        self.tokens = tokens
        self.tokens_taken = tokens_taken
        if list_taken_tokens is None:
            self.list_taken_tokens = []
        else:
            self.list_taken_tokens = list_taken_tokens

        self.search_depth = search_depth
        self.current_depth = current_depth


class PNT:
    def __init__(self):
        self.nodes_visited = 0
        self.nodes_evaluated = 0
        self.max_depth = 0
        self.successors_not_pruned = 0
        self.branching_factor = []

    def reset(self):
        self.nodes_visited = 0
        self.nodes_evaluated = 0
        self.max_depth = 0
        self.successors_not_pruned = 0
        self.branching_factor = []

    # this function keeps track of how many nodes are at which depths to calculate EBF
    def add_branch(self, depth):
        if len(self.branching_factor) < (depth + 1):
            self.branching_factor.append(1)
        else:
            self.branching_factor[depth] += 1

    # returns a list of tokens which are valid moves
    def actions(self, state):
        valid_moves = []

        if state.tokens_taken == 0:
            for token in range(1, state.tokens + 1):
                if (token < state.tokens / 2) and token % 2 == 1:
                    valid_moves.append(token)
        else:
            # player must take a token that is a multiple or factor of the last token taken and cannot have already
            # been taken
            # print("state taken tokens: {}".format(state.tokens_taken))
            # print("state list taken tokens: {}".format(state.list_taken_tokens))
            last_token = state.list_taken_tokens[-1]
            for token in range(1, state.tokens + 1):
                if ((token % last_token == 0) or (last_token % token == 0)) and token not in state.list_taken_tokens:
                    # a move can be made, the game does not end
                    valid_moves.append(token)

        # print("\nvalid moves: {}".format(valid_moves))
        # print("list of tokens taken: {}\n".format(state.list_taken_tokens))
        # valid_moves.reverse()
        return valid_moves

    # determines if a given state is an end state
    def is_terminal(self, state):
        # print("search depth: {}".format(state.search_depth))
        # print("current depth: {}".format(state.current_depth))
        if state.tokens_taken == 0:
            return False

        elif state.search_depth == state.current_depth and state.search_depth != 0:
            return True

        else:
            if len(self.actions(state)) > 0:
                return False
            else:
                return True

    # if tokens taken is odd it is max's move
    def is_max_move(self, state):
        if state.tokens_taken % 2 == 0:
            return True
        else:
            return False

    # this function takes a state and action and applies the action to create a new state
    # assumes the action is valid
    def result(self, state, action):
        new_lst = state.list_taken_tokens[:]
        new_lst.append(action)

        new_state = State(state.tokens, state.tokens_taken + 1, new_lst, state.search_depth, state.current_depth + 1)

        self.max_depth = max(self.max_depth, new_state.current_depth)

        # print("action: {}".format(action))
        # print("new state tokens taken: {}".format(new_state.tokens_taken))
        # print("new state list of tokens taken: {}".format(new_state.list_taken_tokens))
        # print("new state current depth: {}".format(new_state.current_depth))
        # print("old state tokens taken: {}".format(state.tokens_taken))
        # print("old state list of tokens taken: {}".format(state.list_taken_tokens))
        # print("old state current depth: {}".format(state.current_depth))

        return new_state

    def utility(self, state, is_max_turn):
        if len(self.actions(state)) == 0:
            if is_max_turn:
                return -1
            else:
                return 1
        else:
            if 1 not in state.list_taken_tokens:
                return 0

            if is_max_turn:
                # If the last move was 1, count the number of the possible successors (i.e., legal moves).
                # If the count is odd, return 0.5; otherwise, return-0.5.
                if state.tokens_taken > 0 and state.list_taken_tokens[-1] == 1:
                    # if even number of actions
                    if len(self.actions(state)) % 2 == 0:
                        return -0.5
                    else:
                        return 0.5
                # If last move is a prime, count the multiples of that prime in all possible successors.
                # If the count is odd, return 0.7; otherwise, return-0.7
                if state.tokens_taken > 0 and is_prime(state.list_taken_tokens[-1]):
                    count = 0
                    for a in self.actions(state):
                        if a % state.list_taken_tokens[-1] == 0:
                            count += 1

                    if count % 2 == 0:
                        return -0.7
                    else:
                        return 0.7
                else:
                    count = 0
                    for a in self.actions(state):
                        if state.list_taken_tokens[-1] % a == 0:
                            count += 1

                    if count % 2 == 0:
                        return -0.6
                    else:
                        return 0.6
            else:
                # If the last move was 1, count the number of the possible successors (i.e., legal moves).
                # If the count is odd, return 0.5; otherwise, return-0.5.
                if state.tokens_taken > 0 and state.list_taken_tokens[-1] == 1:
                    # if even number of actions
                    if len(self.actions(state)) % 2 == 0:
                        return 0.5
                    else:
                        return -0.5
                # If last move is a prime, count the multiples of that prime in all possible successors.
                # If the count is odd, return 0.7; otherwise, return-0.7
                if state.tokens_taken > 0 and is_prime(state.list_taken_tokens[-1]):
                    count = 0
                    for a in self.actions(state):
                        if a % state.list_taken_tokens[-1] == 0:
                            count += 1

                    if count % 2 == 0:
                        return 0.7
                    else:
                        return -0.7
                else:
                    count = 0
                    for a in self.actions(state):
                        if state.list_taken_tokens[-1] % a == 0:
                            count += 1

                    if count % 2 == 0:
                        return 0.6
                    else:
                        return -0.6


def alpha_beta_search(game, state):
    if game.is_max_move(state):
        return max_value(game, state, -1, 1)
    else:
        return min_value(game, state, -1, 1)


def max_value(game, state, alpha, beta):
    game.nodes_visited += 1
    game.add_branch(state.current_depth)

    if game.is_terminal(state):
        game.nodes_evaluated += 1
        return game.utility(state, MAX_TURN), None

    v1 = -math.inf
    move = None

    for a in game.actions(state):
        v2, a2 = min_value(game, game.result(state, a), alpha, beta)
        if v2 > v1:
            v1 = v2
            move = a
            alpha = max(alpha, v1)
        if v1 >= beta:
            return v1, a
    return v1, move


def min_value(game, state, alpha, beta):
    game.nodes_visited += 1
    game.add_branch(state.current_depth)

    if game.is_terminal(state):
        game.nodes_evaluated += 1
        return game.utility(state, MIN_TURN), None

    v1 = math.inf
    move = None

    for a in game.actions(state):
        v2, a2 = max_value(game, game.result(state, a), alpha, beta)
        if v2 < v1:
            v1 = v2
            move = a
            beta = min(beta, v1)
        if v1 <= alpha:
            return v1, a
    return v1, move


if __name__ == '__main__':

    # states = load("C:\\Users\\Bowen\\Downloads\\testcases\\testcase.txt")
    states = load(sys.argv[1])
    pnt_game = PNT()

    count = 1
    for s in states:
        v, a = alpha_beta_search(pnt_game, s)

        f = open(sys.argv[1][0:sys.argv[1].rindex("\\") + 1] + "output{}.txt".format(count), "w")
        f.write("Move: {}\r".format(a))
        f.write("Value: {:0.1f}\r".format(v))
        f.write("Number of Nodes Visited: {}\r".format(pnt_game.nodes_visited))
        f.write("Number of Nodes Evaluated: {}\r".format(pnt_game.nodes_evaluated))
        f.write("Max Depth Reached: {}\r".format(pnt_game.max_depth))

        branching_factors = []
        for i in range(1, len(pnt_game.branching_factor)):
            branching_factors.append(pnt_game.branching_factor[i] / pnt_game.branching_factor[i - 1])

        if len(branching_factors) == 0:
            f.write("Avg Effective Branching Factor: None\r")
        else:
            f.write("Avg Effective Branching Factor: {:0.1f}\r".format(sum(branching_factors) / len(branching_factors)))

        count += 1

        pnt_game.reset()
