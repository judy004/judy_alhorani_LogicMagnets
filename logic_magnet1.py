class State :
    def __init__(self,board_size,init_board):
        self.board_size = board_size
        self.board = init_board
        self.original_board = [['E' if cell == 'G' else cell for cell in row] for row in init_board]
        self.purple_magnet_pre_value = 'E'
        self.red_magnet_pre_value = 'E'
        


    def valid_move (self,current_row, current_col, next_row, next_col):
        if next_row<0 or next_row>= self.board_size or next_col<0 or next_col>=self.board_size:
            return False
        return self.board[next_row][next_col] in ['E','*']
    
    #movement of purple magnet and repulsion of iron pieces
    def repulsion(self,current_row,current_col, next_row, next_col):
        if not self.valid_move(current_row, current_col, next_row,next_col):
            return False
        self.board[current_row][current_col]= self.purple_magnet_pre_value
        self.purple_magnet_pre_value = self.original_board[next_row][next_col] if self.purple_magnet_pre_value =='E' else self.board[next_row][next_col]
        self.board[next_row][next_col]= 'P'

        #checking the row and col of new purple magnet position
        for i in range(self.board_size):
            # right and left repulsion
            if self.board[next_row][i] == 'G' :
                if i < next_col and self.valid_move(next_row,i, next_row, i-1):
                    self.board[next_row][i-1]= 'G'
                    self.board[next_row][i] = self.original_board[next_row][i]
                elif i> next_col and self.valid_move(next_row, i , next_row, i+1):
                    self.board[next_row][i+1]= 'G'
                    self.board[next_row][i]= self.original_board[next_row][i]
            
            #up and down repulsion
            if self.board[i][next_col] == 'G':
                if i< next_row and self.valid_move(i, next_col, i-1 , next_col):
                    self.board[i-1][next_col]= 'G'
                    self.board[i][next_col]= self.original_board[i][next_col]
                elif i> next_row and self.valid_move(i,next_col,i+1, next_col):
                    self.board[i+1][next_col]='G'
                    self.board[i][next_col]= self.original_board[i][next_col]

        return True
    
    def attraction(self,current_row, current_col, next_row, next_col):
        if not self.valid_move(current_row, current_col, next_row,next_col):
            return False
        self.board[current_row][current_col]= self.red_magnet_pre_value
        self.red_magnet_pre_value = self.original_board[next_row][next_col] if self.red_magnet_pre_value=='E' else self.board[next_row][next_col]
        self.board[next_row][next_col]= 'R'

        #checking the row and col of new red magnet position
        for i in range(self.board_size):
            #left and right attraction
            if self.board[next_row][i]=='G':
                if i < next_col and self.valid_move(next_row, i , next_row, i+1):
                    self.board[next_row][i+1]='G'
                    self.board[next_row][i] = self.original_board[next_row][i]
                elif i> next_col and self.valid_move(next_row,i,next_row,i-1):
                    self.board[next_row][i-1]='G'
                    self.board[next_row][i] = self.original_board[next_row][i]
            
            #up and down attraction
            if self.board[i][next_col] =='G':
                if i< next_row and self.valid_move(i,next_col,i+1,next_col):
                    self.board[i+1][next_col]= 'G'
                    self.board[i][next_col] = self.original_board[i][next_col]
                elif i> next_row and self.valid_move(i,next_col,i-1,next_col):
                    self.board[i-1][next_col]= 'G'
                    self.board[i][next_col] = self.original_board[i][next_col]
        return True
    
    

    # checking wining state
    def wining_state(self):
        for row in self.board:
            if '*' in row:
                return False
        return True      