# VRP

Engineering Thesis python project that uses genetic algorithm to optimize the VRP (Vehicle Routing Problem), a classic challenge in
logistics and transportation. It aims to find efficient routes for a fleet of vehicles to deliver goods or services to a
set of customers.

## Features

- Generate/Optimize VRP problem
- Specify GA parameters
- Visualise solution
- Analyse results
- Read/Save customers to .csv file
- Perform additional optimization using 2-opt

## VRP

The optimization problem considered in this project can be described as efficiently determining routes
for a fleet of vehicles to serve a set of customers while minimizing resource consumption and time.
Vehicles start and end their routes at the same depot point, and each customer must be served exactly once.
This is a generalization of the traveling salesman problem belonging to the family of Vehicle Routing Problems (VRP).
There are various VRP variants, each considering different constraints.
The selected problem in this project assumes all vehicles are identical and does not consider maximum load capacity or
fuel constraints.
Customers differ only in location and can be visited at any time and in any order.
Typically, the objective is to minimize the total length of all routes, but in this case,
an additional goal is to achieve the shortest customer service time,
simplified to be equal to the length of the longest route.

## Genetic algorithm

The genetic algorithm is an optimization technique inspired by biological evolution.
It begins by generating a population of potential solutions, evaluating their quality using a fitness function,
and then selecting individuals for future generations.
Crossover and mutation operators introduce genetic diversity, leading to improved solutions over successive generations.
The algorithm continues until a specified number of generations or a defined stopping condition is reached.

Six crossover operators have been implemented:

- OX1 – Order Crossover
- OX2 – Order-Based Crossover
- POS – Position-Based Crossover
- PMX – Partially Mapped Crossover
- ERX – Edge Recombination Crossover
- CX – Cycle Crossover

## Requirements

- numpy
- pandas
- matplotlib

## Usage

Run the main program by executing 'main.py'.

Perform analysis by executing 'analysis.py'.

## GUI

<img src="screenshots/screen1.png" alt="GUI">
