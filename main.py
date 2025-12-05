from mapword import Map

if __name__ == "__main__":
    print("\nWELCOME TO ARSLAN'S LAND — PATHFINDING ADVENTURE \n")
    print("This simulation lets you explore how a robot navigates a grid world using the A* algorithm!\n")
    
    # CHOOSE GRID SIZE
    while True:
        try:
            rows = int(input("Enter number of rows for the map (e.g., 10): "))
            cols = int(input("Enter number of columns for the map (e.g., 10): "))
            if rows <= 0 or cols <= 0:
                print("Error! The grid size must be positive numbers. Try again.\n")
                continue
            break
        except ValueError:
            print("Error! Please enter valid integer numbers.\n")

    land1 = Map(rows, cols)

    # TERRAIN RANDOMISATION SETUP
    print("\n--- Terrain Randomization Setup ---")
    print("Enter probabilities for each terrain type (should total 100).")
    print("Type 'd' to apply default values or 'c' to customise.")
    print("If total ≠ 100, it will be auto-adjusted proportionally.\n")

    while True:
        try:
            choice = input("Choose an option — (d = default, c = customize): ").strip().lower()

            if choice == 'd':
                n_prob, h_prob, w_prob, o_prob = 65, 15, 10, 10
                print("\nDefault probabilities applied: (65, 15, 10, 10)\n")
                break

            elif choice == 'c':
                n_prob = int(input("Normal terrain (N) probability [%]: ") or 65)
                h_prob = int(input("Hill (H) probability [%]: ") or 15)
                w_prob = int(input("Water (W) probability [%]: ") or 10)
                o_prob = int(input("Obstacle (O) probability [%]: ") or 10)

                # Reject negative entries
                if n_prob < 0 or h_prob < 0 or w_prob < 0 or o_prob < 0:
                    print("Error! Probabilities cannot be negative. Try again.\n")
                    continue

                total = n_prob + h_prob + w_prob + o_prob
                if total != 100:
                    print(f"Total = {total}%. Will be automatically adjusted to 100%.\n")

                break

            else:
                print("Error! Invalid option. Type 'd' or 'c'.\n")

        except ValueError:
            print("Error! Please enter valid integer numbers. Try again.\n")

    # Generate the terrain map
    land1.fill_grid()
    land1.fill_random_grid(n_prob, h_prob, w_prob, o_prob)

    print("\nLegend: N=Normal, O=Obstacle, W=Water, H=Hill, S=Start, G=Goal\n")
    print("Generated Map:\n")
    land1.print_grid()

    # HEURISTIC WEIGHT MENU
    print("\n--- Heuristic Weight Setup ---")
    print("The weight determines how strongly the robot prioritises reaching the goal.")
    print("""
    w = 0   → Dijkstra's Algorithm (slow, explores everything)
    0 < w < 1 → Cautious A* (balanced, more careful)
    w = 1   → Standard A* (optimal and efficient)
    w > 1   → Aggressive A* (faster but might miss the shortest path)
    """)

    while True:
        try:
            weight = float(input("Enter heuristic weight between 0 and 5 (default = 1.0): ") or 1.0)
            if weight < 0 or weight > 5:
                print("\nError! Weight must be between 0 and 5. Try again.\n")
                continue
            break
        except ValueError:
            print("\nError! Invalid input! Please enter a numeric value.\n")

    # RUN THE ALGORITHM
    print("\nRunning Weighted A* Algorithm...\n")
    path = land1.a_star(weight=weight)

    if path:
        input("\nPress Enter to start robot animation...\n")
        land1.animate_path(path, delay=0.4)

        # FINAL SUMMARY
        print("\n===== FINAL RESULTS =====\n")
        print(f"Map size used: {land1.rows} x {land1.cols}")
        print(f"Start: {land1.start}")
        print(f"Goal: {land1.goal}\n")

        print(f"Algorithm used: Weighted A*")
        print(f"Heuristic weight: {weight}\n")

        print("Path found:")
        print(path)

        print(f"\nPath length: {len(path)}")
        print(f"Total movement cost: {sum(land1.move_cost(x, y) for x, y in path)}\n")

    else:
        print("\nNo path could be found — goal is unreachable due to obstacles.\n")
