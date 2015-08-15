#coding:utf-8
from django.contrib import admin

# Register your models here.
from .models import Question,Choice

# TabularInline 以表格的形式呈现
# StackedInline 以堆叠的形式呈现
class ChoiceInline(admin.TabularInline): 
    model = Choice 
    extra = 0
class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    #fieldsets = [ ('Question Information', {'fields': ['question_text']} ), ('Date Information', {'fields': ['pub_date']} )]

    fieldsets = [ ('', {'fields': ['question_text']}), ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),]
    inlines = [ChoiceInline]

    # Customize the admin change list
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date']
    search_fields = ['question_text']
# Register models
admin.site.register(Question, QuestionAdmin)

