# King Of the Hill Chrono Analyzer

- [King Of the Hill Chrono Analyzer](#king-of-the-hill-chrono-analyzer)
  - [1. User manual](#1-user-manual)
    - [1.1 Installation \& Usage](#11-installation--usage)
  - [2. Summary statistics \[WIP\]](#2-summary-statistics-wip)
    - [2.1 Graphs](#21-graphs)
    - [2.2 Metrics](#22-metrics)


## 1. User manual

### 1.1 Installation & Usage

## 2. Summary statistics [WIP]

### 2.1 Graphs

- **Pie chart** Fraction of total time as king
- **Boxplot** Reign time
- **Barplot** Number of crowns claimed

### 2.2 Metrics

**Definitions**

- $N_p$ : number of players.
- $T$ : duration of game (in seconds)
- $C$ : total number of crowns claimed
$$C = \sum_{m=1}^{N_p} c_i$$ 

For each player $i$ :
- $\bar{t}^i$: fraction of time as king for player $i$
$$\bar{t}_i = \frac{t_i}{T} \qquad \bar{t}_i \in [0,1]$$

- $\bar{c}_i$ : normalized number of crowns claimed for player $i$
$$\bar{c}_i = \frac{c_i}{C} \qquad \bar{c}_i \in [0,1]$$

- $w_i$: binary value to indicate the last king.
$$
w_i = \begin{cases}
  1, & \text{if player i is last king} \\
  0, & \text{otherwise}
\end{cases}
$$

**Scores**

Overall linear equal weighted score:

$$
S_{e, i} = \frac{1}{3}(\bar{t}_i + \bar{c}_i + w_i) \qquad S_i \in [0,1]
$$

Overall linear weighted score:

$$
S_{w, i} = 0.5 \cdot \bar{t}_i + 0.3 \cdot \bar{c}_i + 0.2 \cdot w_i \qquad S_i \in [0,1]
$$

Overall linear weighted score with interaction:

$$
S_{wi, i} = 0.3 \cdot \bar{t}_i + 0.3 \cdot \bar{c}_i + 0.2 \cdot \bar{t}_i\bar{c}_i + 0.2 \cdot w_i \qquad S_i \in [0,1]
$$

