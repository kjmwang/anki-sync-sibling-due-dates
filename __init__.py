from anki.consts import QUEUE_TYPE_NEW, CARD_TYPE_NEW
from anki.hooks import addHook
from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip

def process(browser) -> None:
    from_card_ids = list(browser.selected_cards())

    if from_card_ids is None or len(from_card_ids) == 0:
        tooltip("Nothing selected")
        return

    tooltip("Processing " + str(len(from_card_ids)) + " cards")

    for cid in from_card_ids:
        card1 = mw.col.get_card(cid)
        note_id = card1.nid
        note = mw.col.get_note(note_id)
        for sibling in note.cards():
            if sibling.id != cid:
                # Hack: sibling will remain as new card if it hasn't been reviewed before
                if sibling.type == CARD_TYPE_NEW and card1.type != CARD_TYPE_NEW:
                    mw.col.sched.set_due_date([sibling.id], "1")

                sibling.type = card1.type
                sibling.queue = card1.queue
                sibling.due = card1.due
                sibling.ivl = card1.ivl
                sibling.reps = card1.reps
                sibling.factor = card1.factor
                sibling.lapses = card1.lapses
                sibling.original_position = card1.original_position
                sibling.odue = card1.odue

                mw.col.update_card(sibling)

    tooltip("Finished processing" + str(len(from_card_ids)) + " cards")
    del from_card_ids

def setup_menu(browser):
    action = QAction("Sync due date to sibling", browser)

    # Connect action to function
    action.triggered.connect(lambda: process(browser))

    # Add action to the Cards menu
    browser.form.menu_Cards.addSeparator()  # separation line
    browser.form.menu_Cards.addAction(a)

addHook("browser.setupMenus", setup_menu)