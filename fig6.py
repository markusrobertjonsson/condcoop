import numpy as np
import matplotlib.pyplot as plt
import random


CONTROL = "Control"
TREATMENT_10P = "10P"
TREATMENT_40P = "40P"
TREATMENT_LEVEL = "Level"
TREATMENT_IMPACT = "Impact"

UNCONDITIONAL_COOPERATOR = "UC"
CONDITIONAL_COOPERATOR = "CC"
FREE_RIDER = "FR"


def sliding_average(values, sample_size):
    out = [None] * len(values)
    for i, val in enumerate(values):
        if i < sample_size:
            out[i] = sum(values[0: (i + 1)]) / (i + 1)
        else:
            out[i] = sum(values[(i - sample_size): i]) / sample_size
    return out


class Distribution():
    def __init__(self, uc, fr):
        assert(uc <= 1 and uc >= 0)
        assert(fr <= 1 and fr >= 0)
        assert(uc + fr <= 1)
        self.uc = uc        
        self.fr = fr
        self.cc = 1 - (uc + fr)

    def _sample(self):
        r = random.random()
        if r < self.uc:
            return UNCONDITIONAL_COOPERATOR
        elif r < self.uc + self.fr:
            return FREE_RIDER
        else:
            return CONDITIONAL_COOPERATOR

    def sample_group(self):
        group = []
        for _ in range(4):
            s = self._sample()
            if s == UNCONDITIONAL_COOPERATOR:
                player = UnconditionalCooperator()
            elif s == CONDITIONAL_COOPERATOR:
                player = ConditionalCooperator()
            else:
                player = FreeRider()
            group.append(player)
        return Group(group)


class Population():
    def __init__(self, size, distribution):
        assert(size % 4 == 0)
        self.size = size
        self.n_groups = size // 4
        self.distribution = distribution
        self._create_groups()
    
    def _create_groups(self):
        self.groups = []
        for i in range(self.n_groups):
            group = self.distribution.sample_group()
            self.groups.append(group)


class Group():
    def __init__(self, players):
        self.players = players  # List of Player objects

        # Result
        self.final_group_contribution = None

    def _get_others_contributions(self, player):
        others_contributions = []
        for other_player in self.players:
            if other_player != player:
                others_contributions.append(player.last_contribution)
        assert(len(others_contributions) == 3)
        return others_contributions

    def run(self, n_steps):
        # Contributions in first round
        for player in self.players:
            player.get_first_contribution_avg()
        
        for step in range(2, n_steps):
            for player in self.players:
                others_contributions = self._get_others_contributions(player)
                player.others_average = sum(others_contributions) / len(others_contributions)
            
            c = []
            for player in self.players:
                c.append(player.get_contribution())
            
            if step == n_steps - 1:
                c_sum = sum(c)
                self.final_group_contribution = c_sum


class Player():
    def __init__(self):
        self.last_contribution = None

    def get_contribution(self):
        lcp_contribution = self.get_lcp_contribution_avg()
        self.last_contribution = lcp_contribution
        return max(0, min(20, lcp_contribution))

    def get_first_contribution_avg(self):
        c = self._get_first_contribution_avg()
        self.last_contribution = c
        return c

    def _get_first_contribution_avg(self):
        assert(False)

    def get_lcp_contribution_avg(self):
        assert(False)


class UnconditionalCooperator(Player):
    YINTERCEPT = {TREATMENT_10P: 17.51459397, TREATMENT_40P: 16.78084913,
                  TREATMENT_LEVEL: 18.70653308, TREATMENT_IMPACT: 17.3972948} #{CONTROL: 16.21719439, 
    SLOPE = {TREATMENT_10P: -0.065673995, TREATMENT_40P: 0.006177229,
             TREATMENT_LEVEL: -0.020941855, TREATMENT_IMPACT: -0.02865642}  # CONTROL: 0.039325507, 
    CONTR1 = {TREATMENT_10P: 14.72727273, TREATMENT_40P: 14.2967033,
              TREATMENT_LEVEL: 15.5375, TREATMENT_IMPACT: 14.79746835}  # CONTROL: 14.92105263
    YINTERCEPT_AVG = sum(list(YINTERCEPT.values())) / len(YINTERCEPT)
    SLOPE_AVG = sum(list(SLOPE.values())) / len(SLOPE)
    CONTR1_AVG = sum(list(CONTR1.values())) / len(CONTR1)

    def __init__(self):
        super().__init__()

    def _get_first_contribution_avg(self):
        return UnconditionalCooperator.CONTR1_AVG

    def get_lcp_contribution_avg(self):
        a = UnconditionalCooperator.YINTERCEPT_AVG
        b = UnconditionalCooperator.SLOPE_AVG
        return a + b * self.others_average


