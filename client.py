import ikkunasto as ui
import requests
from flask import Response
import json
 
SERVER_URL = "http://127.0.0.1:5000" 
 
state={
    "text box": None,
    "write box": None,
    "oikea": None,
    "vasen": None,
    "nappi" : None,
    "previous text": None
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
    #try:
    material["name"] = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.post(SERVER_URL + "/api/material/", data=json.dumps(material))
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
 
def add_material_volume():
    state["nappi"].destroy()
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume information below separated by commas", True)
    ui.kirjoita_tekstilaatikkoon(state["text box"], "size a, size b, size c, dimension type, bonding length, material")
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_post_material_volume)
 
def send_post_material_volume():
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    #try:
    material_volume["size a"] = text[0]
    material_volume["size b"] = text[1]
    material_volume["size c"] = text[2]
    material_volume["dimension type"] = text[3]
    material_volume["bonding length"] = text[4]
    material_volume["material"] = text[5]
    resp = requests.post(SERVER_URL + "/api/material_volume/", data=json.dumps(material_volume))
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def add_material_fermi():
    state["nappi"].destroy()
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi information below separated by commas", True)
    ui.kirjoita_tekstilaatikkoon(state["text box"], "fermi, material name, material volume id")
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_post_material_fermi)
 
def send_post_material_fermi():
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    #try:
    material_fermi["fermi"] = text[0]
    material_fermi["material"] = text[1]
    material_fermi["volume"] = text[2]
    resp = requests.post(SERVER_URL + "/api/material_fermi/", data=json.dumps(material_fermi))
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def search_material():
    state["nappi"].destroy()
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", empty)
    resp = requests.get(SERVER_URL + "/api/material/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
 
def search_material_volume():
    state["nappi"].destroy()
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", empty)
    resp = requests.get(SERVER_URL + "/api/material_volume/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
 
 
def search_material_fermi():
    state["nappi"].destroy()
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", empty)
    resp = requests.get(SERVER_URL + "/api/material_fermi/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
 
 
def search_material_indi():
    state["nappi"].destroy()
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material name for specific material", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_get_material_indi)
 
def send_get_material_indi():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.get(SERVER_URL + "/api/material/" + text + "/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def search_material_volume_indi():
    state["nappi"].destroy() 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume id for specific material volume", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_get_material_volume_indi)
 
def send_get_material_volume_indi():
    #try: 
    text = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.get(SERVER_URL + "/api/material_volume/" + text + "/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def search_material_fermi_indi():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi id for specific material fermi", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_get_material_fermi_indi)
 
def send_get_material_fermi_indi():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.get(SERVER_URL + "/api/material_fermi/" + text + "/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def edit_material():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material name that you want to edit, and after that name that you want it to be changed to seperated with a comma", True)
    ui.kirjoita_tekstilaatikkoon(state["text box"], "name, new name")
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_put_material)
 
def send_put_material():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    data = {"handle": text[1]}
    resp = requests.put(SERVER_URL + "/api/material/" + text[0] + "/", data=json.dumps(data))
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def edit_material_volume():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume id that you want to edit, and after that every variable seperated by a comma", True)
    ui.kirjoita_tekstilaatikkoon(state["text box"], "id, size a, size b, size c, dimension type, bonding length, material")
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_put_material_volume)
 
def send_put_material_volume():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    material_volume["size a"] = text[1]
    material_volume["size b"] = text[2]
    material_volume["size c"] = text[3]
    material_volume["dimension type"] = text[4]
    material_volume["bonding length"] = text[5]
    material_volume["material"] = text[6]
    resp = requests.put(SERVER_URL + "/api/material_volume/" + text[0] + "/", data=json.dumps(material_volume))
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def edit_material_fermi():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi id that you want to edit, and after that each variable seperated by a comma", True)
    ui.kirjoita_tekstilaatikkoon(state["text box"], "fermi, material name, material volume id")
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_put_material_fermi)
 
def send_put_material_fermi():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    text = text.split(",")
    data = {
        "fermi": text[1],
        "material": text[2],
        "volume id": text[3]
    }
    resp = requests.put(SERVER_URL + "/api/material_fermi/" + text[0] + "/", data=json.dumps(data))
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def delete_material():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material name for delete", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_delete_material)
 
def send_delete_material():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.delete(SERVER_URL + "/api/material/" + text + "/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def delete_material_volume():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material volume id for delete", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_delete_material_volume)
 
def send_delete_material_volume():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.delete(SERVER_URL + "/api/material_volume/" + text + "/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
def delete_material_fermi():
    state["nappi"].destroy()
 
    ui.kirjoita_tekstilaatikkoon(state["text box"], "Enter material fermi id for delete", True)
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", send_delete_material_fermi)
 
def send_delete_material_fermi():
    #try:
    text = ui.lue_kentan_sisalto(state["write box"])
    resp = requests.delete(SERVER_URL + "/api/material_fermi/" + text + "/")
    printable = "Status code {}, header {}\nBody {}".format(resp.status_code, resp.headers, resp.text)
    ui.kirjoita_tekstilaatikkoon(state["text box"], printable, True)
    #except:
    #    ui.kirjoita_tekstilaatikkoon(state["text box"], "Something went wrong", True)
 
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
    ui.luo_nappi(state["vasen"], "Search for an individual material", search_material_indi)
    ui.luo_nappi(state["vasen"], "Search for an individual material volume", search_material_volume_indi)
    ui.luo_nappi(state["vasen"], "Search for an individual material fermi", search_material_fermi_indi)
    ui.luo_nappi(state["vasen"], "Edit a material", edit_material)
    ui.luo_nappi(state["vasen"], "Edit a material volume", edit_material_volume)
    ui.luo_nappi(state["vasen"], "Edit a material fermi", edit_material_fermi)
    ui.luo_nappi(state["vasen"], "Delete a material", delete_material)
    ui.luo_nappi(state["vasen"], "Delete a material volume", delete_material_volume)
    ui.luo_nappi(state["vasen"], "Delete a material fermi", delete_material_fermi)
    ui.luo_nappi(state["vasen"], "Quit", ui.lopeta)
    state["text box"] = ui.luo_tekstilaatikko(state["oikea"], 100,40)
    state["write box"] = ui.luo_tekstikentta(state["oikea"])
    state["nappi"] = ui.luo_nappi(state["oikea"], "Submit", empty)
 
    ui.kaynnista()
 
main()