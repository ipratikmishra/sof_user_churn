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

def get_rep_questioner():
    rep_questioner_data = []
    userId_list = users_df['Id']
    for user in userId_list:
        user_answered_posts = posts_df[(posts_df.PostTypeId == 2) & (posts_df.OwnerUserId == user)]
        parent_post = user_answered_posts['ParentId']
        questioners_ids = posts_df[posts_df.Id.isin(parent_post)]['OwnerUserId']
        mean_rep = users_df[users_df.Id.isin(questioners_ids)].Reputation.mean()
        rep_questioner_data.append({'userid': user, 'mean_reputation': mean_rep})
    rep_questioner = pd.DataFrame(rep_questioner_data)
    rep_questioner = rep_questioner[rep_questioner.mean_reputation.notnull()]
    return rep_questioner


def get_rep_answerers():
    rep_answerers_data = []
    userId_list = users_df['Id']
    for user in userId_list:
        user_asked_posts = posts_df[(posts_df.PostTypeId == 1) & (posts_df.OwnerUserId == user)]['Id']
        answers = posts_df[(posts_df.PostTypeId == 2) & posts_df.ParentId.isin(user_asked_posts)]
        answerer_ids = answers['OwnerUserId']
        mean_rep = users_df[users_df.Id.isin(answerer_ids)].Reputation.mean()
        rep_answerers_data.append({'userid': user, 'mean_reputation': mean_rep})
    rep_answerer = pd.DataFrame(rep_answerers_data)
    rep_answerer = rep_answerer[rep_answerer.mean_reputation.notnull()]
    return rep_answerer

def get_rep_co_answerers():
    rep_co_answerers_data = []
    userId_list = users_df['Id']
    for user in userId_list:
        user_answered_posts = posts_df[(posts_df.PostTypeId == 2) & (posts_df.OwnerUserId == user)]['ParentId']
        co_answers = posts_df[(posts_df.OwnerUserId != user) &
                              (posts_df.ParentId.isin(user_answered_posts))]['OwnerUserId']
        mean_rep = users_df[users_df.Id.isin(co_answers)].Reputation.mean();
        rep_co_answerers_data.append({'userid': user, 'mean_reputation': mean_rep})
    rep_co_answerers = pd.DataFrame(rep_co_answerers_data)
    rep_co_answerers = rep_co_answerers[rep_co_answerers.mean_reputation.notnull()]
    return rep_co_answerers

def get_num_answers_recvd():
    num_answers_recvd_data = []
    userId_list = users_df['Id']
    for user in userId_list:
        user_asked_ques = posts_df[(posts_df.OwnerUserId == user) & (posts_df.PostTypeId == 1)]['Id']
        num_of_ans = posts_df[(posts_df.PostTypeId == 2) & (posts_df.ParentId.isin(user_asked_ques))].shape[0]
        num_of_ques = user_asked_ques.shape[0]
        if num_of_ques==0:
            mean = 0
        else:
            mean = num_of_ans/num_of_ques
        num_answers_recvd_data.append({'userid': user, 'mean_answers_recvd': mean})
    num_answers_recvd = pd.DataFrame(num_answers_recvd_data)
    num_answers_recvd = num_answers_recvd[num_answers_recvd.mean_reputation.notnull()]
    return num_answers_recvd
