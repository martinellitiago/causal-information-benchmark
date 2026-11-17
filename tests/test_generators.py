import math
import unittest
from omegad import DiscreteModel, BinaryProcess, available_processes

class GeneratorTests(unittest.TestCase):
    def test_noisy_parity_analytic_profile(self):
        for n in (2,3,4):
            model=DiscreteModel('parity',n_sources=n,noise=.1)
            law=model.population()
            self.assertAlmostEqual(sum(p for _,p in law),1)
            report=model.diagnostics()
            expected=1+.1*math.log2(.1)+.9*math.log2(.9)
            self.assertAlmostEqual(report['F_bits'],0)
            self.assertAlmostEqual(report['M_bits'],n*expected)
            self.assertEqual(report['query_count'],n*2**(n-1))
            self.assertEqual(len(model.ground_truth()),n)

    def test_iid_validation_and_reproducibility(self):
        for rule in ('parity','majority','additive','product','mixed'):
            model=DiscreteModel(rule)
            self.assertEqual(model.sample(20,3),model.sample(40,3)[:20])
            self.assertGreater(min(p for _,p in model.population()),0)
        for kwargs in ({'noise':0},{'noise':.5},{'n_sources':0},{'n_sources':True},{'coupling':float('nan')},{'rule':'unknown'}):
            with self.assertRaises(ValueError):DiscreteModel(**kwargs)
        with self.assertRaises(ValueError):DiscreteModel('majority',n_sources=2)

    def test_temporal_population_stationarity_and_functional_truth(self):
        self.assertEqual(len(available_processes()),11)
        for name in available_processes():
            model=BinaryProcess(name)
            report=model.diagnostics()
            self.assertLess(report['stationary']['stationarity_L1_residual'],1e-12)
            self.assertAlmostEqual(sum(p for _,p in model.population()),1)
            self.assertEqual(set(model.ground_truth()),set(map(tuple,report['true_lagged_edges'])))
            self.assertEqual(model.sample(20,3),model.sample(40,3)[:20])
        null=BinaryProcess('independent_dynamics')
        self.assertEqual(null.ground_truth(),[])
        self.assertIsNone(null.diagnostics()['target_diagnostics']['B_FM'])

    def test_memory_changes_edges_not_product_parent_profile(self):
        zero=BinaryProcess('kinetic_product',persistence=0)
        sticky=BinaryProcess('kinetic_product',persistence=.9)
        self.assertNotIn(('V1','V1',1),zero.ground_truth())
        self.assertIn(('V1','V1',1),sticky.ground_truth())
        for a,b in zip(zero.diagnostics()['target_diagnostics']['all_queries'],sticky.diagnostics()['target_diagnostics']['all_queries']):
            self.assertAlmostEqual(a['cmi_bits'],b['cmi_bits'])
        parameters=sticky.parameters;parameters['persistence']=0
        self.assertEqual(sticky.parameters['persistence'],.9)

    def test_intermediate_cancellation(self):
        d=BinaryProcess('intermediate_cancellation').diagnostics()['target_diagnostics']
        self.assertGreater(min(r['marginal_mi_bits'] for r in d['parent_audits']),0)
        self.assertGreater(d['minimality_floor_bits'],0)
        self.assertLess(d['local_faithfulness_floor_bits'],1e-10)

if __name__=='__main__':unittest.main()
