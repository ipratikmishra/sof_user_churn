import xml.etree.cElementTree as et
import pandas as pd
 
def getvalueofnode(node):
    """ return node text or None """
    return node.text if node is not None else None
 


def postHistory():
    """ Convert PostHistory.xml to pandas dataframe """

    parsed_xml = et.parse("/home/kick7/Desktop/projects/sml/fp/sof_user_churn/data/raw/PostHistory.xml")
    dfcols = ['PostId', 'UserId', 'CreationDate', 'Text']
    df_xml = pd.DataFrame(columns=dfcols)
    i=0
    for node in parsed_xml.getroot():
        if i%10000==0:
            print(i,df_xml.shape)
        i+=1
        PostId = node.attrib.get('PostId')
        UserId = node.attrib.get('UserId')
        CreationDate = node.attrib.get('CreationDate')
        Text = node.attrib.get('Text')
 
        df_xml = df_xml.append(
            pd.Series([PostId, UserId, CreationDate,
                       Text], index=dfcols),
            ignore_index=True)
 
    return df_xml
 
PostHistory_df_xml=postHistory()
PostHistory_df_xml.to_csv("/home/kick7/Desktop/projects/sml/fp/sof_user_churn/data/processed/PostHistory.csv",index=False)