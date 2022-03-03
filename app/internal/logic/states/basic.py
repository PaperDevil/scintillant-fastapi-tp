from http import HTTPStatus

from scintillant.controllers import ContextUpdater
from scintillant.textutils import RandomSentence


class ScenarioManager(ContextUpdater):

    def _initial_state_(self):
        self.response.text = RandomSentence("<Welcome|Good morning|Hello>, {username}! Do you wanna talk?",
                                            username=self.data.message.user.username).generate()
        self.next_state = self.greeting_ask

    @ContextUpdater.statefunc
    def greeting_ask(self):
        if self.data.message.text.contains_any(['yes', 'of course', 'why not']):
            self.response.text = RandomSentence("It's <great|nice|super> for me!").generate()
            self.next_state = self.goodbye_state
        else:
            self.response.text = "Okay, bye-bye!"
            self.response.status = HTTPStatus.RESET_CONTENT
            self.next_state = None

    @ContextUpdater.statefunc
    def goodbye_state(self):
        self.response.text = 'But im not, sorry!'
        self.response.status = HTTPStatus.RESET_CONTENT
        self.next_state = None
