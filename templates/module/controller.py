# Controllers for {{ module }}
from flask import blueprint


{{ module }}_router = blueprint('{{ module }}', __name__, url_prefix='/{{ module }}')

@{{ module }}_router.route('/')
def index():
    return {
        "message": "Hello from {{ module }}"
        }