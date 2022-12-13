

class UserController:
    def get_all_user_in_workspace(self, workspace_id):
        return User.objects.filter(workspace_id=workspace_id)