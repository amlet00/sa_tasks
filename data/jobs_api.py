from flask import Blueprint, jsonify

from . import db_session
from .jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=("id", "user.surname", "user.name", "job",
                                    "work_size", "collaborators", "start_date", "end_date",
                                    "is_finished"))
                 for item in jobs]
        }
    )