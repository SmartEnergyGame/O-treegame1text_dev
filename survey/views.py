from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Intro(Page):
    def vars_for_template(self):
        return { 'players_in_group' : Constants.players_per_group,'other_players':Constants.players_per_group-1,
                 'endowment':c(self.session.config['endowment']).to_real_world_currency(self.session),'goal':self.session.config['community_goal_decimal']*100}

class survey(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2']
    def before_next_page(self):
        self.player.role()

class AssignationWaitPage(WaitPage):

    body_text = "Waiting for other participants to complete survey."

page_sequence = [Intro,survey, AssignationWaitPage]
