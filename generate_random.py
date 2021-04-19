import sys
import random


def create_puzzle():
    tokens = random.randrange(3, 13)
    tokens_taken = random.randrange(0, tokens - 2)
    list_of_tokens_taken = []
    depth = random.randrange(1, tokens)

    tokens_available = []
    for i in range(0, tokens):
        tokens_available.append(i + 1)

    token_choices = []
    last_token = None

    if tokens_taken >= 1:
        for t in tokens_available:
            if t < tokens / 2 and t % 2 == 1:
                token_choices.append(t)

        last_token = token_choices[random.randrange(0, len(token_choices))]
        list_of_tokens_taken.append(last_token)
        tokens_available.remove(last_token)

    if tokens_taken >= 2:
        for j in range(1, tokens_taken):
            token_choices = []
            for t in tokens_available:
                if (t % last_token == 0 or last_token % t == 0) and t != last_token:
                    token_choices.append(t)

            if len(token_choices) == 0:
                return "Invalid Puzzle"
            else:
                last_token = token_choices[random.randrange(0, len(token_choices))]
                list_of_tokens_taken.append(last_token)
                # print(tokens)
                # print(tokens_taken)
                # print(list_of_tokens_taken)
                # print(tokens_available)
                # print("token choices {}".format(token_choices))
                tokens_available.remove(last_token)

    return "{} {} {} {}".format(tokens, tokens_taken, list_of_tokens_taken, depth).replace("[", "").replace("]", "").replace(",", "").replace("  ", " ")


if __name__ == '__main__':
    f = open(sys.argv[1], "w")

    for i in range(0, int(sys.argv[2])):
        output = create_puzzle()
        while output == "Invalid Puzzle":
            output = create_puzzle()

        f.write("input{}:\r".format(i + 1))
        f.write("\tTakeTokens {}\r".format(output))

    f.close()
