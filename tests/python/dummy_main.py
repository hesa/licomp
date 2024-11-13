import json
import sys

from licomp.main_base import LicompParser
from test_lcm import DummyLicense

def main():
    o_parser = LicompParser(DummyLicense(),
                            name = "Dummy license impl",
                            description = "Just a dummy impl",
                            epilog = "Do not use")
    o_parser.run()
    
if __name__ == '__main__':
    main()
