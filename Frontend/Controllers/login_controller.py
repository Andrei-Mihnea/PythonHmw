class LoginController:
    def __init__(self, user_db):
        self.user_db = user_db

    def login(self, username, password):
        user = self.user_db.get_user_by_username(username)
        if user and user.check_password(password):
            return {"message": "Login successful", "user_id": user.id}
        return {"message": "Invalid username or password"}, 401

    def register(self, username, password):
        if self.user_db.get_user_by_username(username):
            return {"message": "Username already exists"}, 400
        new_user = self.user_db.create_user(username, password)
        return {"message": "User created successfully", "user_id": new_user.id}