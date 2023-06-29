def build_categories_dict(categories):
    categories_dict = {}
    for category in categories:
        categories_dict[category.id] = build_subcategories_dict(category.children)
    return categories_dict


def build_subcategories_dict(subcategories):
    subcategories_dict = {}
    for subcategory in subcategories:
        subcategories_dict[subcategory.id] = build_subcategories_dict(subcategory.children)
    return subcategories_dict
