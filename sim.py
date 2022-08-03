import matplotlib.pyplot as plt
import random

# mean coeff	Contributor	Conditional	Free rider
# Control	0.039325507	0.827547183	0.245394485
# 10P	-0.065673995	0.769928283	0.161445329
# 40P	0.006177229	0.80767842	0.333341747
# Level	-0.020941855	1.051772529	0.171781389
# Impact	-0.02865642	0.832255046	-0.129197627

# mean yintercept	Contributor	Conditional	Free rider
# Control	16,21719439	2.060553218	1.408893192
# 10P	17,51459397	2.668407923	4.562105652
# 40P	16,78084913	1.984160769	0.623097156
# Level	18,70653308	-2.658563959	4.182532558
# Impact	17,3972948	1.269983166	7.031233664

CONTROL = "Control"
TREATMENT_10P = "10P"
TREATMENT_40P = "40P"
TREATMENT_LEVEL = "Level"
TREATMENT_IMPACT = "Impact"


def get_threshold(treatment):
    if treatment in (TREATMENT_10P, TREATMENT_40P, TREATMENT_IMPACT):
        return 60
    elif treatment == TREATMENT_LEVEL:
        return random.randint(60, 70)
    else:
        return 0


def get_is_check_round(treatment):
    if treatment in (TREATMENT_40P, TREATMENT_IMPACT, TREATMENT_LEVEL):
        return random.random() < 0.6
    elif treatment == TREATMENT_10P:
        return random.random() < 0.1
    else:
        return False


class Player():
    def __init__(self, treatment):
        self.treatment = treatment

    def get_contribution(self, prev_average, fails):
        lcp_contribition = self.get_lcp_contribution(prev_average)
        if len(fails) >= 3 and fails[-3]:
            return lcp_contribition + 9 / 4
        elif len(fails) >= 4 and fails[-4]:
            return lcp_contribition + 7 / 4
        else:
            return lcp_contribition

    def get_lcp_contribution(self, prev_average):
        raise Exception()


class UnconditionalCooperator(Player):
    YINTERCEPT = {CONTROL: 16.21719439, TREATMENT_10P: 17.51459397, TREATMENT_40P: 16.78084913,
                  TREATMENT_LEVEL: 18.70653308, TREATMENT_IMPACT: 17.3972948}
    SLOPE = {CONTROL: 0.039325507, TREATMENT_10P: -0.065673995, TREATMENT_40P: 0.006177229,
             TREATMENT_LEVEL: -0.020941855, TREATMENT_IMPACT: -0.02865642}

    def __init__(self, treatment):
        super().__init__(treatment)

    def get_lcp_contribution(self, prev_average):
        a = UnconditionalCooperator.YINTERCEPT[self.treatment]
        b = UnconditionalCooperator.SLOPE[self.treatment]
        return a + b * prev_average


class ConditionalCooperator(Player):
    YINTERCEPT = {CONTROL: 2.060553218, TREATMENT_10P: 2.668407923, TREATMENT_40P: 1.984160769,
                  TREATMENT_LEVEL: -2.658563959, TREATMENT_IMPACT: 1.269983166}
    SLOPE = {CONTROL: 0.827547183, TREATMENT_10P: 0.769928283, TREATMENT_40P: 0.80767842,
             TREATMENT_LEVEL: 1.051772529, TREATMENT_IMPACT: 0.832255046}

    def __init__(self, treatment):
        super().__init__(treatment)

    def get_lcp_contribution(self, prev_average):
        a = ConditionalCooperator.YINTERCEPT[self.treatment]
        b = ConditionalCooperator.SLOPE[self.treatment]
        return a + b * prev_average


class FreeRider(Player):
    YINTERCEPT = {CONTROL: 1.408893192, TREATMENT_10P: 4.562105652, TREATMENT_40P: 0.623097156,
                  TREATMENT_LEVEL: 4.182532558, TREATMENT_IMPACT: 7.031233664}
    SLOPE = {CONTROL: 0.245394485, TREATMENT_10P: 0.161445329, TREATMENT_40P: 0.333341747,
             TREATMENT_LEVEL: 0.171781389, TREATMENT_IMPACT: -0.129197627}

    def __init__(self, treatment):
        super().__init__(treatment)

    def get_lcp_contribution(self, prev_average):
        a = FreeRider.YINTERCEPT[self.treatment]
        b = FreeRider.SLOPE[self.treatment]
        return a + b * prev_average


class Simulation():
    def __init__(self, player1, player2, player3, player4):
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        assert(player1.treatment == player2.treatment == player3.treatment == player4.treatment)
        self.treatment = player1.treatment

        self.fails = list()

        # To plot
        self.x = list()
        self.y = list()

    def write_xy(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def run(self):
        nsteps = 200        

        # Contributions in first round
        c1 = 10
        c2 = 10
        c3 = 10
        c4 = 10
        c_sum = c1 + c2 + c3 + c4
        c_avg = c_sum / 4
        
        self.write_xy(1, c_avg)
        self.check(c_sum)

        for step in range(2, nsteps):
            prev_average1 = (c2 + c3 + c4) / 3
            prev_average2 = (c1 + c3 + c4) / 3
            prev_average3 = (c1 + c2 + c4) / 3
            prev_average4 = (c1 + c2 + c3) / 3

            c1 = self.player1.get_contribution(prev_average1, self.fails)
            c2 = self.player2.get_contribution(prev_average2, self.fails)
            c3 = self.player3.get_contribution(prev_average3, self.fails)
            c4 = self.player3.get_contribution(prev_average4, self.fails)
            c_sum = c1 + c2 + c3 + c4
            c_avg = c_sum / 4

            self.write_xy(step, c_avg)
            self.check(c_sum)
    
    def check(self, c_sum):
        is_check_round = get_is_check_round(self.treatment)
        failed_check = False
        if (is_check_round):
            threshold = get_threshold(self.treatment)
            if c_sum < threshold:
                failed_check = True
        self.fails.append(failed_check)

    def plot(self):
        plt.plot(self.x, self.y)
        plt.show()


if __name__ == "__main__":
    treatment = TREATMENT_40P
    player1 = UnconditionalCooperator(treatment)
    player2 = ConditionalCooperator(treatment)
    player3 = FreeRider(treatment)
    player4 = FreeRider(treatment)
    sim = Simulation(player1, player2, player3, player4)
    sim.run()
    sim.plot()
