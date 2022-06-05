import logging
import warnings
from functools import partial
import moments
import gadma
import os
import sys
import importlib

import numpy as np
from ConfigSpace.hyperparameters import CategoricalHyperparameter,\
                                        UniformFloatHyperparameter

# Import ConfigSpace and different types of parameters
from smac.configspace import ConfigurationSpace
from smac.facade.smac_bohb_facade import BOHB4HPO
from smac.facade.smac_hpo_facade import SMAC4HPO
# Import SMAC-utilities
from smac.scenario.scenario import Scenario

import multiprocessing
from multiprocessing import Pool

INSTANCES = [['2_DivMig_5_Sim'], ['2_ExpDivNoMig_5_Sim'],
             ['2_BotDivMig_8_Sim'], ['2_YRI_CEU_6_Gut']]

ITER_PER_PAR = 200

def load_module(dirname, filename):
    save_dir = os.path.abspath(".")
    os.chdir(os.path.abspath(dirname))
    sys.path.append(".")
    if "demographic_model" in sys.modules:
        del sys.modules["demographic_model"]
    module = importlib.import_module(
        os.path.join(dirname, filename).replace('/', '.').rstrip('.py'))
    sys.path = sys.path[:-1]
    os.chdir(save_dir)
    return module

# Target Algorithm
def gadma_from_cfg(run_id, cfg, seed, instance):
    """
    Creates gadma run from the proposed configuration.

    :param outputdir: directory with output where gadma could save its output.
    :param cfg: configuration of hyperparameters.
    :param seed: random seed.
    :param instance: instance to run gadma on.
    """
    print("RUN ON", instance)

    # Get info from instance
    module = load_module(os.path.join("demographic_inference_data", instance),
                         "main_script.py")
    data = module.data        
    model_func = module.model_func
    lower_bound = module.lower_bound
    upper_bound = module.upper_bound
    p_ids = module.par_labels
    n_par = len(lower_bound)

    engine = 'moments'

    # Remember seed
    np.random.seed(seed)

    # get number of individuals
    p_elitism = cfg["p_elitism"]
    p_mutation = cfg['p_mutation']
    p_crossover = cfg["p_crossover"]
    p_random = cfg["p_random"]
    # normalize
    summ = p_elitism + p_mutation + p_crossover + p_random
    p_elitism /= summ
    p_mutation /= summ
    p_crossover /= summ
    p_random /= summ

    gen_size = 10 #cfg['gen_size']
    n_elitism = int(gen_size * p_elitism)
    n_mutation = int(gen_size * p_mutation)
    n_crossover = int(gen_size * p_crossover)
    n_random = int(gen_size - n_elitism - n_mutation - n_crossover)

    report_file = f"current_gadma_run_{run_id}_2r"
    open(report_file, 'w').close()
    eval_file = f"eval_file_{run_id}"

    # Run gadma
    res = gadma.Inference.optimize_ga(data, model_func, engine, args=(),
                                      lower_bound=lower_bound,
                                      upper_bound=upper_bound,
                                      p_ids=p_ids,
                                      X_init=None, Y_init=None,
                                      gen_size=gen_size,
                                      mut_strength=cfg['mut_strength'],
                                      const_mut_strength=cfg['const_mut_str'],
                                      mut_rate=cfg['mut_rate'],
                                      const_mut_rate=cfg['const_mut_rate'],
                                      n_stuck_gen=10000,
                                      num_init=n_par*20,
                                      n_elitism=n_elitism,
                                      p_mutation=n_mutation/float(gen_size),
                                      p_crossover=n_crossover/float(gen_size),
                                      p_random=n_random/float(gen_size),
                                      ga_maxiter=None,
                                      ga_maxeval=n_par*ITER_PER_PAR,
                                      local_optimizer=None,
                                      ls_maxiter=None,
                                      ls_maxeval=None,
                                      verbose=1,
                                      callback=None,
                                      save_file=None,
                                      eval_file=None,
                                      report_file=report_file)
    
    return - res.y
logging.getLogger("Inference").setLevel(logging.DEBUG)
logger = logging.getLogger("SMAC")
logging.basicConfig(level=logging.INFO)  # logging.DEBUG for debug output
logging.getLogger().setLevel(logging.INFO)

# Build Configuration Space which defines all parameters and their ranges
cs = ConfigurationSpace()

# We define a few possible parameters
gen_size = CategoricalHyperparameter('gen_size', choices=[10, 50, 100],
                                     default_value=10)
mut_strength = UniformFloatHyperparameter('mut_strength', 1e-15, 1,
                                          default_value=0.2)
const_mut_strength = UniformFloatHyperparameter('const_mut_str', 1, 2,
                                                default_value=1.01)
mut_rate = UniformFloatHyperparameter('mut_rate', 1e-15, 1,
                                      default_value=0.2)
const_mut_rate = UniformFloatHyperparameter('const_mut_rate', 1, 2,
                                            default_value=1.02)
p_elitism = UniformFloatHyperparameter('p_elitism', 0, 1,
                                       default_value=0.2)
p_mutation = UniformFloatHyperparameter('p_mutation', 0, 1,
                                        default_value=0.3)
p_crossover = UniformFloatHyperparameter('p_crossover', 0, 1,
                                         default_value=0.3)
p_random = UniformFloatHyperparameter('p_random', 0, 1,
                                       default_value=0.2)
num_init_const = CategoricalHyperparameter('num_init_const', choices=[5, 10, 20],
                                     default_value=10)

# Add the parameters to configuration space
cs.add_hyperparameters([#gen_size,
                        mut_strength, const_mut_strength,
                        mut_rate, const_mut_rate, #num_init_const,
                        p_elitism, p_mutation, p_crossover, p_random])

intensifier_kwargs = {}

# Scenario object
scenario = Scenario({"run_obj": "quality",  # we optimize quality (alternatively runtime)
                     "runcount-limit": 10000,  # max. number of function evaluations;
                     "cs": cs,  # configuration space
                     "deterministic": False,
                     "shared_model": True,
                     "output_dir": "../smac_runs/smac3-output-3round/",
                     "input_psmac_dirs": "../smac_runs/smac3-output-3round/run_*",
                     "instances": INSTANCES,
                     })

i = int(sys.argv[1])
# Optimize, using a SMAC-object
print("Optimizing! Depending on your machine, this might take a few minutes.")
tae_runner = partial(gadma_from_cfg, i)
smac = SMAC4HPO(scenario=scenario, rng=np.random.RandomState(i),
                tae_runner=tae_runner, run_id = i,
                intensifier_kwargs=intensifier_kwargs,
                initial_design=None,
                initial_configurations=[cs.get_default_configuration()])

incumbent = smac.optimize()

def_costs = []
for i in INSTANCES:
    cost = smac.get_tae_runner().run(cs.get_default_configuration(), i[0])[1]
    def_costs.append(cost)
print("Value for default configuration: %.4f" % (np.mean(def_costs)))

inc_costs = []
for i in INSTANCES:
    cost = smac.get_tae_runner().run(incumbent, i[0])[1]
    inc_costs.append(cost)
print("Optimized Value: %.4f" % (np.mean(inc_costs)))
