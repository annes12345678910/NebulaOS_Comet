#include "dict.h"

#include <string.h>

void* dict_GetValueByKeyName(Dictionary *dict, const char* keyName) {
    for (unsigned int i = 0; i < dict->size - 1; i++)
    {
        DictKey* key = &dict->keys[i];

        // strcmp will segfault at null
        if (key->name)
        {
            if (strcmp(keyName, key->name))
            {
                return key->value;
            }
        }
    }
    return NULL;
}
