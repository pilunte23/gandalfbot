import os
import nextcord
from nextcord import File, Embed
from PIL import Image
import re

def create_image(datacard):
    find=False
    """ add every patch in the list img """
    list_img = []
    file_url = "./sda_cgbuilder/images/simulateur/carte/"+datacard['id_extension']+"/"+ datacard['numero_identification']+".jpg"
    if os.path.isfile(file_url):
        list_img.append(file_url)
    file_url = "./sda_cgbuilder/images/simulateur/carte/"+datacard['id_extension']+"/"+ datacard['numero_identification']+"A.jpg"
    if os.path.isfile(file_url):
        list_img.append(file_url)
    file_url = "./sda_cgbuilder/images/simulateur/carte/"+datacard['id_extension']+"/"+ datacard['numero_identification']+"B.jpg"
    if os.path.isfile(file_url):
        list_img.append(file_url)

    #max width, height

    max_width = 0
    max_height = 0
    total_width = 0
    total_height = 0
    for i in list_img:
        im = Image.open(i)
        w, h = im.size
        total_width += w
        total_height += h
        if max_width < w:
            max_width = w
        if max_height < h:
            max_height = h
    print(list_img)
    if len(list_img) > 0:
        find= True
        """ creating the new img who will be send """
        new_img = Image.new('RGB', (total_width, max_height), (250,250,250))
        """ we paste every image in the new_img """
        largeur=0
        for i in list_img:
            image = Image.open(i)
            w, h = image.size
            new_img.paste(image, (largeur, 0))
            largeur += w
        """ saving the result in a png """
        new_img.save("./createimage.png", "PNG" )
    return find

async def sendcard(self,interaction,datacard):
    """ beautiful embed """
    sphere, sphere_color, sphere_emoji = info_sphere(self,datacard)
    cycle=info_cycle(datacard)

    embed = Embed(title=f"{sphere_emoji} {datacard['titre']}",color=sphere_color)
    find_image= create_image(datacard)
 
    pack_file = File(f"./assets/pack/{datacard['id_extension']}.png", filename="pack.png")
    embed.set_author(name=f"{datacard['lbl extension']}", url= f"https://sda.cgbuilder.fr/liste_carte/{datacard['id_extension']}/")
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_footer(text=f"{cycle}")
    if find_image:
        file_url="./createimage.png"
        file = File(file_url, filename="image.jpg")
        embed.set_image(url="attachment://image.jpg")
        await interaction.send(files=[file,pack_file], embed=embed)
    else:
        if datacard['texte']:
            embed.add_field(name = "", value =f"{convert(self,datacard['texte'])}")   
        await interaction.send(files=[pack_file], embed=embed)


def convert(self,text):
    rep = {"<b>": "**","</b>": "**","<i>": "*","</i>": "*","<br>": "\n"} 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text= text.replace("$gouvernail$", str(nextcord.utils.get(self.bot.emojis, name='gouvernail')))
    text= text.replace("$attaque$", str(nextcord.utils.get(self.bot.emojis, name='attack')))
    text= text.replace("$defense$", str(nextcord.utils.get(self.bot.emojis, name='defense')))
    text= text.replace("$menace$", str(nextcord.utils.get(self.bot.emojis, name='threat')))
    text= text.replace("$volonte$", str(nextcord.utils.get(self.bot.emojis, name='willpower')))
    text= text.replace("$orage$", str(nextcord.utils.get(self.bot.emojis, name='orage')))
    text= text.replace("$pluie$", str(nextcord.utils.get(self.bot.emojis, name='pluie')))
    text= text.replace("$nuage$", str(nextcord.utils.get(self.bot.emojis, name='nuage')))
    text= text.replace("$sacquet$", str(nextcord.utils.get(self.bot.emojis, name='baggins')))
    text= text.replace("$oeil$", str(nextcord.utils.get(self.bot.emojis, name='oeil')))
    text= text.replace("$communaute$", str(nextcord.utils.get(self.bot.emojis, name='fellowship')))
    text= text.replace("$tactique$", str(nextcord.utils.get(self.bot.emojis, name='tactics')))
    text= text.replace("$connaissance$", str(nextcord.utils.get(self.bot.emojis, name='lore')))
    text= text.replace("$commandement$", str(nextcord.utils.get(self.bot.emojis, name='leadership')))
    text= text.replace("$energie$", str(nextcord.utils.get(self.bot.emojis, name='spirit'))) 
    text= text.replace("$neutre$", str(nextcord.utils.get(self.bot.emojis, name='neutral')))
    return text

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
        cycle="A long Extented Party : Serment des Rohirrim "
    if datacard['id_extension'] in ['86', '97']:
        cycle="A long Extented Party : Scénario Indépendant"
    if datacard['id_extension'] == "82":
        cycle="Starter pack : Les Nains de Durin"
    if datacard['id_extension'] == "83":
        cycle="Starter pack : Les Elfes de la Lórien"
    if datacard['id_extension'] == "84":
        cycle="Starter pack : Les Défenseurs du Gondor"
    if datacard['id_extension'] == "85":
        cycle="Starter pack : Les Cavaliers du Rohan"
    if datacard['id_extension'] == "89":
        cycle="Les Ténèbres de la Forêt Noire"
    return cycle

