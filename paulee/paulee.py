from bs4 import BeautifulSoup
import re

with open("./paulee/Paulee.html") as page:
    soup = BeautifulSoup(page, "html.parser")

merchants={}

wineclimates = {
    "Chablis" : 
        { 
            "Grand Cru": ["Blanchot"," Bougros"," Grenouilles"," La Moutonne"," Les Clos"," Preuses"," Valmur"," Vaudesir"],
            "Premier Cru" :['Beauroy','Berdiot','Beugnons','Butteaux','Chapelot','Chatains','Chaume de Talvat','Cote de Brechain','Cote de Cuissy','Cote de Fontenay','Cote de Jouan','Cote de Lechet','Cote de Savant','Cote de Vaubarousse','Cote des Pres Girots','Forets','Fourchaume','L\'Homme Mort','Les Beauregards','Les Epinottes','Les Fourneaux','Les Lys','Melinots','Mont de Milieu','Montee de Tonnerre','Montmains','Morein','Pied d\'Aloup','Roncieres','Sechet','Troesmes','Vaillons','Vau Ligneau','Vau Ragons','Vau de Vey','Vaucoupin','Vaugiraut','Vaulorent','Vaupulent','Vosgros']
        },
    "Côte de Beaune" :
        {

            'Aloxe-Corton' : [],
            'Auxey-Duresses' : [],
            'Beaune': [],
            'Blagny' : [],
            'Chassagne-Montrachet' : [],
            'Chorey-les-Beaune' : [],
            'Corton Grand Cru' : [],
            'Cote de Beaune-Villages' : [],
            'Ladoix' : [],
            'Maranges' : ['1er Cru Clos de la Boutiere','1er Cru Clos de la Fussiere','1er Cru La Fussière','1er Cru Le Clos des Loyeres','1er Cru Le Clos des Rois','1er Cru Le Croix Moines','1er Cru Les Clos Roussots'],
            'Meursault' : [],
            'Monthelie' : [],
            'Pernand-Vergelesses' : [],
            'Pommard' : [],
            'Puligny-Montrachet' : ['Bâtard-Montrachet','Bienvenues-Bâtard-Montrachet','Chevalier-Montrachet','Le Montrachet','Puligny-Montrachet\\s*(1er Cru)?'],
            'Saint-Aubin' : [],
            'Saint-Romain' : [],
            'Santenay' : [],
            'Savigny-les-Beaune' : [],
            'Volnay' : []
        },
    "Côte de Nuits" :
        {
            "Gevrey-Chambertin" : ["Chambertin-Clos de Bèze","Charmes-Chambertin","Chapelle-Chambertin","Griotte-Chambertin","Le Chambertin","Latricières-Chambertin","Mazis-Chambertin","Ruchottes-Chambertin"],
            "Morey-St.Denis" : ["Clos de la Roche","Clos de Tart","Clos des Lambrays","Clos Saint Denis"],
            "Chambolle-Musigny" : ["Bonnes Mares","Le Musigny","Clos de Vougeot","Clos Vougeot"],
            "Flagey-Echézeaux" : ["Echézeaux","Grands Echézeaux"],
            "Vosne-Romanée" : ["La Grande Rue","La Romanée","La Tâche" ,"Richebourg","Romanée-Conti","Romanée-Saint-Vivant"],
            "Côte de Beaune" : ["Corton-Charlemagne","Le Corton","Corton"],
            "Chablis" : [],
            "Beaujolais" : [],
            "Bourgogne" : [],
            "Chassagne-Montrachet" : []
        }
}


def get_wine_climates():
    #chablis
    climate_list=[]
    for region in wineclimates:
        for village in wineclimates[region]:
            climates=wineclimates[region]
            for climate in climates:
                climatecollection=climates[climate]
                for name in climatecollection:
                    winename = "{2}:{1}:({0})?".format(region.strip(),village.strip(),name.strip())
                    climate_list.append('\s*'.join(winename.split(':')[::-1]))
    return climate_list


def print_merchants(climates):
    for key, value in merchants.items():
        for m in value:
            match = list(filter(lambda name: re.match(name,m) , climates))
            if len(match) > 0:
                print("Match")
                break



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
                        #if found is False:
                        #    print("--{0}".format(winename))
                    terroircollection.append(winename)
                if len(terroircollection) > 0:
                    merchants.update({p.string:terroircollection})
            except:
                pass
    
if __name__ == "__main__":
    climates = get_wine_climates()
    scann_page()
    print_merchants(climates)