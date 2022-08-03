{% extends "emails/base.tpl" %}


{% block body %}
Hello {{ full_name }},

{{msg}}

Thanks, you rock!

{% endblock %}

{% block html %}
 Simto Private Limited,
Chicago, Illinious, USA
{% endblock %}

