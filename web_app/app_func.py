

def outcome_det(pos_deet):
    if pos_deet['end_of_poss'] == 1:
        actual_outcome = pos_deet['target_cat']
    else:
        actual_outcome = "?"
    return actual_outcome

def score_det(g_deet):
    if g_deet['posteam'] == g_deet['away_team']:
        home_score = int(g_deet['posteam_score'])
        away_score = int(g_deet['defteam_score'])
    else:
        home_score = int(g_deet['defteam_score'])
        away_score = int(g_deet['posteam_score'])
    return home_score, away_score

def fave_det(g_deet):
    if g_deet['pos_fave'] == 1:
        favorite = g_deet['posteam']
    elif g_deet['posteam'] == g_deet['away_team']:
        favorite = g_deet['home_team']
    else:
        favorite = g_deet['away_team']
    return favorite


def time_remaining(gsr):
    if gsr > 2700:
        mnt = int((gsr - 2700)//60)
        sec = int((gsr - 2700) - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q1 - {mnt}:{sec}'
    elif gsr > 1800:
        mnt = int((gsr - 1800)//60)
        sec = int((gsr - 1800) - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q2 - {mnt}:{sec}'
    elif gsr > 900:
        mnt = int((gsr - 900)//60)
        sec = int((gsr - 900) - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q3 - {mnt}:{sec}'
    else:
        mnt = int((gsr - 0)//60)
        sec = int(gsr - (mnt * 60))
        if sec < 10:
            sec = f'0{sec}'
        return f'Q4 - {mnt}:{sec}'

def yard_det(g_deet, s_deet):    
    if s_deet['yardline_100'] >= 50:
        yardline = g_deet['posteam'] + ' ' + str(100 - s_deet['yardline_100'])
    else:
        if g_deet['posteam'] == g_deet['home_team']:
            yardline = g_deet['away_team'] + ' ' + str(s_deet['yardline_100'])
        else:
            yardline = g_deet['home_team'] + ' ' + str(s_deet['yardline_100'])
    return yardline

pred_dict = {0: 'TD', 1: 'FG', 2: 'punt', 3: 'other'}

if __name__ == '__main__':
    pass