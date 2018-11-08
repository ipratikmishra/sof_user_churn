import pandas as pd
import numpy as np

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
