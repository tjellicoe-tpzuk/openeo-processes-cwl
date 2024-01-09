# openEO Processes Dask Update to Support CWL

This repository defines an openEO implementation directly branched from the [openeo-processes-dask](https://github.com/Open-EO/openeo-processes-dask) repository. This previous implementation has been augmented with the introduction of
two new processes, one to convert data into a suitable format for cwl and another to execute a given cwl script on this generated data file. In order to support these processes, new process definitions and subtypes have been defined in
the spec file path. If these are deemed suitable, they can then form part of the openEO specification in future to ensure any additional implementations can also choose to support the running of CWL scripts.

## How to Use this Repository

There are two ways to test this repository, the first is to run the `minibackend_demo_cwl.ipynb` Jupyter Notebook provided under `/examples/`, make sure to run this notebook in a virtual environment with the requirements.txt file installed before. Achieve this by runner `ipython kernel install --user --name=venv` within a virtual environment named `venv`.
The second method is to run the `parse_graph.py` script which executes the process graph as a single script and saves the generated outputs locally. Currently, both of these scripts load and run the `cwl-example.json` process graph
defined under `examples/data`. However, new process graphs can be defined and updated in the scripts to test other processes as well. You can also specify a number of inputs within these json files including the CWL script location
as well as the domain if the CWL is to be executed via another application.
In order to run either of the examples that make use of an ADES deployment, either `cwl-example-ades` or `cwl-prepare-ades`, you must provide a `.env` file with a git token generated for your GitHub account. The file `.env_sample` is provided as an example of this file, please copy it and add your own generated token to this file. You also need to make sure that your minikube domain is correct in the `cwl-example-ades.json` file. You can identify this IP address by running `minikube ip` in the terminal.

## Current Issues

The scripts here are currently only functional when run as a two stage process to demonstrate that both functions work as expected independently. This is due to the fact that the data used within the openEO environment mainly consists of
datacube objects while those understood by the demonstration CWL scripts rely on STAC objects and tif files. Therefore, work is still being done to understand the best way to integrate these two data types and ensure seemless interfacing
between the openEO and CWL stages of the process graph.
