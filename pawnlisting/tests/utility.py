from django.contrib.auth import get_user_model

class Utility:

    def generate_pawn_data(self, name, level=50, vocation="Mage", gender="Male", primary_inclination="Nexus", secondary_inclination="Pioneer"):
        return {"name": name, "level": level, "vocation": vocation, "gender": gender,
            "primary_inclination": primary_inclination, "secondary_inclination": secondary_inclination}

    def create_user_log_in(self, username):
        user, created = get_user_model().objects.get_or_create(username=username)
        user.set_password("12345")
        user.save()
    
        self.client.login(username=username, password="12345")
        return user