def id_extension_by_cycle_name(list_name):
    list_id =[]
    for name in list_name:
        if name == "Tout":
            list_id.extend(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '50', '51', '52', '53', '54', '55', '56', '65', '66', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '43', '44', '45', '46', '47', '48', '49', '57', '80', '81', '90', '92', '93', '95', '96', '86', '97', '82', '83', '84', '85', '89'])
        if name == "Boîte de Base":
            list_id.append("1") 
        if name == "Cycle 1 : Ombres de la Forêt Noire":
            list_id.extend(['2', '3', '4', '5', '6', '7'])
        if name == "Cycle 2 : Royaume de Cavenain":
            list_id.extend(['8', '9', '10', '11', '12', '13', '14'])          
        if name == "Cycle 3 : Face à l'Ombre":
            list_id.extend(['15', '16', '17', '18', '19', '20', '21'])
        if name == "Cycle 4 : Le Créateur d'Anneaux":
            list_id.extend(['22', '23', '24', '25', '26', '27', '28'])    
        if name == "Cycle 5 : Le Réveil d'Angmar":
            list_id.extend(['29', '30', '31', '32', '33', '34', '35'])
        if name == "Cycle 6 : Chasse-Rêve":
            list_id.extend(['36', '37', '38', '39', '40', '41', '42'])          
        if name == "Cycle 7 : Les Haradrim":
            list_id.extend(['50', '51', '52', '53', '54', '55', '56'])
        if name == "Cycle 8 : Ered Mithrin":
            list_id.extend(['65', '66', '68', '69', '70', '71', '72'])   
        if name == "Cycle 9 : La Vengeance du Mordor":
            list_id.extend(['73', '74', '75', '76', '77', '78', '79'])   
        if name == "Extension de saga : Par Monts et par Souterrains":
            list_id.append("43")  
        if name == "Extension de saga : Au Seuil de la Porte":
            list_id.append("44")  
        if name == "Extension de saga : Les Cavaliers Noirs":
            list_id.append("45")  
        if name == "Extension de saga : La Route s'Assombrit":
            list_id.append("46")  
        if name == "Extension de saga : La Trahison de Saroumane":
            list_id.append("47")  
        if name == "Extension de saga : La Terre de l'Ombre":
            list_id.append("48")  
        if name == "Extension de saga : La Flamme de l'Ouest":
            list_id.append("49")  
        if name == "Extension de saga : La Montagne de Feu":
            list_id.append("57")  
        if name == "A long Extented Party : Serment des Rohirrim":
            list_id.extend(['80', '81', '90', '92', '93', '95', '96'])
        if name == "A long Extented Party : Scénario Indépendant":
            list_id.extend(['86', '97'])   
        if name == "Starter pack : Les Nains de Durin":
            list_id.append("82")  
        if name == "Starter pack : Les Elfes de la Lórien":
            list_id.append("83")  
        if name == "Starter pack : Les Défenseurs du Gondor":
            list_id.append("84")  
        if name == "Starter pack : Les Cavaliers du Rohan":
            list_id.append("85")  
        if name == "Les Ténèbres de la Forêt Noire":
            list_id.append("89") 
    return list_id


def info_sphere(self,datacard):
    sphere, sphere_color, sphere_emoji ="", 0xFFFFFF,""

    if "id_sphere_influence" in datacard:
        if datacard['id_sphere_influence'] == "300":
            sphere, sphere_color, sphere_emoji="leadership", 0x8B23F9, str(nextcord.utils.get(self.bot.emojis, name='leadership'))
        if datacard['id_sphere_influence'] == "301":
            sphere, sphere_color, sphere_emoji ="lore",  0x0E7A12,str(nextcord.utils.get(self.bot.emojis, name='lore')) 
        if datacard['id_sphere_influence'] == "302":
            sphere, sphere_color, sphere_emoji ="spirit",0x33DDFF, str(nextcord.utils.get(self.bot.emojis, name='spirit'))
        if datacard['id_sphere_influence'] == "303":
            sphere, sphere_color, sphere_emoji ="tactics",0xDB140B, str(nextcord.utils.get(self.bot.emojis, name='tactics'))
        if datacard['id_sphere_influence'] == "304":
            sphere, sphere_color, sphere_emoji ="neutral",0x797B7A, str(nextcord.utils.get(self.bot.emojis, name='neutral'))
        if datacard['id_sphere_influence'] == "305":
            sphere, sphere_color, sphere_emoji ="fellowship",0xD99611, str(nextcord.utils.get(self.bot.emojis, name='fellowship'))
        if datacard['id_sphere_influence'] == "306":
            sphere, sphere_color, sphere_emoji  ="baggins",0xD3D911,str(nextcord.utils.get(self.bot.emojis, name='baggins'))
    return sphere, sphere_color, sphere_emoji

def hero_value(hero_string):
    match hero_string:
        case None:
            return "all"
        case "Aléatoire (par défaut)":
            return "all"
        case "Commandement":
            return"leadership"
        case "Connaissance":
            return "lore"
        case "Energie": 
            return "spirit"
        case "Tactique":
            return "tactics"
        case "Neutre":
            return "neutral"
        case "Sacquet":
            return "baggins"
        case "Communauté":
            return"fellowship"
        case "Pas de second héro":
            return "no"
        case "Pas de troisième héro":
            return "no"

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
        case "Ennemi":
            return "404"
        case "Lieu":
            return "405"
        case "Traitrise":
            return "406"
        case "Objectif":
            return "407"
        case "Quête annexe rencontre":
            return "413"
        case "Préparation":
            return "415"              
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