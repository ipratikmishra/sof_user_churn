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

print(get_accepted_answerer_reputation())