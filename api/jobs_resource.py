import datetime

from data import db_session
from data.jobs import Jobs

from flask import jsonify
from flask_restful import Resource, reqparse, abort

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify(
            {
                'job': job.to_dict(only=(
                    "id", "user.surname", "user.name", "job",
                    "work_size", "collaborators", "start_date", "end_date",
                    "is_finished"))
            }
        )

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs':  [item.to_dict(only=("job", "work_size", "collaborators", "is_finished"))
                                  for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            end_date=datetime.datetime.now() + datetime.timedelta(60 * 60 * args['work_size']),
            is_finished=args['is_finished'],
        )
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})
