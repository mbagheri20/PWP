import ikkunasto as ui

state={
    "text box": None,
    "write box": None,
    "oikea": None,
    "vasen": None,
    "nappi" : None
}

material = {
    "name": None
}

material_volume = {
    "size a": None,
    "size b": None,
    "size c": None,
    "dimension type": None,
    "bonding length": None,
    "material": None
}

material_fermi = {
    "fermi": None,
    "material": None,
    "volume": None
}


def add_material():
    state["nappi"].destroy()
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter name below", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_post_material)

def send_post_material():
    try:
        material["name"] = ui.lue_kentan_sisalto(state["write box"])
    except:
        pass
    print(material) #Make the post request here

def add_material_volume():
    state["nappi"].destroy()
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume information below separated by commas", True)
    ui.kirjoita_tekstilaatikkoon(state["text box"], "size a, size b, size c, dimension type, bonding length, material")
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_post_material_volume)

def send_post_material_volume():
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    try:
        material_volume["size a"] = text[0]
        material_volume["size b"] = text[1]
        material_volume["size c"] = text[2]
        material_volume["dimension type"] = text[3]
        material_volume["bonding length"] = text[4]
        material_volume["material"] = text[5]
    except:
        pass
    print(material_volume) #Make the post request here

def add_material_fermi():
    state["nappi"].destroy()
    ui.kirjoita_tekstilaatikkoon(state["text box"],  "Enter material fermi information below separated by commas", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_post_material_fermi)

def send_post_material_fermi():
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    try:
        material_fermi["fermi"] = text[0]
        material_fermi["material"] = text[1]
        material_fermi["volume"] = text[2]
    except:
        pass
    print(material_fermi)

def search_material():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material name for specific material or leave it blank for all materials", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_get_material)

def send_get_material():
    text = ui.lue_kentan_sisalto(state["write box"])
    if(text != None):
        materials = "only one" #get one materials here
    else:
        materials = "all" #get all material here
    ui.kirjoita_tekstilaatikkoon(state["text box"], materials, True)

def search_material_volume():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume id for specific material volume or leave it blank for all materials", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_get_material_volume)

def send_get_material_volume():
    text = ui.lue_kentan_sisalto(state["write box"])
    if(text != None):
        materials = "only one" #get one materials here
    else:
        materials = "all" #get all material here
    ui.kirjoita_tekstilaatikkoon(state["text box"], materials, True)

def search_material_fermi():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi id for pecific material ors leave it blank for all materials", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_get_material_fermi)

def send_get_material_fermi():
    text = ui.lue_kentan_sisalto(state["write box"])
    if(text != None):
        materials = "only one" #get one materials here
    else:
        materials = "all" #get all material here
    ui.kirjoita_tekstilaatikkoon(state["text box"], materials, True)

def edit_material():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material  name for editing", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_put_material)

def send_put_material():
    try:
        response = "a response"
    except:
        pass
    ui.kirjoita_tekstilaatikkoon(state["text box"], response, True) #print print

def edit_material_volume():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume id for editing", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_put_material_volume)

def send_put_material_volume():
    try:
        response = "a response"
    except:
        pass
    ui.kirjoita_tekstilaatikkoon(state["text box"], response, True) #print print

def edit_material_fermi():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi id for editing", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_put_material_fermi)

def send_put_material_fermi():
    try:
        response = "a response"
    except:
        pass
    ui.kirjoita_tekstilaatikkoon(state["text box"], response, True) #print print

def delete_material():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material name for delete", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_delete_material)

def send_delete_material():
    try:
        response = "a response"
    except:
        pass
    ui.kirjoita_tekstilaatikkoon(state["text box"], response, True) #print print

def delete_material_volume():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume id for delete", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_delete_material_volume)

def send_delete_material_volume():
    try:
        response = "a response"
    except:
        pass
    ui.kirjoita_tekstilaatikkoon(state["text box"], response, True) #print print

def delete_material_fermi():
    state["nappi"].destroy()
    state["write box"] = None
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi id for delete", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_delete_material_fermi)

def send_delete_material_fermi():
    try:
        response = "a response"
    except:
        pass
    ui.kirjoita_tekstilaatikkoon(state["text box"], response, True) #print print

def empty():
    pass

def main():
    ikkuna = ui.luo_ikkuna("Material Database")
    state["vasen"] = ui.luo_kehys(ikkuna, ui.VASEN)
    state["oikea"] = ui.luo_kehys(ikkuna, ui.OIKEA)
    ui.luo_nappi(state["vasen"], "Add material", add_material)
    ui.luo_nappi(state["vasen"], "Add material volume", add_material_volume)
    ui.luo_nappi(state["vasen"], "Add material fermi", add_material_fermi)
    ui.luo_nappi(state["vasen"], "Search for material", search_material)
    ui.luo_nappi(state["vasen"], "Search for material volume", search_material_volume)
    ui.luo_nappi(state["vasen"], "Search for material fermi", search_material_fermi)
    ui.luo_nappi(state["vasen"], "Edit a material", edit_material)
    ui.luo_nappi(state["vasen"], "Edit a material volume", edit_material_volume)
    ui.luo_nappi(state["vasen"], "Edit a material fermi", edit_material_fermi)
    ui.luo_nappi(state["vasen"], "Delete a material", delete_material)
    ui.luo_nappi(state["vasen"], "Delete a material volume", delete_material_volume)
    ui.luo_nappi(state["vasen"], "Delete a material fermi", delete_material_fermi)
    ui.luo_nappi(state["vasen"], "Quit", ui.lopeta)
    state["text box"] = ui.luo_tekstilaatikko(state["oikea"], 50,30)
    state["write box"] = ui.luo_tekstikentta(state["oikea"])
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", empty)
    
    ui.kaynnista()

main()