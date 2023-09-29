from measure_ambiguity.models import encode_balls
from ._builtin import Page
from .models import Constants


class Instructions(Page):
    def vars_for_template(self):
        to_return = {
            'num_balls': encode_balls([1, 1, 1]),
            'draw_ball': True,
            'probabilities': [0, 1, 2, 5] + [10 + step for step in range(0, 70, 5)] + [85, 100],
            'state': Constants.state,
            'show_proportions': False,
            'option': 'Bingo Blower' if self.participant.vars['event'] == 'blower' else 'DOW'
            }
        return {
            **to_return,
            'proportions': [[num_ball, colour, percentage] for num_ball, colour, percentage in
                            zip(self.participant.vars['number_balls'], Constants.human_colour_states, self.participant.vars['percentage_balls'])],
            } if self.participant.vars['event'] == 'blower' else to_return


class Control(Instructions):
    form_model = 'player'
    form_fields = ['control_question_A_or_B_10', 'control_question_if_A_10', 'control_question_A_or_B_60', 'control_question_if_B_60']

    def vars_for_template(self):
        super_returns = super().vars_for_template()
        winning_state = f"a {Constants.human_colour_states[0]} ball is drawn" if self.participant.vars['event'] == 'blower' else f"the Dow {Constants.DOW_states[0]}"
        label = f'What happens if {winning_state}?'
        return {
            **super_returns,
            'label': label
            }


page_sequence = [Instructions, Control]
