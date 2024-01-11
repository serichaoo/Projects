# quick arbitrage calculator

# theory: 
# suppose we have events E_1, E_2, ..., E_N, where sum(P(E_i))=1
# each event with return ratio (European Decimal Odd) R_1, R_2, ..., R_n
# where if you bet 1 unit of currency on E_i and win, you receive r_i units of currency
# suppose we have 1 unit of currency
# and bet r_1, r_2, ..., r_n for their corresponding events, where sum r_i = 1
# then, the guaranteed profit is min(R_i * r_i) - 1 over all i
# suppose min(R_i * r_i) = m
# => R_i * r_i >= m => r_i >= m / R_i for all i
# => sum(r_i) = 1 >= sum(m / R_i) = m * sum(1/R_i)
# => m <= (sum(1/R_i))^-1
# the maximum possible guaranteed minimum is m = (sum(1/R_i))^-1,
# which is obtained when r_i = (1/R_i) * (sum(1/R_i))^-1
# then, profit > 0 iff m > 1 <=> sum(1/R_i) < 1

# alternatively, informally, to not lose profit, we require R_i * r_i >= 1 for all i
# => r_i >= 1/R_i for all i, so we first take r_i = 1/R_i. If sum(r_i) >= 1, a profit
# cannot be guaranteed. Otherwise, we can scale each r_i up by a ratio such that sum(r_i) = 1,
# yielding r_i = (1/R_i) * (sum(1/R_i))^-1

bettingOddsStr = input("This script is designed to maximize the guaranteed profits " +
                "given a certain number of events, where one is guaranteed to occur " +
                "and where each event has their own (European) decimal betting odds. " +
                "Note that for these betting odds, if you invest 1 unit of currency " +
                "on an event with odds R, and it occurs, then the net profit is R-1.\n"
                "Enter the (European) decimal betting odds for every event: ")

bettingOdds = [float(ratio) for ratio in bettingOddsStr.replace(",", " ").split()]

if len(bettingOdds) == 0:
    print("You must input at least one ratio.")
    exit()
for odds in bettingOdds:
    if odds < 0:
        print("Your ratios must all be non-negative.")
        exit()

sumReciprocals = 0
for odds in bettingOdds:
    sumReciprocals += 1/odds

m = 1/sumReciprocals

if m <= 1:
    print("A profit cannot be guaranteed.")
    exit()

bettingRatios = [(1/odds) * m for odds in bettingOdds]

print("To maximize the guaranted profit, for each corresponding event, we bet by allocating the following ratios:", end = "")
for index, bettingRatio in enumerate(bettingRatios):
    print(" " + str(bettingRatio), end = "")
    if index != len(bettingRatios) - 1:
        print(",", end = "")
print(".")