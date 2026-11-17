"""Target-parent information diagnostics. Finite laws, bits, standard library.

Omega_D compares endpoints; local faithfulness requires EVERY admissible
parent/conditioning-set query. No aggregate sum certifies that requirement.
"""
import itertools
import math
from collections import defaultdict

TOL = 1e-10


def cmi(law, source, target, conditioning=()):
    """CMI from a normalized finite law [(state, probability), ...]."""
    joint, xz, yz, zz = (defaultdict(float) for _ in range(4))
    for state, p in law:
        if p <= 0:
            continue
        z = tuple(state[i] for i in conditioning)
        x, y = state[source], state[target]
        joint[x, y, z] += p
        xz[x, z] += p
        yz[y, z] += p
        zz[z] += p
    value = math.fsum(p * math.log2(p * zz[z] / (xz[x, z] * yz[y, z]))
                      for (x, y, z), p in joint.items())
    if value < -1e-12:
        raise ArithmeticError("Negative CMI: " + str(value))
    return max(0.0, value)


def mutual_information(law, sources, target):
    """Aggregate sources into one variable; supports an empty source set."""
    packed = [(tuple([tuple(s[i] for i in sources), s[target]]), p)
              for s, p in law]
    return cmi(packed, 0, 1)


def audit(law, parents, target, names=None, thresholds=(1e-6, 1e-4, 1e-2)):
    parents = tuple(sorted(set(parents)))
    if target in parents:
        raise ValueError("The target column cannot also be a source column")
    if not math.isclose(math.fsum(p for _, p in law), 1, abs_tol=1e-12):
        raise ValueError("The finite law must be normalized")
    if any(p < 0 or not math.isfinite(p) for _, p in law):
        raise ValueError("Probabilities must be finite and nonnegative")
    names = names or [str(i) for i in range(len(law[0][0]))]
    rows, parent_rows = [], []
    for i in parents:
        others = tuple(j for j in parents if j != i)
        values = []
        for k in range(len(parents)):
            for z in itertools.combinations(others, k):
                v = cmi(law, i, target, z)
                row = {"parent": names[i], "conditioning": [names[j] for j in z],
                       "depth": k, "cmi_bits": v}
                values.append(row)
                rows.append(row)
        smallest = min(r["cmi_bits"] for r in values)
        parent_rows.append({"parent": names[i], "marginal_mi_bits": values[0]["cmi_bits"],
                            "minimality_margin_bits": values[-1]["cmi_bits"],
                            "local_faithfulness_margin_bits": smallest,
                            "minimizing_sets": [r["conditioning"] for r in values
                                                if abs(r["cmi_bits"]-smallest) < TOL],
                            "first_visible_depth_at_tolerance": next(
                                (r["depth"] for r in values if r["cmi_bits"] > TOL), None)})
    n = len(parents)
    total = mutual_information(law, parents, target)
    F = math.fsum(r["marginal_mi_bits"] for r in parent_rows)
    M = math.fsum(r["minimality_margin_bits"] for r in parent_rows)
    ladder = []
    for k in range(n):
        layer = [r["cmi_bits"] for r in rows if r["depth"] == k]
        ladder.append({"depth": k, "query_count": len(layer),
                       "mean_cmi_bits": math.fsum(layer)/len(layer),
                       "minimum_cmi_bits": min(layer),
                       "fraction_at_or_below_numerical_tolerance": sum(v <= TOL for v in layer)/len(layer)})
    threshold_profiles = []
    for tau in thresholds:
        layer_fractions = [sum(r["cmi_bits"] <= tau for r in rows if r["depth"] == k)
                           / sum(r["depth"] == k for r in rows) for k in range(n)]
        threshold_profiles.append({"threshold_bits": tau,
                                   "fraction_below_by_depth": layer_fractions,
                                   "equal_depth_fraction_below": math.fsum(layer_fractions)/n if n else None})
    return {"scope": "known true parents; all subsets of the other true parents; not global faithfulness",
            "number_of_parents": n, "query_count": len(rows),
            "numerical_tolerance_bits": TOL, "total_target_information_bits": total,
            "F_bits": F, "M_bits": M, "omega_D_bits": F-M,
            "B_FM": (F-M)/(F+M) if F+M > TOL else None,
            "f_normalized": F/(n*total) if n and total > TOL else None,
            "m_normalized": M/(n*total) if n and total > TOL else None,
            "local_faithfulness_floor_bits": min((r["local_faithfulness_margin_bits"] for r in parent_rows), default=None),
            "minimality_floor_bits": min((r["minimality_margin_bits"] for r in parent_rows), default=None),
            "equal_depth_mean_cmi_bits": math.fsum(r["mean_cmi_bits"] for r in ladder)/n if n else None,
            "parent_audits": parent_rows, "conditioning_ladder": ladder,
            "threshold_profiles": threshold_profiles, "all_queries": rows}
