EPUB Workflow Plugin pour Calibre
===================================

Version: 1.0.0
Auteur: Florent Bertiaux

DESCRIPTION
-----------

Plugin d'automatisation pour le traitement d'EPUB avec menu interactif, 
traitement batch et balayage récursif.

FONCTIONNALITÉS
---------------

Le plugin permet de traiter les EPUBs sélectionnés dans Calibre avec les actions suivantes :

1. Convertir EPUB to EPUB (rafraîchir HTML)
   - Reconvertit l'EPUB pour nettoyer et rafraîchir le HTML

2. Réparer le HTML
   - Corrige les erreurs HTML dans le fichier EPUB

3. Beautifier tous les fichiers
   - Formate et indente le code HTML/CSS pour une meilleure lisibilité

4. Supprimer le CSS inutilisé
   - Supprime les règles CSS non utilisées dans le document
   - Optimise les feuilles de style

5. Vérifier et corriger automatiquement les erreurs
   - Détecte les erreurs courantes dans l'EPUB
   - Corrige automatiquement les erreurs possibles

6. Supprimer les polices intégrées
   - Supprime les polices embarquées dans le fichier EPUB
   - Réduit la taille du fichier

INSTALLATION
------------

1. Ouvrez Calibre
2. Allez dans Préférences > Plugins > Charger un plugin depuis un fichier
3. Sélectionnez le fichier ZIP du plugin (épub_workflow_plugin.zip)
4. Redémarrez Calibre si nécessaire

Le plugin apparaîtra dans le menu des actions de Calibre.

UTILISATION
-----------

1. Sélectionnez un ou plusieurs livres EPUB dans votre bibliothèque Calibre
2. Cliquez sur l'action "EPUB Workflow" dans le menu des actions
3. Sélectionnez les actions à effectuer dans le dialog de configuration
4. Cliquez sur "OK" pour démarrer le traitement

Note: Les fichiers .kepub.epub sont automatiquement ignorés.

CONFIGURATION
-------------

Le plugin mémorise vos dernières actions sélectionnées pour les réutiliser 
lors de la prochaine utilisation.

FICHIERS IGNORÉS
----------------

- Les fichiers se terminant par .kepub.epub sont automatiquement ignorés
  (format spécifique Kobo)

REQUIS
------

- Calibre 6.0 ou supérieur
- Python 3.8 ou supérieur
- Les outils Calibre (ebook-convert) doivent être dans le PATH

SUPPORT
-------

Pour signaler un bug ou proposer une amélioration, veuillez contacter l'auteur.

LICENCE
-------

GPL v3

