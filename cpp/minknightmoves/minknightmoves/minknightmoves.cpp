#include <vector>
#include<map>
#include <climits>
#include <iostream>

constexpr auto NMAX = 300;
constexpr auto NMAX2 = (2 * NMAX + 1) * (2 * NMAX + 1);

using namespace std;

class Solution {
public:
    Solution()
    {
        initCells();
    }
    class Cell {
    public:
        int x;
        int y;
        vector<Cell*> moves;
        Cell(const int& _x, const int& _y) {
            x = _x;
            y = _y;
        }
    };
    Cell** board;
    map<Cell*, int> visited;
    void initCells()
    {
        board = (Cell**)malloc(NMAX2 * sizeof(Cell*));
        for (int i = -NMAX; i < NMAX; i++)
            for (int j = -NMAX; j < NMAX; j++) {
                //               board[i][j] = nullptr;
 //               *(board + NMAX2 + NMAX * i + j) = NULL;
 //               std::cout << i << " " << j << " becomes " << NMAX * (i + NMAX) + (NMAX + j) << endl;

                *(board + NMAX * (NMAX + i) + j + NMAX) = nullptr;
            }
    }
    Cell* cellPtr(const int& xp, const int& yp) {
//        Cell* current = board[NMAX + xp][NMAX + yp];
        Cell *current = *( board + NMAX*(NMAX+xp) + NMAX + yp );
        return current;
    }
    Cell* addCell(const int& xp, const int& yp) {

        Cell* current = new Cell(xp, yp);
//        board[NMAX + xp][NMAX + yp] = current;
        *(board + NMAX * (NMAX + xp) + NMAX + yp) = current;
        return current;
    }
    Cell* addIfNotExists(const int& xp, const int& yp) {
//        Cell* current = board[NMAX + xp][NMAX + yp];
        Cell* current = *(board + NMAX * (NMAX + xp) + NMAX + yp);
        if (current == nullptr) {
            current = new Cell(xp, yp);
//            board[NMAX + xp][NMAX + yp] = current;
            *(board + NMAX * (NMAX + xp) + NMAX + yp) = current;
        }
        return current;
    }
    bool checkMoves(Cell* baseCell)
    {
        vector<pair<int, int>> jumps = { {2,1},{1,2},{-2,-1},{-1,-2},{-2,1},{-1,2},{2,-1},{1,-2} };
        bool targetIn = false;
        if (baseCell->moves.size() == 0) {
            for (auto jump : jumps) {
                int xp = baseCell->x + jump.first;
                int yp = baseCell->y + jump.second;
                if (xp == 0 && yp == 0)
                    targetIn = true;
                if ((abs(xp) + abs(yp)) > 300)
                    continue;
                Cell* current = addIfNotExists(xp, yp);
                baseCell->moves.push_back(current);
            }
        }
        return false;
    }
    int minKnightMoves(int x, int y) {
        //MAIN LEETCODE FUNCTION
        int moves = 0;
        Cell* board0 = addIfNotExists(x, y);
        if (visited.find(board0) != visited.end())
            return visited[board0];
        if (checkMoves(board0))
            return 1;
        int movMin = INT_MAX;
        for (auto cell : board0->moves) {
            int cellMoves;
            if (visited.find(cell) != visited.end())
                cellMoves = minKnightMoves(cell->x, cell->y);
            else
                cellMoves = visited[cell];
            if (cellMoves < movMin)
                movMin = cellMoves;
        }
        visited[board0] =  movMin;
        return movMin + 1;
    }
};

int main(int argc, char** argv)
{
    Solution sol;
    int x = 4;
    int y = 2;
    int moves = sol.minKnightMoves(x,y);
    std::cout << x << " " << y << endl;
    std::cout << moves << endl;
}