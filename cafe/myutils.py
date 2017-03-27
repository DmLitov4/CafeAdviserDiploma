from .models import Cities, Cuisine, Kind, Cafe, Areaplace, Photo

def transliterate(string):

    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E',}

    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Sch',
                                                          u'Ю': u'Yu',
                                                          u'Я': u'Ya',}


    lower_case_letters = {u'а': u'a',
                       u'б': u'b',
                       u'в': u'v',
                       u'г': u'g',
                       u'д': u'd',
                       u'е': u'e',
                       u'ё': u'e',
                       u'ж': u'zh',
                       u'з': u'z',
                       u'и': u'i',
                       u'й': u'y',
                       u'к': u'k',
                       u'л': u'l',
                       u'м': u'm',
                       u'н': u'n',
                       u'о': u'o',
                       u'п': u'p',
                       u'р': u'r',
                       u'с': u's',
                       u'т': u't',
                       u'у': u'u',
                       u'ф': u'f',
                       u'х': u'h',
                       u'ц': u'ts',
                       u'ч': u'ch',
                       u'ш': u'sh',
                       u'щ': u'sch',
                       u'ъ': u'',
                       u'ы': u'y',
                       u'ь': u'',
                       u'э': u'e',
                       u'ю': u'yu',
                       u'я': u'ya',}

    capital_and_lower_case_letter_pairs = {}

    for capital_letter, capital_letter_translit in capital_letters_transliterated_to_multiple_letters.items():
        for lowercase_letter, lowercase_letter_translit in lower_case_letters.items():
            capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter, lowercase_letter)] = u"%s%s" % (capital_letter_translit, lowercase_letter_translit)

    for dictionary in (capital_and_lower_case_letter_pairs, capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.items():
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = string.replace(cyrillic_string, latin_string.upper())

    return string

def common_elements(list1, list2):
    return list(set(list1) & set(list2))

def get_cafe(cafe_id):
    return Cafe.objects.get(id=cafe_id)

def get_cafe_list():
    return Cafe.objects.order_by('rating').reverse()

def get_latest_list():
    return Cafe.objects.order_by('created_date').reverse()[:4]

def get_cities_list():
    return Cities.objects.all()

def get_cuisines_list():
    return Cuisine.objects.all()

def get_areas_list():
    return Areaplace.objects.all()

def get_kinds_list():
    return Kind.objects.all()

def count_weight(cuisines, areas, kinds, parking, minbill, maxbill, cafe):
    current_cuisines = cafe.cuisines.values_list('id', flat=True)
    cuisines = list(map(int, cuisines))
    cuisineweight = len(common_elements(cuisines, current_cuisines)) * cuisine_weight
    print(len(common_elements(cuisines, current_cuisines)))
    current_area = cafe.areaplace_id
    if current_area in areas:
        areaweight = area_weight
    else:
        areaweight = 0 
    current_kind = cafe.kind_id
    if current_kind in kinds:
        kindweight = kind_weight
    else:
        kindweight = 0

    if cafe.bill > int(minbill) and cafe.bill < int(maxbill):
        priceweight = price_weight
    else:
        priceweight = 0

    return cuisineweight + areaweight + kindweight + priceweight