from db_ctrl.users import Users
user=Users()

data= user.query_all_users()
print(data)