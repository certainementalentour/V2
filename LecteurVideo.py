# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pyglet
import os

pyglet.options['search_local_libs'] = True  # recherche des binaires de ffmpeg

try:
    avutil = pyglet.lib.load_library('avutil', win32=('avutil-58', 'avutil-57', 'avutil-56'))
    swresample = pyglet.lib.load_library('swresample', win32=('swresample-4', 'swresample-3'))
    avcodec = pyglet.lib.load_library('avcodec', win32=('avcodec-60', 'avcodec-59', 'avcodec-58'))
    avformat = pyglet.lib.load_library('avformat', win32=('avformat-60', 'avformat-59', 'avformat-58'))
    # vérifie ffmpeg
    if not pyglet.media.have_ffmpeg():
        raise ImportError("chargement de ffmpeg raté")
except ImportError as e:
    print(f"erreur de chargement des bibliothèques FFmpeg: {e}")
    print("considérer ajouter les dll nécessaires dans le dossier lib")
    raise SystemExit(1)


class LecteurVideo:


    def __init__(self, chemin_video):
        self.chemin_video = chemin_video
        self.son_actif = True
        self.pause = False
        self.lecteur = pyglet.media.Player()
        self.plein_ecran = False
        self.taille_originale = None

        # Charger et lire la vidéo
        try:
            self.media = pyglet.media.load(self.chemin_video)
            self.lecteur.queue(self.media)
            self.lecteur.play()
        except Exception as e:
            print(f'erreur lors du chargement: {e}')
        
        # Créer la fenêtre
        self.window = pyglet.window.Window(width=self.media.video_format.width, height=self.media.video_format.height)
        self.taille_originale = (self.media.video_format.width, self.media.video_format.height)
        emplacement_icone = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ressources", "logoLecteur.png")
        if os.path.exists(emplacement_icone):
            icone = pyglet.image.load(emplacement_icone)
            self.window.set_icon(icone)
        self.window.set_caption("b3c6eeb598c14ba6e7753783358dffec")

        @self.window.event
        def on_close():  # pour la croix sur la fenêtre de la vidéo
            self.fermer()

        # Ajouter le gestionnaire d'événement "end of stream" (fermeture auto)
        @self.lecteur.event
        def on_player_eos():
            print("Lecture terminée, sans doute avec des erreurs")
            self.fermer()

        # Ajouter le gestionnaire d'événement on_draw
        @self.window.event  # sert à reconnaitre des évènements standards comme on_draw
        def on_draw():  # ne pas renommer ou pyglet risque de criser
            self.window.clear()
            if self.lecteur.source and self.lecteur.source.video_format:
                if self.plein_ecran:
                    # Calculer le ratio pour maintenir le DAR
                    window_ratio = self.window.width / self.window.height
                    video_ratio = self.taille_originale[0] / self.taille_originale[1]

                    if window_ratio > video_ratio:
                        # dans le cas où la fenêtre serait plus large que la vidéo
                        height = self.window.height
                        width = height * video_ratio
                    else:
                        # fenêtre plus large
                        width = self.window.width
                        height = width / video_ratio
                    # centrer la vidéo
                    x = (self.window.width - width) / 2
                    y = (self.window.height - height) / 2

                    self.lecteur.texture.blit(x, y, width=width, height=height)
                else:
                    self.lecteur.texture.blit(0, 0)
        '''
normalement c'est utile mais seul une autre divinité que moi peut expliquer
        '''
        @self.window.event
        def on_key_press(symbol, modifiers):
            self.clavier(symbol, modifiers)

        self.window.push_handlers(self)
        pyglet.app.run()

    def clavier(self, symbol, modifiers):
        from pyglet.window import key
        if symbol == key.ESCAPE or symbol == key.Q:  # Quitter le programme
            self.fermer()
        elif symbol == key.F:  # plein-écran
            self.basculer_plein_ecran()
        elif symbol == key.SPACE:  # Pause/Reprise
            if self.pause:
                self.lecteur.play()
            else:
                self.lecteur.pause()
            self.pause = not self.pause
        elif symbol == key.M:  # Couper/Rétablir le son
            self.son_actif = not self.son_actif
            self.lecteur.volume = 1.0 if self.son_actif else 0.0
        elif symbol == key.RIGHT:  # Avancer de 5 secondes
            self.lecteur.seek(self.lecteur.time + 5)
        elif symbol == key.LEFT:  # Reculer de 5 secondes
            self.lecteur.seek(max(0, self.lecteur.time - 5))

    def basculer_plein_ecran(self):
        self.plein_ecran = not self.plein_ecran
        if self.plein_ecran:
            self.window.set_fullscreen(True)
        else:
            self.window.set_fullscreen(False)
            self.window.set_size(*self.taille_originale)
    def fermer(self):
        self.lecteur.pause()
        self.window.close()
        pyglet.app.exit()
