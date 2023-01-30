# King Of the Hill Chrono Analyzer

- [King Of the Hill Chrono Analyzer](#king-of-the-hill-chrono-analyzer)
  - [1. User manual](#1-user-manual)
    - [1.1 Installation \& Usage](#11-installation--usage)
      - [1.1.1 Setup](#111-setup)
      - [1.1.2 Usage](#112-usage)
  - [2. Summary statistics \[WIP\]](#2-summary-statistics-wip)
    - [2.1 Graphs](#21-graphs)
    - [2.2 Metrics](#22-metrics)


## 1. User manual

### 1.1 Installation & Usage

**Requirements:** Need a working installation of [Python](https://www.python.org/downloads/).

The installation is quite simple. Simply clone the repo.

#### 1.1.1 Setup

This tool is made to be used alongside the **associated application: King Of The Hill Chrono**. You can get the app from this repo for now (see [releases](https://github.com/Wolgamonox/koth-ping-pong-app/releases))). This guide will be updated if it gets uploaded to official application stores. Note this makes it only available to Android users for now.

You will also need to be on the same wifi network with your laptop and your phone.

#### 1.1.2 Usage

Once you're all setup, simply launch the script `start-server.bat`. This will launch a [Flask](https://flask.palletsprojects.com/en/2.2.x/) server and open a webpage displaying a QR code (you might need to refresh the page).

To connect your phone to the server, open the app on your phone and tap on the QR code in the top-right corner (it should be <span style='color:red;'>**red**</span>, meaning it is disconnected).

Scan the QR code. The icon should turn <span style='color:green;'>**green**</span>. 

It's done! Now when you finish a game, a new tab should open in your browser with a statistic summary of your game. See the [next section](#2-summary-statistics) for more detail about this summary.

For a guide on how to use the app, check the [app readme](https://github.com/Wolgamonox/koth-ping-pong-app#readme).

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

