import os
import qrcode
from flask import current_app
from models import Group, User, db


class GroupManager:
    def create_group(self, group_name, group_description):
        group = Group(name=group_name, description=group_description)
        db.session.add(group)
        db.session.commit()
        return group.id

    def create_invite_link(self, group_id):
        group = Group.query.get(group_id)
        if not group:
            raise ValueError("Group not found")
        join_link = f"https://example.com/group/{group_id}/join"

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(join_link)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        # Ensure the 'static/qr_codes' directory exists
        qr_codes_dir = os.path.join(
            current_app.root_path, "static", "qr_codes")
        os.makedirs(qr_codes_dir, exist_ok=True)

        qr_code_filename = f"group_{group_id}_invite.png"
        qr_code_path = os.path.join(qr_codes_dir, qr_code_filename)
        img.save(qr_code_path)

        # Return the relative path to the QR code image
        qr_code_url = f"qr_codes/{qr_code_filename}"
        return join_link, qr_code_url

    def send_join_request(self, user_id, group_id):
        group = Group.query.get(group_id)
        user = User.query.get(user_id)
        if not group or not user:
            raise ValueError("Group or User not found")
        group.member_requests.append(user.id)
        db.session.commit()
        return True

    def accept_join_request(self, group_id, user_id):
        group = Group.query.get(group_id)
        user = User.query.get(user_id)
        if not group or not user:
            raise ValueError("Group or User not found")
        group.member_requests.remove(user.id)
        group.members.append(user.id)
        user.group_memberships.append(group.id)
        db.session.commit()

    def reject_join_request(self, group_id, user_id):
        group = Group.query.get(group_id)
        user = User.query.get(user_id)
        if not group or not user:
            raise ValueError("Group or User not found")
        group.member_requests.remove(user.id)
        db.session.commit()

    def leave_group(self, group_id, user_id):
        group = Group.query.get(group_id)
        user = User.query.get(user_id)
        if not group or not user:
            raise ValueError("Group or User not found")
        group.members.remove(user.id)
        user.group_memberships.remove(group.id)
        db.session.commit()
        return True

    def remove_member(self, group_id, user_id):
        group = Group.query.get(group_id)
        user = User.query.get(user_id)
        if not group or not user:
            raise ValueError("Group or User not found")
        group.members.remove(user.id)
        user.group_memberships.remove(group.id)
        db.session.commit()
        return True

    def group_search(self, group_name):
        groups = Group.query.filter(Group.name.like(f"%{group_name}%")).all()
        return [group.name for group in groups]

    def view_group_members(self, group_id):
        group = Group.query.get(group_id)
        if not group:
            raise ValueError("Group not found")
        return [User.query.get(member_id).username for member_id in group.members]