class ConditionalCooperator(Player):
    YINTERCEPT = {TREATMENT_10P: 2.668407923, TREATMENT_40P: 1.984160769,
                  TREATMENT_LEVEL: -2.658563959, TREATMENT_IMPACT: 1.269983166}  # CONTROL: 2.060553218, 
    SLOPE = {TREATMENT_10P: 0.769928283, TREATMENT_40P: 0.80767842,
             TREATMENT_LEVEL: 1.051772529, TREATMENT_IMPACT: 0.832255046}  # CONTROL: 0.827547183, 
    CONTR1 = {TREATMENT_10P: 12.78333333, TREATMENT_40P: 12.04081633,
              TREATMENT_LEVEL: 12.11538462, TREATMENT_IMPACT: 10.85185185}  # CONTROL: 12.38541667
    YINTERCEPT_AVG = sum(list(YINTERCEPT.values())) / len(YINTERCEPT)
    SLOPE_AVG = sum(list(SLOPE.values())) / len(SLOPE)
    CONTR1_AVG = sum(list(CONTR1.values())) / len(CONTR1)

    def __init__(self):
        super().__init__()

    def _get_first_contribution_avg(self):
        return ConditionalCooperator.CONTR1_AVG

    def get_lcp_contribution_avg(self):
        a = ConditionalCooperator.YINTERCEPT_AVG
        b = ConditionalCooperator.SLOPE_AVG
        return a + b * self.others_average


class FreeRider(Player):
    YINTERCEPT = {TREATMENT_10P: 4.562105652, TREATMENT_40P: 0.623097156,
                  TREATMENT_LEVEL: 4.182532558, TREATMENT_IMPACT: 7.031233664}  # CONTROL: 1.408893192
    SLOPE = {TREATMENT_10P: 0.161445329, TREATMENT_40P: 0.333341747,
             TREATMENT_LEVEL: 0.171781389, TREATMENT_IMPACT: -0.129197627}  # CONTROL: 0.245394485
    CONTR1 = {TREATMENT_10P: 9.666666667, TREATMENT_40P: 5.714285714,
              TREATMENT_LEVEL: 15, TREATMENT_IMPACT: 8.333333333}  # CONTROL: 7.111111111, 
    YINTERCEPT_AVG = sum(list(YINTERCEPT.values())) / len(YINTERCEPT)
    SLOPE_AVG = sum(list(SLOPE.values())) / len(SLOPE)
    CONTR1_AVG = sum(list(CONTR1.values())) / len(CONTR1)

    def __init__(self):
        super().__init__()

    def _get_first_contribution_avg(self):
        return FreeRider.CONTR1_AVG

    def get_lcp_contribution_avg(self):
        a = FreeRider.YINTERCEPT_AVG
        b = FreeRider.SLOPE_AVG
        return a + b * self.others_average


class Simulation():
    def __init__(self, size, distribution):
        self.population = Population(size, distribution)

    def run(self, n_steps):
        for group in self.population.groups:
            group.run(n_steps)

    def get_proportion_successful_groups(self):
        p = 0
        for group in self.population.groups:
            if group.final_group_contribution >= 60:
                p += 1
        p /= self.population.n_groups        
        return p


def vary_only_uc():
    def _compute_fr(uc):
        # Empirically: UC:0.56, CC:0.358, FR:0.035, so CC/FR=10.2
        fr = (1 - uc) / 11.2
        cc = 10.2 * fr
        assert(abs(uc + fr + cc - 1) < 0.0001), f"{uc + fr + cc} is not 1."
        return fr

    RESOLUTION = 20
    ucs = [i / RESOLUTION for i in range(RESOLUTION + 1)]
    ps = []
    for uc in ucs:
        fr = _compute_fr(uc)
        distribution = Distribution(uc, fr)
        simulation = Simulation(4000, distribution)
        simulation.run(200)
        p = simulation.get_proportion_successful_groups()
        ps.append(p)
        # print(f"{uc},{fr} => {p}")
    plt.plot(ucs, ps)
    plt.plot([0.56, 0.56], [0, 1], color='k')
    plt.grid()
    plt.xlabel("Proportion unconditional cooperators")
    plt.ylabel("Proportion successful groups in population")
    plt.show()


def vary_uc_fr():
    RESOLUTION = 100
    ucs = [i / RESOLUTION for i in range(RESOLUTION + 1)]
    frs = [i / RESOLUTION for i in range(RESOLUTION + 1)]

    ps = []
    for uc in ucs:
        for fr in frs:
            if uc + fr > 1:
                p = 0
            else:
                distribution = Distribution(uc, fr)
                simulation = Simulation(4000, distribution)
                simulation.run(100)
                p = simulation.get_proportion_successful_groups()
            ps.append(p)
            # print(f"{uc},{fr} => {p}")

    ps = np.array(ps)
    # maxp = max(ps)
    Z = ps.reshape(len(ucs), len(frs))
    # UC, FR = np.meshgrid(ucs, frs)
    FR, UC = np.meshgrid(ucs, frs)

    # print(UC)
    # print(FR)
    # print(Z)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    levels = np.linspace(0, 1, 11)
    c = ax.contourf(UC, FR, Z, levels=levels, cmap=plt.get_cmap(name='jet', lut=1024))

    # tickdiff = (levels[1] - levels[0]) / 2
    cbarticks = [x for x in levels]
    cbar = plt.colorbar(c, ticks=cbarticks, ticklocation=None)
    cbarticklabels = [str(x) for x in levels]
    cbar.set_ticklabels(cbarticklabels)  # vertically oriented colorbar
    cbar.ax.tick_params(bottom=False, top=False, left=False, right=False, which='both')
    
    plt.title("Proportion successful groups")
    plt.xlabel("$UC$")
    plt.ylabel("$FR$")
    plt.show()


if __name__ == "__main__":
    # vary_uc_fr()
    vary_only_uc()
