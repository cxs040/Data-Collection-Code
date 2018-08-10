from django import template
from kibosurvey.models import  productResults, programmingResults


register = template.Library()

@register.assignment_tag
def product(user, question, productresults):
    
    result = productresults.filter(user_id_number=user,question_number=question).values('rating_number')
    if result.count() == 0:
        return "N/A"
    else:
        return result[0].values()[0]


@register.assignment_tag
def programming(user, question, programmingresults):
    
    result = programmingresults.filter(user_id_number=user,question_number=question).values('rating_number')
    
    if result.count() == 0:
        return "N/A"
    else:
        return result[0].values()[0]


@register.assignment_tag
def count(page, itemnumber):
    
    result = (page - 1) * 10 + itemnumber

    return result
