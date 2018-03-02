#!/usr/bin/env python3

import libTwitterAnalysis

def analyseHashtag(query):
    tweets = libTwitterAnalysis.search("#" + query, maxTweets=5000, fName=query + ".txt")
    return libTwitterAnalysis.analyseTweets(tweets)

def getCriptoFromFile(file):
    lines = []
    with open(input_file) as f:
        lines = f.readlines()
    return lines

def main(argv):
    inputfile = ''
    domaine = ''
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["ifile="])
    except getopt.GetoptError:
        print ('createDNSRecords.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('createDNSRecords.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    cryptocurrencies = getCriptoFromFile(inputfile)
    for cryptocurrency in cryptocurrencies_names:
        cryptocurrencies.append(analyseHashtag(cryptocurrency))

if __name__ == '__main__':
    main(sys.argv[1:])
