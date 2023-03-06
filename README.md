# King Of the Hill Stats Website

- [King Of the Hill Stats Website](#king-of-the-hill-stats-website)
  - [Summary statistics](#summary-statistics)
    - [Graphs](#graphs)
    - [Score](#score)
      - [Score for the **total reign time**: $S_{\Delta t}^i$](#score-for-the-total-reign-time-s_delta-ti)
      - [Score for the **reign time**: $S_{\delta t}$](#score-for-the-reign-time-s_delta-t)
      - [Score for the **last king**: $S_{W}^i$](#score-for-the-last-king-s_wi)
  - [Deployement checklist:](#deployement-checklist)


## Summary statistics

### Graphs

- **Pie chart:** Fraction of total reign time
- **Boxplot:** Distribution of reign time
- **Barplot:** Number of crowns claimed
- **Lineplot:** Visualization of the crown transitions

### Score

$T$ : duration of game (in seconds)

For a player $i$ we have:

#### Score for the **total reign time**: $S_{\Delta t}^i$

$$\bar{S}_{\Delta t}^i =  \alpha \frac{\Delta t^i}{T}$$

where $\Delta t^i$ is the total reign time of a player $i$.

$$ S_{\Delta t}^i = \lceil \bar{S}_{\Delta t}^i \rceil \in \N$$

#### Score for the **reign time**: $S_{\delta t}$

$$\bar{S}_{\delta t}^i = \beta \sum_{k=1}^m (\delta t_k^i)^\sigma$$

where $\delta t_k^i$ is the k<sup>th</sup> reign time of a player $i$ and $m$ is the total number of reigns of a player.

$$ S_{\delta t}^i = \lceil \bar{S}_{\delta t}^i \rceil \in \N$$


#### Score for the **last king**: $S_{W}^i$

$$
S_{W}^i = \begin{cases}
  P_{LK}, & \text{if player } i \text{ is last king} \\
  0, & \text{otherwise}
\end{cases}
$$

where $P_{LK}$ are the points awarded for being last king.


**Tuning parameters**
- $\alpha \in \N$: Importance of total reign time
- $\beta \in \R$: Importance of reign time.
- $\sigma \in \R$: Also importance of reign time, exponent of the transformation function.
- $P_{LK}$: Importance of being the last king.


## Deployement checklist:

1. Pull from git
2. Run `py manage.py collectstatic`
3. Reload website on pythonanywhere