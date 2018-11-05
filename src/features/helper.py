import pandas as pd
import numpy as np

class helper:
    def get_user_id(self,inp):
        
        post_df=pd.read_csv("/home/kick7/Desktop/projects/sml/fp/sof_user_churn/data/processed/posts.csv")
        post_df.drop(columns=['LastEditorUserId','LastEditDate','LastActivityDate'],inplace=True)
        post_df.dropna(inplace=True)
        post_df[['OwnerUserId']]=post_df[['OwnerUserId']].astype(int)

        post_df['CreationDate']=pd.to_datetime(post_df['CreationDate'])
        post_df['diff'] = post_df.sort_values(['OwnerUserId','CreationDate'], ascending=[True, True]).groupby('OwnerUserId')['CreationDate'].diff()
        post_df=post_df.sort_values(['OwnerUserId', 'CreationDate'], ascending=[True, True]).reset_index(drop=True)
        post_df=post_df[post_df['OwnerUserId']!=-1].reset_index(drop=True)

        post_df=post_df.fillna(0)


        k=inp+1
        k_df=post_df.groupby('OwnerUserId').filter(lambda x:x['CreationDate'].count()>=k)
        k_df=k_df.sort_values(["OwnerUserId","CreationDate"]).reset_index()
        k_df['diff']=pd.to_timedelta(k_df['diff'])
        
        days=365/2
        l_k_df=k_df.sort_values(['OwnerUserId','CreationDate'], ascending=[True, True]).groupby('OwnerUserId').nth(k-1).reset_index()
        l_k_df.drop(columns=['index'],inplace=True)
        c_k_df=l_k_df.sort_values(['OwnerUserId','CreationDate'], ascending=[True, True]).groupby('OwnerUserId').filter(lambda x:x['diff']>=pd.to_timedelta(str(days)+' days'))
        nc_k_df=l_k_df.sort_values(['OwnerUserId','CreationDate'], ascending=[True, True]).groupby('OwnerUserId').filter(lambda x:x['diff']<pd.to_timedelta(str(days)+' days'))
        l_oc_k_df=post_df.groupby('OwnerUserId').filter(lambda x:x['CreationDate'].count()==k-1)
        oc_k_df=l_oc_k_df.sort_values(['OwnerUserId','CreationDate'], ascending=[True, True]).groupby('OwnerUserId').nth(k-2).reset_index()


        Churn_users= c_k_df['OwnerUserId'].tolist()
        Other_churn= oc_k_df['OwnerUserId'].tolist()
        NonChurn_users=nc_k_df['OwnerUserId'].tolist()
        Churn_users.extend(Other_churn)
        return(Churn_users,NonChurn_users)



