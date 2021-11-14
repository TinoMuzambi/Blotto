import random

if __name__=="__main__":
    # Initialise Alice with our proposed solution
    alice = [0,0,0,0,0,33,33,33,1,0]
    bob = []

    # Initialise number of times alice and bob wins.
    alice_wins = 0
    bob_wins = 0

    # Run k iterations
    for k in range(1000):
        # Initialise bob's random guess.
        bob = []

        # Initialise check for if alice won.
        check = False
        # Initialise check for if bob won.
        check2 = False

        # Append 10 random guess.
        for i in range(10):
            if sum(bob) < 100:
                bob.append(random.randint(0, 100 - sum(bob)))
            else:
                bob.append(0)

        # Print layouts for Bob and Alice.
        print("{:6}".format("Castle"), end=" ")
        for i in range(len(alice)):
            print("{:>3}".format("C" + str(i + 1)), end=" ")
            # print("C" + str(i + 1), end = " ")
        print()
        print("{:6}".format("Alice"), end=" ")
        for i in range(len(alice)):
            print("{:>3}".format(alice[i]), end=" ")
        print()
        print("{:6}".format("Bob"), end=" ")
        for i in range(len(bob)):
            print("{:>3}".format(bob[i]), end=" ")
        print()

        # Check for three consecutive wins for Alice
        while i in range(len(alice) - 2):
            if alice[i] > bob[i] and alice[i + 1] > bob[i + 1] and alice[i + 2] > bob[i + 2]:
                print("Alice won\n")
                alice_wins+=1
                check = True
                break

        # Check for three consecutive wins for Bob only if Alice didn't win.
        if check is False:
        #     for i in range(len(alice) - 2):
            if alice[i] < bob[i] and alice[i + 1] < bob[i + 1] and alice[i + 2] < bob[i + 2]:
                print("Bob won\n")
                bob_wins += 1
                check2 = True
                break

        # Initialise score for calculating when no one got three consecutive wins.
        alice_score = 0
        bob_score = 0
        # If alice and bob didn't win
        if check is False and check2 is False:
            # Calculate bob's and alice's score.
            for i in range(len(alice)):
                if alice[i] > bob[i]:
                    alice_score += i + 1
                elif alice[i] < bob[i]:
                    bob_score += i + 1

            # Check who wins overall and increment counters for alice and bob accordingly
            if alice_score > bob_score:
                alice_wins += 1
                print("Alice won with " + str(alice_score) + "\n")
            else:
                bob_wins += 1
                print("Bob won with " + str(bob_score) + "\n")

    # Print statistics
    print("Alice wins", alice_wins)
    print("Bob wins", bob_wins)

    # Save statistics to file
    file =open("statistics.txt", "a")
    file.writelines(str(alice) + "\n")
    file.writelines("Alice won " + str(alice_wins) + " times" + "\n")
    file.writelines("Bob won " + str(bob_wins) + " times" + "\n")
    file.close()
