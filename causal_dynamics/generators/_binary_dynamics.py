"""Four-node lag-one binary mechanisms; synchronous independent innovations."""
import itertools
import math
import random
from ..measures import information as pm

NODES = ["V1", "V2", "V3", "V4"]
STATES = list(itertools.product((0, 1), repeat=4))
INDEX = {x: i for i, x in enumerate(STATES)}
TARGET = 3


def cases():
    return [
        {"id": "kinetic_pairwise", "label": "Kinetic / additive", "family": "kinetic", "persistence": 0.65,
         "terms": [[[0], 0.6], [[1], -0.5]]},
        {"id": "kinetic_product", "label": "Kinetic / product", "family": "kinetic", "persistence": 0.65,
         "terms": [[[0, 1], 0.8]]},
        {"id": "kinetic_mixed", "label": "Kinetic / mixed", "family": "kinetic", "persistence": 0.65,
         "terms": [[[0, 1], 0.8], [[0], 0.18], [[1], 0.14]]},
        {"id": "boolean_parity", "label": "Boolean / parity", "family": "boolean", "persistence": 0.65,
         "rule": "parity", "error": 0.1},
        {"id": "boolean_majority", "label": "Boolean / majority", "family": "boolean", "persistence": 0.65,
         "rule": "majority", "error": 0.1},
        {"id": "redundant_drivers", "label": "Redundant drivers", "family": "correlated", "copy_error": 0.005,
         "rule": "additive"},
        {"id": "intermediate_cancellation", "label": "Intermediate CI zero", "family": "correlated", "copy_error": 0.1,
         "rule": "intermediate"},
        {"id": "sis_pairwise", "label": "SIS / pairwise", "family": "contagion", "recovery": 0.35,
         "import_probability": 0.04, "pair_rate": 0.35, "group_rate": 0.0,
         "edges": [[0, 1], [1, 2], [2, 3], [0, 3]], "triangles": []},
        {"id": "sis_simplicial", "label": "SIS / mixed simplicial", "family": "contagion", "recovery": 0.35,
         "import_probability": 0.04, "pair_rate": 0.15, "group_rate": 0.7,
         "edges": [[0, 1], [1, 2], [2, 3], [0, 3], [1, 3]], "triangles": [[0, 1, 3], [1, 2, 3]]},
        {"id": "sis_group_only", "label": "SIS / group infection", "family": "contagion", "recovery": 0.35,
         "import_probability": 0.04, "pair_rate": 0.0, "group_rate": 0.9,
         "edges": [], "triangles": [[0, 1, 3], [1, 2, 3]]},
        {"id": "independent_dynamics", "label": "Independent null", "family": "null"},
    ]


def probabilities(case, state):
    s = [2*x-1 for x in state]
    family = case["family"]
    if family == "null":
        return [0.5]*4
    if family in ("kinetic", "boolean"):
        p = [(1+case["persistence"]*s[i])/2 for i in range(3)]
        if family == "kinetic":
            field = math.fsum(c*math.prod(s[i] for i in group) for group, c in case["terms"])
            target = 1/(1+math.exp(-2*field))
        else:
            bit = sum(state[:3]) % 2 if case["rule"] == "parity" else int(sum(state[:3]) >= 2)
            target = 1-case["error"] if bit else case["error"]
        return p+[target]
    if family == "correlated":
        copy = 1-case["copy_error"] if state[0] else case["copy_error"]
        if case["rule"] == "additive":
            target = 1/(1+math.exp(-2*0.65*(s[1]+s[2])))
        else:
            target = (1+0.35*s[2]+0.45*s[1]*s[0]+0.10*s[0])/2
        return [0.5, copy, copy, target]
    if family != "contagion":
        raise ValueError(family)
    p = []
    for i in range(4):
        if state[i]:
            p.append(1-case["recovery"])
            continue
        pair_count = sum(state[b if a == i else a] for a, b in case["edges"] if i in (a, b))
        group_count = sum(math.prod(state[j] for j in tri if j != i)
                          for tri in case["triangles"] if i in tri)
        hazard = case["pair_rate"]*pair_count + case["group_rate"]*group_count
        p.append(1-(1-case["import_probability"])*math.exp(-hazard))
    return p


