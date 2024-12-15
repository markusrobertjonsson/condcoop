import matplotlib.pyplot as plt
import random


CONTROL = "Control"
TREATMENT_10P = "10P"
TREATMENT_40P = "40P"
TREATMENT_LEVEL = "Level"
TREATMENT_IMPACT = "Impact"


def sliding_average(values, sample_size):
    out = [None] * len(values)
    for i, val in enumerate(values):
        if i < sample_size:
            out[i] = sum(values[0: (i + 1)]) / (i + 1)
        else:
            out[i] = sum(values[(i - sample_size): i]) / sample_size
    return out


def get_threshold(treatment):
    if treatment in (TREATMENT_10P, TREATMENT_40P, TREATMENT_IMPACT):
        return 60
    elif treatment == TREATMENT_LEVEL:
        return random.randint(50, 70)
    else:
        return 0


def get_is_check_round(treatment):
    if treatment in (TREATMENT_40P, TREATMENT_IMPACT, TREATMENT_LEVEL):
        return random.random() < 0.4
    elif treatment == TREATMENT_10P:
        return random.random() < 0.1
    else:
        return False


class Player():
    def __init__(self, treatment):
        self.treatment = treatment

    def get_contribution(self, prev_average, fails, average_contributions):
        lcp_contribition = self.get_lcp_contribution_avg(prev_average)
        if len(fails) >= 3 and fails[-3]:
            # return max(0, min(20, lcp_contribition + 9 / 4))
            return max(0, min(20, average_contributions[-3] + 9 / 4))
        elif len(fails) >= 4 and fails[-4]:
            # return max(0, min(20, lcp_contribition + 7 / 4))
            # return max(0, min(20, average_contributions[-4] + 7 / 4))
            return max(0, min(20, average_contributions[-4] + 16 / 4))
        else:
            return max(0, min(20, lcp_contribition))

    def get_first_contribution(self):
        pass

    def get_first_contribution_avg(self):
        pass

    def get_lcp_contribution(self, prev_average):
        pass

    def get_lcp_contribution_avg(self, prev_average):
        pass


class UnconditionalCooperator(Player):
    YINTERCEPT = {CONTROL: 16.21719439, TREATMENT_10P: 17.51459397, TREATMENT_40P: 16.78084913,
                  TREATMENT_LEVEL: 18.70653308, TREATMENT_IMPACT: 17.3972948}
    SLOPE = {CONTROL: 0.039325507, TREATMENT_10P: -0.065673995, TREATMENT_40P: 0.006177229,
             TREATMENT_LEVEL: -0.020941855, TREATMENT_IMPACT: -0.02865642}
    CONTR1 = {CONTROL: 14.92105263, TREATMENT_10P: 14.72727273, TREATMENT_40P: 14.2967033,
              TREATMENT_LEVEL: 15.5375, TREATMENT_IMPACT: 14.79746835}
    YINTERCEPT_AVG = sum(list(YINTERCEPT.values())) / len(YINTERCEPT)
    SLOPE_AVG = sum(list(SLOPE.values())) / len(SLOPE)
    CONTR1_AVG = sum(list(CONTR1.values()) )/ len(CONTR1)

    def __init__(self, treatment):
        super().__init__(treatment)

    def get_first_contribution(self):
        return UnconditionalCooperator.CONTR1[self.treatment]

    def get_first_contribution_avg(self):
        return UnconditionalCooperator.CONTR1_AVG

    def get_lcp_contribution(self, prev_average):
        a = UnconditionalCooperator.YINTERCEPT[self.treatment]
        b = UnconditionalCooperator.SLOPE[self.treatment]
        return a + b * prev_average

    def get_lcp_contribution_avg(self, prev_average):
        a = UnconditionalCooperator.YINTERCEPT_AVG
        b = UnconditionalCooperator.SLOPE_AVG
        return a + b * prev_average


