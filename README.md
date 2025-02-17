# Cooperation in the face of disaster: Code for the agent-based simulation, and experiment data
This repository contains the Python source code for the simulations as well as the experiment data in the paper "Cooperation in the face of disaster" by Marijane Luistro Jonsson and Markus Jonsson.

## Description of simulation
This is an agent-based simulation of a population of 4,000 players divided into 1,000 groups with four players in each group.
Each group interacts in 200 rounds of the baseline public-goods experiment used in all treatment groups (_Control_, _10P_, _40P_, _Impact_, and _Level_) described in the manuscript. 

- Each player is assigned a player-type based on the empirically found distribution of the four player-types _Unconditional Cooperator_ (UC), _Conditional Cooperator_ (CC), and _Free-rider_ (FR).
- Each player-type uses the LCP profile determined by the emprrically found average profile for that player-type.
- In each round each player gives a contribution as an integer 0-20, computed using the player's LCP profile and the average contribution in the previous round of the other group members. In the first round, the average initial contributions for each player type is used.

Figure 6 in the manuscript shows varying proportions of UC ($x$-axis), where the CC/FR ratio is fixed to the empirically found value 215/21 = 10.2. After 200 rounds (where we observed that the contribution levels had converged) the simulation was terminated and the converged group contribution $g$ was compared to the threshold level 60. If $g < 60$, the group is considered unsuccessful, otherwise successful. The proportion of successful groups in the population is then used as a measure of the population's success

### How to produce Figure 6 (on Linux)
```
git clone git@github.com:markusrobertjonsson/condcoop.git
cd condcoop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python fig6.py
```

## Description of experiment data
The file `Data_Main.xlsx` contains the contributions of the experiment participants in all treatments. 

- The sheet `DiffTreatments` contains the data for the treatments *Control*, *10P*, *40P*, *Impact*, and *Level* collected in Sweden and Phiippines.
- The sheet `DiffProb` contains the data for the treatments *Control*, *10P*, *40P*, *70P*, and *100P* collected in Sweden.

## License Information
- **Code**: This repository's source code is licensed under the MIT License. See the [LICENSE](LICENSE) file.
- **Data**: The data used in this research is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0). See the [LICENSE-DATA](LICENSE-DATA) file.
