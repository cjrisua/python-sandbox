from bs4 import BeautifulSoup

with open("./paulee/Paulee.html") as page:
    soup = BeautifulSoup(page, "html.parser")

merchants={}

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
                    if terroir.name == "em":
                        item_index = terroircollection.index(terroir.previous_sibling.string)
                        terroircollection[item_index] = terroircollection[item_index] + " "+ terroir.string
                    else:
                        terroircollection.append(terroir)
                if len(terroircollection) > 0:
                    merchants.update({p.string:terroircollection})
            except:
                pass
    
if __name__ == "__main__":
    scann_page()
    print_merchants()