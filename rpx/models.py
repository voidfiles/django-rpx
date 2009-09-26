from django.db import models

class RpxData(models.Model):
    """holds bonus info about the user
    some of this this could alternately be implemented by using the rpx
    mapping api. but that requires more network traffic and still doesn't
    provide a place to stash all the user metadata.
    """
    user = models.OneToOneField("auth.User")#this could be a foreignKey if we wish to associate many profiles with the user. hm.
    profile_pic_url = models.URLField(blank=True, verify_exists=False)
    info_page_url = models.URLField(blank=True, verify_exists=False)
    identifier = models.URLField(verify_exists=False, max_length=255)
    provider = models.TextField()
    # class Admin:
    #     list_display = ('',)
    #     search_fields = ('',)

    def __unicode__(self):
        return u"RpxUserData for %s" % self.user.username
        
