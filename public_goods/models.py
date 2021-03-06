from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools

doc = """
        Public good game section (Rounds and feedback).
      """

class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 2
    num_rounds = 2

    results_template = 'public_goods/Results_c.html'

    """Amount allocated to each player"""
    max_savings = c(5)
    multiplier = 1


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        savings_session = [p.savings for p in self.get_players() if p.savings != None]
        if savings_session:
            return {
                'avg_saving': sum(savings_session)/len(savings_session),
                'min_saving': min(savings_session),
                'max_saving': max(savings_session),
            }
        else:
            return {
                'avg_saving': '(no data)',
                'min_saving': '(no data)',
                'max_saving': '(no data)',
            }

    def creating_session(self):
        # self.Constants.endowment = self.session.config['endowment']
        # treatments = itertools.cycle(['control', 't1', 't2','t3'])
        endowment = c(self.session.config['endowment'])
        for g in self.get_groups():
            g.com_goal = self.session.config['community_goal_decimal']
        if self.round_number == 1:
            for g in self.get_groups():
                # treatment = next(treatments)

                for p in g.get_players():
                    # p.participant.vars['treat'] = treatment
                    # p.treat = p.participant.vars['treat']
                    p.participant.vars['endowment'] = endowment
                    p.endowment = p.participant.vars['endowment']

        # if self.round_number > 1:
        #     for p in self.get_players():
        #         p.treat = p.participant.vars['treat']


class Group(BaseGroup):
    com_goal = models.FloatField(min=0, max=1)
    total_savings = models.CurrencyField(initial=0)
    average_savings = models.CurrencyField()
    individual_savings_share = models.FloatField()
    min_round = models.IntegerField(initial=1, doc="go back to x last round. E.g. 1 for last round")

    def set_payoffs(self):
        people_in_treatment = self.get_players()
        people_in_treatment_num = len(people_in_treatment)
        self.total_savings = sum([p.savings for p in people_in_treatment])
        self.individual_savings_share = self.total_savings / (people_in_treatment_num * self.session.config['endowment'])
        self.average_savings = self.total_savings / people_in_treatment_num

        if self.com_goal > 0:
            if self.individual_savings_share >= self.com_goal:
                for p in people_in_treatment:
                    p.participant.vars['endowment'] = p.participant.vars['endowment'] - p.savings
                    p.financial_reward = (p.participant.vars['endowment']).to_real_world_currency(self.session) + (self.total_savings / Constants.players_per_group).to_real_world_currency(self.session)
                    p.endowment = p.participant.vars['endowment']
                    if self.round_number > self.min_round:
                        p.last_savings = p.in_round(self.round_number - self.min_round).savings
            else:
                for p in self.get_players():
                    p.participant.vars['endowment'] = p.participant.vars['endowment'] - p.savings
                    p.financial_reward = p.participant.vars['endowment'].to_real_world_currency(self.session)
                    p.endowment = p.participant.vars['endowment']
                    if self.round_number > self.min_round:
                        p.last_savings = p.in_round(self.round_number - self.min_round).savings
#
    #def set_payoffs(self):
    #    for treatment_name in ['control', 'D', 'DTI']:
    #            people_in_treatment = self.get_players_by_treatment(treatment_name)
    #            people_in_treatment_num = len(people_in_treatment)
    #            total_savings = sum([p.savings for p in people_in_treatment])
    #            individual_savings_share = total_savings / (people_in_treatment_num * self.session.config['endowment'])
    #            average_savings = total_savings / people_in_treatment_num
#
    #            if self.com_goal > 0:
    #                if individual_savings_share >= self.com_goal:
    #                    for p in people_in_treatment:
    #                        p.participant.vars['endowment'] = p.participant.vars['endowment'] - p.savings
    #                        p.financial_reward = p.participant.vars['endowment'].to_real_world_currency(self.session) + (self.total_savings / Constants.players_per_group).to_real_world_currency(self.session)
    #                        p.endowment = p.participant.vars['endowment']
    #                        if self.round_number > self.min_round:
    #                            p.last_savings = p.in_round(self.round_number - self.min_round).savings
    #                else:
    #                    for p in self.get_players_by_treatment(treatment_name):
    #                        p.participant.vars['endowment'] = p.participant.vars['endowment'] - p.savings
    #                        p.financial_reward = p.participant.vars['endowment'].to_real_world_currency(self.session)
    #                        p.endowment = p.participant.vars['endowment']
    #                        if self.round_number > self.min_round:
    #                            p.last_savings = p.in_round(self.round_number - self.min_round).savings
#


class Player(BasePlayer):
    treatment = models.CharField(doc="Treatment of each player")
    endowment = models.CurrencyField(
        min=0,
        doc="endowment by each player"
    )
    peers =
    savings = models.CurrencyField(min=0, max=Constants.max_savings, doc="Savings by each player",choices=[c(0), c(2), c(4)])
    financial_reward = models.FloatField(min=0)
    last_savings = models.CurrencyField(initial=0)
