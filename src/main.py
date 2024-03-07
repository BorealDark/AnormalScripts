import argparse
from optimization import *
pd.options.mode.chained_assignment = None  # default='warn'


parser = argparse.ArgumentParser(
    description='Programa que optimiza diferentes procesos de mi trabajo en Steam.',
    epilog="Example of use: python .\src\main.py -cs")

#MARKETPLACE.TF
parser.add_argument('-mpibp', '--mpinventoryBpPrices', help= "creates an Excel spreadsheet containing a list of items that has to be put for sale on the Marketplace.tf shop (CHECK BP PRICES (PRICES.TF))", required=False, action='store_true')
parser.add_argument('-mpi', '--mpinventoryNoBpPrices', help= "creates an Excel spreadsheet containing a list of items that has to be put for sale on the Marketplace.tf shop (DOESN'T CHECK BP PRICES)", required=False, action='store_true')

parser.add_argument('-mpl', '--mplooses', help= "generates an Excel spreadsheet highlighting items that are currently resulting in losses on the Marketplace.tf shop", required=False, action='store_true')

#LOOT.FARM
parser.add_argument('-lr', '--lootfarmrust', help = "creates an Excel spreadsheet with the best RUST items from loot.farm", required=False, action='store_true')
parser.add_argument('-lt', '--lootfarmtf', help = "creates an Excel spreadsheet with the best TF2 items from loot.farm", required=False, action='store_true')

#BACKPACK
parser.add_argument('-bpscm', '--bptoscm', help = 'Profitable TF2 items (BACKPACK BUY ORDER) to sell on the scm', required=False, action='store_true')
parser.add_argument('-bpsoscm', '--bpsotoscm', help = 'Profitable TF2 items (BACKPACK SELL ORDER) to sell on the scm', required=False, action='store_true')



def parse():
    return parser.parse_args()

def usage_help():
    return parser.print_help()

def main():
    print("lol")

if __name__ == '__main__':
    args = parser.parse_args()


    #MARKETPLACE.TF
    if(args.mpinventoryBpPrices):
        print("Generating an Excel spreadsheet containing a list of items that has to be put for sale on the Marketplace.tf shop")
        Optimization().getMarketplaceItems(True)
    
    if(args.mpinventoryNoBpPrices):
        print("Generating an Excel spreadsheet containing a list of items that has to be put for sale on the Marketplace.tf shop")
        Optimization().getMarketplaceItems(False)

    if(args.mplooses):
        print("Generating an Excel spreadsheet highlighting items that are currently resulting in losses on the Marketplace.tf shop")
        Optimization().getNonProfitableMarketplaceItems()

    #LOOT.FARM
    if(args.lootfarmrust):
        print("Generating an Excel spreadsheet containing a list of profitable RUST items from loot.farm")
        Optimization().lootfarm(252490)

    if(args.lootfarmtf):
        print("Generating an Excel spreadsheet containing a list of profitable TF2 items from loot.farm")
        Optimization().lootfarm(440)

    #BACKPACK

    if(args.bptoscm):
        print("Getting all the profitable tf2 items from bp buy orders to sell on scm")
        Optimization().bpbotoscm()
    
    if(args.bpsotoscm):
        print("Getting all the profitable tf2 items from bp sell orders to sell on scm")
        Optimization().bpsotoscm()

