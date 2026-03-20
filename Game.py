
class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.revise_calls = 0 #how many arcs were processed
        self.domain_removals = 0 #how many domain values were deleted

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self, heuristic) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        rows = range(9)
        columns = range(9)
        board = self.sudoku.get_board()
        queue = []

        for row in rows:
            for column in columns:
                field = board[row][column]

                if field.is_finalized():
                    field.domain = [field.get_value()]
                
                for neighbour_field in field.get_neighbours():
                    queue.append((field, neighbour_field))
        
        max_queue_size = len(queue) #keep track of maximum number of arcs in the queue at any point

        while queue:
############################### Heuristics Block ################################
            if heuristic.lower() == "fifo":
            #FIFO heuristic (baseline)
                (current_field, neighbour_field) = queue.pop(0) 

            if heuristic.lower() == 'mrv':
                #priority queue heuristic (MRV)
                best_index = 0
                best_field, best_neighbour = queue[0]
                best_size = best_field.get_domain_size()

                for i in range(1, len(queue)):
                    field_i, neighbour_i = queue[i]
                    size_i = field_i.get_domain_size()
                    if size_i < best_size:
                        best_index = i
                        best_field, best_neighbour = field_i, neighbour_i
                        best_size = size_i
                
                (current_field, neighbour_field) = queue.pop(best_index)

            if heuristic.lower() == 'lcv':
                #Most restraining arc first heuristic
                index = None
                for count, (field, neighbour_field) in enumerate(queue):
                    if field.get_domain_size() == 1 or neighbour_field.get_domain_size() == 1:
                        index = count
                        break

                if index == None: #No indexes to be finalized found
                    index = 0 #revert back to baseline
                
                (current_field, neighbour_field) = queue.pop(index)
########################## End of Heuristics block ###############################

            if self.revised(current_field, neighbour_field):
                if current_field.get_domain_size() == 0:
                    return False
                
                for other_neighbour in current_field.get_other_neighbours(neighbour_field):
                    queue.append((other_neighbour, current_field))
                    if len(queue) > max_queue_size:
                        max_queue_size = len(queue)
        
        self.solve_sudoku_rec(board)

        print("AC-3 complexity:")
        print(f"Revise calls: {self.revise_calls}")
        print(f"Total domain removals: {self.domain_removals}")
        print(f"Max queue-size: {max_queue_size}")
        return True

    def revised(self, current_field, neighbour_field):
        revised = False
        current_domain = current_field.get_domain()[:]
        neighbour_domain = neighbour_field.get_domain()
        self.revise_calls += 1

        for val_cur in current_domain:
            support = False
            for val_neighbour in neighbour_domain:
                if val_cur != val_neighbour:
                    support = True
                    break

            if not support:
                current_field.remove_from_domain(val_cur)
                self.domain_removals += 1
                revised = True
        
        return revised
    
    def solve_sudoku_rec(self, board):
        rows = range(9)
        columns = range(9)

        def finalize_fields():
            for row in rows:
                for column in columns:
                    field = board[row][column]
                    if not field.is_finalized() and field.get_domain_size() == 1:
                        field.set_value(field.get_domain()[0])

        def find_unfinalized_fields():
            for row in rows:
                for column in columns:
                    field = board[row][column]
                    if not field.is_finalized() and field.get_domain_size() > 1:
                        return row, column
            return None, None
        
        def backtrack():
            finalize_fields()
            row, column = find_unfinalized_fields()
            if row is None:
                #If all cells are finalized
                return True
            
            board_copy = [[(board[row][column].get_value(), board[row][column].get_domain()[:]) for column in columns] for row in rows]

            field = board[row][column]
            for value in field.get_domain():
                conflict = False
                for neighbour in field.get_neighbours():
                    if neighbour.is_finalized() and neighbour.get_value() == value:
                        conflict = True
                        break
                if conflict: 
                    continue
                #try value in field.get_domain()
                field.set_value(value)
                if backtrack():
                    return True
                for row in rows:
                    for column in columns:
                        value, domain = board_copy[row][column]
                        cell = board[row][column]
                        cell.set_value(value)
                        cell.domain = domain[:]
            #No value is possible and field isn't finalized (unsolvable sudoku)
            return False
        
        return backtrack()

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        rows = range(9)
        columns = range(9)
        board = self.sudoku.get_board()

        #Check fixed values for mistakes
        for row in rows:
            for column in columns:
                field = board[row][column]
                value = field.get_value()

                if value != 0: #found a solution
                    for neighbour_field in field.get_neighbours():
                        if neighbour_field.get_value() == value:
                            print(f"Value conflict: ({row},{column}) and a neighbor both have value {value}")
                            return False
        
        #Check arc consistency of domains
        for row in rows:
            for column in columns:
                field = board[row][column]
                domain = field.get_domain()

                for neighbour_field in field.get_neighbours():
                    neighbour_domain = neighbour_field.get_domain()

                    for val_cur in domain:
                        support = False
                        for val_neighbour in neighbour_domain:
                            if val_neighbour != val_cur:
                                support = True
                                break
                        if not support:
                            print(f"Arc inconsistency: value {val_cur} in domain of ({row},{column})")
                            return False
        return True
