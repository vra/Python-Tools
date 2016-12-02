import argparse
import sys

def my_arg_parse():
	parser = argparse.ArgumentParser(description='My program to process data')

	parser.add_argument('--type', dest='type', type=str,default='txt',
		    			help='Type of data to process')
	parser.add_argument('--size', dest='size', type=int, default=8,
		    			help='The size of each data')
	parser.add_argument('--filename', dest='file_name', type=str, default='a',
						help='The file name of data to process')

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(1)
	
	args = parser.parse_args()
	print '===data info summary==='
	print '1. file name: ', args.file_name
	print '2. data type: ', args.type
	print '3. data size: ', args.size
	print '===Processing done=== '


if __name__ == '__main__':
	my_arg_parse()
