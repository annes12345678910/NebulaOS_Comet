#include "dict.h"

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void* dict_GetValueByKeyName(Dictionary *dict, const char* keyName) {
    for (unsigned int i = 0; i < dict->size; i++)
    {
        DictKey* key = &dict->keys[i];

        // strcmp will segfault at null
        if (key->name)
        {
            if (strcmp(keyName, key->name) == 0)
            {
                return key->value;
            }
        }
    }
    return NULL;
}

void* dict_GetValueByIndex(Dictionary *dict, unsigned int index) {
    //DictKey* key = &dict->keys[index];
    return dict->keys[index].value;
}

Dictionary dict_CreateDict(Dictionary *dict, unsigned int initialSize) {
    Dictionary eme;
    eme.keys = malloc(sizeof(DictKey) * initialSize);
    if (!eme.keys) {
        perror("Failed to create dictionary (malloc returned NULL)");
        exit(EXIT_FAILURE);
    }
    
    eme.size = initialSize;
}

void dict_AddKey(Dictionary *dict, const char* keyName, void* value) {
    dict->keys = realloc(dict->keys, dict->size + 1);
    if (!dict->keys)
    {
        perror("Failed to resize dictionary (realloc returned NULL)");
        exit(EXIT_FAILURE);
    }
    
    dict->size++;
}
