import numpy
import argparse
import glob
from matplotlib import pyplot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("fnames", help = "VNA txt file/s to plot. Can be globed.")
    parser.add_argument("fnames", help = "VNA txt file/s to plot. Can be globed.")
    parser.add_argument("-t", "--title", type = str, default = None, help = "Title of graph")
    parser.add_argument("-x", "--x-label", type = str, default = None, help = "X label of graph")
    parser.add_argument("-y", "--y-label", type = str, default = None, help = "Y label of graph")
    parser.add_argument("-l", "--x-limits", type = str, default = None, help = "X limits for graph")
    parser.add_argument("-L", "--y-limits", type = str, default = None, help = "Y limits for graph")
    parser.add_argument("-s", "--save", type = str, default = None, help = "Write png of figure with supplied name")
    args=parser.parse_args()

    fnames = sorted(glob.glob(args.fnames))

    data = "PRIZM-100-NS-S11.txt"

    for fname in fnames:
        fopen = open(fname, "r")
        lines = fopen.readlines()[46:]

        temp_line = lines[0].replace(",", ".")
        print(temp_line)
        data = numpy.array([map(float, temp_line.split()[:3])])

        for line in lines[1:]:
            temp_line = line.replace(",", ".")
            values = numpy.array([map(float, temp_line.split()[:3])])
            data = numpy.append(data, values, axis=0)
        print("file name", fname, "Data Shape", data.shape)
        #mean = numpy.mean(data[:,1])*numpy.ones(data.shape[0])
        #pyplot.plot(data[:,0]/1.0e6, mean, label="mean")
        pyplot.plot(data[:,0]/(1.0e6), data[:,1], label=fname[fname.rfind("/")+1:-4])

    if args.x_limits != None:
        limits = args.x_limits.split(":")
        pyplot.xlim(float(limits[0]),float(limits[1]))

    if args.y_limits != None:
        limits = args.y_limits.split(":")
        pyplot.ylim(float(limits[0]), float(limits[1]))

    if args.title != None:
        pyplot.title(args.title)

    if args.x_label != None:
        pyplot.xlabel(args.x_label)

    if args.y_label != None:
        pyplot.ylabel(args.y_label)

    #pyplot.legend(loc='lower center', ncol=6)
    pyplot.legend(loc='lower right')

    if args.save != None:
        pyplot.savefig(args.save)
    else:
        pyplot.show()
