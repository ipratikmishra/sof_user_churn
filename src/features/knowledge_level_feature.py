import pandas as pd
import numpy as np
from datetime import datetime
import time

fmt = '%Y-%m-%d %H:%M:%S'

users_df = pd.read_csv("../../data/processed/users.csv", delimiter = ',')
posts_df = pd.read_csv("../../data/processed//posts.csv", delimiter = ',')


def get_accepted_answerer_reputation():
    accepted_answerer_data = []
    userId_list = users_df['Id']
    for user in userId_list:
        accepted_postid_list = posts_df[(posts_df.OwnerUserId == user) & (posts_df.PostTypeId == 1) &
                                        (posts_df.AcceptedAnswerId.notnull())]['AcceptedAnswerId']
        accepted_answerer_userIds = posts_df[posts_df.Id.isin(accepted_postid_list)]['OwnerUserId']
        mean_rep = users_df[users_df.Id.isin(accepted_answerer_userIds)].Reputation.mean()
        accepted_answerer_data.append({'userid': user, 'mean_reputation': mean_rep})
    accepted_answerer_rep = pd.DataFrame(accepted_answerer_data)
    accepted_answerer_rep = accepted_answerer_rep[accepted_answerer_rep.mean_reputation.notnull()]
    return accepted_answerer_rep


def get_max_reputation_answerer():
    meanOfmax_answerer_reputation_data = []
    userId_list = users_df['Id']
    for user in userId_list:
        user_question_post_id_list = posts_df[(posts_df.OwnerUserId == user) & (posts_df.PostTypeId == 1)]['Id']
        max_rep_list = []
        for post_id in user_question_post_id_list:
            answerer_user_id = posts_df[posts_df.ParentId == post_id]['OwnerUserId']
            rept = users_df[users_df.Id.isin(answerer_user_id)].Reputation.max()
            max_rep_list.append(rept)
        if (len(max_rep_list) > 0):
            meanOfmax_answerer_reputation_data.append({'userid': user, 'max_rep_answerer': np.mean(max_rep_list)})
    meanOfMax_reputation_answerer = pd.DataFrame(meanOfmax_answerer_reputation_data)
    return meanOfMax_reputation_answerer



def get_num_questions_answered():
    userId_to_noofHis_questions_answered = []
    userId_list = users_df['Id']
    for user in userId_list:
        user_question_post_id_list = posts_df[(posts_df.OwnerUserId == user) & (posts_df.PostTypeId == 1)]['Id']
        user_questions_answered = 0
        for post_id in user_question_post_id_list:
            counter = len(posts_df[posts_df.ParentId == post_id])
            if (counter > 0):
                user_questions_answered += 1
        if (user_questions_answered > 0):
            userId_to_noofHis_questions_answered.append(
                {'userid': user, 'number_ofHis_questions_answered': user_questions_answered})
    userId_to_his_questions_answered = pd.DataFrame(userId_to_noofHis_questions_answered)
    return userId_to_his_questions_answered




def get_time_for_first_answer():
    userId_to_mean_time_for_first_answ = []
    userId_list = users_df['Id']
    for user in userId_list:
        # user_question_post_id_df
        df = posts_df[(posts_df.OwnerUserId == user) & (posts_df.PostTypeId == 1)][['Id', 'CreationDate']]
        first_answered_time_list = []

        for index, row in df.iterrows():
            # Formating the date format of the question created date
            question_date = row['CreationDate']
            question_date = question_date.replace("T", " ")
            question_date = question_date[: len(question_date) - 4]
            d1 = datetime.strptime(question_date, fmt)
            d1_ts = time.mktime(d1.timetuple())

            answered_date_list = posts_df[posts_df.ParentId == row['Id']]['CreationDate'].tolist()
            answered_time_diff_list = []

            # Formating the date format of the answer created date for the given quesiton and Convert to Unix timestamp
            for date in answered_date_list:
                date = date.replace("T", " ")
                date = date[: len(date) - 4]
                d2 = datetime.strptime(date, fmt)
                d2_ts = time.mktime(d2.timetuple())
                answered_time_diff_list.append(int(d2_ts - d1_ts) / 60)

            answered_time_diff_list.sort()
            if (len(answered_time_diff_list) > 0):
                first_answered_time_list.append(answered_time_diff_list[0])

        if (len(first_answered_time_list) > 0):
            mean_response_time = sum(first_answered_time_list) / len(first_answered_time_list)
            userId_to_mean_time_for_first_answ.append({'userid': user, 'time_for_first_answer': mean_response_time})

    userId_to_mean_time_for_first_answ_DF = pd.DataFrame(userId_to_mean_time_for_first_answ)
    return userId_to_mean_time_for_first_answ_DF
