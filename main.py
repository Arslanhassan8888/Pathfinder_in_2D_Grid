"""
Main program for running the weighted A* pathfinding simulation.

This script handles:
- User input (map size, terrain probabilities, heuristic weight)
- Grid generation
- Execution of the weighted A* algorithm
- Displaying results and optional re-planning when obstacles are added

"""

from mapword import Map

# ANSI color codes for terminal text formatting
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

if __name__ == "__main__":
    # Display welcome message and the purpose of the simulation
    print(f"\n{YELLOW}WELCOME TO ARSLAN'S LAND — PATHFINDING ADVENTURE{RESET} \n")
    print(f"{GREEN}This simulation lets you explore how a robot navigates a grid world using the A* algorithm!{RESET}\n")
    
    # CHOOSE GRID SIZE
    # Get user input for map dimensions
    print(f"{YELLOW}--- Map Size Setup ---{RESET}")
    while True:
        try:
            rows = int(input(f"{GREEN}Enter number of rows for the map (e.g., 10): {RESET}"))
            cols = int(input(f"{GREEN}Enter number of columns for the map (e.g., 10): {RESET}"))
            if rows <= 0 or cols <= 0:
                print(f"{RED}Error! The grid size must be positive numbers. Try again.{RESET}\n")
                continue
            break
        except ValueError:
            print(f"{RED}Error! Please enter valid integer numbers.{RESET}\n")

    land1 = Map(rows, cols)

    # TERRAIN RANDOMISATION SETUP
    # The user can choose default or custom probabilities for terrain types
    print(f"\n{YELLOW}--- Terrain Randomization Setup ---{RESET}")
    print("Enter probabilities for each terrain type (should be total 100).")
    print("Type 'd' to apply default values or 'c' to customise.")
    print("If total ≠ 100, it will be auto-adjusted proportionally.\n")

    while True:
        try:
            choice = input(f"{GREEN}Choose an option — (d = default, c = customize): {RESET}").strip().lower()

            if choice == 'd':
                n_prob, h_prob, w_prob, o_prob = 65, 15, 10, 10
                print(f"\n{GREEN}Default probabilities applied: (65, 15, 10, 10){RESET}\n")
                break

            elif choice == 'c':
                n_prob = int(input(f"{GREEN}Normal terrain (N) probability [%]: {RESET}"))
                h_prob = int(input(f"{GREEN}Hill (H) probability [%]: {RESET}"))
                w_prob = int(input(f"{GREEN}Water (W) probability [%]: {RESET}"))
                o_prob = int(input(f"{GREEN}Obstacle (O) probability [%]: {RESET}"))

                # Reject negative entries
                if n_prob < 0 or h_prob < 0 or w_prob < 0 or o_prob < 0:
                    print(f"{RED}Error! Probabilities cannot be negative. Try again.{RESET}\n")
                    continue

                total = n_prob + h_prob + w_prob + o_prob
                if total != 100:
                    print(f"{YELLOW}Total = {total}%. Will be automatically adjusted to 100%.{RESET}\n")

                break

            else:
                print(f"{RED}Error! Invalid option. Type 'd' or 'c'.{RESET}\n")

        except ValueError:
            print(f"{RED}Error! Please enter valid integer numbers. Try again.{RESET}\n")

    # GENERATE THE GRID
    land1.fill_grid()
    land1.fill_random_grid(n_prob, h_prob, w_prob, o_prob)

    # DISPLAY THE GENERATED MAP
    print(f"\n{YELLOW}Legend:{RESET} N=Normal, O=Obstacle, W=Water, H=Hill, S=Start, G=Goal\n")
    print(f"{YELLOW}Generated Map:{RESET}\n")
    land1.print_grid()


    # HEURISTIC WEIGHT MENU
    # The weight determines how strongly the robot prioritises reaching the goal
    print(f"\n{YELLOW}--- Heuristic Weight Setup ---{RESET}")
    print("The weight determines how strongly the robot prioritises reaching the goal.")
    print("""
    w = 0   → Dijkstra's Algorithm (slow, explores everything)
    0 < w < 1 → Cautious A* (balanced, more careful)
    w = 1   → Standard A* (optimal and efficient)
    w > 1   → Aggressive A* (faster but might miss the shortest path)
    """)

    while True:
        try:
            weight = float(input(f"{GREEN}Enter heuristic weight between 0 and 5 (default = 1.0): {RESET}"))
            if weight < 0 or weight > 5:
                print(f"\n{RED}Error! Weight must be between 0 and 5. Try again.{RESET}\n")
                continue
            break
        except ValueError:
            print(f"\n{RED}Error! Invalid input! Please enter a numeric value.{RESET}\n")

    # RUN THE ALGORITHM
    print(f"\n{YELLOW}Running Weighted A* Algorithm...{RESET}\n")
    path = land1.a_star(weight=weight)

    # ANIMATE THE ROBOT MOVEMENT IF PATH FOUND
    if path:
        input(f"\n{GREEN}Press Enter to start robot animation...{RESET}\n")
        land1.animate_path(path, delay=0.4)

        # FINAL SUMMARY
        print(f"\n{YELLOW}===== FINAL RESULTS ====={RESET}\n")
        print(f"{GREEN}Map size used:{RESET} {land1.rows} x {land1.cols}")
        print(f"{GREEN}Start:{RESET} {land1.start}")
        print(f"{GREEN}Goal:{RESET} {land1.goal}\n")

        print(f"{GREEN}Algorithm used: Weighted A*{RESET}")
        print(f"{GREEN}Heuristic weight:{RESET} {weight}\n")

        print(f"{GREEN}Path found:{RESET}")
        print(path)

        print(f"\n{GREEN}Path length:{RESET} {len(path)}")
        print(f"{GREEN}Total movement cost:{RESET} {sum(land1.move_cost(x, y) for x, y in path)}\n")

    else:
        print(f"\n{RED}No path could be found — goal is unreachable due to obstacles.{RESET}\n")
        

    #ADD NEW OBSTACLES & RE-RUN A*
    # Allow user to add new obstacles and re-run the algorithm
    while True:
        add_obs = input(f"\n{GREEN}Would you like to simulate new unexpected obstacles? (y/n): {RESET}").strip().lower()
        if add_obs == 'y':
            try:
                x = int(input(f"{GREEN}Enter row index (0 to {land1.rows - 1}): {RESET}"))
                y = int(input(f"{GREEN}Enter column index (0 to {land1.cols - 1}): {RESET}"))

                # Validation of coordinates (within bounds and not on start/goal)
                if not land1.in_bounds(x, y):
                    print(f"{RED}Error: position out of bounds!{RESET}")
                    continue
                if (x, y) == land1.start or (x, y) == land1.goal:
                    print(f"{RED}Error: cannot place an obstacle on Start or Goal!{RESET}")
                    continue
                # Place the new obstacle
                land1.grid[x][y] = f"{RED}O{RESET}"
                print(f"{YELLOW}New obstacle added at ({x}, {y}).{RESET}")
                print(f"{YELLOW}Updated Map:{RESET}\n")
                land1.print_grid()

            except ValueError:
                print(f"{RED}Invalid input! Please enter integers.{RESET}\n")
                continue

            # Re-run A* after new obstacle placement
            print(f"\n{YELLOW}Re-running A* algorithm to find new path...{RESET}\n")
            new_path = land1.a_star(weight=weight)

            if new_path:
                input(f"\n{GREEN}Press Enter to see the robot navigate the new route...{RESET}\n")
                land1.animate_path(new_path, delay=0.5)
                
                # FINAL SUMMARY FOR NEW PATH
                print(f"\n{GREEN}New path successfully found!{RESET}")
                print(f"Path length: {len(new_path)}")
                print(f"Total movement cost: {sum(land1.move_cost(x, y) for x, y in new_path)}\n")
                print(new_path)
            else:
                print(f"{RED}No valid path found — the robot is trapped by new obstacles!{RESET}\n")

        elif add_obs == 'n' or add_obs == '':
            print(f"{YELLOW}No new obstacles added. Simulation complete.{RESET}\n")
            break
        else:
            print(f"{RED}Please answer with 'y' or 'n'.{RESET}")


