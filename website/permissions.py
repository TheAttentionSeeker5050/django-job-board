

# create custom permissions
def isOwnerOfObject(self, object_owner_id):
    # first make sure the user is logged in
    if not self.request.user.is_authenticated:
        return False
    # check if the user is the owner of the job
    if self.request.user == object_owner_id:
        return True
    else:
        return False