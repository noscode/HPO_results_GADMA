# Hyperparameter optimization results for GADMA

This repository contains runs of GADMA with different configurations of hyperparameters received by SMAC.

Hyperparameter is a parameter of an algorithm. The performance of each algorithm depends on its hyperparameters.

Genetic algorithm in GADMA has 10 hyperparameters overall. We performed optimization of hyperparameters using SMAC software. First round dedicated to optimization of all 10 hyperparameters failed to find better configuration than initial one. In order to archive proper grid search additional 2-6 rounds of SMAC optimization were launched.

Hyperparameter optimizatio was performed for *moments* engine in GADMA, however, configurations were validated for several engines.

The following is included:
- `scripts` - python scripts to run SMAC optimization.
- `smac_runs` - results of SMAC runs.
- `comparison_on_datasets` - comparison of genetic algorithm configurations on train and test datasets for different engines (*dadi*, *moments*, *momi2*)

## Dependencies

- [`GADMA2`](https://github.com/ctlab/GADMA) - GADMA with updated interface.
- [`deminf_data`](https://github.com/noscode/demographic_inference_data) - package with datasets for *moments* engine.
- [`SMAC3`](https://github.com/automl/SMAC3) of version 0.13.1.

To install dependencies:

```
$ pip install -r requirements.txt
```

## Scripts

This directory contains scripts that were used to run SMAC optimization for different rounds. Round 1 included all 10 hyperparameters. For rounds 2-6 two hyperparatemeters (`gen_size`, `num_init_const`) were fixed to several values in order to archive the grid search.

To rerun smac optimization (e.g. 1 round):

```
$ python3 run_smac_1round.py
```

## SMAC results

Directory `smac_runs` contains results of our SMAC runs. Each round was launched for two weeks in parallel on 10 kernels. Each parallel launch had its own incumbent. The result incumbents were compared by the value of average cost.

Script `summary.py` provides information about runs of each round:

```
$ python3 summary.py <number of round>
```

Example of summary for round 2:
```
$ python3 summary.py 2
INFO:smac.scenario.scenario.Scenario:Reading scenario file: smac3-output-2round/run_1/scenario.txt
INFO:smac.utils.io.cmd_reader.CMDReader:Output to smac3-output_2022-06-04_14:44:16_419544
INFO:root:Shared model mode: Finished loading new runs, found 21269 new runs.

Estimated costs per each incumbent (with get_instance_costs_for_config function):
                            2_YRI_CEU_6_Gut  2_BotDivMig_8_Sim  2_ExpDivNoMig_5_Sim  2_DivMig_5_Sim
Min Cost                        1066.823000        1035.905000          1503.119000     1310.931000
smac3-output-2round/run_2       1141.248676        2032.806834          2347.927054     1454.027968
smac3-output-2round/run_1       1144.375218        2253.355705          2276.273316     1471.223237
smac3-output-2round/run_4       1161.729050        2131.934633          2756.521474     1473.309016
smac3-output-2round/run_6       1161.943432        2334.410564          2654.981192     1518.442462
smac3-output-2round/run_9       1159.641459        2279.082279          2834.446360     1477.425542
smac3-output-2round/run_3       1150.891096        2368.960152          2776.490105     1472.584012
smac3-output-2round/run_8       1151.475600        2340.093866          2869.215946     1475.430818
smac3-output-2round/run_7       1159.011022        2336.741916          2881.719284     1497.274510
smac3-output-2round/run_5       1155.309697        2468.998250          2846.190433     1491.525088
smac3-output-2round/run_10      1148.530692        2573.855804          2809.213550     1460.994262

Number of runs per each incumbent:
                            2_BotDivMig_8_Sim  2_DivMig_5_Sim  2_ExpDivNoMig_5_Sim  2_YRI_CEU_6_Gut
smac3-output-2round/run_2                 130             130                  130              130
smac3-output-2round/run_1                 136             136                  136              136
smac3-output-2round/run_4                 136             137                  136              136
smac3-output-2round/run_6                 138             137                  138              137
smac3-output-2round/run_9                 109             108                  109              108
smac3-output-2round/run_3                 126             125                  126              126
smac3-output-2round/run_8                 114             115                  114              115
smac3-output-2round/run_7                 128             128                  128              128
smac3-output-2round/run_5                 117             116                  116              116
smac3-output-2round/run_10                136             136                  135              136

Incumbent configurations:
                            const_mut_rate  const_mut_str  mut_rate  mut_strength  p_crossover  p_elitism  p_mutation  p_random
smac3-output-2round/run_2         1.475288       1.302280  0.273263      0.775539     0.842128   0.954995    0.646529  0.050116
smac3-output-2round/run_1         1.262595       1.266866  0.172958      0.823437     0.386438   0.600085    0.159792  0.073320
smac3-output-2round/run_4         1.627934       1.606579  0.000149      0.653444     0.864626   0.934097    0.601728  0.554872
smac3-output-2round/run_6         1.920108       1.538222  0.223288      0.894689     0.973497   0.931526    0.315751  0.226808
smac3-output-2round/run_9         1.549317       1.455264  0.013160      0.651856     0.785719   0.977611    0.782097  0.599443
smac3-output-2round/run_3         1.274279       1.533981  0.033356      0.581459     0.704062   0.933020    0.828314  0.538755
smac3-output-2round/run_8         1.574723       1.348629  0.028402      0.603769     0.754690   0.942985    0.707727  0.543537
smac3-output-2round/run_7         1.574723       1.451258  0.000149      0.603769     0.787597   0.956812    0.763974  0.543551
smac3-output-2round/run_5         1.904359       1.510300  0.000149      0.648148     0.796360   0.934097    0.709438  0.557902
smac3-output-2round/run_10        1.581973       1.479898  0.000413      0.603075     0.754608   0.935613    0.780255  0.546509

Final overall:
                            Average cost  Sum number of runs
smac3-output-2round/run_2    1744.002633                 520
smac3-output-2round/run_1    1786.306869                 544
smac3-output-2round/run_4    1880.125718                 545
smac3-output-2round/run_6    1919.543509                 550
smac3-output-2round/run_9    1940.501976                 434
smac3-output-2round/run_3    1943.165034                 503
smac3-output-2round/run_8    1956.234840                 458
smac3-output-2round/run_7    1968.686683                 512
smac3-output-2round/run_5    1991.534883                 465
smac3-output-2round/run_10   1996.654903                 543

Total number of runs: 21269
Total number of configurations: 1080
```

## Comparison on datasets

Comparison was performed for three engines: *moments*, *dadi* and *momi2*. There were four train datasets and six test datasets. Each configuration was run 128 times for each dataset.
