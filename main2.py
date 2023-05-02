import traceback
import os
import time
import pandas as pd
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Files path
jobs_path = r'C:\Users\naveesai\Downloads\Taraki Assesment\job_listings.csv'
candidates_path = r'C:\Users\naveesai\Downloads\Taraki Assesment\candidate_information.csv'

#getting file modified time for update check
modifiedOn1   = os.path.getmtime(jobs_path)
modifiedOn2 = os.path.getmtime(candidates_path)

#dataframed and variables
df = pd.read_csv(jobs_path)
df2 = pd.read_csv(candidates_path)
count = 0
modify = 0

#While loop is used so that it continuously checks for updates in the data and implement the recommendation system again
while(True):
    count+=1
    df_jbs = df.fillna("")
    df_cand = df2.fillna("")

    #converting data types to appropriate type - string
    df_jbs=df_jbs.convert_dtypes()
    df_cand=df_cand.convert_dtypes()

    # #Resetting the index of the row entries in both of the files as original index changed if remove the rows with missing data
    # df_jbs = df_jbs.reset_index()
    # df_cand = df_cand.reset_index()

    #changing the case of string words using lambda functions
    df_jbs['title']= df_jbs['title'].apply(lambda x: x.title())
    df_jbs['company']= df_jbs['company'].apply(lambda x: x.title())
    df_jbs['location']= df_jbs['location'].apply(lambda x: x.title())
    df_jbs['requirements']= df_jbs['requirements'].apply(lambda x: x.title())

    #changing the case of string words using lambda functions
    df_cand['name']= df_cand['name'].apply(lambda x: x.title())
    df_cand['phone_number']= df_cand['phone_number'].apply(lambda x: x.title())
    df_cand['gender']= df_cand['gender'].apply(lambda x: x.title())
    df_cand['location']= df_cand['location'].apply(lambda x: x.title())
    df_cand['education']= df_cand['education'].apply(lambda x: x.title())
    df_cand['skills']= df_cand['skills'].apply(lambda x: x.title())
    df_cand['jobs_preference']= df_cand['jobs_preference'].apply(lambda x: x.title())
    df_cand['job_location_preference']= df_cand['job_location_preference'].apply(lambda x: x.title())

    #Function to change/convert the text accent/special characters to standard ascii characters
    def accent_conversion(accented_text):
        ct = []
        for t in accented_text:
            normal_text = unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode("utf-8")
            ct.append(normal_text)
        return ct

    clean_text = accent_conversion(df_jbs['location'])
    df_jbs['location'] = clean_text

    clean_text = accent_conversion(df_cand['location'])
    df_cand['location'] = clean_text

    clean_text = accent_conversion(df_cand['education'])
    df_cand['education'] = clean_text

    clean_text = accent_conversion(df_cand['job_location_preference'])
    df_cand['job_location_preference'] = clean_text

    #adding new columns of description in both data frames and bio- column dataframe in candidates dataframe to use multiple paramenters for recommendation system
    df_jbs["description"] = df_jbs['title'].astype(str) +" "+ df_jbs["requirements"]+" "+df_jbs['location']
    df_cand["description"] = df_cand['jobs_preference'].astype(str) +" "+ df_cand['skills']+" "+df_cand['job_location_preference']
    df_cand["bio"] = df_cand['name'].astype(str) +" "+ df_cand['email']+" "+df_cand['gender']

    #For writing the preprocessed/clead data to excel file to check all the data
    df_cand.to_csv(r'C:\Users\naveesai\Desktop\candidate_file.csv')
    df_jbs.to_csv(r'C:\Users\naveesai\Desktop\jobs_file.csv')

    #implementing recommendation system using content filtering
    tfidf = TfidfVectorizer(stop_words='english')

    df_jbs['description'] =df_jbs['description'].fillna("")
    tfidf_matrix = tfidf.fit_transform(df_jbs['description'])

    cosine_sin = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df_jbs.index, index=df_cand['description'])

    def get_recommendation(titles, cosine_sin=cosine_sin):
        idx = indices[titles]
        sin_score = enumerate(cosine_sin[idx])
        sin_score = sorted(sin_score, key=lambda x: x[1].any(), reverse=True)
        sin_score = sin_score[1:11]
        sin_index = [i[0] for i in sin_score]
        print(df_jbs['title'].iloc[sin_index]+"--"+ df_jbs['company'].iloc[sin_index])

    #taking the profile parameter and getting its relevant description data
    def profile(pp):
        ptp = df_cand.index[df_cand['bio'] == pp].tolist()
        desc = (df_cand['description'].values[ptp]).astype(str)
        get_recommendation(desc[0])
    #Function for checking the monitoring data source files for updates
    def check():
        global df
        global df2
        global modify
        global modifiedOn1
        global modifiedOn2
        try:
            time.sleep(0.1)  #pause of 1 second
#getting latest file modified time
            modified1 = os.path.getmtime(jobs_path)
            mtime1 = time.ctime(modified1)
            modified2 = os.path.getmtime(candidates_path)
            mtime2 = time.ctime(modified2)
#check for updates in the jobs file
            if modified1 != modifiedOn1:
                modify = 1
                print("Jobs data modified")
                print(mtime1)
                modifiedOn1 = modified1
                df = pd.read_csv(jobs_path)
#check for updates in the candidate file
            elif modified2 !=modifiedOn2:
                modify = 1
                print("Candidate data modified")
                print(mtime2)
                modifiedOn2 = modified2
                #df = pd.read_csv(jobs_path)
                df2 = pd.read_csv(candidates_path)
            else:
                #print("No Update")
                pass

        except Exception as e:
            print(traceback.format_exc())
#Check for implementing the recommendation only if it is being implemented 1st time or any file is modified
    if count==1 or modify == 1:
        profile("Dory Springate dspringatej2@unesco.org Male")
        modify=0
#calling the check function which is running continuously and checking the files for updates
    check()