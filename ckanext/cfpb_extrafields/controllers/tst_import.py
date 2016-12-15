from ckanext.cfpb_extrafields.digutils import make_rec

if __name__ == "__main__":
    with open("/home/cfpb/boehmm/dig.xlsm", "r") as f:
        result = make_rec(f)
        print repr(result)
