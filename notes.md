# Project: All the Art

## Target(s) 

1) WikiArt
    - Domain: www.wikiart.org

## Targeted Elements

### Artists

www.wikiart.org/en/Alphabet/{Letter}/text-list

Possible Letters:

```python
letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'ø'}
```

### Artist Works

www.wikiart.org/en/{ARTIST_NAME}/all-works/text-list

### Genres

www.wikiart.org/en/artists-by-genre

```python
genre_selector = {'class': 'dottedItem'}
```

### Genre Artists

www.wikiart.org/en/artists-by-genre/{GENRE_NAME}/text-list

```python
list_selector = {'class': 'masonry-text-view masonry-text-view-all'}
```

### Fields

www.wikiart.org/en/artists-by-field

```python
field_selector = {'class': 'dottedItem'}
```

### Field Artists

https://www.wikiart.org/en/artists-by-field/{FIELD_NAME}#!#resultType:text

```python
list_selector = {'dynamic-html': 'artistsHtml'}
```

### School

https://www.wikiart.org/en/artists-by-painting-school

```python
school_selector = {'class': 'dottedItem'}
```

### School Artists

www.wikiart.org/en/artists-by-painting-school/{SCHOOL_NAME}#!#resultType:text

```python
list_selector = {'dynamic-html': 'artistsHtml'}
```

### Nationalities

https://www.wikiart.org/en/artists-by-nation

```python
institution_selector = {'class': 'dottedItem'}
```

### Nationality Artists

https://www.wikiart.org/en/artists-by-nation/{NATION_NAME}#!#resultType:text

```python
list_selector = {'dynamic-html': 'artistsHtml'}
```

### Centuries

www.wikiart.org/en/artists-by-century

```python
century_selector = {'class': 'dottedItem'}
```

### Century Artists

www.wikiart.org/en/artists-by-century/{CENTURY_NAME}#!#resultType:text

```python
list_selector = {'dynamic-html': 'artistsHtml'}
```

### Art Institutions

www.wikiart.org/en/artists-by-art-institution

```python
institution_selector = {'class': 'dottedItem'}
```

### Art Institutions Artists

www.wikiart.org/en/artists-by-art-institution/{INSTITUTION_NAME}#!#resultType:text

```python
list_selector = {'dynamic-html': 'artistsHtml'}
```