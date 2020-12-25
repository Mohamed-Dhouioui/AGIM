from django.db.models.fields import NOT_PROVIDED

from ..models import Profile 

def set_field(instance, field, value):
    instance.__dict__[field] = value
    instance.save()


def get_field(instance, field):
    return instance.__dict__[field]


# This doesn't work for profiles since i generated their values
def restore_defaults(instance):
    for field in instance._meta.get_fields():
        if field.default != NOT_PROVIDED:
            setattr(instance, field.name, field.default)   
    instance.save() 


def activate_profile(config, room_index, profile_index):
    profile = Profile.objects.get(room_index=room_index, is_active=True)
    profile.is_active = False
    profile.save()
    del profile 

    profile = Profile.objects.get(room_index=room_index, profile_index=profile_index)
    profile.is_active = True
    profile.save()   

    config.active_profile = profile
    config.save()