from django.contrib import admin
from .models import Review, Product

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_text', 'sentiment_label', 'is_fake', 'timestamp')
    list_filter = ('is_fake', 'sentiment_label')  # Add filtering options for 'is_fake' and 'sentiment_label'
    search_fields = ('user__username', 'review_text')
    
    # Make the review fields read-only, so they can't be edited
    readonly_fields = ('product', 'user', 'review_text', 'sentiment_label', 'is_fake', 'timestamp')

    # Disable adding or changing reviews but allow deleting them
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True  # Admin can delete reviews

admin.site.register(Review, ReviewAdmin)
admin.site.register(Product)
