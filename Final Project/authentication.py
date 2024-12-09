'''Verify if a user’s username and password are correct.
Determine the user's role and subject if authentication is successful.'''
def authenticate_user(username, password, user_data):
    user_record = user_data[(user_data['User'] == username) & (user_data['Password'] == password)]
    if not user_record.empty:
        return user_record.iloc[0]['Role'], user_record.iloc[0]['Subject']
    else:
        return None, None