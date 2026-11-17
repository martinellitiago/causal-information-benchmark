# Omega D: endpoints and intermediate conditioning

Companion figures for [*Shaking the causal tree: On the faithfulness and minimality assumptions beyond pairwise interactions*](https://arxiv.org/abs/2203.10665v3), by Tiago Martinelli, Diogo O. Soares-Pinto and Francisco A. Rodrigues.

![Endpoint and all-depth contrasts across copy, additive and parity dominated mixtures.](assets/omega-mixture-regions-en.png)

Each column explores a region of the same probability simplex: **copy dominated, additive dominated, or parity dominated**. The named distribution has at least 60% mixture weight. Each anchor contains 8% uniform noise. All six panels share the same vertical and color scales.

**Top row — the paper's endpoint balance:**

$$\Omega_D=F-M=3(L_0-L_2).$$

**Bottom row — the exploratory contrast including intermediate conditioning:**

$$\Delta_{\mathrm{all}}=L_0+L_1+L_2-M=I(\mathbf X;Y)-M.$$

For three sources, L₀ averages the three marginal information values, L₁ averages the six intermediate conditional information values, and L₂ averages the three fully conditioned values. Thus F = 3L₀ and M = 3L₂. Equal weight is given to each conditioning depth. The sum of the depth means equals joint mutual information by the averaged chain rule.

Each Q marks the largest absolute gap between the two contrasts found on its regional grid. These are numerical grid extrema. The bottom row aggregates intermediate information; individual zero queries still require the complete local audit.

[Download the six-panel PDF](assets/omega-mixture-regions-en.pdf) · [Endpoint surface](assets/omega-explained-en.png) · [All-depth surface](assets/omega-surface-guide-en.png) · [Derivation and figure details](docs/INFORMATION_GEOMETRY.md)

## Reproduce the figures

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dynamics-lock.txt
python -B scripts/plot_explainer.py
```

[Grid values](results/geometry/simplex.csv) · [Regional extrema](results/geometry/regional-extremes.json) · [Citation](CITATION.cff) · [MIT license](LICENSE)
