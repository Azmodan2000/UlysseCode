### UlysseCode
Installation automatique de programme sous windows

##  Pour utiliser le code : 

L'adresse de dossier exemple "C:/Users/Chriqui/Desktop/Executor/installeurs" dans la valeur de dossier dans le code Ulysse.py doit être remplacé par 
l'adresse du dossier contenant les fichiers exécutables à lancer et faire dérouler automatiquement. Une fois cette modification faite, il suffit normalement de lancer le code et les programmes vont s'installer au fur et à mesure. Appuyez deux fois sur Ctrl+C pour mettre fin au processus (une seule fois est comptée comme une erreur ce qui aura pour effet de continuer le programme), et il faut bien lancer le code en tant qu'administrateur 


## Pour la suite éventuelle du projet : 

J'ai essayé de détailler les différentes fonctions dans le code, mais à noter que tous les exécutables ne fonctionneront pas. J'ai utilisé [clubic](https://www.clubic.com/telecharger/) pour identifier les différents exécutables à tester. Voici la liste de ceux qui ont fonctionné : 


- _Firefox_Setup_118.0.2_
- _picasa_3-9_fr_12684_
- _Postman-win64-Setup_
- _poweriso-windows-8.7-25078_
- _speedfan_4-52_en_11074_
- _supercopier_2-0-3-11_fr_11010_32_
- _teamviewer-windows-15.50.5-32680_
- _vlc-media-player_3-0-19_fr_10829_
- _winrar-x64-624fr_

# Plusieurs axes d'amélioration à couvrir: 

**Sur le fonctionnement :**

 - Il faudrait s'assurer que le code ne lance pas d'erreur quand l'exécutable a fini son travail.
 - Il faudrait réduire au maximum les time.sleep de manière à rendre l'exécution du code efficace
 - Il faudrait créer un exécutable pour le lancement du code. Pour cela une méthode prometteuse est d'utiliser Pyinstaller et de rentrer en ligne de commande :
     ``` pyinstaller --onefile --console --uac-admin Ulysse.py ```
   ce qui permet de créer un exécutable en un seul fichier, qui s'ouvre en console et qui demande directement l'élévation de privilège à administrateur. Attention         
   cependant, le paramètre
   ```--hidden-import pwinauto```
   pourrait s'avérer nécessaire

**Sur la portée du code:**

- Il faudrait généraliser plus aux exécutables dont les fenêtres sont reconnues :
    - En réussissant à faire clicker Ulysse lorsque la fenêtre Choix de la langue d'installation s'affiche (exemples : _telegram-windows-4.14.13-190_ ou                             _revo-uninstaller_2-4-5_fr_39528_)
    - En trouvant une solution lorsque deux fenêtres au même nom sont trouvée (_wampserver_2-5_fr_27009_64_)
- Il faudrait trouver une solution pour les .msi : ils semblent impossibles à automatiser, j'avais essayé d'autres bibliothèques que pywinauto, comme os pour passer           directement par la console pour le lancement. A creuser
- Potentielle reconnaissance de texte à terme pour les boutons dans une interface non reconnue par pywinauto. pywinauto reconnait dans de nombreux cas la fenêtre mais pas     les boutons, on peut alors se baser sur la reconnaissance de texte pour identifier les boutons qui sont habituellement en composants enfants de la fenêtre.

