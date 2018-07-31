import csgolounge
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id",help="PHPSESSID on csgo lounge")
    parser.add_argument("-sleep",help="Count seconds of sleep",type=int)
    parser.add_argument("-fv",help="Your float value which you want to find",type=float)
    parser.add_argument("-start",help="Start url to find (277000000)",type=int)
    parser.add_argument("-end",help="End url to find (277000000)",type=int)
    args = parser.parse_args()
    if args.id and args.sleep:
        csgolounge.PHPSESSID = args.id
        if args.fv:
            csgolounge.FLOAT = args.fv
        if args.start:
            csgolounge.START = args.start
        if args.end:
            csgolounge.END = args.end
        csgolounge.StartFinder(args.sleep)
    else:
        print('Type -h for help')
