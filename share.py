import os
import nextcord

async def create_image(datacard):
    list_file = []
    file_url = "./sda_cgbuilder/images/simulateur/carte/"+datacard['id_extension']+"/"+ datacard['numero_identification']+".jpg"
    if os.path.isfile(file_url):
        list_file.append(file_url)
    else:
        file_url = "./sda_cgbuilder/images/simulateur/carte_horizontale/"+datacard['id_extension']+"/"+ datacard['numero_identification']+".jpg"
        if os.path.isfile(file_url):
           list_file.append(file_url)
        else:
            file_url = "./sda_cgbuilder/images/simulateur/carte_horizontale/"+datacard['id_extension']+"/"+ datacard['numero_identification']+"A.jpg"
            if os.path.isfile(file_url):
               list_file.append(file_url)
               file_urlB = "./sda_cgbuilder/images/simulateur/carte_horizontale/"+datacard['id_extension']+"/"+ datacard['numero_identification']+"B.jpg"
               list_file.append(file_urlB)
    return await list_file

async def sendcard(self,interaction,datacard):
    """ beautiful embed """
    sphere, sphere_color = info_sphere(datacard)
    cycle=info_cycle(datacard)
    file_url = "./sda_cgbuilder/images/simulateur/carte/"+datacard['id_extension']+"/"+ datacard['numero_identification']+".jpg"
    embed = nextcord.Embed(title=datacard['titre'],color=sphere_color)
    file = nextcord.File(file_url, filename="image.jpg")
    pack_file = nextcord.File(f"./assets/pack/{datacard['id_extension']}.png", filename="pack.png")
    embed.set_author(name=f"{datacard['lbl extension']}", url= f"https://sda.cgbuilder.fr/liste_carte/{datacard['id_extension']}/")
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_image(url="attachment://image.jpg")
    embed.set_footer(text=f"{cycle}")
    await interaction.send(files=[file,pack_file], embed=embed)

def info_cycle(datacard):
    cycle=""
    if datacard['id_extension'] in ['2', '3', '4', '5', '6', '7']:
        cycle="Cycle 1 : Ombres de la Forêt Noire"
    if datacard['id_extension'] in ['8', '9', '10', '11', '12', '13', '14']:
        cycle="Cycle 2 : Royaume de Cavenain"
    if datacard['id_extension'] in ['15', '16', '17', '18', '19', '20', '21']:
        cycle="Cycle 3 : Face à l'Ombre"
    if datacard['id_extension'] in ['22', '23', '24', '25', '26', '27', '28']:
        cycle="Cycle 4 : Le Créateur d'Anneaux"
    if datacard['id_extension'] in ['29', '30', '31', '32', '33', '34', '35']:
        cycle="Cycle 5 : Le Réveil d'Angmar"
    if datacard['id_extension'] in ['36', '37', '38', '39', '40', '41', '42']:
        cycle="Cycle 6 : Chasse-Rêve"
    if datacard['id_extension'] in ['50', '51', '52', '53', '54', '55', '56']:
        cycle="Cycle 7 : Les Haradrim"
    if datacard['id_extension'] in ['65', '66', '68', '69', '70', '71', '72']:
        cycle="Cycle 8 : Ered Mithrin"
    if datacard['id_extension'] in ['73', '74', '75', '76', '77', '78', '79']:
        cycle="Cycle 9 : La Vengeance du Mordor"
    if datacard['id_extension'] == "43":
        cycle="Extension de saga : Par Monts et par Souterrains"
    if datacard['id_extension'] == "44":
        cycle="Extension de saga : Au Seuil de la Porte"
    if datacard['id_extension'] == "45":
        cycle="Extension de saga : Les Cavaliers Noirs"
    if datacard['id_extension'] == "46":
        cycle="Extension de saga : La Route s'Assombrit"
    if datacard['id_extension'] == "47":
        cycle="Extension de saga : La Trahison de Saroumane"
    if datacard['id_extension'] == "48":
        cycle="Extension de saga : La Terre de l'Ombre"
    if datacard['id_extension'] == "49":
        cycle="Extension de saga : La Flamme de l'Ouest"
    if datacard['id_extension'] == "57":
        cycle="Extension de saga : La Montagne de Feu"
    if datacard['id_extension'] in ['80', '81', '90', '92', '93', '95', '96']:
        cycle=["Serment des Rohirrim (ALEP)"]
    if datacard['id_extension'] in ['86', '97']:
        cycle=["Scénario Indépendant (ALEP)"]
    if datacard['id_extension'] == "89":
        cycle="Les Ténèbres de la Forêt Noire"
    return cycle

def info_sphere(datacard):
    sphere, sphere_color ="", 0xFFFFFF
    if datacard['id_sphere_influence'] == "300":
        sphere="leadership", 0x8B23F9
    if datacard['id_sphere_influence'] == "301":
        sphere, sphere_color ="lore",  0x0E7A12
    if datacard['id_sphere_influence'] == "302":
        sphere, sphere_color ="spirit",0x33DDFF
    if datacard['id_sphere_influence'] == "303":
        sphere, sphere_color ="tactics",0xDB140B
    if datacard['id_sphere_influence'] == "304":
        sphere, sphere_color ="neutral",0x797B7A
    if datacard['id_sphere_influence'] == "305":
        sphere, sphere_color ="fellowship",0xD99611
    if datacard['id_sphere_influence'] == "306":
        sphere, sphere_color ="baggins",0xD3D911
    return sphere, sphere_color


def get_id_type_carte(word):
    match word:
        case "Héro":
            return "400"
        case "Allié":
            return "401"
        case "Evènement":
            return "402"
        case "Attachement":
            return "403"
        case "Objectif Allié":
            return "409"
        case "Trésor":
            return "410"
        case "Campagne":
            return "411"
        case "Quête Annexe Joueur":
            return "412"
        case "Navire Objectif":
            return "413"
        case "Objectif Héros":
            return "414"
        case "Contrat":
            return "418"      
        case _:
            return "all"
        
def get_id_sphere(word):
    match word:
        case "Commandement":
            return "300"
        case "Connaissance":
            return "301"
        case "Energie":
            return "302"
        case "Tactique":
            return "303"
        case "Neutre":
            return "304"
        case "Communauté":
            return "305"        
        case "Sacquet":
            return "306"
        case _:
            return "all"