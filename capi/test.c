#include "dict.h"

#include <stdlib.h>
#include <stdio.h>

#define COUNT 3
#define INDEXTOGET 2

int main(int argc, char const *argv[])
{
    int val1 = 0;
    char val2 = 'E';
    unsigned int val3 = 20;

    Dictionary mydict;
    mydict.keys = malloc(sizeof(DictKey) * COUNT);
    mydict.size = COUNT;

    mydict.keys[0].name = "snot";
    mydict.keys[0].type = TYPE_INT;

    mydict.keys[1].name = "booger";
    mydict.keys[1].type = TYPE_CHAR;

    mydict.keys[2].name = "meow";
    mydict.keys[2].type = TYPE_UINT;

    mydict.keys[0].value = &val1;
    mydict.keys[1].value = &val2;
    mydict.keys[2].value = &val3;

    DictKey *k = &mydict.keys[INDEXTOGET];

    /*
    printf("The value of %s is ", k->name);
    switch (k->type) {
        case TYPE_INT:
            printf("%d\n", *(int *)k->value);
            break;
        case TYPE_CHAR:
            printf("%c\n", *(char *)k->value);
            break;
        case TYPE_UINT:
            printf("%u\n", *(unsigned int *)k->value);
            break;
    }
    */

    printf("Wow %p\n", dict_GetValueByKeyName(&mydict, "booger"));
    for (unsigned int i = 0; i < mydict.size; i++)
    {
        DictKey* key = &mydict.keys[i];
        printf("Key %s has value %p\n", key->name, key->value);
    }
    

    return 0;
}
