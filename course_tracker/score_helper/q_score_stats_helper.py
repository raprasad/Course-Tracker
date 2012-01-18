from decimal import Decimal
"""
Quick class for summing q scores, finding avg, mean, etc.
"""

class QScoreStatsHelper:
    def __init__(self, q_score_list, exclude_zero_scores=True):
        self.q_score_list = q_score_list
        if exclude_zero_scores:
            self.q_score_list = filter(lambda x: x > 0, self.q_score_list)
        
        self.sum_score = Decimal('0')
        self.mean_score = Decimal('0')
        self.median_score = Decimal('0')
        self.num_scores = 0
        
        self.calc_scores()
    
    def calc_scores(self):
        if self.q_score_list is None or len(self.q_score_list) == 0:
            return
            
        self.q_score_list.sort()
        self.sum_score = sum(self.q_score_list)
        self.num_scores = len(self.q_score_list)
        if self.num_scores == 0:
            return
        self.mean_score = self.sum_score / self.num_scores
        
        if len(self.q_score_list) == 1:
            self.median_score = self.q_score_list[0]
        
        elif len(self.q_score_list) % 2 == 1:   # odd number, take middle score
            self.median_score = self.q_score_list[self.num_scores/2]
        
        else:   # even number, avg middle two numbers
            mid_right  = self.q_score_list[ self.num_scores/2 ]
            mid_left = self.q_score_list[ (self.num_scores/2)-1 ]
            self.median_score = (mid_left + mid_right) / Decimal('2')
        
        
        
        