class ConditionalCooperator(Player):
    YINTERCEPT = {CONTROL: 2.060553218, TREATMENT_10P: 2.668407923, TREATMENT_40P: 1.984160769,
                  TREATMENT_LEVEL: -2.658563959, TREATMENT_IMPACT: 1.269983166}
    SLOPE = {CONTROL: 0.827547183, TREATMENT_10P: 0.769928283, TREATMENT_40P: 0.80767842,
             TREATMENT_LEVEL: 1.051772529, TREATMENT_IMPACT: 0.832255046}
    CONTR1 = {CONTROL: 12.38541667, TREATMENT_10P: 12.78333333, TREATMENT_40P: 12.04081633,
              TREATMENT_LEVEL: 12.11538462, TREATMENT_IMPACT: 10.85185185}
    YINTERCEPT_AVG = sum(list(YINTERCEPT.values())) / len(YINTERCEPT)
    SLOPE_AVG = sum(list(SLOPE.values())) / len(SLOPE)
    CONTR1_AVG = sum(list(CONTR1.values()) )/ len(CONTR1)

    def __init__(self, treatment):
        super().__init__(treatment)

    def get_first_contribution(self):
        return ConditionalCooperator.CONTR1[self.treatment]

    def get_first_contribution_avg(self):
        return ConditionalCooperator.CONTR1_AVG

    def get_lcp_contribution(self, prev_average):
        a = ConditionalCooperator.YINTERCEPT[self.treatment]
        b = ConditionalCooperator.SLOPE[self.treatment]
        return a + b * prev_average

    def get_lcp_contribution_avg(self, prev_average):
        a = ConditionalCooperator.YINTERCEPT_AVG
        b = ConditionalCooperator.SLOPE_AVG
        return a + b * prev_average


class FreeRider(Player):
    YINTERCEPT = {CONTROL: 1.408893192, TREATMENT_10P: 4.562105652, TREATMENT_40P: 0.623097156,
                  TREATMENT_LEVEL: 4.182532558, TREATMENT_IMPACT: 7.031233664}
    SLOPE = {CONTROL: 0.245394485, TREATMENT_10P: 0.161445329, TREATMENT_40P: 0.333341747,
             TREATMENT_LEVEL: 0.171781389, TREATMENT_IMPACT: -0.129197627}
    CONTR1 = {CONTROL: 7.111111111, TREATMENT_10P: 9.666666667, TREATMENT_40P: 5.714285714,
              TREATMENT_LEVEL: 15, TREATMENT_IMPACT: 8.333333333}
    YINTERCEPT_AVG = sum(list(YINTERCEPT.values())) / len(YINTERCEPT)
    SLOPE_AVG = sum(list(SLOPE.values())) / len(SLOPE)
    CONTR1_AVG = sum(list(CONTR1.values()) )/ len(CONTR1)

    def __init__(self, treatment):
        super().__init__(treatment)

    def get_first_contribution(self):
        return FreeRider.CONTR1[self.treatment]

    def get_first_contribution_avg(self):
        return FreeRider.CONTR1_AVG

    def get_lcp_contribution(self, prev_average):
        a = FreeRider.YINTERCEPT[self.treatment]
        b = FreeRider.SLOPE[self.treatment]
        return a + b * prev_average

    def get_lcp_contribution_avg(self, prev_average):
        a = FreeRider.YINTERCEPT_AVG
        b = FreeRider.SLOPE_AVG
        return a + b * prev_average