def kernel(case):
    q = [probabilities(case, x) for x in STATES]
    if not all(0 < p < 1 for ps in q for p in ps):
        raise ValueError("Every transition probability must have full support")
    transition = [[math.prod(p if b else 1-p for b, p in zip(y, ps))
                   for y in STATES] for ps in q]
    return q, transition


def stationary(transition):
    pi = [1/len(STATES)]*len(STATES)
    for iteration in range(20000):
        nxt = [math.fsum(pi[i]*transition[i][j] for i in range(len(pi))) for j in range(len(pi))]
        norm = math.fsum(nxt)
        nxt = [p/norm for p in nxt]
        if sum(abs(a-b) for a, b in zip(pi, nxt)) < 1e-14:
            residual = sum(abs(math.fsum(nxt[i]*transition[i][j] for i in range(len(pi)))-nxt[j])
                           for j in range(len(pi)))
            return nxt, {"iterations": iteration+1, "stationarity_L1_residual": residual,
                         "minimum_stationary_probability": min(nxt)}
        pi = nxt
    raise ArithmeticError("Stationary distribution did not converge")


def ground_truth(q):
    edges, responses = [], []
    for j in range(4):
        for i in range(4):
            effect = max(abs(q[idx][j]-q[INDEX[x[:i]+(1-x[i],)+x[i+1:]]][j])
                         for idx, x in enumerate(STATES))
            if effect > 1e-13:
                edges.append([NODES[i], NODES[j], 1])
                responses.append({"source": NODES[i], "target": NODES[j], "lag": 1,
                                  "max_controlled_probability_change": effect})
    return edges, responses


def analyze(case):
    q, transition = kernel(case)
    pi, convergence = stationary(transition)
    edges, responses = ground_truth(q)
    parents = [NODES.index(a) for a, b, lag in edges if b == NODES[TARGET]]
    law = [(x+(y,), pi[k]*(q[k][TARGET] if y else 1-q[k][TARGET]))
           for k, x in enumerate(STATES) for y in (0, 1)]
    diagnostic = pm.audit(law, parents, 4, [n+"(t)" for n in NODES]+["V4(t+1)"])
    candidate = [{"source": NODES[i], "marginal_mi_bits": pm.cmi(law, i, 4),
                  "full_past_cmi_bits": pm.cmi(law, i, 4, tuple(j for j in range(4) if j != i))}
                 for i in range(4)]
    return {"id": case["id"], "label": case["label"], "family": case["family"], "mechanism": case,
            "true_lagged_edges": edges, "controlled_response_audit": responses,
            "target": "V4(t+1)", "true_target_parents": [NODES[i]+"(t)" for i in parents],
            "stationary": convergence, "stationary_probabilities": pi,
            "target_diagnostics": diagnostic, "all_past_candidate_queries": candidate,
            "population_marginal_screen_target_recall": sum(candidate[i]["marginal_mi_bits"] > pm.TOL for i in parents)/len(parents) if parents else None,
            "population_full_past_target_recall": sum(candidate[i]["full_past_cmi_bits"] > pm.TOL for i in parents)/len(parents) if parents else None}


def sample(case, rows, seed, pi=None):
    if rows < 2:
        raise ValueError("At least two time points required")
    rng = random.Random(seed)
    if pi is None:
        pi, _ = stationary(kernel(case)[1])
    u, cum = rng.random(), 0.0
    state = STATES[-1]
    for x, p in zip(STATES, pi):
        cum += p
        if u <= cum:
            state = x
            break
    data = [state]
    for _ in range(rows-1):
        state = tuple(int(rng.random() < p) for p in probabilities(case, state))
        data.append(state)
    return data
