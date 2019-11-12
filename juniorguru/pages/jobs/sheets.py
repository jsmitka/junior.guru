import re
import hashlib
from urllib.parse import urlparse

import arrow


def coerce_record(record):
    return coerce({
        r'^timestamp$': ('timestamp', coerce_timestamp),
        r'^company name$': ('company_name', coerce_text),
        r'^job type$': ('job_type', coerce_text),
        r'^title$': ('title', coerce_text),
        r'^company website link$': ('company_link', coerce_text),
        r'^email address$': ('email', coerce_text),
        r'^location$': ('location', coerce_text),
        r'^description$': ('description', coerce_text),
        r'know basics of': ('requirements', coerce_set),
        r'^approved$': ('is_approved', coerce_boolean),
    }, record)


def coerce(mapping, record):
    job = {}

    for key_pattern, (key_name, key_coerce) in mapping.items():
        key_re = re.compile(key_pattern, re.I)

        for record_key, record_value in record.items():
            if key_re.search(record_key):
                job[key_name] = key_coerce(record_value)

    job['id'] = create_id(job['timestamp'], job['company_link'])
    return job


def coerce_text(value):
    if value:
        return value.strip()


def coerce_boolean_words(value):
    if value is not None:
        return dict(yes=True, no=False).get(value.strip())


def coerce_timestamp(value):
    if value:
        return arrow.get(value.strip(), 'M/D/YYYY HH:mm:ss').naive


def coerce_set(value):
    if value:
        return sorted(set([item.strip() for item in value.split(',')]))
    return []


def coerce_boolean(value):
    return bool(value.strip()) if value else False


def create_id(timestamp, company_link):
    parse_result = urlparse(company_link)
    seed = f'{timestamp:%Y-%m-%dT%H:%M:%S} {parse_result.netloc}'
    return hashlib.sha224(seed.encode()).hexdigest()
