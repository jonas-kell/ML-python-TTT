#include <stdio.h>

int board[3][3];
int minimax(int depth, int isMaximizing);
int best_position(int *matrix);
int checkWinner();

//  assignmeint of variables:
//  matrix gets broken into pieces
//  a 0 indicates no placed symbol
//  a 1 indicates a placed symbol of the type of the person whose next move is requested (make sure to transpose to this state accordingly)
//  a 2 indicates a placed symbol of the type of the opponent (make sure to transpose to this state accordingly)
//  assumes there is space. may run into trouble if not the case
int best_position(int *matrix)
{
    // get input from the dll
    board[0][0] = matrix[0];
    board[0][1] = matrix[1];
    board[0][2] = matrix[2];
    board[1][0] = matrix[3];
    board[1][1] = matrix[4];
    board[1][2] = matrix[5];
    board[2][0] = matrix[6];
    board[2][1] = matrix[7];
    board[2][2] = matrix[8];

    // AI to make its turn
    int bestScore = -999999;
    int move_y, move_x;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            // Is the spot available?
            if (board[i][j] == 0)
            {
                board[i][j] = 1;
                int score = minimax(0, 0);
                board[i][j] = 0;
                if (score > bestScore)
                {
                    bestScore = score;
                    move_y = i;
                    move_x = j;
                }
            }
        }
    }
    board[move_y][move_x] = 1;

    // return to the dll
    matrix[0] = board[0][0];
    matrix[1] = board[0][1];
    matrix[2] = board[0][2];
    matrix[3] = board[1][0];
    matrix[4] = board[1][1];
    matrix[5] = board[1][2];
    matrix[6] = board[2][0];
    matrix[7] = board[2][1];
    matrix[8] = board[2][2];
}

int minimax(int depth, int isMaximizing)
{
    int result = checkWinner();
    if (result != 0)
    {
        if (result == 1)
            return +10;
        else if (result == 2)
            return -10;
        else
            return 0;
    }

    if (isMaximizing)
    {
        int bestScore = -999999;
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                // Is the spot available?
                if (board[i][j] == 0)
                {
                    board[i][j] = 1;
                    int score = minimax(depth + 1, 0);
                    board[i][j] = 0;
                    if (score > bestScore) // max
                    {
                        bestScore = score;
                    }
                }
            }
        }
        return bestScore;
    }
    else
    {
        int bestScore = 999999;
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                // Is the spot available?
                if (board[i][j] == 0)
                {
                    board[i][j] = 2;
                    int score = minimax(depth + 1, 1);
                    board[i][j] = 0;
                    if (score < bestScore) // min
                    {
                        bestScore = score;
                    }
                }
            }
        }
        return bestScore;
    }
}

// returns 0 if undecided game
// returns 1 if 1s won game
// returns 2 if 2s won game
// returns 3 if draw
int checkWinner()
{
    // check rows
    for (int i = 0; i < 3; i++)
    {
        if (
            board[i][0] != 0 && board[i][0] == board[i][1] && board[i][1] == board[i][2])
        {
            return board[i][0];
        }
    }

    // check columns
    for (int i = 0; i < 3; i++)
    {
        if (
            board[0][i] != 0 && board[0][i] == board[1][i] && board[1][i] == board[2][i])
        {
            return board[0][i];
        }
    }

    // check diagonals
    if (board[0][0] != 0 && board[0][0] == board[1][1] && board[1][1] == board[2][2])
    {
        return board[0][0];
    }
    if (board[0][2] != 0 && board[0][2] == board[1][1] && board[1][1] == board[2][0])
    {
        return board[0][2];
    }

    // count 0s(open spots)
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (board[i][j] == 0)
            {
                return 0;
            }
        }
    }
    return 3;
}