from core.database import db
from apps.user.models import User


class CategoryAccess(db.Model):
    __tablename__ = 'category_access'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    root_access = db.Column(db.Boolean, default=False)
    add_user = db.Column(db.Boolean, default=False)
    delete_user = db.Column(db.Boolean, default=False)
    edit_user = db.Column(db.Boolean, default=False)
    add_job = db.Column(db.Boolean, default=True)
    delete_job = db.Column(db.Boolean, default=False)
    update_job = db.Column(db.Boolean, default=False)
    show_job = db.Column(db.Boolean, default=True)
    show_user = db.Column(db.Boolean, default=True)
    print_job = db.Column(db.Boolean, default=True)
    check_job = db.Column(db.Boolean, default=True)
    service_job = db.Column(db.Boolean, default=True)

    # users = db.relationship(User, backref='category_access', lazy=True)

    def __serialize__(self, id=None):
        data = {
            "id": self.id,
            "name": self.name,
            "root_access": self.root_access,
            "add_user": self.add_user,
            "delete_user": self.delete_user,
            "edit_user": self.edit_user,
            "add_job": self.add_job,
            "delete_job": self.delete_job,
            "update_job": self.update_job,
            "show_job": self.show_job,
            "print_job": self.print_job,
            "check_job": self.check_job,
            "service_job": self.service_job
        }
        if id:
            ca = CategoryAccess.query.filter_by(id=id).first()
            if not ca:
                return None
            data = {
                "id": ca.id,
                "name": ca.name,
                "root_access": ca.root_access,
                "add_user": ca.add_user,
                "delete_user": ca.delete_user,
                "edit_user": ca.edit_user,
                "add_job": ca.add_job,
                "delete_job": ca.delete_job,
                "update_job": ca.update_job,
                "show_job": ca.show_job,
                "print_job": ca.print_job,
                "check_job": ca.check_job,
                "service_job": ca.service_job
            }
        return data
