{% extends "emails/base.tpl" %}


{% block subject %}
Hello {{ full_name }},
{% endblock %}

{% block body %}

{{msg}}

Thanks, you rock!

{% endblock %}

{% block html %}
 Simto Private Limited,
Chicago, Illinious, USA
{% endblock %}

