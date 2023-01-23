from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.subscriptions import Subscription

subscription_bp = Blueprint("subscriptions", __name__)
subscription_api = Api(subscription_bp)


class SubscriptionAPI(Resource):
    def get(self, id):
        subscription = db.session.query(Subscription).get(id)
        if subscription:
            return subscription.to_dict()
        return {"message": "subscription not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        args = parser.parse_args()

        subscription = Subscription(args["username"])
        try:
            db.session.add(subscription)
            db.session.commit()
            return subscription.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("premium", required=True, type=bool)
        args = parser.parse_args()

        try:
            subscription = db.session.query(Subscription).get(args["id"])
            if subscription:
                subscription.premium = args["premium"]
                db.session.commit()
            else:
                return {"message": "subscription not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            subscription = db.session.query(Subscription).get(args["id"])
            if subscription:
                db.session.delete(subscription)
                db.session.commit()
                return subscription.to_dict()
            else:
                return {"message": "subscription not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


class SubscriptionListAPI(Resource):
    def get(self):
        subscriptions = db.session.query(Subscription).all()
        return [subscription.to_dict() for subscription in subscriptions]


subscription_api.add_resource(SubscriptionAPI, "/subscription")
subscription_api.add_resource(SubscriptionListAPI, "/subscriptionList")