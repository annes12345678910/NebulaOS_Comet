typedef enum {
    TYPE_LONGLONG,
    TYPE_LONG,
    TYPE_INT,
    TYPE_SHORT,
    TYPE_CHAR,

    TYPE_ULONGLONG,
    TYPE_ULONG,
    TYPE_UINT,
    TYPE_USHORT,
    TYPE_UCHAR,

} ValueType;

typedef struct
{
    void* value;
    char* name;
    ValueType type;
} DictKey;

typedef struct
{
    DictKey* keys;
    unsigned int size;
} Dictionary;
