from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
import time
import re 
import os

#permet de démarrer l'application, et d'essayer de récupérer une fenêtre en début de processus 
#(avec le nom de l'application ou "Installation de" suivi du nom de l'application)
def init_code(localisation, first_window_title,app_name):
    if first_window_title == "":
         app = Application().start(f"C:/Users/Chriqui/Desktop/Executor/installeurs/{localisation}")
    else:     
        app = Application().start(f"C:/Users/Chriqui/Desktop/Executor/installeurs/{localisation}").connect(title=first_window_title, timeout=100)
    try: 
        time.sleep(3)
        main_window=app.top_window()
    except (ElementNotFoundError,RuntimeError) :
        time.sleep(5)
        main_window = find_window_by_partial_title(app_name)
    if not main_window.exists():
        time.sleep(5)
        main_window = find_window_by_partial_title(app_name)
    if not main_window.exists():
        main_window = find_window_by_partial_title("Installation de "+app_name)
    try: 
        main_window.wait("visible", timeout=100)
        return app, main_window
    except : 
        return None
    
#generate_name permet de récupérer le début du nom du fichier exécutable afin de récupérer le nom du logiciel 
#pour trouver plus facilement la ou les bonnes fenêtres. Ce n'est pas toujours suffisant cependant. 
def generate_name(localisation):
    name = localisation.split('-')[0].split('_')[0].split(".")[0]
    return name

#according_controls permet de trouver la liste des boutons de la fenêtre donnée en argument. 
#On en profite pour enlever les charactères problématiques comme &
def according_controls(window, title, app_name, class_name="Button"):
    max_retries = 5  # Nombre maximum de tentatives
    current_retry = 0
    window_exists = bool(window.exists())
    if not window_exists:
        window = find_window_by_partial_title(app_name)
        window_exists = bool(window.exists())
        if not window_exists:
            return[]
    while current_retry < max_retries:
        try:
            child_controls = window.children()
            title_without_ampersands=title.replace('&','')
            desired_controls = [control for control in child_controls if
                                hasattr(control, 'window_text') and hasattr(control, 'class_name') and
                                title_without_ampersands.lower() in control.window_text().replace('&', '').lower() and (class_name == "" or control.class_name() == class_name)]
            return desired_controls
        except Exception as e:
            current_retry += 1
            print(f"Erreur lors de la récupération des contrôles enfants : {e}. Tentative {current_retry} sur {max_retries}.")
            time.sleep(1) 
    print(f"Échec de la récupération des contrôles après {max_retries} tentatives.")
    return []


#utilise les expressions régulières pour trouver une fenêtre contenant le partial_title en argument. 
def find_window_by_partial_title(partial_title):
    try:
        pattern = re.compile(f".*{re.escape(partial_title)}.*", re.IGNORECASE)
        return Application().connect(title_re=pattern).top_window()
    except Exception as e:
        print(f"Erreur lors de la recherche de la fenêtre : {e}")
        return None


#executor_loop est la boucle d'exécution qui vérifie la bonne existence de la fenêtre, et en cherche une nouvelle au cas où la précédente aurait disparu. 
#Ensuite on clique sur les boutons en fonction de leurs noms, et ce basé sur un certain ordre pour la bonne exécution de l'installeur. 
def executor_loop(app, mainwindow, app_name):
    if not mainwindow.exists():
        mainwindow = find_window_by_partial_title(app_name)
    click_buttons(["Je Refuse", "I Agree",
                   "J’accepte - suivant","J'accepte","J'accepteButton","install","next","suivant","termin","fermer","finish",
                   "Yes",'Oui','Close','ok'], app, app_name, mainwindow)
    time.sleep(1)
    if mainwindow.exists() or (mainwindow := find_window_by_partial_title(app_name)):
        executor_loop(app, mainwindow, app_name)
                    
                    
#click_buttons récupère les boutons contenant le nom donné en argument et clique le premier correspondant, renvoyant true une fois l'action opérée. 
def click_buttons(possible_button_name, app, app_name, mainwindow):
    button_list=[]
    for button_name in possible_button_name:
        button_list += according_controls(mainwindow,button_name,app_name)
    if len(button_list) !=0:
        for button in button_list: 
            if button.is_enabled():
                button.click()
                return True
        else : 
            return False
    else: 
        return False
        
#la fonction executor s'assure du lancement de l'application via init_code puis lance la boucle d'exécution 
#afin que les boutons soient cliqués pour avancer dans le processus
def executor (localisation, app_name="", first_window_title=""): 
    if app_name == "": 
        app_name = generate_name(localisation)
    app, mainwindow = init_code(localisation, first_window_title,app_name)
    executor_loop(app, mainwindow,app_name)

#Ulysse lance executor sur les exécutables dans la liste donnée en argument. On temporise 20 secondes entre chaque exécutable, 
#et on continue même si il y a une erreur car le bon fonctionnement de l'algorithme finit sur une erreur (on ne trouve plus de fenêtre correspondante)
def Ulysse(install_list):
    a=0
    for fichier in install_list:
        a+=1
        if a==1:
            try: 
                executor(fichier,'Mozilla Firefox')
            except: 
                continue 
        else:
            time.sleep(20)
            try: 
                executor(fichier)
            except: 
                continue 

dossier = "C:/Users/Chriqui/Desktop/Executor/installeurs"
fichiers = os.listdir(dossier)
fichiers_exe = [fichier for fichier in fichiers if fichier.endswith(".exe")]
Ulysse(fichiers_exe)


