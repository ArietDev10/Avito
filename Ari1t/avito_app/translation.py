from modeltranslation.translator import TranslationOptions,register
from .models import Category, SubCategory, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    filter = ('category_name',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    filter = ('subcategory_name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    filter = ('product_name', 'description',)