"""A specified mixture-flat triangle inside the full-support 15-simplex.

This is an illustrative information family, not a fitted causal model,
not an estimator, and not evidence of novelty of KL projections.
"""
import csv
import itertools
import json
import math
from pathlib import Path
import premise_metrics as pm

ROOT = Path(__file__).resolve().parents[1]
STATES = list(itertools.product((0,1), repeat=4))
NOISE = 0.08
RESOLUTION = 45


def anchors():
    copy, parity, additive = [], [], []
    for state in STATES:
        xs, y = state[:3], state[3]
        s = [2*x-1 for x in xs]
        cp = .5 if state in ((0,0,0,0),(1,1,1,1)) else 0
        pa = 1/8 if y == (xs[0]^xs[1]^xs[2]) else 0
        target = (1+.25*s[0]+.30*s[1]+.35*s[2])/2
        ad = (target if y else 1-target)/8
        copy.append((1-NOISE)*cp+NOISE/16)
        parity.append((1-NOISE)*pa+NOISE/16)
        additive.append((1-NOISE)*ad+NOISE/16)
    return copy, parity, additive


def law_at(copy_weight, parity_weight):
    if copy_weight < -1e-12 or parity_weight < -1e-12 or copy_weight+parity_weight > 1+1e-12:
        raise ValueError("Weights must lie in the triangle")
    a, b, c = anchors()
    third = 1-copy_weight-parity_weight
    return [(s, copy_weight*x+parity_weight*y+third*z) for s,x,y,z in zip(STATES,a,b,c)]


def fisher_matrix(copy_weight, parity_weight):
    """Natural-log Fisher metric in the two free mixture coordinates."""
    a, b, c = anchors()
    p = [prob for _,prob in law_at(copy_weight, parity_weight)]
    dr, ds = [x-z for x,z in zip(a,c)], [y-z for y,z in zip(b,c)]
    return [[math.fsum(u*v/prob for u,v,prob in zip(der1,der2,p))
             for der2 in (dr,ds)] for der1 in (dr,ds)]


def kl(p, q):
    return math.fsum(x*math.log2(x/y) for x,y in zip(p,q) if x)


def lifted_ci_projection(law, i, target, subset):
    """KL-optimal CI marginal, lifted with the original remaining conditional."""
    from collections import defaultdict
    pxyz, pxz, pyz, pz = (defaultdict(float) for _ in range(4))
    for state, p in law:
        z = tuple(state[k] for k in subset)
        x, y = state[i], state[target]
        pxyz[x,y,z] += p
        pxz[x,z] += p
        pyz[y,z] += p
        pz[z] += p
    result = []
    for state, p in law:
        z = tuple(state[k] for k in subset)
        x,y = state[i],state[target]
        qxyz = pxz[x,z]*pyz[y,z]/pz[z]
        result.append((state, p*qxyz/pxyz[x,y,z]))
    return result


def grid(resolution=RESOLUTION):
    rows = []
    for ir in range(resolution+1):
        for js in range(resolution+1-ir):
            r,s = ir/resolution, js/resolution
            law = law_at(r,s)
            d = pm.audit(law, (0,1,2), 3)
            f = fisher_matrix(r,s)
            floor = d["local_faithfulness_floor_bits"]
            minimizing = [q for q in d["all_queries"] if abs(q["cmi_bits"]-floor)<1e-10]
            rows.append({"copy_weight": r, "parity_weight": s, "additive_weight": 1-r-s,
                         "F_bits": d["F_bits"], "M_bits": d["M_bits"], "omega_D_bits": d["omega_D_bits"],
                         "equal_depth_mean_bits": d["equal_depth_mean_cmi_bits"],
                         "delta_ladder_bits": 3*d["equal_depth_mean_cmi_bits"]-d["M_bits"],
                         "local_faithfulness_floor_bits": floor, "minimality_floor_bits": d["minimality_floor_bits"],
                         "total_information_bits": d["total_target_information_bits"],
                         "fisher_area_density": math.sqrt(f[0][0]*f[1][1]-f[0][1]**2),
                         "weakest_queries": json.dumps(minimizing, separators=(",", ":"))})
    return rows


def main():
    rows = grid()
    output = ROOT/"results/geometry"
    output.mkdir(parents=True, exist_ok=True)
    with (output/"simplex.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    metadata = {"scope": "Illustrative mixture family; not a causal-discovery experiment", "sources": 3, "target": 1,
                "full_probability_simplex_dimension": 15, "mixture_slice_dimension": 2,
                "uniform_contamination": NOISE, "grid_resolution": RESOLUTION, "grid_points": len(rows),
                "minimum_joint_probability": min(p for r,s in ((1,0),(0,1),(0,0)) for _,p in law_at(r,s)),
                "fisher_log_units": "natural; KL_bits locally equals quadratic_form/(2 ln 2)",
                "delta_ladder_status": "Exploratory all-depth contrast, not a new validated faithfulness metric",
                "minimum_minimality_floor_over_grid": min(r["minimality_floor_bits"] for r in rows)}
    (output/"metadata.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print(json.dumps(metadata))


if __name__ == "__main__":
    main()
