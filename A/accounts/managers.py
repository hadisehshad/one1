from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone_number, email, name, family, password):

        if not phone_number:
            raise ValueError('user must have a phone number')

        if not email:
            raise ValueError('user must have a email')

        if not name:
            raise ValueError('user must have a name')

        if not family:
            raise ValueError('user must have a family')

        #if not work_experience:
            #raise ValueError('user must have a work_experience')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
             #role_type = role_type,
             #work_experience = work_experience
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser1(self, phone_number, email, name, family, password):

        if not phone_number:
            raise ValueError('user must have a phone number')

        if not email:
            raise ValueError('user must have a email')

        if not name:
            raise ValueError('user must have a name')

        if not family:
            raise ValueError('user must have a family')

        #if not work_experience:
            #raise ValueError('user must have a work_experience')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            #role_type = role_type,
            #work_experience = work_experience
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email,name, family, password):
        user = self.create_superuser1(phone_number, email, name, family, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
