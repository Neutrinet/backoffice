from django import template


register = template.Library()


@register.simple_tag
def componentorder_sum(component_list):
    return sum([x.count_in_current_group_order() for x in component_list])
