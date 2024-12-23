"""Module with helper functions for the app."""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from geopy import distance
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def generate_distance_matrix(customers_df: pd.DataFrame) -> list:
    """Take a dataframe with coordinates as input and create a distance matrix.

    Args:
        customers_df (pd.DataFrame): pandas DataFrame with lat and lon info.

    Returns:
        list: a n * n matrix containing the distances in km between locations.

    """
    customers_list = list(
        customers_df[["lat", "lon"]].itertuples(index=False, name=None),
    )

    return [
        [round(distance.distance(i, j).km) for j in customers_list]
        for i in customers_list
    ]


def create_data_model(
    customers_df: pd.DataFrame, vehicles_df: pd.DataFrame,
) -> dict:
    """Create a dictionary to store all the data for the VRP.

    Args:
        customers_df (pd.DataFrame): customers pandas dataframe
        vehicles_df (pd.DataFrame): vehicles pandas dataframe

    Returns:
        dict: a dict to contain all the required data

    """
    data = {}

    data["distance_matrix"] = generate_distance_matrix(customers_df)
    data["demands"] = customers_df["demands"].to_list()
    data["vehicle_capacities"] = vehicles_df["capacity"].to_list()
    data["num_vehicles"] = vehicles_df.shape[0]
    data["depot"] = 0
    data["vehicle_name"] = vehicles_df["id"].to_list()
    data["locations"] = list(
        customers_df[["lat", "lon"]].itertuples(index=False, name=None),
    )

    return data


def print_solution_cvrp(
    data: dict,
    manager: pywrapcp.RoutingIndexManager,
    routing: pywrapcp.RoutingModel,
    solution: pywrapcp.Assignment,
) -> str:
    """Print CVRP solution."""
    output = []
    output.append(
        f"<p style='color:Tomato;'>Objective: {solution.ObjectiveValue()}</p>",
        )
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        output.append(f"<p>Route for vehicle {vehicle_id}:<br>")
        route_distance = 0
        route_load = 0
        route_output = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            route_output.append(f" {node_index} Load({route_load}) -> ")
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id,
            )
        route_output.append(
            f" {manager.IndexToNode(index)} Load({route_load})<br>")
        output.append("".join(route_output))
        output.append(f"Distance of the route: {route_distance}km<br>")
        output.append(f"Load of the route: {route_load}</p>")
        total_distance += route_distance
        total_load += route_load
    output.append(f"<p>Total distance of all routes: {total_distance}km<br>")
    output.append(f"Total load of all routes: {total_load}</p>")

    return "".join(output)


def print_solution_vrp(
    data: dict,
    manager: pywrapcp.RoutingIndexManager,
    routing: pywrapcp.RoutingModel,
    solution: pywrapcp.Assignment,
) -> str:
    """Print Basic VRP solution."""
    output = []
    output.append(
        f"""
        <p style='color:Tomato;'>Objective: {solution.ObjectiveValue():,}</p>
        """,
    )
    max_route_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        output.append(
            f"<p>Route for vehicle {data["vehicle_name"][vehicle_id]}:<br>"
            )
        route_distance = 0
        route_output = []
        while not routing.IsEnd(index):
            route_output.append(f" {manager.IndexToNode(index)} -> ")
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id,
            )
        route_output.append(f"{manager.IndexToNode(index)}<br>")
        output.append("".join(route_output))
        output.append(f"Distance of the route: {route_distance:,}km</p>")
        max_route_distance = max(route_distance, max_route_distance)
    output.append(
        f"<p>Maximum of the route distances: {max_route_distance:,}km</p>",
        )

    routes = extract_routes(manager, routing, solution)
    visualize_routes_with_networkx(data, routes)

    return "".join(output)


def solver_ortools_cvrp(data_model: dict) -> None:
    """Run cvrp solver."""
    # Instantiate the data model.
    data = data_model

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"],
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index: int, to_index: int) -> float:
        """Return the callback of the distance between the two nodes.

        Args:
            from_index (int): start node
            to_index (int): end node

        Returns:
            float: distance from node to node

        """
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        return data["distance_matrix"][from_node][to_node]

    # Register a transit callback.
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index: int) -> bool:
        """Return the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback,
        )
    routing.AddDimensionWithVehicleCapacity(
        evaluator_index=demand_callback_index,
        slack_max=0,
        vehicle_capacities=data["vehicle_capacities"],
        fix_start_cumul_to_zero=True,
        name="Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution_cvrp(data, manager, routing, solution)
    return "No solution found!"


def solver_ortools_vrp(data_model: dict) -> str:
    """Run vrp solver."""
    # Instantiate the data problem.
    data = data_model

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"],
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index: int, to_index: int) -> float:
        """Return the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        evaluator_index=transit_callback_index,
        slack_max=0,  # no slack
        capacity=10**6,  # vehicle maximum travel distance
        fix_start_cumul_to_zero=True,  # start cumul to zero
        name=dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution_vrp(data, manager, routing, solution)
    return "No solution found !"


def extract_routes(
    manager: pywrapcp.RoutingIndexManager,
    routing: pywrapcp.RoutingModel,
    solution: pywrapcp.Assignment,
) -> list:
    """Extract the routes from the solution provided by OR-Tools."""
    routes = []
    for vehicle_id in range(routing.vehicles()):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))  # Add the end node
        routes.append(route)

    [routes.remove(route) for route in routes if len(route) == 2]
    return routes


def visualize_routes_with_networkx(data: dict, routes: list) -> None:
    """Visualizes the routes using NetworkX."""
    G = nx.DiGraph()

    # Add nodes and edges for each route
    for route in routes:
        for i in range(len(route) - 1):
            G.add_edge(route[i], route[i + 1])

    # Define positions for nodes
    positions = {i: coord for i, coord in enumerate(data["locations"])}

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos=positions,
        with_labels=True,
        node_size=700,
        node_color="lightblue",
        font_weight="bold",
        arrowsize=20,
    )

    # Save the graph to a static folder
    graph_path = "static/graph.png"
    plt.savefig(graph_path, format="png")
    plt.close()
