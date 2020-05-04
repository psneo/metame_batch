import sys
import os
import shutil
import metame.r2parser as r2parser
import argparse



def mutate(input_, output_, debug, force, log_path):
    r = r2parser.R2Parser(input_, True, debug=debug, force_replace=force)
    patches = r.iterate_fcn()
    r.close()
    if patches:
        dir_ = os.path.dirname(output_)
        os.makedirs(dir_, exist_ok=True)
        shutil.copy(input_, output_)

        r = r2parser.R2Parser(output_, False, debug=debug, write=True)
        r.patch_binary(patches)
        r.close()
    else:
        print("unable to mutate {0}".format(input_))
        if log_path:
            with open(log_path, "a") as myfile:
                myfile.write("unable to mutate {0}\n".format(input_))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metamorphic engine that modifies assembly code keeping the same functionality")
    parser.add_argument("-i", "--input", help="input path")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-b", "--batch", action="store_true", help="batch mode")
    parser.add_argument("-d", "--debug", action="store_true", help="print debug information")
    parser.add_argument("-f", "--force", action="store_true", help="force instruction replacement when possible (decreases metamorphism entropy!)")
    args = parser.parse_args()

    if args.batch:
        output_dir = None
        if not args.input:
            parser.print_help()
            sys.exit(1)

        if not os.path.isdir(args.input):
            print("Batch mode selected but input is not a directory")
            sys.exit(1)

        if not args.output:
            output_dir = os.path.join(os.pathos.getcwd(),"output")
            print("mutated files will be saved in {0}".format(output_dir))
        else:
	        output_dir = os.path.join(args.output,"metame_output")

        os.makedirs(output_dir)
        
        # create log file
        log_path = os.path.join(output_dir, "metame.log")
        if not os.path.exists(log_path ):
            with open(log_path, "w"): pass


        base_filepath = os.path.abspath(args.input)
        for subdir, dirs, files in os.walk(base_filepath):
            for file_ in files:
                filepath = os.path.join(subdir, file_)
                if filepath.startswith(output_dir):
                    continue
                r_filepath = filepath.replace(base_filepath,"")
                output_p = os.path.join(output_dir, r_filepath[1:])
                mutate(filepath, output_p, args.debug, args.force, log_path)
        		
    else:
        if not args.input or not args.output:
            parser.print_help()
            sys.exit(1)
        mutate(args.input, args.output, args.debug, args.force)
