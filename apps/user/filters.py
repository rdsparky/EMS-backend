from django_filters import rest_framework as filters
from .models import User
from django.db.models import Case, When, Value, CharField


class UserFilter(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id")
    email = filters.CharFilter(field_name="email")
    first_name = filters.CharFilter(field_name="first_name")
    last_name = filters.CharFilter(field_name="last_name")

    # def filter_full_name(self, queryset, name, value):
    #     # Perform case-insensitive partial match on the 'name' field
    #     queryset = queryset.filter(full_name__icontains=value)

    #     # Order the queryset based on the position of the search term in the name
    #     queryset = queryset.annotate(
    #         name_index=Case(
    #             When(full_name__icontains=value, then=Value(1)),
    #             default=Value(2),
    #             output_field=CharField(),
    #         )
    #     ).order_by("name_index")
    #     return queryset

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
