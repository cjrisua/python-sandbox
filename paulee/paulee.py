from bs4 import BeautifulSoup
import re

with open("./paulee/Paulee.html") as page:
    soup = BeautifulSoup(page, "html.parser")

merchants={}

villages = { 
    "Gevrey-Chambertin" : ["Chambertin-Clos de Bèze","Charmes-Chambertin","Chapelle-Chambertin","Griotte-Chambertin","Le Chambertin","Latricières-Chambertin","Mazis-Chambertin","Ruchottes-Chambertin"],
    "Morey-St.Denis" : ["Clos de la Roche","Clos de Tart","Clos des Lambrays","Clos Saint Denis"],
    "Chambolle-Musigny" : ["Bonnes Mares","Le Musigny","Clos de Vougeot","Clos Vougeot"],
    "Flagey-Echézeaux" : ["Echézeaux","Grands Echézeaux"],
    "Vosne-Romanée" : ["La Grande Rue","La Romanée","La Tâche" ,"Richebourg","Romanée-Conti","Romanée-Saint-Vivant"],
    "Côte de Beaune" : ["Corton-Charlemagne","Le Corton","Corton"],
    "Puligny-Montrachet" : ["Bâtard-Montrachet","Bienvenues-Bâtard-Montrachet","Chevalier-Montrachet","Le Montrachet"]
    "Chablis" : [],
    "Beaujolais" : [],
    "Bourgogne" : [],
    "Chassagne-Montrachet" : []
 }

def print_merchants():
    for key, value in merchants.items():
        for m in value:
            print("{0},{1}".format(key,m))


def scann_page():
    print("Start Scanning")
    divcollection = soup.find_all("div", id="block-3d19470d13313378c002")
    div = next(divcollection[0].children)
    
    for p in  soup.find_all("p"):
        if p.string is None:
            pass
        else:
            places =p.next_sibling
            try:
                terroircollection=[]
                for terroir in list(filter(lambda x: x.string is not None,places.contents)):
                    winename = terroir
                    if terroir.name == "em":
                        item_index = terroircollection.index(terroir.previous_sibling.string)
                        terroircollection[item_index] = "{0} {1}".format(terroircollection[item_index],terroir.string)
                        winename = terroircollection[item_index]

                    #grab vintage
                    vintage = re.search(r"20[0-9]{2}", winename)
                    #village
                    
                    #winevillage = filter(lambda n: str(winename).__contains__(n), list(villages.keys()))
                    if "Grand" in winename:
                        found = False
                        for parcel in villages:
                            wineparcel = list(filter(lambda n: str(winename).__contains__(n), list(villages[parcel])))
                            if len(wineparcel) > 0:
                                found = True
                                #print("Famus Parcel {0}=>{1}".format(parcel,villages[parcel][0]))
                                break
                        if found is False:
                            print("--{0}".format(winename))

                    terroircollection.append(winename)
                if len(terroircollection) > 0:
                    merchants.update({p.string:terroircollection})
            except:
                pass
    
if __name__ == "__main__":
    scann_page()
    #print_merchants()