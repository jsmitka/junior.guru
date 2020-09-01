from flask import render_template, send_from_directory
from playhouse.shortcuts import model_to_dict

from juniorguru.models import Job, JobDropped, JobError, Metric, db
from juniorguru.scrapers.monitoring import RESPONSES_BACKUP_DIR
from juniorguru.web import app


ADMIN_NAV = {
    'Rozcestník': 'admin',
    'Newsletter': 'admin_newsletter',
    'Stažené nabídky': 'admin_jobs_scraped',
    'Zahozené nabídky': 'admin_jobs_dropped',
    'Chyby při stahování': 'admin_jobs_errors',
}


def models_to_dicts(objects):
    return list(map(model_to_dict, objects))


def models_to_dicts_with_metrics(objects):
    return [
        dict(metrics=obj.metrics, **model_to_dict(obj))
        for obj in objects
    ]


@app.route('/a/')
def admin():
    with db:
        metrics = Metric.as_dict()
    return render_template('admin.html', metrics=metrics)


@app.route('/a/newsletter/')
def admin_newsletter():
    with db:
        jobs = list(Job.newsletter_listing(10))
    return render_template('admin_newsletter.html', jobs=jobs)


@app.route('/a/jobs-scraped/')
def admin_jobs_scraped():
    with db:
        jobs = models_to_dicts_with_metrics(Job.scraped_listing())
    return render_template('admin_jobs_scraped.html', jobs=jobs)


@app.route('/a/jobs-dropped/')
def admin_jobs_dropped():
    with db:
        jobs_dropped = models_to_dicts(JobDropped.admin_listing())
    return render_template('admin_jobs_dropped.html', jobs_dropped=jobs_dropped)


@app.route('/a/jobs-errors/')
def admin_jobs_errors():
    with db:
        jobs_errors = models_to_dicts(JobError.admin_listing())
    return render_template('admin_jobs_errors.html', jobs_errors=jobs_errors)


@app.route('/a/responses-backup/<path:path>')
def admin_responses_backup(path):
    return send_from_directory(RESPONSES_BACKUP_DIR, path, mimetype='text/plain')


@app.context_processor
def inject_admin():
    return dict(admin_nav=ADMIN_NAV)
