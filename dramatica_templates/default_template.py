from dramatica.templates import DramaticaTemplate
from dramatica.timeutils import *


__manifest__ = {
    "name"        : "NXTV",
    "description" : "NXTV programming structure",
    "author"      : "martas@imm.cz"
}

COLOR_MUSIC = "#00aa00"


class Template(DramaticaTemplate):
    def apply(self):
        MAIN_GENRES = {
            MON : ["horror"], 
            TUE : ["social", "conspiracy"],
            WED : ["arts"],
            THU : ["technology"],
            FRI : ["rock", "drama", "comedy"],
            SAT : ["rock", "drama", "comedy"],
            SUN : ["drama", "comedy"]
        }[self.dow]


        DAY_JINGLES = {
            MON : "path like '%horror_%'",
            TUE : "path like '%paranoia_%'",
            WED : False,
            THU : "path like '%tech_%'",
            FRI : False,
            SAT : False,
            SUN : False
        }[self.dow]


        self.add_block("06:00", title="Morning mourning", run_mode=2, color=COLOR_MUSIC)
        self.configure(
            solver="MusicBlock",
            genre=["Pop", "Rock", "Alt rock"],
            target_duration=dur("01:00:00"),
            jingles="id_folder = 8",
            promos="id_folder = 3",
            )

        self.add_block("10:00", title="Some movie", run_mode=2)
        self.configure(
            solve_empty=True,
            post_main="path LIKE '%program_%'",
            genre=MAIN_GENRES,
            jingles=DAY_JINGLES
            )   

        self.add_block("12:00", title="NX Rocks", color=COLOR_MUSIC)
        jingles = "path LIKE '%vedci_zjistili%'"
        if DAY_JINGLES:
            jingles += " OR " + DAY_JINGLES
        self.configure(
            solver="MusicBlock",
            genre="Rock",
            intro_jingle="path LIKE '%vedci_zjistili%'",
            outro_jingle="path LIKE '%program_%'",
            jingles=jingles,
            promos="id_folder = 3",
            )   

        self.add_block("15:00", title="Another movie")
        self.configure(
            solve_empty=True,
            post_main="path LIKE '%program_%'",
            genre=MAIN_GENRES,
            jingles=jingles
            )   

        ###############################
        ## Prime time

        if self.dow in [FRI, SAT]:
            self.add_block("18:00", title="Rock pub", color=COLOR_MUSIC)
            self.configure(
                solver="MusicBlock",
                genre="Rock",
                intro_jingle="path LIKE '%rockpub%'",
                outro_jingle="path LIKE '%rockpub%'",
                jingles="path LIKE '%vedci_zjistili%' or path LIKE '%rockpub%'"
                )
            nachtmetal_start = "00:00"

        else:
            self.add_block("19:00", title="PostX", color=COLOR_MUSIC)
            self.configure(
                solver="MusicBlock",
                genre="Alt rock",
                intro_jingle="path LIKE '%postx_short%'",
                outro_jingle="path LIKE '%program_%'",
                jingles="path LIKE '%postx_short%'"
                )   

            self.add_block("21:00", title="Movie of the day")
            self.configure(
                solve_empty=True,
                post_main="path LIKE '%program_%'",
                genre=MAIN_GENRES,
                jingles=DAY_JINGLES
                )   

            nachtmetal_start = "23:00"


        ## Prime time
        ###############################
        ## Graveyard slot

        self.add_block(nachtmetal_start, title="Nachtmetal", color=COLOR_MUSIC)
        self.configure(
            solver="MusicBlock",
            genre=["Metal"],
            intro_jingle="path LIKE '%nachtmetal_intro%'",
            jingles="path LIKE '%nachtmetal_short%'",
            target_duration=dur("02:00:00"),
            )   

