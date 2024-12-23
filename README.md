# VEHICLE ROUTING PROBLEM

## Video Demo: <URL HERE>

## Description:
The **VRP Solver** is a web-based application designed to address various forms of the Vehicle Routing Problem (VRP). It allows users to define customer locations and vehicle details to compute optimal delivery or pickup routes. Using real-world geographic coordinates, it calculates distances between locations based on geodesic measurements and solves routing challenges using Google's OR-Tools. The tool supports visualization of results for better understanding and analysis.

Supported VRP variations include:
- VRP (basic)
- CVRP (Capacitated VRP)
- VRPTW (VRP with Time Windows) *(Coming soon)*
- VRPPD (Pickup and Delivery) *(Coming soon)*
- VRPB (Backhauls) *(Coming soon)*

This project is perfect for logistics professionals, researchers, or anyone interested in vehicle routing optimization.

## Features:
- **Real-World Geography**: Supports real-world coordinates, enabling accurate distance calculations using geodesic formulas.
- **Multiple VRP Variations**: Currently supports the basic VRP and CVRP (Capacitated VRP). Other variations such as VRPTW (VRP with Time Windows), VRPPD (Pickup and Delivery), and VRPB (Backhauls) are planned for future updates.
- **Visualization**: Provides route visualizations using networkx and matplotlib, making results easier to interpret.
- **Customizable Input**: Users can upload CSV files to define customers and vehicles, tailoring the solution to specific scenarios.
- **Scalable**: Handles small to medium-sized datasets effectively, with the potential for future optimizations to support larger problems.

## Project Structure
The following outlines the files and directories in the project and their purpose:

### Main Files
- ```app.py```: The main Flask application file. It handles routing, manages sessions, and serves the HTML templates.
- ```functions.py```: Contains all the necessary functions for running the app. Includes functions for building the distance matrix, callbacks, and invoking Google OR-Tools solvers.
-```test_functions.py```: Includes unit tests for functions used by the app.

### Templates
- ```templates/apology.html```: A fallback page that displays error messages to the user.
- ```templates/index.html```: The homepage that introduces the VRP Solver and provide the steps for the user to follow.
- ```templates/layout.html```: The base layout for all pages, including the navbar and footer.
- ```templates/output.html```: Displays the computed solution and route visualization.
- ```templates/solver.html```: The page where users select the desired solver to use.
- ```templates/upload_files.html```: The page where users upload their input CSV files.

### Static Files
- ```static/styles.css```: Custom CSS for styling the app.
- ```static/sample_customers.csv```: Sample file for the required Customers CSV file.
- ```static/sample_vehicles.csv```: Sample file for the required Vehicles CSV file.
- ```static/graph.png```: Visualization for the solution.

### Configuration and Documentation Files
- ```requirements.txt```: Lists all the Python dependencies needed for the project.
- ```README.md```: Provides an overview of the project, setup instructions, and usage guide.
- ```LICENSE```: Specifies the terms under which the project can be used, modified, and distributed.

### Utility Files
- ```.gitignore```: Specifies files and directories that should be ignored by Git.

## Getting Started:
Follow these steps to set up and run the VRP Solver locally:

### Prerequisites
Before you begin, ensure you have the following:
- Python 3.8+
- Libraries: Flask, OR-Tools, Geopy, Matplotlib, and NetworkX.

### Installation
1. Clone the Repository:
```
git clone https://github.com/lymvs/vrp.git
cd vrp
```
2. Install Dependencies: Install the required Python libraries using pip:
```
pip install -r requirements.txt
```
3. Run the Application: Start the Flask develpment server:
```
flask run
```
Access the application at http://127.0.0.1:5000.

## Usage:
### Step 1: Select a VRP Type
On the homepage, choose the type of Vehicle Routing Problem to solve. Current options include:

- **VRP (Basic)**: Route optimization without additional constraints.
- **CVRP**: Routes optimized with vehicle capacity limits.
Other options such as VRPTW, VRPPD, and VRPB are marked as "Coming Soon."

### Step 2: Upload Data Files
Navigate to the upload page and provide the required CSV files:

- **Customers File**: Specifies customer locations and demands.
- **Vehicles File**: Defines available vehicles and their capacities.
Ensure the CSV files follow the format described below.

### Step 3: Solve and Visualize
After uploading the data, submit the form to compute the solution. The application will:

1. Display the computed routes for each vehicle.
2. Show a visualization of the routes, with nodes and edges representing customer locations and vehicle paths.

## Input Data Format:
### Customers
| Column Name       | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| customer_id       | Unique identifier for the customer                                 |
| latitude	        | Geographical latitude of the customer                              |
| longitude	        | Geographical longitude of the customer                             |
| demands           | The amount of goods the customer needs to be delivered             |
| time_window_start | Time window start for when a customer can be visited (Coming Soon) |
| time_window_end   | Time window end for when a customer can be visited (Coming Soon)   |
| pick_up_location  | Specify if the customer is a pick-up location (Coming Soon)        |
| delivery_location | Specify if the customer is a delivery location (Coming Soon)       |

### Vehicles
| Column Name | Description                           |
| ----------- | ------------------------------------- |
| vehicle_id  | Unique identifier for the vehicle     |
| capacity    | The vehicle's capacity to carry goods |

## Technologies Used:
- **Backend**: Flask handles the application logic and routing.
- **Optimization Egine**: Google OR-Tools provides advance VRP solvers.
- **Distance Calculation**: Geopy calculates geodesic distances between locations.
- **Visualization**: NetworkX and Matplotlib generate graph-based route visualizations.
- **Styling**: Bootstrap ensures a responsive and user-friendly interface.

## Visualization:
Results are presented graphically:
- Nodes represent customers and the depot.
- Edges show vehicle routes.
- Helps to analyze the effectiveness of the solution.

## Contributing:
Contributions to this project are welcome! Here's how you can contribute:
1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix:
```
git checkout -b feature-name
```
3. Commit and push your changes, then create a pull request.

Suggestions for additional features or optimizations are also appreciated.

## License:
The project is licensed under the **MIT License**.

## Acknowledgements:
- Google OR-Tools: For providing powerful optimization tools.
- Geopy: For accurate geodesic distance calculations.
- Matplotlib & NetworkX: For route visualizations.
- Bootstrap: For the UI framework.