class Simulation():
    def __init__(self, constellation):
        self.player1 = constellation[0]
        self.player2 = constellation[1]
        self.player3 = constellation[2]
        self.player4 = constellation[3]
        assert(self.player1.treatment == self.player2.treatment == self.player3.treatment == self.player4.treatment)
        self.treatment = self.player1.treatment

        self.fails = list()
        self.contributions1 = list()
        self.contributions2 = list()
        self.contributions3 = list()
        self.contributions4 = list()

        # To plot
        self.x = list()
        self.y = list()

    def write_xy(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def run(self):
        nsteps = 200

        # Contributions in first round
        c1 = self.player1.get_first_contribution_avg()
        c2 = self.player2.get_first_contribution_avg()
        c3 = self.player3.get_first_contribution_avg()
        c4 = self.player4.get_first_contribution_avg()
        c_sum = c1 + c2 + c3 + c4
        c_avg = c_sum / 4
        
        self.write_xy(1, c_avg)
        self.check(c_sum)
        self.contributions1.append(c1)
        self.contributions2.append(c2)
        self.contributions3.append(c3)
        self.contributions4.append(c4)

        for step in range(2, nsteps):
            prev_average1 = (c2 + c3 + c4) / 3
            prev_average2 = (c1 + c3 + c4) / 3
            prev_average3 = (c1 + c2 + c4) / 3
            prev_average4 = (c1 + c2 + c3) / 3

            c1 = self.player1.get_contribution(prev_average1, self.fails, self.contributions1)
            c2 = self.player2.get_contribution(prev_average2, self.fails, self.contributions2)
            c3 = self.player3.get_contribution(prev_average3, self.fails, self.contributions3)
            c4 = self.player3.get_contribution(prev_average4, self.fails, self.contributions4)
            c_sum = c1 + c2 + c3 + c4
            c_avg = c_sum / 4

            self.write_xy(step, c_avg)
            self.check(c_sum)
            self.contributions1.append(c1)
            self.contributions2.append(c2)
            self.contributions3.append(c3)
            self.contributions4.append(c4)
    
    def check(self, c_sum):
        is_check_round = get_is_check_round(self.treatment)
        failed_check = False
        if (is_check_round):
            threshold = get_threshold(self.treatment)
            if c_sum < threshold:
                failed_check = True
        self.fails.append(failed_check)

    def plot(self, label):
        x = self.x
        y = self.y  
        # y = sliding_average(self.y, 200)
        plt.plot(x, y, label=label)


if __name__ == "__main__":
    treatments = [CONTROL, TREATMENT_10P, TREATMENT_40P, TREATMENT_LEVEL, TREATMENT_IMPACT]
    for t in treatments:
        plt.figure()

        constellations = {"3UC 1FR": [UnconditionalCooperator(t), UnconditionalCooperator(t), UnconditionalCooperator(t), FreeRider(t)],
                          "2UC 2CC": [UnconditionalCooperator(t), UnconditionalCooperator(t), ConditionalCooperator(t), ConditionalCooperator(t)],
                          "1UC 2CC 1FR": [UnconditionalCooperator(t), ConditionalCooperator(t), ConditionalCooperator(t), FreeRider(t)]
                         }

        for label, constellation in constellations.items():
            sim = Simulation(constellation)
            sim.run()
            sim.plot(label)
        plt.xlim([0, 200])    
        plt.ylim([0, 20])
        plt.grid(axis='y')
        plt.plot([0, 200], [15, 15], '--', linewidth=1, color='k')
        plt.title(t)
        plt.legend()

    # Plot LCP-lines
    treatments = [CONTROL, TREATMENT_10P, TREATMENT_40P, TREATMENT_LEVEL, TREATMENT_IMPACT]
    plt.figure()
    for t in treatments:
        cc = ConditionalCooperator(t)
        uc = UnconditionalCooperator(t)
        fr = FreeRider(t)
        x_values = list(range(21))
        y_cc = list()
        y_uc = list()
        y_fr = list()
        for x in x_values:
            y_cc.append(cc.get_lcp_contribution(x))
            y_uc.append(uc.get_lcp_contribution(x))
            y_fr.append(fr.get_lcp_contribution(x))
        plt.plot(x_values, y_cc, label="cc", color='r')
        plt.plot(x_values, y_uc, label="uc", color='g')
        plt.plot(x_values, y_fr, label="fr", color='b')
        plt.legend()
        plt.title(t)
        plt.grid()
        plt.xlim([0, 20])
        plt.ylim([0, 20])
        plt.plot(x_values, y_cc, label="cc", color='r')

    y_cc = list()
    y_uc = list()
    y_fr = list()
    for x in x_values:
        y_cc.append(cc.get_lcp_contribution_avg(x))
        y_uc.append(uc.get_lcp_contribution_avg(x))
        y_fr.append(fr.get_lcp_contribution_avg(x))
    plt.plot(x_values, y_cc, label="cc_avg", color='k', lw=3)
    plt.plot(x_values, y_uc, label="uc_avg", color='k', lw=3)
    plt.plot(x_values, y_fr, label="fr_avg", color='k', lw=3)

    plt.show()
