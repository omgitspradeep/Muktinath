{% extends "emails/base.tpl" %}


{% block subject %}
Hello {{ full_name }},
{% endblock %}

{% block body %}

You just ordered for an {{invitation_type}} invitation book, with following details:
  
      Ordered Date: {{ordered_date}}
      Expiry Date: {{expiry_date}}
      {%if plan%}
        No of Days: {{plan.no_of_days}}
        No. of Invitees: {{plan.no_of_invitees}}
        Amount you paid: {{plan.plan_price}}

      {%endif%}

      Thanks, you rock!

{% endblock %}

{% block html %}
 Simto Private Limited,
Chicago, Illinious, USA
{% endblock %}

