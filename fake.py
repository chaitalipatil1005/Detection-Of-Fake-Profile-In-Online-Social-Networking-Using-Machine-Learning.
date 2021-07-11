
import streamlit as st
import tensorflow as tf
from keras.models import Sequential, load_model
import pandas as pd
import numpy as np
import gc
import json
from PIL import Image



# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


    




def main():
    st.sidebar.subheader("Fake Profile Detection")
    st.title("Fake Twitter Profile Detection")
	
	
    image = Image.open('G:/Project2020-21/F.jpeg')
    col1, col2, col3 = st.beta_columns([1,6,1])
    with col1:
            st.write("")
    with col2:
            st.image(image, width=300)
    with col3:
            st.write("")
			
 
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)
    
    

    if choice == "Home":
        st.subheader("Fake Profile Detection using Machine Learning")

            
    elif choice == "Login":
        st.subheader("Please Enter Valid Credentials")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login/Logout"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                st.sidebar.success("login Success.")
                df_user_prediction = pd.DataFrame(columns = ['statuses_count', 'followers_count', 'friends_count',
                                                                                'favourites_count', 'listed_count', 'url', 'time_zone'])
                col1, col2 = st.beta_columns([1,1])
                with st.form(key='my_form'):
                    sc = col1.number_input("Enter Tweets Count")
                    fc = col2.text_input("Enter Followers Count")
                    frc = col1.text_input("Enter Following Count")
                    frrc = col2.text_input("Enter Favorites Count")
                    lc = col1.text_input("Listed Count")
                    submit_button = st.form_submit_button(label='Submit')
                    if(submit_button):
                        df_user_prediction.loc[0,"statuses_count"] = int(sc)
                        df_user_prediction.loc[0,"followers_count"] = int(fc)
                        df_user_prediction.loc[0,"friends_count"] = int(frc)
                        df_user_prediction.loc[0,"favourites_count"] = int(frrc)
                        df_user_prediction.loc[0,"listed_count"] = 52
                        df_user_prediction.loc[0,"url"] = 2
                        df_user_prediction.loc[0,"time_zone"] = 2021
                        df_user_prediction = df_user_prediction.astype(np.float64)
                        st.write(df_user_prediction)
                        model = load_model('model_twitter.hdf5')
                        model.summary()
                        prediction = model.predict(df_user_prediction)
                        print ('Prediction:' + str(prediction))
                        print ('---' * 10)
                        print (prediction.item(0))
                        prediction_value = prediction.item(0)
                        fake = False
                        if prediction_value == -1.0:
                            print ('it is -1.0')
                            st.success("Profile is not Fake.")
                        if prediction_value != -1.0:
                            print ('is not -1.0')
                            st.error("Profile is Fake.")

                        print(fake)

                
                    
            else:
                st.warning("Incorrect Username/Password")




    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()