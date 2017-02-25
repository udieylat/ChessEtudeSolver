from Solver import *
from optparse import OptionParser


def Main():
    parser = OptionParser()
    parser.add_option("-i", "--input_filename")
    parser.add_option("-t", "--type", type="choice", choices=["mate_in_2", "mate_in_3", "mate_in_4", "selfmate", "helpmate"])
    parser.add_option("-n", "--num_solutions", default=1, type=int)

    options, _ = parser.parse_args()

    board = read_board(options.input_filename)

    if options.type == "mate_in_2":
    	solve_mate_in_two(board)
    elif options.type == "mate_in_3":
    	solve_mate_in_three(board)
    elif options.type == "mate_in_4":
    	solve_mate_in_four(board)
    elif options.type == "selfmate":
    	solve_selfmate_in_two(board)
    elif options.type == "helpmate":
    	board.turn = BLACK
    	solve_helpmate_in_two(board, options.num_solutions)
    else:
    	print "Invalid etude type:", options.type

if __name__ == '__main__':
    Main()
