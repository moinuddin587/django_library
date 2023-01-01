from django.contrib import admin

from .models import Genre,Book,BookInstance,Author

#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Genre)
#admin.site.register(Author)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = (0)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','display_genre')

    inlines = [BookInstanceInline]

admin.site.register(Book, BookAdmin)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (
            None, {
                'fields': ('id', 'book', 'imprint')
            }
        ),
        (
            'Availability', {
                'fields' : ('due_back', 'status', 'borrower')
            }
        )
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name',('date_of_birth', 'date_of_death')]
