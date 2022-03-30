from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language

class BookInline(admin.TabularInline):
    model = Book
    
    extra = 0

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]
# admin.site.register(Book, BookAdmin)



# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_title','status', 'borrower','due_back','display_id')
    list_filter = ('status','due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
# admin.site.register(BookInstance, BookInstanceAdmin)




admin.site.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name')
    # inlines = [BookInline]

admin.site.register(Language)