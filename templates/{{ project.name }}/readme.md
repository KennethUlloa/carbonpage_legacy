{% from "macros.omit" import capitalize%}
# {{ project.name }} {{ capitalize("Hello") }}
## Authors
{% for author in project_authors %} - {{ author }}{% endfor %}