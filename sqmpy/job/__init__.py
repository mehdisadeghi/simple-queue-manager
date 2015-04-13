"""
    sqmpy.job
    ~~~~~~~~~

    Provides job submission and monitoring.
"""
from flask import Blueprint

from ..core import core_services
from .manager import JobManager

__author__ = 'Mehdi Sadeghi'


job_blueprint = Blueprint('job', __name__, url_prefix='/job')

@job_blueprint.context_processor
def job_cnx_processor():
    return dict(active_page=job_blueprint.name)

# Register the component in core
core_services.register(JobManager())